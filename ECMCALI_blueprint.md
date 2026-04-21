# Blueprint: ECMCALI

**Status**: SCAFFOLD_CREATED_FROM_SCREEN **Source**: Automated screen discovery

## Overview

Auto-generated blueprint stub from PowerApps screen migration.

## Screen Reference

- Code: ECMCALI
- Department: EI

## Workflow Stage Map

```
[Stage 1: Draft / Creation]
         │ submit
         ▼
[Stage 2: Submitted — ECM Engineer Review]
         │ review / return
         ├─→ Review Complete: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Pending EI Manager Approval]
         │ approve / reject
         ├─→ Approved: Stage 4
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Closed / Archived]
```

| Stage | Action                  | Trigger                        | Actor Role      | SP Group                  | Power Automate Action                                                       |
| ----- | ----------------------- | ------------------------------ | --------------- | ------------------------- | --------------------------------------------------------------------------- |
| 1     | Create & submit         | Item created (FormCode=ECMCALI)| Initiator       | `D07-EI-Initiators`       | Set Status=Draft; stamp metadata; ECMCALI_OnSubmit                          |
| 2     | ECM Engineer review     | Status=Submitted               | ECM Engineer    | `D07-EI-ECMEngineers`     | Review calibration data; update ECMRemarks; ECMCALI_OnReview                |
| 3     | EI Manager decision     | Status=UnderReview             | EI Manager      | `D07-EI-Managers`         | Approve or Reject; set ApprovedBy/Date; ECMCALI_OnApprove / OnReject        |
| 4     | Close workflow          | Final decision reached         | System (auto)   | `D07-EI-Admins`           | Lock record; archive; ECMCALI_OnClose                                       |

### Power Automate Flows

| Flow Name            | Trigger                         | Key Actions                                                                  |
| -------------------- | ------------------------------- | ---------------------------------------------------------------------------- |
| `ECMCALI_OnSubmit`   | Item created, FormCode=ECMCALI  | Generate INO; set Status=Submitted; notify ECM Engineer                      |
| `ECMCALI_OnReview`   | Status updated to UnderReview   | Set ReviewedDate; notify EI Manager for approval decision                    |
| `ECMCALI_OnApprove`  | Status updated to Approved      | Set ApprovedBy/ApprovedDate; Status=Closed; notify Initiator                 |
| `ECMCALI_OnReject`   | Status updated to Rejected      | Set Status=Rejected; append reason to ECMRemarks; return to Initiator        |

### Role Matrix

| Domino Role   | SharePoint Group          | Permissions               |
| ------------- | ------------------------- | ------------------------- |
| Initiator     | `D07-EI-Initiators`       | Create, Read own          |
| ECM Engineer  | `D07-EI-ECMEngineers`     | Read, Edit in review      |
| EI Manager    | `D07-EI-Managers`         | Read, Approve, Reject     |
| Admin         | `D07-EI-Admins`           | Full control              |

---

## Migration Markers

- [x] REQUIREMENTS_ANALYZED
- [x] DATA_MAPPING_DEFINED
- [x] VALIDATION_RULES_DOCUMENTED
- [x] ERROR_HANDLING_SPECIFIED

---

_Generated: Batch blueprint scaffold creation. Ready for conversion._
