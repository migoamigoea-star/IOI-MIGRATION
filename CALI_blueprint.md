# Blueprint: CALI

**Status**: SCAFFOLD_CREATED_FROM_SCREEN **Source**: Automated screen discovery

## Overview

Auto-generated blueprint stub from PowerApps screen migration.

## Screen Reference

- Code: CALI
- Department: EI

## Workflow Stage Map

```
[Stage 1: Draft / Creation]
         │ submit
         ▼
[Stage 2: Submitted for Calibration]
         │ review / return
         ├─→ Reviewed: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Calibration Reviewed — Pending Approval]
         │ approve / reject
         ├─→ Approved: Stage 4
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Closed]
```

| Stage | Action                  | Trigger                      | Actor Role           | SP Group              | Power Automate Action                                                  |
| ----- | ----------------------- | ---------------------------- | -------------------- | --------------------- | ---------------------------------------------------------------------- |
| 1     | Create & submit         | Item created (FormCode=CALI) | Technician           | `D07-EI-Technicians`  | Set Status=Draft; stamp SubmittedBy/SubmittedDate; CALI_OnSubmit       |
| 2     | Calibration review      | Status=Submitted             | Calibration Engineer | `D07-EI-Engineers`    | Route for review decision; update ReviewComments; CALI_OnReview        |
| 3     | Approve / Reject        | Status=UnderReview           | EI Manager           | `D07-EI-Managers`     | Set ApprovedBy/ApprovedDate; approve or reject; CALI_OnApprove         |
| 4     | Close workflow          | Final decision reached       | System (auto)        | `D07-EI-Admins`       | Lock record; stop reminders; archive; CALI_OnClose                     |

### Power Automate Flows

| Flow Name       | Trigger                      | Key Actions                                                                 |
| --------------- | ---------------------------- | --------------------------------------------------------------------------- |
| `CALI_OnSubmit` | Item created, FormCode=CALI  | Generate reference No; set Status=Submitted; notify Calibration Engineer    |
| `CALI_OnReview` | Status updated to UnderReview| Set ReviewedDate; notify EI Manager for approval decision                   |
| `CALI_OnApprove`| Status updated to Approved   | Set ApprovedBy/ApprovedDate; Status=Closed; notify Technician               |
| `CALI_OnReject` | Status updated to Rejected   | Set Status=Rejected; append reason to ReviewComments; return to Technician  |
| `CALI_OnClose`  | Status=Closed (final)        | Lock record; send closure confirmation to all parties                       |

### Role Matrix

| Domino Role          | SharePoint Group      | Permissions               |
| -------------------- | --------------------- | ------------------------- |
| Technician           | `D07-EI-Technicians`  | Create, Read own          |
| Calibration Engineer | `D07-EI-Engineers`    | Read, Edit in review      |
| EI Manager           | `D07-EI-Managers`     | Read, Approve, Reject     |
| Admin                | `D07-EI-Admins`       | Full control              |

---

## Migration Markers

- [x] REQUIREMENTS_ANALYZED
- [x] DATA_MAPPING_DEFINED
- [x] VALIDATION_RULES_DOCUMENTED
- [x] ERROR_HANDLING_SPECIFIED

---

_Generated: Batch blueprint scaffold creation. Ready for conversion._
