---
form_code: 3_SAPSLoc_Internal
dept: IT
official_name: "Tank Creation/Extend/Transfer form used for internal tank and storage-location lifecycle changes in SAP."
module: M4 - SAP Management
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/3_SAPSLoc_Internal_analysis.md
---

# Blueprint - 3_SAPSLoc_Internal

## 1. Purpose

This blueprint defines the migration target for 3_SAPSLoc_Internal from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 3_SAPSLoc_Internal
Staging list: IT_3_SAPSLoc_Internal_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/3_SAPSLoc_Internal_analysis.md

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
[Stage 3: SAP Admin — Internal Tank Processing]
         │ processed / reject
         ├─→ Processed: Stage 4
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Closed — Tank/Location Updated in SAP]
```

### Stage Matrix

| Stage # | Stage Name               | Trigger                           | Actor         | Actions                                                                      | Next Stage    | Notifications                 |
| ------- | ------------------------ | --------------------------------- | ------------- | ---------------------------------------------------------------------------- | ------------- | ----------------------------- |
| 1       | Request Draft            | New request started               | Initiator     | Enter tank/location change type (Create/Extend/Transfer), SAP parameters     | 2             | HOD (approver)                |
| 2       | HOD Approval             | Record submitted for HOD review   | HOD           | Review request; approve or return with comments                              | 3 or 1        | Initiator on return           |
| 3       | SAP Admin Processing     | HOD approved                      | SAP Admin     | Process internal tank lifecycle change in SAP; confirm completion            | 4 or 1        | HOD, Initiator                |
| 4       | Closed                   | SAP processing complete           | System (auto) | Set Status=Closed; lock record; notify all parties                           | —             | Initiator, HOD, SAP Admin     |

### Trigger-Condition Matrix

| Stage        | Trigger Condition                              | Required Checks                                    | Advance Path                  | Return/Reject Path                         |
| ------------ | ---------------------------------------------- | -------------------------------------------------- | ----------------------------- | ------------------------------------------ |
| Draft        | Item created with FormType=3_SAPSLoc_Internal  | ChangeType, TankID/LocationID, SAPParams present   | Route to HOD approval queue   | Missing-fields notice to initiator         |
| HOD Approval | Item updated by HOD                            | Business justification present; change type valid  | Notify SAP Admin to process   | Return with comment to initiator           |
| SAP Process  | SAP Admin confirms processing                  | SAP system confirmation code present               | Close record                  | Reject with explanation; return to HOD     |

### Power Automate Flows

| Flow Name                      | Trigger                       | Key Actions                                                                       |
| ------------------------------ | ----------------------------- | --------------------------------------------------------------------------------- |
| `3_SAPSLoc_Internal_OnSubmit`  | Item created                  | Validate fields; set Status=Submitted; stamp SubmittedDate; notify HOD            |
| `3_SAPSLoc_Internal_OnApprove` | Status updated to HODApproved | Notify SAP Admin; set Status=PendingProcess; stamp ApprovedDate                   |
| `3_SAPSLoc_Internal_OnComplete`| Status updated to Processed   | Set Status=Closed; stamp ClosedDate; lock record; notify Initiator and HOD        |

## 4. Screen Set

- 3_SAPSLoc_Internal_List
- 3_SAPSLoc_Internal_New
- 3_SAPSLoc_Internal_View
- 3_SAPSLoc_Internal_Edit
- 3_SAPSLoc_Internal_Approval

## 5. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 6. Navigation

3_SAPSLoc_Internal_List -> 3_SAPSLoc_Internal_New -> 3_SAPSLoc_Internal_Approval -> 3_SAPSLoc_Internal_View
