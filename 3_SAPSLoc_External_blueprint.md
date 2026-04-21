---
form_code: 3_SAPSLoc_External
dept: IT
official_name: "External Tank & Storage Location Creation request form used to create SAP-related tank/storage location master records through controlled request and approval."
module: M4 - SAP Management
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/3_SAPSLoc_External_analysis.md
---

# Blueprint - 3_SAPSLoc_External

## 1. Purpose

This blueprint defines the migration target for 3_SAPSLoc_External from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 3_SAPSLoc_External
Staging list: IT_3_SAPSLoc_External_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/3_SAPSLoc_External_analysis.md

## 3. Workflow

### Stage Flow Diagram

```
[Stage 1: Request Draft — Initiator]
         │ submit
         ▼
[Stage 2: HOD Approval]
         │ approve / return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: SAP Admin — External Location Creation]
         │ created / reject
         ├─→ Created: Stage 4
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Closed — Location Active in SAP]
```

### Stage Matrix

| Stage # | Stage Name                   | Trigger                           | Actor         | Actions                                                              | Next Stage     | Notifications                |
| ------- | ---------------------------- | --------------------------------- | ------------- | -------------------------------------------------------------------- | -------------- | ---------------------------- |
| 1       | Request Draft                | New request started               | Initiator     | Enter tank/storage location details, type, SAP parameters            | 2              | HOD (approver)               |
| 2       | HOD Approval                 | Record submitted for HOD review   | HOD           | Review request; approve or return with comments                      | 3 or 1         | Initiator on return          |
| 3       | SAP Admin Creation           | HOD approved                      | SAP Admin     | Create external location record in SAP; confirm creation             | 4 or 1         | HOD, Initiator               |
| 4       | Closed                       | SAP location created              | System (auto) | Set Status=Closed; lock record; notify all parties                   | —              | Initiator, HOD, SAP Admin    |

### Trigger-Condition Matrix

| Stage        | Trigger Condition                              | Required Checks                               | Advance Path                  | Return/Reject Path                         |
| ------------ | ---------------------------------------------- | --------------------------------------------- | ----------------------------- | ------------------------------------------ |
| Draft        | Item created with FormType=3_SAPSLoc_External  | LocationName, LocationType, SAPParams present | Route to HOD approval queue   | Missing-fields notice to initiator         |
| HOD Approval | Item updated by HOD                            | Business justification present                | Notify SAP Admin to create    | Return with comment to initiator           |
| SAP Creation | SAP Admin confirms creation                    | SAP system confirmation code present          | Close record                  | Reject with explanation; return to HOD     |

### Power Automate Flows

| Flow Name                      | Trigger                       | Key Actions                                                                      |
| ------------------------------ | ----------------------------- | -------------------------------------------------------------------------------- |
| `3_SAPSLoc_External_OnSubmit`  | Item created                  | Validate fields; set Status=Submitted; stamp SubmittedDate; notify HOD           |
| `3_SAPSLoc_External_OnApprove` | Status updated to HODApproved | Notify SAP Admin; set Status=PendingCreation; stamp ApprovedDate                 |
| `3_SAPSLoc_External_OnComplete`| Status updated to Created     | Set Status=Closed; stamp ClosedDate; lock record; notify Initiator and HOD       |

## 4. Screen Set

- 3_SAPSLoc_External_List
- 3_SAPSLoc_External_New
- 3_SAPSLoc_External_View
- 3_SAPSLoc_External_Edit
- 3_SAPSLoc_External_Approval

## 5. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 6. Navigation

3_SAPSLoc_External_List -> 3_SAPSLoc_External_New -> 3_SAPSLoc_External_Approval -> 3_SAPSLoc_External_View
