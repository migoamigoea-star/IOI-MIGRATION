---
form_code: 2_SAPDR_PanCen
dept: IT
official_name: "Pan Century SAP/Procedure entry form for controlled document setup with title, category, effective date, revision, department, and team ownership."
module: M6 - Disaster Recovery
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/2_SAPDR_PanCen_analysis.md
---

# Blueprint - 2_SAPDR_PanCen

## 1. Purpose

This blueprint defines the migration target for 2_SAPDR_PanCen from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 2_SAPDR_PanCen
Staging list: IT_2_SAPDR_PanCen_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/2_SAPDR_PanCen_analysis.md

## 3. Workflow

### Stage Flow Diagram

```
[Stage 1: Document Draft — Initiator]
         │ submit
         ▼
[Stage 2: Department / HOD Review]
         │ approve / return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: SAP Admin Finalization — Publish]
         │ publish / reject
         ├─→ Published: Active
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Active / Published]
```

### Stage Matrix

| Stage # | Stage Name               | Trigger                       | Actor          | Actions                                                               | Next Stage     | Notifications                    |
| ------- | ------------------------ | ----------------------------- | -------------- | --------------------------------------------------------------------- | -------------- | -------------------------------- |
| 1       | Document Draft           | New request started           | Initiator      | Enter title, category, effective date, revision, department, team     | 2              | HOD/Department Head              |
| 2       | Department Review        | Record submitted for review   | HOD            | Review document details; approve or return with comments              | 3 or 1         | Initiator on return              |
| 3       | SAP Admin Finalization   | HOD approved                  | SAP Admin      | Validate SAP setup parameters; publish or reject                      | 4 or 1         | Initiator, HOD                   |
| 4       | Active / Published       | SAP Admin publishes           | System (auto)  | Set Status=Active; expose record in production register               | —              | Initiator, relevant stakeholders |

### Trigger-Condition Matrix

| Stage         | Trigger Condition                         | Required Checks                                  | Advance Path               | Return/Reject Path                           |
| ------------- | ----------------------------------------- | ------------------------------------------------ | -------------------------- | -------------------------------------------- |
| Draft         | Item created with FormType=2_SAPDR_PanCen | title, category, effectiveDate, dept populated   | Route to HOD review queue  | Missing-fields notice to initiator           |
| HOD Review    | Item updated by HOD reviewer              | Data completeness; effective date validity       | Mark approved; notify SAP Admin | Flag issues; return to initiator with comments |
| SAP Finalize  | Item updated by SAP Admin                 | SAP parameter correctness; revision consistency  | Publish to active register | Reject with explanation; return to initiator |

### Power Automate Flows

| Flow Name                    | Trigger                        | Key Actions                                                                         |
| ---------------------------- | ------------------------------ | ----------------------------------------------------------------------------------- |
| `2_SAPDR_PanCen_OnSubmit`    | Item created                   | Validate fields; set Status=Submitted; stamp SubmittedDate; notify HOD              |
| `2_SAPDR_PanCen_OnReview`    | Status updated to UnderReview  | Route to HOD; stamp ReviewDate; notify HOD                                          |
| `2_SAPDR_PanCen_OnComplete`  | Status updated to HODApproved  | Notify SAP Admin; set Status=PendingPublish; stamp ApprovedDate                     |

## 4. Screen Set

- 2_SAPDR_PanCen_List
- 2_SAPDR_PanCen_New
- 2_SAPDR_PanCen_View
- 2_SAPDR_PanCen_Edit
- 2_SAPDR_PanCen_Approval

## 5. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 6. Navigation

2_SAPDR_PanCen_List -> 2_SAPDR_PanCen_New -> 2_SAPDR_PanCen_Approval -> 2_SAPDR_PanCen_View
