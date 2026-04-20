# Technical Blueprint: NDF — Night Duty Manager's Findings

## Blueprint Status

| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | VALIDATED   |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PASS        |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

---

## Form Identity

| Field                      | Value                                                 |
| -------------------------- | ----------------------------------------------------- |
| Form Code                  | NDF                                                   |
| Official Name              | Night Duty Manager's Findings                         |
| Department                 | HR                                                    |
| Module                     | Operations — Night Duty Reporting                     |
| Site(s)                    | PRAI, JOHOR                                           |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/NDF.pdf |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline) |
| Official Name Claim Status | Claimed from source PDF title                         |
| Blueprint Version          | 1.0                                                   |
| Blueprint Date             | 2026-04-19                                            |
| Architect                  | GitHub Copilot (Architect)                            |

---

## Purpose

NDF records structured findings made by the Night Duty Manager during plant inspection rounds. Each
report captures the inspection team composition, date, time, and up to 10 individual findings, each
assigned to a responsible department and PIC with a category and acknowledgement status. Findings
are distributed to named recipients for follow-up. The migrated solution must preserve the multi-row
findings structure via a child table and maintain the original distributon trail.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "NDF"

### Parent List: MainDB_HR (NDF header record)

| #   | SP Internal Name | Display Label           | Column Type         | Required | Classification   | Source Mapping / Notes                                  |
| --- | ---------------- | ----------------------- | ------------------- | -------- | ---------------- | ------------------------------------------------------- |
| 1   | Title            | Title                   | Single line text    | Yes      | SYSTEM-COMPUTED  | NDF prefix + INNumber                                   |
| 2   | FormCode         | Form Code               | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value NDF                                         |
| 3   | INNumber         | IN Number               | Single line text    | No       | SYSTEM-COMPUTED  | `txtINNumberC` — auto-generated                         |
| 4   | TeamMembers      | Inspection Team Members | Multiple lines text | Yes      | USER-ENTERED     | `TeamMembers`                                           |
| 5   | DateVisit        | Inspection Date         | Date and Time       | Yes      | USER-ENTERED     | `DateVisit`                                             |
| 6   | InspectionTime   | Inspection Time         | Single line text    | Yes      | USER-ENTERED     | `Time`                                                  |
| 7   | SendTo           | Send To                 | Multiple lines text | No       | USER-ENTERED     | `SendTo` — distribution list (email addresses or names) |
| 8   | CurrentStatus    | Current Status          | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, Distributed                           |
| 9   | WorkflowStage    | Workflow Stage          | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=Distributed                       |
| 10  | EnvironmentTag   | Environment             | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                         |
| 11  | IsLocked         | Is Locked               | Yes/No              | No       | WORKFLOW-MANAGED | True after distribution                                 |

### Child List: HR_NDF_Findings

Stores up to 10 findings per NDF report. Normalized from the Domino repeating rows.

| #   | SP Internal Name | Display Label       | Column Type         | Required | Notes                                                        |
| --- | ---------------- | ------------------- | ------------------- | -------- | ------------------------------------------------------------ |
| 1   | NDFRef           | NDF Reference       | Lookup (MainDB_HR)  | Yes      | Links to parent NDF record                                   |
| 2   | FindingSeq       | Finding No          | Number              | Yes      | Sequence 1–10; order within report                           |
| 3   | Description      | Finding Description | Multiple lines text | Yes      | `Desc` — what was observed                                   |
| 4   | Department       | Department          | Single line text    | Yes      | `Dept` — responsible department                              |
| 5   | PIC              | Person in Charge    | Single line text    | Yes      | `PIC`                                                        |
| 6   | Category         | Category            | Choice              | Yes      | `Category` — Safety, Housekeeping, Equipment, Process, Other |
| 7   | Acknowledged     | Acknowledged        | Yes/No              | No       | `Att` — acknowledgement flag                                 |
| 8   | FindingRemarks   | Remarks             | Multiple lines text | No       | Review feedback on this finding                              |

---

## Workflow Stage Map

```
[Night Duty Manager] → STAGE 1: Draft (enter findings + team)
      ↓ Submit
STAGE 2: Submitted (record locked for distribution)
      ↓ Distribute
STAGE 3: Distributed (SendTo recipients notified, IsLocked = Yes)
```

| Stage | Action       | Actor Role         | SP Group     | Power Automate Trigger                                                    |
| ----- | ------------ | ------------------ | ------------ | ------------------------------------------------------------------------- |
| 1     | Create Draft | Night Duty Manager | D05-HR-Staff | When item created — NDF record initialised                                |
| 2     | Submit       | Night Duty Manager | D05-HR-Staff | When Status='Draft' and manager submits                                   |
| 3     | Distribute   | System             | —            | When Status='Submitted' → PA sends to SendTo addresses, sets IsLocked=Yes |

---

## Role Matrix

| Domino Group        | SharePoint Group | SP Group Name  | Permissions                |
| ------------------- | ---------------- | -------------- | -------------------------- |
| Night Duty Managers | HR Staff         | D05-HR-Staff   | Contribute (create + edit) |
| HR Manager          | HR Manager       | D05-HR-Manager | Full Control               |

---

## Power Automate Actions

| Flow Name         | Trigger                              | Action                                                                          |
| ----------------- | ------------------------------------ | ------------------------------------------------------------------------------- |
| HR_NDF_OnSubmit   | When Status='Draft' → item submitted | Generate INNumber, stamp date, set Stage=2, trigger distribution                |
| HR_NDF_Distribute | When Status='Submitted'              | Email SendTo list with NDF summary; set CurrentStatus=Distributed, IsLocked=Yes |

---

## Screen Inventory

| Screen Name | Type      | Purpose                                                  | Visible To                   |
| ----------- | --------- | -------------------------------------------------------- | ---------------------------- |
| NDF_List    | Gallery   | List all NDF reports with date and status filter         | D05-HR-Staff, D05-HR-Manager |
| NDF_New     | Form      | New NDF: header fields + editable findings child gallery | D05-HR-Staff                 |
| NDF_View    | Read-only | View full NDF report with all findings rows              | D05-HR-Staff, D05-HR-Manager |
| NDF_Edit    | Form      | Edit draft NDF (header + findings)                       | D05-HR-Staff (creator)       |

---

## Navigation Map

```
NDF_List → [New] → NDF_New
NDF_List → [View] → NDF_View
NDF_List → [Edit] → NDF_Edit (Draft only)
```

---

## Migration Risks & Notes

1. **Repeating rows (up to 10 findings):** Domino uses repeating rows fields
   (Desc/Dept/PIC/Category/Att). In M365, these must be normalized to `HR_NDF_Findings` child table
   with a Lookup to the parent. Craftsman must pre-create finding rows when NDF is created (up to 10
   blank rows) or implement an add-row gallery pattern.

2. **Distribution to SendTo list:** Domino auto-emails the SendTo list on submit. In M365, Power
   Automate parses the `SendTo` field (text) and iterates addresses. Validate email format via
   IsMatch() before distribution. Risk: invalid email addresses in SendTo field causing PA failures.

3. **Acknowledgement tracking per finding:** The `Att` (acknowledged) column per finding row must be
   updatable after distribution — PICs should be able to mark their finding as acknowledged without
   full edit access. Implement targeted edit on `Acknowledged` field only in a separate screen or
   via direct Power Automate action.

4. **Sequence preservation:** The 10-finding sequence (FindingSeq 1–10) must be displayed in order.
   Gallery sort by `FindingSeq` is mandatory in both NDF_New and NDF_View screens.

5. **Night duty context:** NDF is used during night shifts — mobile-friendly layout is important for
   NDF_New and NDF_View. Craftsman must implement responsive layout optimized for tablet/mobile form
   factor.

---

## v3 Impossibilities

| Domino Feature                               | v3 Status  | Workaround                                                                     |
| -------------------------------------------- | ---------- | ------------------------------------------------------------------------------ |
| Dynamic repeating rows (1–10 variable)       | LIMITED    | Child table with gallery; max 10 rows pre-seeded or add-row pattern            |
| In-form email distribution on save           | NOT NATIVE | Power Automate distributes on Status='Submitted'                               |
| PIC acknowledgement without full edit rights | LIMITED    | Targeted PA flow to update Acknowledged field; or separate quick-action screen |

---

## Reference PDF

| Field          | Value                                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/NDF.pdf                                                          |
| Page Count     | 4                                                                                                              |
| Field Evidence | txtINNumberC, TeamMembers, DateVisit, Time, SendTo; Desc/Dept/PIC/Category/Att ×10 rows — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (11 columns) + child table HR_NDF_Findings (8 columns)
- [x] Child table: HR_NDF_Findings normalizes repeating finding rows from Domino
- [x] Workflow Stage Map: ASCII diagram + formal trigger-condition table present
- [x] Role Matrix: all roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 2 flows named with HR*NDF*[EventName] convention
- [x] Screen Inventory: 4 screens listed with visibility rules
- [x] Navigation Map: screen flow documented
- [x] Migration Risks & Notes: 5 risks with mitigations
- [x] v3 Impossibilities: 3 items documented with workarounds
- [x] Reference PDF: path, page count, field evidence confirmed
- [x] Zero unresolved markers present in document
- [x] Blueprint Status section present and correctly populated

**COMPLETION STATUS: COMPLETE**

---

## Sentinel Validation Report

**Validation Date:** 2026-04-19  
**Validator Agent:** Sentinel v1.1  
**Blueprint:** NDF (HR)  
**Input Status:** COMPLETE

### Validation Results

| Check # | Validation Item                 | Status  | Evidence / Comment                           |
| ------- | ------------------------------- | ------- | -------------------------------------------- |
| 1       | Form Identity table present     | ✅ PASS | Required identity fields present             |
| 2       | Section order compliance        | ✅ PASS | Canonical blueprint section order maintained |
| 3       | Workflow Stage Map formal table | ✅ PASS | Stage/action table present                   |
| 4       | Role Matrix mapped to SP groups | ✅ PASS | D05-HR role mappings present                 |
| 5       | Domino field mappings           | ✅ PASS | Schema and field evidence documented         |
| 6       | Marker gate status              | ✅ PASS | check-markers.sh exit code 0                 |

### Validation Verdict

**GATE STATUS:** ✅ **PASS** — Blueprint meets all compliance requirements. Ready for Craftsman
dispatch.

---

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:59:09Z
