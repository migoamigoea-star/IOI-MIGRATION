# Blueprint: ISO50001SOP

**Status**: SCAFFOLD_CREATED_FROM_SCREEN **Source**: Automated screen discovery

## Overview

Auto-generated blueprint stub from PowerApps screen migration.

## Screen Reference

- Code: ISO50001SOP
- Department: EI

## Workflow Stage Map

```
[Stage 1: Draft — SOP Authored]
         │ submit for review
         ▼
[Stage 2: Under Review — Energy Manager]
         │ reviewed / return
         ├─→ Reviewed: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: ISO Coordinator Approval]
         │ approve / reject
         ├─→ Approved: Stage 4
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Published / Active]
```

| Stage | Action                   | Trigger                            | Actor Role       | SP Group                    | Power Automate Action                                                       |
| ----- | ------------------------ | ---------------------------------- | ---------------- | --------------------------- | --------------------------------------------------------------------------- |
| 1     | Author & submit SOP      | Item created (FormCode=ISO50001SOP)| Document Author  | `D07-EI-Authors`            | Set Status=Draft; stamp AuthoredDate; ISO50001SOP_OnSubmit                  |
| 2     | Energy Manager review    | Status=Submitted                   | Energy Manager   | `D07-EI-EnergyManagers`     | Review SOP content; add ReviewComments; ISO50001SOP_OnReview                |
| 3     | ISO Coordinator approval | Status=UnderReview                 | ISO Coordinator  | `D07-EI-ISOCoord`           | Approve or Reject; set ApprovedBy/Date; ISO50001SOP_OnApprove / OnReject    |
| 4     | Publish SOP              | Status=Approved                    | System (auto)    | `D07-EI-Admins`             | Set Status=Published; set EffectiveDate; lock record; ISO50001SOP_OnPublish |

### Power Automate Flows

| Flow Name                 | Trigger                             | Key Actions                                                                  |
| ------------------------- | ----------------------------------- | ---------------------------------------------------------------------------- |
| `ISO50001SOP_OnSubmit`    | Item created, FormCode=ISO50001SOP  | Generate document reference No; set Status=Submitted; notify Energy Manager  |
| `ISO50001SOP_OnReview`    | Status updated to UnderReview       | Stamp ReviewedDate; notify ISO Coordinator                                   |
| `ISO50001SOP_OnApprove`   | Status updated to Approved          | Set ApprovedBy/Date; Status=Published; set EffectiveDate; notify Author      |
| `ISO50001SOP_OnReject`    | Status updated to Rejected          | Append rejection reason to ReviewComments; return to Document Author         |
| `ISO50001SOP_OnPublish`   | Status=Published (final)            | Lock record; distribute to ISO50001 SOP register; notify all stakeholders    |

### Role Matrix

| Domino Role       | SharePoint Group            | Permissions               |
| ----------------- | --------------------------- | ------------------------- |
| Document Author   | `D07-EI-Authors`            | Create, Read, Edit own    |
| Energy Manager    | `D07-EI-EnergyManagers`     | Read, Review              |
| ISO Coordinator   | `D07-EI-ISOCoord`           | Read, Approve, Reject     |
| Admin             | `D07-EI-Admins`             | Full control              |

---

## Migration Markers

- [x] REQUIREMENTS_ANALYZED
- [x] DATA_MAPPING_DEFINED
- [x] VALIDATION_RULES_DOCUMENTED
- [x] ERROR_HANDLING_SPECIFIED

---

_Generated: Batch blueprint scaffold creation. Ready for conversion._
