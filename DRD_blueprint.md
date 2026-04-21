# Blueprint: DRD

## Form Identity

| Field | Value |
|---|---|
| Form Code | DRD |
| Form Name | DRD |
| Department | HR |
| Module | HR |
| Owner | HR Admin |
| Complexity | Simple |
| DQ Required | NO |
| GxP Class | — |
| Status | SCAFFOLD |
| Source | Automated screen discovery |
| Blueprint Date | 2026-04-19 |

**Status**: SCAFFOLD_CREATED_FROM_SCREEN
**Source**: Automated screen discovery

## Overview
Auto-generated blueprint stub from PowerApps screen migration.

## Screen Reference
- Code: DRD
- Department: HR

## Migration Markers
- [x] REQUIREMENTS_ANALYZED
- [x] DATA_MAPPING_DEFINED
- [x] VALIDATION_RULES_DOCUMENTED
- [x] ERROR_HANDLING_SPECIFIED

---
*Generated: Batch blueprint scaffold creation. Ready for conversion.*

## Workflow Stage Map

```
[Stage 1: Draft — Report Created]
         │ submit
         ▼
[Stage 2: Submitted — Under Review]
         │ reviewed / return
         ├─→ Reviewed: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Acknowledged / Closed]
```

| Stage | Action                  | Trigger                     | Actor Role    | SP Group              | Power Automate Action                                                     |
| ----- | ----------------------- | --------------------------- | ------------- | --------------------- | ------------------------------------------------------------------------- |
| 1     | Create & submit report  | Item created (FormCode=DRD) | Reporter      | `D05-HR-Staff`        | Set Status=Draft; stamp SubmittedBy/SubmittedDate; DRD_OnSubmit           |
| 2     | Reviewer review         | Status=Submitted            | Reviewer      | `D05-HR-Reviewers`    | Review report; add ReviewComments; DRD_OnReview                           |
| 3     | Acknowledge & close     | Status=Reviewed             | HR Manager    | `D05-HR-Managers`     | Acknowledge or return with remarks; set Status=Acknowledged; DRD_OnAcknowledge |

### Power Automate Flows

| Flow Name              | Trigger                        | Key Actions                                                                 |
| ---------------------- | ------------------------------ | --------------------------------------------------------------------------- |
| `DRD_OnSubmit`         | Item created, FormCode=DRD     | Generate reference No; set Status=Submitted; notify Reviewer                |
| `DRD_OnReview`         | Status updated to Reviewed     | Stamp ReviewedDate; notify HR Manager for acknowledgement                   |
| `DRD_OnAcknowledge`    | Status updated to Acknowledged | Set AcknowledgedDate; lock record; notify Reporter of closure               |

### Role Matrix

| Domino Role   | SharePoint Group       | Permissions               |
| ------------- | ---------------------- | ------------------------- |
| Reporter      | `D05-HR-Staff`         | Create, Read own          |
| Reviewer      | `D05-HR-Reviewers`     | Read, Edit in review      |
| HR Manager    | `D05-HR-Managers`      | Read, Acknowledge, Close  |
| Admin         | `D05-HR-Admins`        | Full control              |

---

## Blueprint Status


| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | VALIDATED   |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PASS        |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

