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

### Stage Flow Diagram

```
[Stage 1: Draft — Requester Submission]
         │ submit
         ▼
[Stage 2: Division / HOD Approval]
         │ approve / return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: SGM Ops Approval]
         │ approve / reject
         ├─→ Approved: Stage 4
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Engineering PIC Assignment & Execution]
         │ execution complete
         ▼
[Stage 5: Requester Acceptance]
         │ accept / dispute
         ├─→ Accepted: Stage 6
         └─→ Disputed: Stage 4
         ▼
[Stage 6: Closed]
```

### Stage Matrix

| Stage # | Stage Name                       | Trigger                             | Actor                   | Actions                                                           | Next Stage      | Notifications                     |
| ------- | -------------------------------- | ----------------------------------- | ----------------------- | ----------------------------------------------------------------- | --------------- | --------------------------------- |
| 1       | Request Draft                    | New ENGSR submitted                 | Requester               | Fill service/project details, objectives, background              | 2               | Division Head / HOD               |
| 2       | Division / HOD Approval          | Status=Submitted                    | Division Head / HOD     | Review scope and justification; approve or return                 | 3 or 1          | Requester on return               |
| 3       | SGM Ops Approval                 | Status=HODApproved                  | SGM Operations          | Executive-level sign-off; approve or reject                       | 4 or 1          | Requester / HOD on reject         |
| 4       | Engineering PIC Assignment       | Status=SGMApproved                  | Engineering PIC         | Assign PIC; execute service request; record progress              | 5               | Requester, SGM, HOD               |
| 5       | Requester Acceptance             | Status=Executed                     | Requester               | Review deliverables; accept or raise dispute                      | 6 or 4          | PIC, Engineering team on dispute  |
| 6       | Closed                           | Status=Accepted                     | System (auto)           | Lock record; stamp ClosedDate; archive                            | —               | All parties                       |

### Trigger-Condition Matrix

| Stage           | Trigger Condition                | Required Checks                                          | Advance Path                    | Return/Reject Path                        |
| --------------- | -------------------------------- | -------------------------------------------------------- | ------------------------------- | ----------------------------------------- |
| Draft           | Item created with FormType=ENGSR | ProjectTitle, rbService, Objectives, Requestor populated | Route to HOD approval queue     | Missing-fields notice to requester        |
| HOD Approval    | Status=Submitted                 | Scope clarity; budget alignment                          | Advance to SGM Ops approval     | Return with comments to requester         |
| SGM Ops         | Status=HODApproved               | Strategic priority check                                 | Advance to PIC assignment       | Reject with explanation; notify requester |
| PIC Execution   | Status=SGMApproved               | PIC assigned; EngNum stamped                             | Mark execution complete         | Escalate if stalled (3-day nudge)         |
| Acceptance      | Status=Executed                  | Deliverable documentation present                        | Close record                    | Return to PIC for rework                  |

### Power Automate Flows

| Flow Name                  | Trigger                        | Key Actions                                                                                    |
| -------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------- |
| `ENGSR_OnSubmit`           | Item created, FormCode=ENGSR   | Generate EngNum; set Status=Submitted; stamp SubmittedDate; notify HOD/Division Head           |
| `ENGSR_OnApproval`         | Status updated to HODApproved  | Notify SGM Ops; set Status=PendingSGMApproval                                                  |
| `ENGSR_OnSGMApprove`       | Status updated to SGMApproved  | Notify Engineering team; set Status=PendingPIC; stamp SGMApprovedDate                         |
| `ENGSR_OnPICAssignment`    | PIC field populated             | Stamp PICAssignedDate; set Status=InProgress; notify Requester of assigned engineer            |
| `ENGSR_OnClose`            | Status updated to Executed     | Notify Requester for acceptance; stamp ExecutedDate; set Status=PendingAcceptance              |
| `ENGSR_OnAccept`           | Status updated to Accepted     | Set Status=Closed; stamp ClosedDate; lock record; notify all parties                          |
| `ENGSR_SLANudge`           | Scheduled daily                | Check days since PICAssignedDate; alert PIC if stalled > 3 working days                       |

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
