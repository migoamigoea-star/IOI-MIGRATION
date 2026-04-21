# Blueprint: PRODSYSMOD

**Status**: SCAFFOLD_CREATED_FROM_SCREEN **Source**: Automated screen discovery

## Overview

Auto-generated blueprint stub from PowerApps screen migration.

## Screen Reference

- Code: PRODSYSMOD
- Department: EI

## Workflow Stage Map

```
[Stage 1: Draft — Modification Request Raised]
         │ submit
         ▼
[Stage 2: Engineering Review]
         │ reviewed / return
         ├─→ Reviewed: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: EI Management Approval]
         │ approve / reject
         ├─→ Approved: Stage 4
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Implementation in Progress]
         │ implementation complete
         ▼
[Stage 5: Closed / Verified]
```

| Stage | Action                        | Trigger                              | Actor Role      | SP Group               | Power Automate Action                                                         |
| ----- | ----------------------------- | ------------------------------------ | --------------- | ---------------------- | ----------------------------------------------------------------------------- |
| 1     | Raise & submit request        | Item created (FormCode=PRODSYSMOD)   | Initiator       | `D07-EI-Initiators`    | Set Status=Draft; stamp SubmittedDate; PRODSYSMOD_OnSubmit                    |
| 2     | Engineering review            | Status=Submitted                     | Engineer        | `D07-EI-Engineers`     | Technical feasibility review; add EngRemarks; PRODSYSMOD_OnReview             |
| 3     | Management approval           | Status=UnderReview                   | EI Manager      | `D07-EI-Managers`      | Approve or Reject with justification; PRODSYSMOD_OnApprove / OnReject         |
| 4     | Implementation                | Status=Approved                      | Engineer        | `D07-EI-Engineers`     | Execute modification; record completion; PRODSYSMOD_OnImplement               |
| 5     | Close & verify                | Status=Implemented                   | System (auto)   | `D07-EI-Admins`        | Stamp ClosedDate; lock record; archive; PRODSYSMOD_OnClose                    |

### Power Automate Flows

| Flow Name                 | Trigger                              | Key Actions                                                                  |
| ------------------------- | ------------------------------------ | ---------------------------------------------------------------------------- |
| `PRODSYSMOD_OnSubmit`     | Item created, FormCode=PRODSYSMOD    | Generate reference No; set Status=Submitted; notify Engineer for review      |
| `PRODSYSMOD_OnReview`     | Status updated to UnderReview        | Stamp ReviewedDate; notify EI Manager for approval decision                  |
| `PRODSYSMOD_OnApprove`    | Status updated to Approved           | Set ApprovedBy/Date; Status=Implementation; notify Engineer to proceed       |
| `PRODSYSMOD_OnReject`     | Status updated to Rejected           | Append rejection reason; return to Initiator for revision                    |
| `PRODSYSMOD_OnImplement`  | Status updated to Implemented        | Stamp ImplementedDate; notify EI Manager for final sign-off                  |
| `PRODSYSMOD_OnClose`      | Status=Closed (final)                | Lock record; update production modification register; archive                |

### Role Matrix

| Domino Role   | SharePoint Group        | Permissions                   |
| ------------- | ----------------------- | ----------------------------- |
| Initiator     | `D07-EI-Initiators`     | Create, Read own              |
| Engineer      | `D07-EI-Engineers`      | Read, Review, Implement       |
| EI Manager    | `D07-EI-Managers`       | Read, Approve, Reject         |
| Admin         | `D07-EI-Admins`         | Full control                  |

---

## Migration Markers

- [ ] REQUIREMENTS_ANALYZED
- [ ] DATA_MAPPING_DEFINED
- [ ] VALIDATION_RULES_DOCUMENTED
- [ ] ERROR_HANDLING_SPECIFIED

---

_Generated: Script-driven scaffold. Requires manual completion._
