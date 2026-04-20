---
form_code: ENGSR
dept: ENG
official_name: "Engineering Service Request"
module: M2 - Project Requests
owner: "Engineering"
complexity: Complex
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_03_ENG/ENGSR_analysis.md
---

# Blueprint — Engineering Service Request (ENGSR)

## 1. Purpose

ENGSR is used to submit and manage engineering service/project requests, route multi-level approvals, assign engineering PIC ownership, and capture requester acceptance at closure.

## 2. SharePoint Data Model

Primary list: `MainDB_ENG` with `FormType = "ENGSR"`
Staging list: `ENG_ENGSR_List`

Key fields:
- `EngNum`, `CompName`, `nmRequestor`, `dtDate`, `txtDept`, `txtProjectTitle`
- `rbService`, `CarNum`, `txtOthers`, `soft`
- `txtObjectives`, `rbOutput`, `txtOthers_1`, `txtBackground`
- Standard workflow fields: `CurrentAction`, status/approval metadata, `EnvironmentTag`

## 3. Workflow

1. Draft by requester
2. Division/HOD approval
3. SGM Ops approval
4. Engineering verification and PIC assignment
5. Execution and completion verification
6. Requester acceptance and closure

Power Automate flow set:
- `ENGSR_OnSubmit`
- `ENGSR_OnApproval`
- `ENGSR_OnPICAssignment`
- `ENGSR_OnClose`

## 4. Screens

- `ENGSR_List`
- `ENGSR_New`
- `ENGSR_View`
- `ENGSR_Edit`
- `ENGSR_Approval`

## 5. Migration Notes

1. Preserve engineering reference number (`EngNum`) as immutable audit key.
2. Keep conditional "Others" fields active only when related choice paths are selected.
3. Ensure full approval history and PIC handoff events are captured in child approval records.
4. Apply `EnvironmentTag` and role-based visibility for DEV/TEST/PROD operation.
