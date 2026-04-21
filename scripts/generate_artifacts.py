#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def extract_section(lines: List[str], title: str) -> List[str]:
    pattern = re.compile(rf"^##\s+.*{re.escape(title)}.*$", re.IGNORECASE)
    start = None
    for idx, line in enumerate(lines):
        if pattern.match(line.strip()):
            start = idx + 1
            break
    if start is None:
        return []
    end = len(lines)
    for idx in range(start, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break
    return lines[start:end]


def split_row(row: str) -> List[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def parse_table(lines: List[str], start_index: int = 0) -> Tuple[List[str], List[List[str]], int]:
    for idx in range(start_index, len(lines) - 1):
        if lines[idx].strip().startswith("|") and re.match(r"^\|\s*-", lines[idx + 1].strip()):
            headers = split_row(lines[idx])
            rows: List[List[str]] = []
            cursor = idx + 2
            while cursor < len(lines) and lines[cursor].strip().startswith("|"):
                rows.append(split_row(lines[cursor]))
                cursor += 1
            return headers, rows, cursor
    return [], [], start_index


def parse_first_table(lines: List[str]) -> Tuple[List[str], List[List[str]]]:
    headers, rows, _ = parse_table(lines, 0)
    return headers, rows


def parse_table_after(lines: List[str], heading_pattern: str) -> Tuple[List[str], List[List[str]]]:
    for idx, line in enumerate(lines):
        if re.search(heading_pattern, line, re.IGNORECASE):
            headers, rows, _ = parse_table(lines, idx)
            return headers, rows
    return [], []


def parse_status(lines: List[str]) -> Dict[str, str]:
    section = extract_section(lines, "Blueprint Status")
    headers, rows = parse_first_table(section)
    if not headers:
        return {}
    if len(headers) < 2:
        return {}
    return {row[0]: row[1] for row in rows if len(row) >= 2}


def parse_target_list(lines: List[str]) -> str:
    schema_section = extract_section(lines, "SharePoint Schema")
    for line in schema_section:
        match = re.search(r"Target List:\s*`([^`]+)`", line)
        if match:
            return match.group(1).strip()
        match = re.search(r"Target List:\s*([A-Za-z0-9_ -]+)", line)
        if match:
            return match.group(1).strip()
    parent_headers, parent_rows = parse_table_after(schema_section, r"Parent List")
    if parent_headers:
        match = re.search(r"Parent List:\s*([A-Za-z0-9_ -]+)", " ".join(schema_section))
        if match:
            return match.group(1).strip()
    return ""


def parse_sharepoint_fields(lines: List[str]) -> List[Dict[str, str]]:
    schema_section = extract_section(lines, "SharePoint Schema")
    headers, rows = parse_table_after(schema_section, r"Parent List")
    if not headers:
        headers, rows = parse_first_table(schema_section)
    header_index = {name.strip().lower(): idx for idx, name in enumerate(headers)}
    fields: List[Dict[str, str]] = []
    for row in rows:
        field = {
            "internal_name": row[header_index.get("sp internal name", 1)].strip() if len(row) > 1 else "",
            "display_label": row[header_index.get("display label", 2)].strip() if len(row) > 2 else "",
            "column_type": row[header_index.get("column type", 3)].strip() if len(row) > 3 else "",
            "required": row[header_index.get("required", 4)].strip() if len(row) > 4 else "",
            "notes": row[header_index.get("notes", 6)].strip() if len(row) > 6 else "",
        }
        if field["internal_name"]:
            fields.append(field)
    return fields


def parse_role_matrix(lines: List[str]) -> List[Dict[str, str]]:
    section = extract_section(lines, "Role Matrix")
    headers, rows = parse_first_table(section)
    header_index = {name.strip().lower(): idx for idx, name in enumerate(headers)}
    roles = []
    for row in rows:
        roles.append(
            {
                "domino_role": row[header_index.get("domino role / field", 0)].strip() if row else "",
                "sharepoint_group": row[header_index.get("sharepoint group", 1)].strip() if len(row) > 1 else "",
                "permission_level": row[header_index.get("permission level", 2)].strip() if len(row) > 2 else "",
            }
        )
    return [role for role in roles if role.get("sharepoint_group")]


def parse_screen_inventory(lines: List[str]) -> List[Dict[str, str]]:
    section = extract_section(lines, "Screen Inventory")
    headers, rows = parse_first_table(section)
    header_index = {name.strip().lower(): idx for idx, name in enumerate(headers)}
    screens = []
    for row in rows:
        screens.append(
            {
                "screen_name": row[header_index.get("screen name", 0)].strip() if row else "",
                "purpose": row[header_index.get("purpose", 1)].strip() if len(row) > 1 else "",
                "visible_to": row[header_index.get("visible to", 2)].strip() if len(row) > 2 else "",
            }
        )
    return [screen for screen in screens if screen.get("screen_name")]


def parse_navigation_map(lines: List[str]) -> List[List[str]]:
    section = extract_section(lines, "Navigation Map")
    for line in section:
        if "->" in line and "|" not in line:
            return [parse_navigation_token(token) for token in line.split("->")]
    return []


def parse_navigation_token(token: str) -> List[str]:
    token = token.strip().strip("`")
    if token.startswith("(") and token.endswith(")"):
        token = token[1:-1]
    token = token.replace(" or ", "|").replace("/", "|")
    return [part.strip() for part in token.split("|") if part.strip()]


def parse_workflow_sequence(lines: List[str]) -> List[str]:
    section = extract_section(lines, "Workflow Stage Map")
    for line in section:
        if "->" in line and "|" not in line:
            return [part.strip(" `") for part in line.split("->") if part.strip()]
    return []


def parse_workflow_stages(lines: List[str]) -> List[Dict[str, str]]:
    section = extract_section(lines, "Workflow Stage Map")
    headers, rows = parse_first_table(section)
    header_index = {name.strip().lower(): idx for idx, name in enumerate(headers)}
    stages = []
    for row in rows:
        stages.append(
            {
                "stage": row[header_index.get("stage", 0)].strip() if row else "",
                "action": row[header_index.get("action", 1)].strip() if len(row) > 1 else "",
                "actor_role": row[header_index.get("actor role", 2)].strip() if len(row) > 2 else "",
            }
        )
    return [stage for stage in stages if stage.get("stage")]


def parse_power_automate_actions(lines: List[str]) -> List[Dict[str, str]]:
    section = extract_section(lines, "Power Automate Actions")
    headers, rows = parse_first_table(section)
    header_index = {name.strip().lower(): idx for idx, name in enumerate(headers)}
    flows = []
    for row in rows:
        flows.append(
            {
                "stage": row[header_index.get("stage", 0)].strip() if row else "",
                "flow_name": row[header_index.get("flow name", 1)].strip() if len(row) > 1 else "",
                "trigger": row[header_index.get("trigger", 2)].strip() if len(row) > 2 else "",
                "actions": row[header_index.get("actions", 3)].strip() if len(row) > 3 else "",
            }
        )
    return [flow for flow in flows if flow.get("flow_name")]


def normalize_choices(notes: str) -> List[str]:
    cleaned = re.sub(r"[`]", "", notes or "").strip()
    if not cleaned:
        return []
    if "," in cleaned and not re.search(r"\bvia\b|\bset\b|\bflow\b|\btrigger\b", cleaned, re.IGNORECASE):
        return [item.strip() for item in cleaned.split(",") if item.strip()]
    return []


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return value.strip("_")


def render_sharepoint_script(
    form_code: str,
    list_name: str,
    fields: List[Dict[str, str]],
    roles: List[Dict[str, str]],
) -> str:
    field_lines = []
    for field in fields:
        required = "$true" if field["required"].strip().lower() == "yes" else "$false"
        choices = normalize_choices(field["notes"]) if field["column_type"].lower() == "choice" else []
        choice_text = f"@({', '.join([f'\"{choice}\"' for choice in choices])})" if choices else "@()"
        field_lines.append(
            "    @{ InternalName = \"" + field["internal_name"] + "\"; DisplayName = \""
            + field["display_label"]
            + "\"; Type = \""
            + field["column_type"]
            + "\"; Required = "
            + required
            + "; Choices = "
            + choice_text
            + " }"
        )
    role_lines = []
    for role in roles:
        role_lines.append(
            "    @{ GroupName = \""
            + role["sharepoint_group"]
            + "\"; PermissionLevel = \""
            + role["permission_level"]
            + "\" }"
        )
    return "\n".join(
        [
            "param(",
            "    [Parameter(Mandatory = $true)]",
            "    [string]$SiteUrl,",
            f"    [string]$ListName = \"{list_name}\",",
            "    [int]$ReadSecurity = 1,",
            "    [int]$WriteSecurity = 1",
            ")",
            "",
            "Import-Module PnP.PowerShell -ErrorAction Stop",
            "Connect-PnPOnline -Url $SiteUrl -Interactive",
            "",
            "$list = Get-PnPList -Identity $ListName -ErrorAction SilentlyContinue",
            "if (-not $list) {",
            "    New-PnPList -Title $ListName -Template GenericList -EnableVersioning $true -EnableAttachments $true",
            "}",
            "Set-PnPList -Identity $ListName -EnableVersioning $true -EnableAttachments $true -ReadSecurity $ReadSecurity -WriteSecurity $WriteSecurity",
            "Set-PnPList -Identity $ListName -BreakRoleInheritance -CopyRoleAssignments",
            "",
            "function Ensure-ListField {",
            "    param(",
            "        [string]$InternalName,",
            "        [string]$DisplayName,",
            "        [string]$Type,",
            "        [bool]$Required,",
            "        [string[]]$Choices",
            "    )",
            "    $existing = Get-PnPField -List $ListName -Identity $InternalName -ErrorAction SilentlyContinue",
            "    if ($existing) {",
            "        return",
            "    }",
            "    if ($Type -eq \"Choice\") {",
            "        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Choice -AddToDefaultView -Required:$Required -Choices $Choices",
            "        return",
            "    }",
            "    if ($Type -eq \"Multiple lines\") {",
            "        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Note -AddToDefaultView -Required:$Required",
            "        return",
            "    }",
            "    if ($Type -eq \"Single line\") {",
            "        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Text -AddToDefaultView -Required:$Required",
            "        return",
            "    }",
            "    if ($Type -eq \"Date and Time\") {",
            "        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type DateTime -AddToDefaultView -Required:$Required",
            "        return",
            "    }",
            "    if ($Type -eq \"Person or Group\") {",
            "        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type User -AddToDefaultView -Required:$Required",
            "        return",
            "    }",
            "    if ($Type -eq \"Currency\") {",
            "        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Currency -AddToDefaultView -Required:$Required",
            "        return",
            "    }",
            "    if ($Type -eq \"Yes/No\") {",
            "        Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type Boolean -AddToDefaultView -Required:$Required",
            "        return",
            "    }",
            "    Add-PnPField -List $ListName -InternalName $InternalName -DisplayName $DisplayName -Type $Type -AddToDefaultView -Required:$Required",
            "}",
            "",
            "$fields = @(",
            *field_lines,
            ")",
            "",
            "foreach ($field in $fields) {",
            "    Ensure-ListField -InternalName $field.InternalName -DisplayName $field.DisplayName -Type $field.Type -Required $field.Required -Choices $field.Choices",
            "}",
            "",
            "$roleAssignments = @(",
            *role_lines,
            ")",
            "",
            "foreach ($assignment in $roleAssignments) {",
            "    $group = Get-PnPGroup -Identity $assignment.GroupName -ErrorAction SilentlyContinue",
            "    if (-not $group) {",
            "        $group = New-PnPGroup -Title $assignment.GroupName",
            "    }",
            "    Set-PnPGroupPermissions -Identity $assignment.GroupName -AddRole $assignment.PermissionLevel -List $ListName",
            "}",
            "",
            f"Write-Host \"[{form_code}] SharePoint list provisioning completed for $ListName.\"",
        ]
    )


def render_screen_yaml(
    screen: Dict[str, str],
    navigation: Dict[str, List[str]],
    workflow_stages: List[str],
) -> str:
    visible_to = [item.strip() for item in re.split(r",|/| and ", screen["visible_to"]) if item.strip()]
    lines = [
        "screen:",
        f"  name: {screen['screen_name']}",
        f"  purpose: {screen['purpose']}",
        "  visibleTo:",
    ]
    if visible_to:
        lines.extend([f"    - {role}" for role in visible_to])
    else:
        lines.append("    - All")
    lines.append("  navigation:")
    lines.append("    previous:")
    for prev in navigation.get("previous", []):
        lines.append(f"      - {prev}")
    if not navigation.get("previous"):
        lines.append("      - None")
    lines.append("    next:")
    for nxt in navigation.get("next", []):
        lines.append(f"      - {nxt}")
    if not navigation.get("next"):
        lines.append("      - None")
    lines.append("  workflowStages:")
    for stage in workflow_stages:
        lines.append(f"    - {stage}")
    lines.append("  placeholders:")
    lines.append("    - section: Header")
    lines.append("      controls: []")
    lines.append("    - section: Content")
    lines.append("      controls: []")
    lines.append("    - section: Actions")
    lines.append("      controls: []")
    return "\n".join(lines) + "\n"


def build_navigation_lookup(navigation_groups: List[List[str]]) -> Dict[str, Dict[str, List[str]]]:
    flat_sequence: List[List[str]] = navigation_groups
    lookup: Dict[str, Dict[str, List[str]]] = {}
    for idx, options in enumerate(flat_sequence):
        previous = flat_sequence[idx - 1] if idx > 0 else []
        next_items = flat_sequence[idx + 1] if idx + 1 < len(flat_sequence) else []
        for screen in options:
            if screen not in lookup:
                lookup[screen] = {"previous": [], "next": []}
            lookup[screen]["previous"] = sorted(set(lookup[screen]["previous"] + previous))
            lookup[screen]["next"] = sorted(set(lookup[screen]["next"] + next_items))
    return lookup


def build_user_stories(
    form_code: str,
    workflow_stages: List[Dict[str, str]],
    workflow_sequence: List[str],
    screens: List[Dict[str, str]],
    roles: List[Dict[str, str]],
    fields: List[Dict[str, str]],
) -> str:
    lines = [f"# {form_code} User Stories", ""]
    if workflow_stages:
        lines.append("## Workflow Stories")
        for idx, stage in enumerate(workflow_stages):
            stage_code = stage["stage"].strip()
            next_stage = "Closed"
            if stage_code.upper() in {"D", "DISCARD"}:
                next_stage = "Discarded"
            elif workflow_sequence and stage_code.isdigit():
                numeric_index = int(stage_code) - 1
                if 0 <= numeric_index < len(workflow_sequence) - 1:
                    next_stage = workflow_sequence[numeric_index + 1]
            elif workflow_sequence and idx + 1 < len(workflow_sequence):
                next_stage = workflow_sequence[idx + 1]
            elif idx + 1 < len(workflow_stages):
                next_stage = workflow_stages[idx + 1]["stage"]
            story = (
                f"- As a {stage['actor_role']}, I want to {stage['action']}, "
                f"so that the workflow progresses to {next_stage}."
            )
            lines.append(story)
        lines.append("")
    if screens:
        lines.append("## Screen Stories")
        for screen in screens:
            visible_to = screen["visible_to"] or "authorized users"
            story = (
                f"- As a {visible_to}, I want to use {screen['screen_name']}, "
                f"so that {screen['purpose']}."
            )
            lines.append(story)
        lines.append("")
    if roles:
        lines.append("## Role Stories")
        for role in roles:
            story = (
                f"- As a {role['domino_role']}, I want {role['permission_level']} access "
                f"via {role['sharepoint_group']}, so that I can complete my responsibilities."
            )
            lines.append(story)
        lines.append("")
    required_fields = [field for field in fields if field["required"].strip().lower() == "yes"]
    if required_fields:
        lines.append("## Acceptance Criteria")
        for field in required_fields:
            lines.append(f"- {field['display_label']} is required.")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_flow_json(flow: Dict[str, str], form_code: str) -> Dict[str, str]:
    return {
        "flowName": flow["flow_name"],
        "stage": flow["stage"],
        "trigger": flow["trigger"],
        "actions": flow["actions"],
        "sourceBlueprint": form_code,
        "steps": [],
    }


def generate_for_blueprint(path: Path, output_root: Path, force: bool) -> List[Path]:
    lines = read_lines(path)
    status = parse_status(lines)
    if not force:
        if status.get("Architect Checklist", "").strip().upper() != "COMPLETE":
            return []
        if status.get("Craftsman Build", "").strip().upper() != "NOT_STARTED":
            return []
    form_code = path.stem.replace("_blueprint", "")
    list_name = parse_target_list(lines) or f"MainDB_{form_code}"
    fields = parse_sharepoint_fields(lines)
    roles = parse_role_matrix(lines)
    screens = parse_screen_inventory(lines)
    navigation_groups = parse_navigation_map(lines)
    workflow_sequence = parse_workflow_sequence(lines)
    workflow_stages = parse_workflow_stages(lines)
    flows = parse_power_automate_actions(lines)

    generated_files: List[Path] = []

    sharepoint_dir = output_root / "provisioning" / "sharepoint"
    sharepoint_dir.mkdir(parents=True, exist_ok=True)
    sharepoint_script = sharepoint_dir / f"{form_code}.ps1"
    sharepoint_script.write_text(
        render_sharepoint_script(form_code, list_name, fields, roles),
        encoding="utf-8",
    )
    generated_files.append(sharepoint_script)

    powerapps_dir = output_root / "powerapps" / form_code / "screens"
    powerapps_dir.mkdir(parents=True, exist_ok=True)
    navigation_lookup = build_navigation_lookup(navigation_groups)
    for screen in screens:
        screen_path = powerapps_dir / f"{screen['screen_name']}.yaml"
        screen_path.write_text(
            render_screen_yaml(
                screen,
                navigation_lookup.get(screen["screen_name"], {"previous": [], "next": []}),
                workflow_sequence,
            ),
            encoding="utf-8",
        )
        generated_files.append(screen_path)

    flows_dir = output_root / "flows" / form_code
    flows_dir.mkdir(parents=True, exist_ok=True)
    for flow in flows:
        flow_path = flows_dir / f"{slugify(flow['flow_name'])}.json"
        flow_path.write_text(json.dumps(build_flow_json(flow, form_code), indent=2) + "\n", encoding="utf-8")
        generated_files.append(flow_path)

    stories_dir = output_root / "user-stories"
    stories_dir.mkdir(parents=True, exist_ok=True)
    stories_path = stories_dir / f"{form_code}_user_stories.md"
    stories_path.write_text(
        build_user_stories(form_code, workflow_stages, workflow_sequence, screens, roles, fields),
        encoding="utf-8",
    )
    generated_files.append(stories_path)

    return generated_files


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate implementation artifacts from blueprint files.")
    parser.add_argument("--blueprint", type=str, help="Path to a single blueprint file.")
    parser.add_argument("--repo-root", type=str, default=None, help="Repository root (defaults to script parent).")
    parser.add_argument("--output-root", type=str, default=None, help="Output root (defaults to repo root).")
    parser.add_argument("--force", action="store_true", help="Ignore blueprint status gating.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    output_root = Path(args.output_root).resolve() if args.output_root else repo_root

    if args.blueprint:
        blueprints = [Path(args.blueprint).resolve()]
    else:
        blueprints = sorted(repo_root.glob("*_blueprint.md"))

    all_generated: List[Path] = []
    for blueprint in blueprints:
        all_generated.extend(generate_for_blueprint(blueprint, output_root, args.force))

    if not all_generated:
        print("No artifacts generated. Check blueprint status gating or file paths.")
    else:
        print(f"Generated {len(all_generated)} artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
