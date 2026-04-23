#!/usr/bin/env python3
"""
ai_test_agent.py — AI-powered test agent for Power Apps Canvas Apps
====================================================================
Modes
-----
  analyse   (default)  Analyse Power Apps Test Engine results + screenshots
                       using GPT-4o Vision and produce a structured bug report.
  generate             Generate a YAML test plan from a blueprint + user story
                       using GPT-4o.

Usage
-----
  # Analyse an existing test run
  python ai_test_agent.py \\
      --results-dir testing/results/IOIP \\
      --blueprint IOIP_blueprint.md \\
      --user-story user_stories/IOIP_user_story.md

  # Auto-generate additional test cases
  python ai_test_agent.py \\
      --mode generate \\
      --blueprint IOIP_blueprint.md \\
      --user-story user_stories/IOIP_user_story.md \\
      --output testing/test-engine/tests/IOIP/generated_tests.yaml

Environment variables required
-------------------------------
  AZURE_OPENAI_ENDPOINT   Azure OpenAI resource endpoint
  AZURE_OPENAI_KEY        Azure OpenAI API key
  AZURE_OPENAI_DEPLOYMENT GPT-4o deployment name (default: gpt-4o)
"""

from __future__ import annotations

import argparse
import base64
import json
import logging
import os
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv
from PIL import Image
from rich.console import Console
from rich.table import Table

load_dotenv()

console = Console()
log = logging.getLogger("ai_test_agent")

# ── Constants ──────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = Path(__file__).parent / "prompts"
CONFIG_PATH = Path(__file__).parent / "config.yaml"
RESULTS_FILENAME = "testResults.json"
SCREENSHOT_DIR_NAME = "screenshots"
REPORT_FILENAME = "ai_bug_report.json"
PR_COMMENT_FILENAME = "pr_comment.md"
DEFAULT_DEPLOYMENT = "gpt-4o"
MAX_SCREENSHOTS = 50
SCREENSHOT_MAX_WIDTH = 1280


# ── Config helpers ─────────────────────────────────────────────────────────────

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open() as f:
            return yaml.safe_load(f) or {}
    return {}


def get_openai_client():
    """Return a configured Azure OpenAI client (openai >= 1.x)."""
    try:
        from openai import AzureOpenAI  # type: ignore
    except ImportError:
        console.print("[bold red]ERROR:[/] openai package not installed. Run: pip install openai>=1.30.0")
        sys.exit(1)

    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_OPENAI_KEY", "")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", DEFAULT_DEPLOYMENT)
    api_version = "2024-02-01"

    if not endpoint or not api_key:
        console.print(
            "[bold red]ERROR:[/] AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY must be set."
        )
        sys.exit(1)

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )
    return client, deployment


# ── File helpers ───────────────────────────────────────────────────────────────

def read_text(path: Path | str) -> str:
    p = Path(path)
    if not p.exists():
        log.warning("File not found: %s", p)
        return ""
    return p.read_text(encoding="utf-8")


def read_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    if not path.exists():
        console.print(f"[bold red]ERROR:[/] Prompt file not found: {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def encode_screenshot(path: Path, max_width: int = SCREENSHOT_MAX_WIDTH) -> str:
    """Return a base64-encoded PNG string, resized if wider than max_width."""
    with Image.open(path) as img:
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        import io
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")


def collect_screenshots(results_dir: Path, limit: int = MAX_SCREENSHOTS) -> list[dict]:
    """Return a list of {filename, b64} dicts for all PNGs in the results dir."""
    screenshot_dir = results_dir / SCREENSHOT_DIR_NAME
    if not screenshot_dir.exists():
        # Fall back to any PNG in results_dir itself
        screenshot_dir = results_dir

    pngs = sorted(screenshot_dir.glob("**/*.png"))[:limit]
    screenshots = []
    for p in pngs:
        try:
            screenshots.append({"filename": p.name, "b64": encode_screenshot(p)})
        except Exception as exc:
            log.warning("Could not encode screenshot %s: %s", p, exc)
    return screenshots


def build_openai_vision_messages(
    system_prompt: str,
    screenshots: list[dict],
    user_text: str,
) -> list[dict]:
    """Build the messages list for a GPT-4o vision call."""
    content: list[dict] = [{"type": "text", "text": user_text}]
    for ss in screenshots:
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{ss['b64']}",
                    "detail": "low",
                },
            }
        )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
    ]


# ── Teams notification ─────────────────────────────────────────────────────────

def send_teams_notification(report: dict) -> None:
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL", "").strip()
    if not webhook_url:
        return

    status_emoji = {"PASS": "✅", "FAIL": "❌", "NEEDS_REVIEW": "⚠️"}.get(
        report.get("overallStatus", ""), "❓"
    )
    bug_count = len(report.get("bugs", []))
    warn_count = len(report.get("warnings", []))

    card = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FF0000" if report.get("overallStatus") == "FAIL" else "FFA500",
        "summary": f"Power Apps AI Test Report — {report.get('appName', 'unknown')}",
        "sections": [
            {
                "activityTitle": f"{status_emoji} AI Test Report: {report.get('appName', 'unknown')}",
                "activitySubtitle": report.get("analysisTimestamp", ""),
                "facts": [
                    {"name": "Status", "value": report.get("overallStatus", "")},
                    {"name": "Bugs found", "value": str(bug_count)},
                    {"name": "Warnings", "value": str(warn_count)},
                    {"name": "Summary", "value": report.get("summary", "")},
                ],
            }
        ],
    }

    try:
        resp = requests.post(webhook_url, json=card, timeout=10)
        resp.raise_for_status()
        log.info("Teams notification sent (HTTP %s)", resp.status_code)
    except Exception as exc:
        log.warning("Failed to send Teams notification: %s", exc)


# ── PR comment builder ─────────────────────────────────────────────────────────

SEVERITY_EMOJI = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🔵"}


def build_pr_comment(report: dict) -> str:
    status_emoji = {"PASS": "✅", "FAIL": "❌", "NEEDS_REVIEW": "⚠️"}.get(
        report.get("overallStatus", ""), "❓"
    )
    lines = [
        f"## {status_emoji} Power Apps AI Test Report — `{report.get('appName', 'unknown')}`",
        "",
        f"> **Status:** {report.get('overallStatus')}  ",
        f"> **Run ID:** {report.get('runId', 'n/a')}  ",
        f"> **Timestamp:** {report.get('analysisTimestamp', 'n/a')}",
        "",
        f"**Summary:** {report.get('summary', '')}",
        "",
    ]

    bugs = report.get("bugs", [])
    if bugs:
        lines += [f"### 🐛 Bugs Found ({len(bugs)})", ""]
        for bug in bugs:
            emoji = SEVERITY_EMOJI.get(bug.get("severity", ""), "⚪")
            lines += [
                f"#### {emoji} [{bug['id']}] {bug['title']}",
                f"- **Severity:** {bug.get('severity')}",
                f"- **Category:** {bug.get('category')}",
                f"- **Test Case:** `{bug.get('testCaseName', 'n/a')}`",
                f"- **Expected:** {bug.get('expectedBehaviour', '')}",
                f"- **Actual:** {bug.get('actualBehaviour', '')}",
                f"- **Evidence:** `{bug.get('evidence', '')}`",
                f"- **Suggested Fix:** {bug.get('suggestedFix', 'n/a')}",
                "",
            ]

    warnings = report.get("warnings", [])
    if warnings:
        lines += [f"### ⚠️ Warnings ({len(warnings)})", ""]
        for warn in warnings:
            lines.append(f"- **[{warn['id']}]** ({warn.get('category', '')}) {warn.get('description', '')}")
        lines.append("")

    passing = report.get("passingTests", [])
    if passing:
        lines += [f"### ✅ Passing Tests ({len(passing)})", ""]
        for t in passing:
            lines.append(f"- {t}")
        lines.append("")

    gaps = report.get("coverageGaps", [])
    if gaps:
        lines += ["### 📋 Coverage Gaps", ""]
        for g in gaps:
            lines.append(f"- {g}")
        lines.append("")

    return "\n".join(lines)


# ── Mode: analyse ──────────────────────────────────────────────────────────────

def run_analyse(args: argparse.Namespace) -> None:
    results_dir = Path(args.results_dir)
    if not results_dir.exists():
        console.print(f"[bold red]ERROR:[/] Results directory not found: {results_dir}")
        sys.exit(1)

    # Load test run summary
    summary_path = results_dir / RESULTS_FILENAME
    test_run_summary = read_text(summary_path) if summary_path.exists() else "{}"

    # Load blueprint and user story
    blueprint_content = read_text(args.blueprint) if args.blueprint else ""
    user_story_content = read_text(args.user_story) if args.user_story else ""

    # Collect screenshots
    screenshots = collect_screenshots(results_dir)
    console.print(f"[cyan]Found {len(screenshots)} screenshot(s) to analyse.[/]")

    # Build prompt
    raw_prompt = read_prompt("bug_analyzer_prompt.txt")
    screenshots_json = json.dumps(
        [{"filename": s["filename"]} for s in screenshots], indent=2
    )
    user_text = (
        raw_prompt
        .replace("{test_run_summary}", test_run_summary)
        .replace("{screenshots_json}", screenshots_json)
        .replace("{blueprint_content}", blueprint_content)
        .replace("{user_story_content}", user_story_content)
    )

    # Build vision messages (system prompt is baked into the prompt file)
    messages = build_openai_vision_messages(
        system_prompt=(
            "You are a senior QA engineer specialising in Power Apps Canvas Apps. "
            "Return ONLY the requested JSON — no markdown fences, no preamble."
        ),
        screenshots=screenshots,
        user_text=user_text,
    )

    client, deployment = get_openai_client()
    console.print(f"[cyan]Calling Azure OpenAI ({deployment}) for bug analysis…[/]")

    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=4096,
        temperature=0.1,
    )

    raw_output = response.choices[0].message.content.strip()

    # Parse and validate JSON output
    try:
        report = json.loads(raw_output)
    except json.JSONDecodeError:
        log.warning("Model returned non-JSON; wrapping in minimal report.")
        report = {
            "runId": "unknown",
            "appName": args.blueprint or "unknown",
            "analysisTimestamp": datetime.now(timezone.utc).isoformat(),
            "overallStatus": "NEEDS_REVIEW",
            "summary": "AI agent returned non-JSON output — manual review required.",
            "bugs": [],
            "warnings": [{"id": "WARN-001", "category": "Other", "description": raw_output[:500]}],
            "passingTests": [],
            "coverageGaps": [],
        }

    # Stamp timestamp if missing
    if not report.get("analysisTimestamp"):
        report["analysisTimestamp"] = datetime.now(timezone.utc).isoformat()

    # Write JSON report
    report_path = results_dir / REPORT_FILENAME
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    console.print(f"[green]Bug report written → {report_path}[/]")

    # Write PR comment markdown
    pr_comment = build_pr_comment(report)
    comment_path = results_dir / PR_COMMENT_FILENAME
    comment_path.write_text(pr_comment, encoding="utf-8")
    console.print(f"[green]PR comment written → {comment_path}[/]")

    # Print summary table
    _print_summary_table(report)

    # Teams notification
    config = load_config()
    notify_on = config.get("notifications", {}).get("notify_on", ["FAIL"])
    if report.get("overallStatus") in notify_on:
        send_teams_notification(report)

    # Exit with non-zero code if bugs found (allows CI to fail the build)
    if report.get("overallStatus") == "FAIL":
        sys.exit(1)


def _print_summary_table(report: dict) -> None:
    status = report.get("overallStatus", "?")
    status_color = {"PASS": "green", "FAIL": "red", "NEEDS_REVIEW": "yellow"}.get(status, "white")

    console.print(f"\n[bold {status_color}]Overall Status: {status}[/bold {status_color}]")
    console.print(f"Summary: {report.get('summary', '')}\n")

    bugs = report.get("bugs", [])
    if bugs:
        table = Table(title="Bugs Found", show_lines=True)
        table.add_column("ID", style="bold")
        table.add_column("Severity")
        table.add_column("Category")
        table.add_column("Title")
        for bug in bugs:
            sev = bug.get("severity", "")
            color = {"Critical": "red", "High": "orange3", "Medium": "yellow", "Low": "cyan"}.get(sev, "white")
            table.add_row(
                bug.get("id", ""),
                f"[{color}]{sev}[/{color}]",
                bug.get("category", ""),
                bug.get("title", ""),
            )
        console.print(table)
    else:
        console.print("[green]No bugs detected.[/]")


# ── Mode: generate ─────────────────────────────────────────────────────────────

def run_generate(args: argparse.Namespace) -> None:
    if not args.blueprint:
        console.print("[bold red]ERROR:[/] --blueprint is required for generate mode.")
        sys.exit(1)
    if not args.user_story:
        console.print("[bold red]ERROR:[/] --user-story is required for generate mode.")
        sys.exit(1)

    blueprint_content = read_text(args.blueprint)
    user_story_content = read_text(args.user_story)

    raw_prompt = read_prompt("test_generator_prompt.txt")
    user_text = (
        raw_prompt
        .replace("{blueprint_content}", blueprint_content)
        .replace("{user_story_content}", user_story_content)
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert Power Apps Canvas App test engineer. "
                "Return ONLY valid YAML — no markdown fences, no preamble."
            ),
        },
        {"role": "user", "content": user_text},
    ]

    client, deployment = get_openai_client()
    console.print(f"[cyan]Calling Azure OpenAI ({deployment}) for test generation…[/]")

    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=4096,
        temperature=0.1,
    )

    generated_yaml = response.choices[0].message.content.strip()

    # Validate YAML
    try:
        yaml.safe_load(generated_yaml)
    except yaml.YAMLError as exc:
        console.print(f"[bold yellow]WARNING:[/] Generated output is not valid YAML: {exc}")

    output_path = Path(args.output) if args.output else Path("generated_tests.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generated_yaml, encoding="utf-8")
    console.print(f"[green]Generated test plan written → {output_path}[/]")


# ── CLI ────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI-powered test agent for Power Apps Canvas Apps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              # Analyse test results
              python ai_test_agent.py \\
                --results-dir testing/results/IOIP \\
                --blueprint IOIP_blueprint.md \\
                --user-story user_stories/IOIP_user_story.md

              # Generate test cases
              python ai_test_agent.py --mode generate \\
                --blueprint IOIP_blueprint.md \\
                --user-story user_stories/IOIP_user_story.md \\
                --output testing/test-engine/tests/IOIP/generated_tests.yaml
            """
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["analyse", "generate"],
        default="analyse",
        help="Agent mode: 'analyse' test results or 'generate' test cases (default: analyse)",
    )
    parser.add_argument(
        "--results-dir",
        help="Path to the Power Apps Test Engine output directory (analyse mode)",
    )
    parser.add_argument(
        "--blueprint",
        help="Path to the blueprint markdown file (e.g. IOIP_blueprint.md)",
    )
    parser.add_argument(
        "--user-story",
        help="Path to the user story markdown file (e.g. user_stories/IOIP_user_story.md)",
    )
    parser.add_argument(
        "--output",
        help="Output path for generated YAML test plan (generate mode)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    if args.mode == "analyse":
        run_analyse(args)
    elif args.mode == "generate":
        run_generate(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
