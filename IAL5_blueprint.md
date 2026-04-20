# Technical Blueprint - IAL5

## Blueprint Status

| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | VALIDATED   |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PASS        |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

## Form Identity

| Field                      | Value                                                           |
| -------------------------- | --------------------------------------------------------------- |
| Form Code                  | `IAL5`                                                          |
| Official Name              | `Data Restoration Request`                                      |
| Department                 | `IT`                                                            |
| Module                     | `M2 - IT Support & Service Requests`                            |
| Site(s)                    | `PRAI`                                                          |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/IAL5.pdf` |
| Domino Database            | `IT.nsf`                                                        |
| Official Name Claim Status | `Claimed` (validated against source PDF in client drop)         |
| Blueprint Version          | `1.0`                                                           |
| Blueprint Date             | `2026-04-13`                                                    |
| Architect                  | `GitHub Copilot (Architect Agent)`                              |

---

## Purpose

IAL5 manages IT data restoration requests across submission, assignment, backup-administrator
processing, and closure stages while preserving auditability for requested assets, restoration
outcomes, and stakeholder notifications.

### Governance Notes

- DEC-001 (live submissions): all new IAL5 submissions must write to `MainDB_IT` only. Any
  form-specific list such as `IT_IAL5_List` is historical import/staging only and must not receive
  live submissions.
- DEC-004 (environment strategy): environment-specific values (backup administrator routing
  defaults, manager distribution groups, reminder/escalation windows, sender profile) must be loaded
  from `Config_AppSettings` for `DEV`, `TEST`, and `PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is the sole authoritative
  source for column definitions and is available in this workspace for schema reconciliation.

---

## SharePoint Schema

**Target List:** `MainDB_IT`  
**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal-it/Lists/MainDB_IT`

| Column Name           | SP Type                 | Required | Choices / Source                                                    | Notes                                                            |
| --------------------- | ----------------------- | -------- | ------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Title                 | Single line of text     | Yes      | Auto-generated display ID                                           | Display identifier for IAL5 item                                 |
| FormCode              | Single line of text     | Yes      | Constant `IAL5`                                                     | Routing/filter key                                               |
| INONumber             | Number                  | Yes      | Flow-generated sequence                                             | Domino `INO`; PATTERN-E auto-number via Power Automate only      |
| Site                  | Choice                  | Yes      | Site master list                                                    | Domino `rbSite`                                                  |
| RequestedBy           | Person or Group         | Yes      | User directory                                                      | Domino `nmRequestedBy`                                           |
| Department            | Choice                  | Yes      | Department master list                                              | Domino `lstDept`                                                 |
| RequestMediaReference | Single line of text     | No       | User input                                                          | Domino `txtMedia`                                                |
| ServerName            | Choice                  | Yes      | Server master list                                                  | Domino `lstServerName`                                           |
| RestorePath           | Single line of text     | Yes      | User input                                                          | Domino `txtFilePath`                                             |
| RequestedFileOrFolder | Single line of text     | Yes      | User input                                                          | Domino `txtFileName`                                             |
| RequestReason         | Multiple lines of text  | Yes      | User input                                                          | Domino `txtReason`                                               |
| RequestAttachmentLink | Hyperlink or Picture    | No       | User/flow managed                                                   | Domino `rtxtAttach`; prefer native SharePoint attachment storage |
| CCInternal            | Person or Group (multi) | No       | User directory                                                      | Domino `nmCC`                                                    |
| SubmittedBy           | Person or Group         | Yes      | System/user context                                                 | Domino `nmSubmitted` and mandatory cross-form column             |
| SubmittedDate         | Date and Time           | Yes      | System timestamp                                                    | Domino `dtSubmitted` and mandatory cross-form column             |
| BackupMediaName       | Single line of text     | No       | Backup admin input                                                  | Domino `txtMediaName`                                            |
| BackupMediaDate       | Date and Time           | No       | Backup admin input                                                  | Domino `dtMediadate`                                             |
| RestoredFileName      | Single line of text     | No       | Backup admin input                                                  | Domino `txtFileName1`                                            |
| BackupAdminRemarks    | Multiple lines of text  | No       | Backup admin input                                                  | Domino `Remark`                                                  |
| RestorationStatus     | Choice                  | Yes      | Pending Assignment; In Progress; Completed; Failed; Returned        | Domino `rbStatus`                                                |
| PerformedBy           | Person or Group         | No       | User directory                                                      | Domino `nmPerformed`                                             |
| PerformedDate         | Date and Time           | No       | Flow stamp                                                          | Domino `dtPerformed`                                             |
| CreatorPerson         | Person or Group         | Yes      | System/user context                                                 | Domino `nmRequestor`                                             |
| CreatedOn             | Date and Time           | Yes      | System timestamp                                                    | Domino `dtCreatedOn`                                             |
| ITAdminOwner          | Person or Group         | No       | Config/routing matrix                                               | Domino `ISAdmin`                                                 |
| DisplayServerName     | Single line of text     | No       | Derived helper                                                      | Domino `dsSvrName`                                               |
| MailPenangMgr         | Person or Group (multi) | No       | Routing matrix by site                                              | Domino `MailP_Mgr`                                               |
| MailJohorMgr          | Person or Group (multi) | No       | Routing matrix by site                                              | Domino `MailJ_Mgr`                                               |
| CurrentAction         | Choice                  | Yes      | Draft; Submitted; Assigned; Processing; Completed; Returned; Closed | Domino `CurrentAction`                                           |
| SectionIEditor        | Person or Group         | No       | Workflow managed                                                    | Domino `AEditor1`                                                |
| BackupAdminAssignee   | Person or Group         | No       | Routing matrix                                                      | Domino `nmBKAdmin`                                               |
| SectionIIEditor       | Person or Group         | No       | Workflow managed                                                    | Domino `AEditor2`                                                |
| Status                | Choice                  | Yes      | Draft; Submitted; In Review; Completed; Rejected; Closed            | Workflow control status                                          |
| ApprovedBy            | Person or Group         | No       | Stage actor stamp                                                   | Stage 2/3 approval actor                                         |
| ApprovedDate          | Date and Time           | No       | Flow stamp                                                          | Stage 2/3 approval timestamp                                     |
| Comments              | Multiple lines of text  | No       | User/flow note                                                      | Workflow comments and return reasons                             |
| WorkflowAuditJson     | Multiple lines of text  | No       | Flow-generated JSON                                                 | Optional troubleshooting/audit trace                             |

---

## Workflow Stage Map

```
[Stage 1: Request Submission] --submit--> [Stage 2: Backup Administrator Processing] --complete/fail--> [Stage 3: Final Status Update] --close--> [Stage 4: Closed]
            |                                              |                                                        |
            +---------------------------return for correction-----------------------------------------------+
```

| Stage | Action                                           | Actor Role                                                    | SP Group                                              | Power Automate Trigger                                   |
| ----- | ------------------------------------------------ | ------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------- |
| 1     | Create and submit restoration request            | Requestor (`RequestedBy`)                                     | `D06-IT-Initiators`                                   | When item created in `MainDB_IT` where `FormCode = IAL5` |
| 2     | Assign and process restoration details           | Backup Administrator (`BackupAdminAssignee`)                  | `D06-IT-Editors-L1`                                   | When `Status = Submitted` or `CurrentAction = Assigned`  |
| 3     | Validate completion data and notify stakeholders | IT Admin / Routed editor (`ITAdminOwner` / `SectionIIEditor`) | `D06-IT-IT-Admin`                                     | When `RestorationStatus` transitions to terminal state   |
| 4     | Retain record and close workflow                 | System + IT admin custodian                                   | `D06-IT-Readers` (read) and `D06-IT-IT-Admin` (close) | When `Status = Completed` and closure action executed    |

---

## Role Matrix

| Domino Group                                               | SharePoint Group    | Permission Level                               |
| ---------------------------------------------------------- | ------------------- | ---------------------------------------------- |
| `nmRequestedBy` / `nmSubmitted` (requestor/submitter)      | `D06-IT-Initiators` | Contribute (create/edit own before assignment) |
| `nmBKAdmin` / `AEditor2` (backup administrator processing) | `D06-IT-Editors-L1` | Contribute (assigned processing actions)       |
| `ISAdmin` / `AEditor1` (IT admin/routing owner)            | `D06-IT-IT-Admin`   | Full Control                                   |
| `nmCC` / `MailP_Mgr` / `MailJ_Mgr` (stakeholders/managers) | `D06-IT-Readers`    | Read                                           |

---

## Power Automate Actions

| Stage             | Flow Name          | Trigger                                                       | Actions                                                                                                                                            | Notification Target                |
| ----------------- | ------------------ | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Submit            | `IT_IAL5_Submit`   | SP - When item created (`FormCode = IAL5`)                    | Validate mandatory fields; generate `INONumber`; set `Status=Submitted`; stamp `SubmittedBy/SubmittedDate`; set `CurrentAction=Submitted`          | Backup administrator and requestor |
| Backup Processing | `IT_IAL5_Process`  | SP - When `Status=Submitted` or assignment action invoked     | Resolve backup admin assignee by site/server matrix; set `CurrentAction=Processing`; capture media/restoration details; update `RestorationStatus` | Requestor, CC, site managers       |
| Finalization      | `IT_IAL5_Finalize` | SP - When `RestorationStatus` becomes `Completed` or `Failed` | Enforce performed-by/date checks; stamp `ApprovedBy/ApprovedDate`; set `Status=Completed` or `Rejected`; append audit remarks                      | Requestor, CC, IT admin, managers  |
| Closure           | `IT_IAL5_Close`    | SP - When final state confirmed                               | Set `Status=Closed`; set `CurrentAction=Closed`; persist `WorkflowAuditJson`; retention tagging/reporting flag                                     | IT admin and reporting audience    |

---

## Screen Inventory

| Screen Name | Purpose                                              | Visible To                    |
| ----------- | ---------------------------------------------------- | ----------------------------- |
| `IAL5_List` | Search and track restoration requests                | IT readers, editors, admins   |
| `IAL5_New`  | Submit restoration request                           | IT initiators                 |
| `IAL5_View` | Review request details and status history            | Requestors, assignees, admins |
| `IAL5_Edit` | Process assignment, restoration details, and closure | Backup admins and IT admins   |

---

## Navigation Map

`IAL5_List` -> `IAL5_New` (submit request) -> `IAL5_View` (review status) -> `IAL5_Edit`
(processing/finalization) -> `IAL5_List`.

---

## Migration Risks & Notes

- Risk: Incorrect sequence generation could create duplicate `INONumber` values.
- Mitigation: Use atomic counter strategy in `IT_IAL5_Submit` flow with retry guard.
- Risk: Late completion updates can leave item state inconsistent (`RestorationStatus` vs `Status`).
- Mitigation: Centralize terminal state transitions in finalization flow and disallow direct manual
  edits.

---

## v3 Impossibilities (if any)

| Domino Feature                                                                | Reason Impossible in v3                                                            | Recommended Workaround                                                                                       |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Domino hidden-field lifecycle logic (`CurrentAction`, editor routing helpers) | Canvas apps do not execute Domino form event lifecycle formulas                    | Move all routing/state transitions to Power Automate using explicit status columns                           |
| Rich-text attachment behavior (`rtxtAttach`)                                  | Domino rich text attachment embedding is not preserved one-to-one in Power Apps v3 | Store files in SharePoint item attachments/document library and keep URL/metadata in `RequestAttachmentLink` |
| Inline INO numbering semantics on legacy form save                            | Domino document save formula sequencing is not directly available in Canvas        | Use PATTERN-E auto-number generation in `IT_IAL5_Submit` flow with atomic counter strategy                   |

---

## Reference PDF

- **Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/IAL5.pdf`
- **Analysis source used:** `docs/migration-analysis/Department_06_IT/IAL5_analysis.md`
- **Subforms included:** none explicitly identified
- **Page count:** 2 (from extracted first-page evidence set)

---

## Unresolved Marker Sweep

- `CLARIFY`: 0
- `TODO`: 0
- `UNCLEAR`: 0
- `MISSING`: 0
- `NEEDS REVIEW`: 0

---

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - Data Restoration Request (IAL5)

[✓] All fields identified: [30] fields found, [30] clarified
[✓] Zero unresolved CLARIFY markers: [0] remaining
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining
[✓] Zero unresolved MISSING markers: [0] remaining
[✓] Workflow stages fully mapped: [4] of [4] stages complete
[✓] Power Automate actions defined for each stage: [4] of [4] stages
[✓] Roles mapped to SharePoint groups: [4] of [4] roles mapped
[✓] All mandatory columns mapped: [8] of [8] columns

COMPLETION STATUS: COMPLETE
```

---

## Sentinel Validation Report

**Validation Date:** 2026-04-19T08:14:36Z **Validator Agent:** Sentinel v1.1 (Fallback Mode)
**Blueprint:** IAL5 (Data Restoration Request) **Input Status:** COMPLETE

### Validation Results

| Check # | Validation Item                                                   | Status  | Evidence / Comment                               |
| ------- | ----------------------------------------------------------------- | ------- | ------------------------------------------------ |
| 1       | YAML frontmatter removed — Form Identity table present            | ✅ PASS | Blueprint Status + Form Identity tables found    |
| 2       | Section order compliance (12 sections)                            | ✅ PASS | All required sections verified in order          |
| 3       | Workflow Stage Map formal table present                           | ✅ PASS | Pipe-delimited trigger-condition table confirmed |
| 4       | Role Matrix mapped to SP security groups                          | ✅ PASS | D06-IT-[Role] groups mapped                      |
| 5       | Power Automate flow names follow [DEPT]_[FORM]_[Event] convention | ✅ PASS | IT*IAL5*[Event] naming confirmed                 |
| 6       | Zero CLARIFY / TODO / UNCLEAR / MISSING / NEEDS REVIEW markers    | ✅ PASS | check-markers.sh EXIT 0                          |
| 7       | Architect Verification Checklist status = COMPLETE                | ✅ PASS | COMPLETION STATUS: COMPLETE found                |
| 8       | Blueprint Status table present with all lifecycle fields          | ✅ PASS | All 6 status fields present                      |

### Validation Verdict

**GATE STATUS:** ✅ **PASS** — Blueprint meets all compliance requirements. Lifecycle Status updated
to VALIDATED. Ready for Requirement Synthesizer dispatch.

---

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:14:36Z
