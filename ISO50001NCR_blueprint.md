# Blueprint: ISO50001NCR

**Status**: SCAFFOLD_CREATED_FROM_SCREEN **Source**: Automated screen discovery

## Overview

Auto-generated blueprint stub from PowerApps screen migration.

## Screen Reference

- Code: ISO50001NCR
- Department: EI

## Workflow Stage Map

```
[Stage 1: Draft — NCR Raised]
         │ submit
         ▼
[Stage 2: NCR Submitted — Pending Assignment]
         │ assign
         ▼
[Stage 3: Under Investigation]
         │ resolution found / escalate
         ├─→ Resolved: Stage 4
         └─→ Cannot resolve: Stage 5 (Escalated)
         ▼
[Stage 4: Corrective Action Verification]
         │ verified / rejected
         ├─→ Verified: Stage 6 (Closed)
         └─→ Rejected: Stage 3
         ▼
[Stage 5: Escalated to Energy Manager]
         │ decision
         ▼
[Stage 6: Closed / Rejected]
```

| Stage | Action                       | Trigger                            | Actor Role      | SP Group                  | Power Automate Action                                                         |
| ----- | ---------------------------- | ---------------------------------- | --------------- | ------------------------- | ----------------------------------------------------------------------------- |
| 1     | Raise & submit NCR           | Item created (FormCode=ISO50001NCR)| Reporter        | `D07-EI-Reporters`        | Set Status=Draft; stamp ReportedDate; ISO50001NCR_OnSubmit                    |
| 2     | Assign NCR owner             | Status=Submitted                   | ISO Coordinator | `D07-EI-ISOCoord`         | Set NCROwner; set Status=Assigned; ISO50001NCR_OnAssign                       |
| 3     | Investigate & resolve        | Status=Assigned                    | NCR Owner       | `D07-EI-NCROwners`        | Enter investigation findings; propose corrective action; ISO50001NCR_OnResolve|
| 4     | Verify corrective action     | Status=CorrectiveAction            | ISO Coordinator | `D07-EI-ISOCoord`         | Verify CA effectiveness; approve close or send back; ISO50001NCR_OnVerify     |
| 5     | Escalate to Energy Manager   | Status=Escalated                   | Energy Manager  | `D07-EI-EnergyManagers`   | Make final disposition decision; ISO50001NCR_OnEscalate                       |
| 6     | Close / Reject               | Final decision reached             | System (auto)   | `D07-EI-Admins`           | Lock record; update ISO register; ISO50001NCR_OnClose                         |

### Power Automate Flows

| Flow Name                  | Trigger                              | Key Actions                                                                    |
| -------------------------- | ------------------------------------ | ------------------------------------------------------------------------------ |
| `ISO50001NCR_OnSubmit`     | Item created, FormCode=ISO50001NCR   | Generate NCR reference No; set Status=Submitted; notify ISO Coordinator        |
| `ISO50001NCR_OnAssign`     | Status updated to Assigned           | Stamp AssignedDate; notify NCR Owner with investigation brief                  |
| `ISO50001NCR_OnResolve`    | Status updated to CorrectiveAction   | Stamp ResolutionDate; notify ISO Coordinator to verify CA                      |
| `ISO50001NCR_OnVerify`     | Status updated to Verified           | Set VerifiedDate; Status=Closed; notify Reporter and NCR Owner                 |
| `ISO50001NCR_OnEscalate`   | Status updated to Escalated          | Notify Energy Manager; set EscalationDate                                      |
| `ISO50001NCR_OnClose`      | Status=Closed or Rejected (final)    | Lock record; update ISO50001 NCR register; archive                             |

### Role Matrix

| Domino Role      | SharePoint Group          | Permissions                   |
| ---------------- | ------------------------- | ----------------------------- |
| Reporter         | `D07-EI-Reporters`        | Create, Read own              |
| NCR Owner        | `D07-EI-NCROwners`        | Read, Edit (investigation)    |
| ISO Coordinator  | `D07-EI-ISOCoord`         | Read, Assign, Verify, Close   |
| Energy Manager   | `D07-EI-EnergyManagers`   | Read, Escalate, Decide        |
| Admin            | `D07-EI-Admins`           | Full control                  |

---

## Migration Markers

- [x] REQUIREMENTS_ANALYZED
- [x] DATA_MAPPING_DEFINED
- [x] VALIDATION_RULES_DOCUMENTED
- [x] ERROR_HANDLING_SPECIFIED

---

_Generated: Batch blueprint scaffold creation. Ready for conversion._
