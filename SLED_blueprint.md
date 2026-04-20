## Blueprint Status

| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | UNDER_AUDIT |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PENDING     |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

---

## Form Identity

| Field                      | Value                                                            |
| -------------------------- | ---------------------------------------------------------------- |
| Form Code                  | `SLED`                                                           |
| Official Name              | `SAP Shelf Life Expiration Details`                              |
| Department                 | `STR (Department_16_STR)`                                        |
| Module                     | `M5 - SAP Store Transactions`                                    |
| Site(s)                    | `PRAI`                                                           |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/SLED.pdf` |
| Domino Database            | `PRAI_DB_Design_Original_File/STR`                               |
| Official Name Claim Status | `Claimed (SAPSLED alias uses SLED source form)`                  |
| Blueprint Version          | `1.1`                                                            |
| Blueprint Date             | `2026-04-18`                                                     |
| Architect                  | `GitHub Copilot (Architect mode)`                                |

---

## Purpose

SLED controls shelf-life expiry monitoring and cross-functional disposition of expiring stock. The
workflow routes identification, PP/PUR actioning, QC validation or extension decisions, and
Materials execution while preserving attributable audit trails and pending-action reminders.

## SharePoint Schema

**Target List:** `MainDB_STR`  
**Form Discriminator:** `FormCode = "SLED"`

### Parent List: MainDB_STR

| #   | SP Internal Name   | Display Label        | Column Type     | Required | Classification   | Notes                                                      |
| --- | ------------------ | -------------------- | --------------- | -------- | ---------------- | ---------------------------------------------------------- |
| 1   | FormCode           | Form Code            | Single line     | Yes      | SYSTEM-COMPUTED  | Fixed `SLED`                                               |
| 2   | INO                | SLED Ref No          | Single line     | Yes      | SYSTEM-COMPUTED  | `STR-SLED-YYMM-NNNN` via flow                              |
| 3   | CurrentStatus      | Workflow Status      | Choice          | Yes      | WORKFLOW-MANAGED | Identifying, Disposing, Validating, Adjusting, Closed      |
| 4   | CurrentAction      | Current Action       | Choice          | Yes      | WORKFLOW-MANAGED | Submit, PPReview, PURReview, QCDecision, MATExecute, Close |
| 5   | RunningNo          | Running No           | Single line     | Yes      | SYSTEM-COMPUTED  | Legacy running reference                                   |
| 6   | RequestDate        | Request Date         | Date and Time   | Yes      | USER-ENTERED     | Date opened by Store                                       |
| 7   | StorePIC           | Store PIC            | Person or Group | Yes      | USER-ENTERED     | Request owner                                              |
| 8   | MaterialCode       | Material Code        | Single line     | Yes      | USER-ENTERED     | SAP material code                                          |
| 9   | BatchNo            | Batch No             | Single line     | Yes      | USER-ENTERED     | Expiring batch reference                                   |
| 10  | ExpiryDate         | Expiry Date          | Date and Time   | Yes      | USER-ENTERED     | Batch expiry date                                          |
| 11  | PPAction           | PP Action            | Multiple lines  | No       | USER-ENTERED     | Planning disposition remarks                               |
| 12  | PURAction          | PUR Action           | Multiple lines  | No       | USER-ENTERED     | Procurement disposition remarks                            |
| 13  | QCAction           | QC Decision          | Multiple lines  | No       | USER-ENTERED     | Retest/extension decision                                  |
| 14  | MATAction          | Materials Action     | Multiple lines  | No       | USER-ENTERED     | Execution details                                          |
| 15  | ReminderToAll      | Reminder Flag        | Yes/No          | No       | WORKFLOW-MANAGED | Pending-action reminder control                            |
| 16  | RemDate            | Reminder Date        | Date and Time   | No       | WORKFLOW-MANAGED | Reminder timestamp                                         |
| 17  | PendingActionOwner | Pending Action Owner | Person or Group | No       | WORKFLOW-MANAGED | Current action assignee                                    |
| 18  | SubmittedBy        | Submitted By         | Person or Group | Yes      | SYSTEM-COMPUTED  | Captured on submit                                         |
| 19  | SubmittedDate      | Submitted Date       | Date and Time   | Yes      | SYSTEM-COMPUTED  | Captured on submit                                         |
| 20  | EnvironmentTag     | Environment          | Choice          | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                            |
| 21  | IsLocked           | Is Locked            | Yes/No          | No       | WORKFLOW-MANAGED | Set at closure                                             |

### Child List: STR_SLED_ExpiryLines

| #   | SP Internal Name  | Display Label      | Column Type         | Required | Notes                                      |
| --- | ----------------- | ------------------ | ------------------- | -------- | ------------------------------------------ |
| 1   | SLEDRef           | SLED Reference     | Lookup (MainDB_STR) | Yes      | Parent link                                |
| 2   | LineNo            | Line No            | Number              | Yes      | Sequence                                   |
| 3   | MaterialCode      | Material Code      | Single line         | Yes      | Child stock line                           |
| 4   | BatchNo           | Batch No           | Single line         | Yes      | Child batch                                |
| 5   | QtyAtRisk         | Qty at Risk        | Number              | Yes      | At-risk quantity                           |
| 6   | DispositionStatus | Disposition Status | Choice              | No       | Pending, Retest, Extend, Dispose, Adjusted |

## Workflow Stage Map

`Identifying -> Disposing -> Validating -> Adjusting -> Closed`

| Stage | Action                                | Actor Role      | SP Group                          | Power Automate Trigger            |
| ----- | ------------------------------------- | --------------- | --------------------------------- | --------------------------------- |
| 1     | Identify expiring stock and submit    | Store PIC       | D16-STR-StorePIC                  | Item created with `FormCode=SLED` |
| 2     | Record PP and PUR disposition actions | PP/PUR          | D16-STR-PP, D16-STR-PUR           | `CurrentStatus=Disposing`         |
| 3     | Record QC re-test/extension decision  | QC Reviewer     | D16-QC-Reviewers                  | `CurrentStatus=Validating`        |
| 4     | Execute stock adjustment action       | Materials Team  | D16-STR-Materials                 | `CurrentStatus=Adjusting`         |
| 5     | Close request                         | Store PIC/Admin | D16-STR-StorePIC / D16-STR-Admins | All required actions completed    |

## Role Matrix

| Domino Role / Field | SharePoint Group  | Permission Level |
| ------------------- | ----------------- | ---------------- |
| Store PIC           | D16-STR-StorePIC  | Contribute       |
| PP Reviewer         | D16-STR-PP        | Contribute       |
| PUR Reviewer        | D16-STR-PUR       | Contribute       |
| QC Reviewer         | D16-QC-Reviewers  | Contribute       |
| Materials Executor  | D16-STR-Materials | Contribute       |
| Admin               | D16-STR-Admins    | Full Control     |
| Reader              | D16-STR-Readers   | Read             |

## Power Automate Actions

| Stage    | Flow Name                   | Trigger                                 | Actions                                                            |
| -------- | --------------------------- | --------------------------------------- | ------------------------------------------------------------------ |
| Submit   | STR_SLED_OnSubmit           | Item created with `FormCode=SLED`       | Generate INO, set CurrentStatus=Identifying, notify PP/PUR         |
| Dispose  | STR_SLED_OnDisposition      | `CurrentStatus=Disposing`               | Capture PP/PUR actions and set next owner                          |
| Validate | STR_SLED_OnQCDecision       | `CurrentStatus=Validating`              | Capture QC decision (retest/extend/dispose), notify Materials      |
| Adjust   | STR_SLED_OnMaterialsExecute | `CurrentStatus=Adjusting`               | Capture execution update and line-level disposition                |
| Reminder | STR_SLED_OnReminder         | `ReminderToAll=true` or scheduled check | Notify pending action owner and maintain RemDate                   |
| Close    | STR_SLED_OnClose            | All mandatory stage fields complete     | Set CurrentStatus=Closed, IsLocked=Yes, issue closure notification |

## Screen Inventory

| Screen Name      | Purpose                                    | Visible To                   |
| ---------------- | ------------------------------------------ | ---------------------------- |
| SLED_List        | Track expiring-stock requests and statuses | STR, QC authorized users     |
| SLED_New         | Create new shelf-life expiry request       | Store PIC                    |
| SLED_View        | Read-only detail and history               | Authorized users             |
| SLED_Edit        | Stage-based updates by actor               | Role-based editors           |
| SLED_ExpiryLines | Child-line management for multiple batches | Store PIC, PP/PUR, Materials |

## Navigation Map

`SLED_List -> SLED_New -> SLED_View -> SLED_Edit -> SLED_ExpiryLines -> SLED_List`

## Migration Risks & Notes

- Alias mapping risk between SAPSLED and SLED can cause routing/config mismatch; fix on canonical
  FormCode=SLED and maintain alias mapping in governance notes.
- Multi-batch handling is not safe as flattened columns; use child list to preserve per-batch state
  traceability.
- Reminder and pending-action controls must remain flow-managed; manual status edits can bypass
  required handoffs.

## v3 Impossibilities

| Domino Feature                                                | Reason Impossible in v3                                         | Recommended Workaround                                          |
| ------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| Domino computed section behavior across multi-stage reviewers | Canvas does not replicate Domino section engine                 | Stage-based role visibility and flow-enforced state transitions |
| Domino embedded repeat-block arrays for stock lines           | Canvas form fields do not natively emulate legacy arrays safely | Normalize to child list and render with gallery/table controls  |

## Reference PDF

- Path: `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/SLED.pdf`
- Supporting DQ Evidence:
  `domino-tracker/data/uploads/docs/migration-analysis/DQ/STR/GxP_DQ_SAPSLED_2026-04-17.md`
- Additional Source Evidence:
  `Latest_Client_provided_file/PRAI_DB_Design_Original_File/STR/SLED.pdf`
- Page Count: To be confirmed during Sentinel validation

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - SLED (SAP Shelf Life Expiration Details)

[✓] All required sections present in canonical order
[✓] Blueprint status fields populated with architect gate values
[✓] Zero unresolved CLARIFY markers
[✓] Zero unresolved TODO markers
[✓] Zero unresolved UNCLEAR markers
[✓] Zero unresolved MISSING markers
[✓] Workflow stages mapped for Store, PP, PUR, QC, and Materials
[✓] Child list modeled for multi-batch expiry line handling
[✓] Power Automate actions include reminder and pending-owner controls
[✓] Roles mapped to concrete SharePoint groups

COMPLETION STATUS: COMPLETE
```

**Handoff Status:** NOT READY FOR CRAFTSMAN (Sentinel validation pending)
