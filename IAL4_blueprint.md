# Technical Blueprint - IAL4

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
| Form Code                  | `IAL4`                                                          |
| Official Name              | `Server Records`                                                |
| Department                 | `IT`                                                            |
| Module                     | `M2 - IT Support & Service Requests`                            |
| Site(s)                    | `PRAI`                                                          |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/IAL4.pdf` |
| Domino Database            | `IT.nsf`                                                        |
| Official Name Claim Status | `Claimed` (validated against source PDF in client drop)         |
| Blueprint Version          | `1.0`                                                           |
| Blueprint Date             | `2026-04-13`                                                    |
| Architect                  | `GitHub Copilot (Architect Agent)`                              |

---

## Purpose

IAL4 captures structured server-record entries for IT incident/service analysis, including
chronology, root-cause context, and corrective/preventive actions, then routes records through
distribution and archival stages in `MainDB_IT`.

### Governance Notes

- DEC-001 (live submissions): all new IAL4 submissions write to `MainDB_IT` only. Any form-specific
  list such as `IT_IAL4_List` is historical import/staging only and must not receive live
  submissions.
- DEC-004 (environment strategy): environment-variant values (distribution recipients, reminder
  windows, archive thresholds, sender profile, escalation owner) must be loaded from
  `Config_AppSettings` for `DEV`, `TEST`, and `PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is the sole authoritative
  source for column definitions and is available in this workspace for schema reconciliation.

---

## SharePoint Schema

**Target List:** `MainDB_IT` **URL:**
`https://ioioi.sharepoint.com/sites/ioi-portal-it/Lists/MainDB_IT`

| Column Name          | SP Type                 | Required | Choices / Source                        | Notes                                                          |
| -------------------- | ----------------------- | -------- | --------------------------------------- | -------------------------------------------------------------- |
| Title                | Single line of text     | Yes      | Auto-generated display ID               | Display identifier for IAL4 item                               |
| FormCode             | Single line of text     | Yes      | Constant `IAL4`                         | Routing/filter key                                             |
| Site                 | Choice                  | Yes      | Site master list                        | Domino `rbSite`                                                |
| ServerName           | Choice                  | Yes      | Server master list                      | Domino `lstServerName`                                         |
| RecordType           | Choice                  | Yes      | Record-type list                        | Domino `lstRecType`                                            |
| Mode                 | Choice                  | Yes      | Mode/severity list                      | Domino `rbMode`                                                |
| DateFrom             | Date and Time           | Yes      | User input                              | Domino `dtFrom`                                                |
| DateTo               | Date and Time           | No       | User input                              | Domino `dtTo`                                                  |
| TimeFrom             | Date and Time           | Yes      | User input                              | Domino `tmFrom`                                                |
| TimeTo               | Date and Time           | No       | User input                              | Domino `tmTo`                                                  |
| Overview             | Multiple lines of text  | Yes      | User input                              | Domino `Summary`                                               |
| OverviewDetail       | Multiple lines of text  | No       | User input                              | Domino `txtSummary`                                            |
| Background           | Multiple lines of text  | No       | User input                              | Domino `txtBackground`                                         |
| Analysis             | Multiple lines of text  | No       | User input                              | Domino `txtAnalysis`                                           |
| RootCauseDescription | Multiple lines of text  | No       | User input                              | Domino `txtRootCause`                                          |
| CorrectiveActions    | Multiple lines of text  | No       | User input                              | Domino `txtCA`                                                 |
| PreventiveActions    | Multiple lines of text  | No       | User input                              | Domino `txtPA`                                                 |
| RequiredReboot       | Choice                  | No       | Yes; No                                 | Domino `YESNO`                                                 |
| AttachmentLink       | Hyperlink or Picture    | No       | User/flow managed                       | Domino `SvrAttach`; use native list attachment where available |
| PerformedBy          | Person or Group         | Yes      | User directory                          | Domino `nmReqRecords`                                          |
| CreatorPerson        | Person or Group         | Yes      | System/user context                     | Domino `nmRequestor`                                           |
| CreatedOn            | Date and Time           | Yes      | System timestamp                        | Domino `dtCreatedOn`                                           |
| RoutedEditor         | Person or Group         | No       | Workflow managed                        | Domino `AEditor1`                                              |
| CurrentAction        | Choice                  | Yes      | Draft; Submitted; Distributed; Archived | Domino `CurrentAction`                                         |
| ITAdminOwner         | Person or Group         | No       | Config-driven                           | Domino `ISAdmin`                                               |
| DisplayServerName    | Single line of text     | No       | Derived                                 | Domino `dsSvrName`                                             |
| ISGRecipients        | Person or Group (multi) | No       | Config or workflow resolved             | Domino `ISGRecipients`                                         |
| Status               | Choice                  | Yes      | Draft; Submitted; Distributed; Closed   | Workflow status                                                |
| SubmittedBy          | Person or Group         | Yes      | System/user context                     | Mandatory cross-form column                                    |
| SubmittedDate        | Date and Time           | Yes      | System timestamp                        | Mandatory cross-form column                                    |
| ApprovedBy           | Person or Group         | No       | Stage actor stamp                       | Stage 2 distribution approval stamp                            |
| ApprovedDate         | Date and Time           | No       | Flow managed                            | Stage 2 distribution approval timestamp                        |
| Comments             | Multiple lines of text  | No       | User/flow note                          | Workflow note and archive remarks                              |
| ArchivedDate         | Date and Time           | No       | Flow managed                            | Archive evidence timestamp                                     |
| WorkflowAuditJson    | Multiple lines of text  | No       | Flow generated                          | Optional troubleshooting trace                                 |

---

## Workflow Stage Map

```
[Stage 1: Record Entry] --submit--> [Stage 2: IT Distribution Approval] --approve--> [Stage 3: Archive]
     |                                      |                                      |
     |                                      reject                                  retain/close
     +-------------------------rework----------------------------------------------+
```

| Stage | Action                                                  | Actor Role                                             | SP Group            | Power Automate Trigger                                   |
| ----- | ------------------------------------------------------- | ------------------------------------------------------ | ------------------- | -------------------------------------------------------- |
| 1     | Create and submit server record                         | Record owner (`PerformedBy`)                           | `D06-IT-Initiators` | When item created in `MainDB_IT` where `FormCode = IAL4` |
| 2     | Validate record completeness and approve distribution   | IT distribution owner (`ITAdminOwner` / routed editor) | `D06-IT-Editors-L1` | When `Status = Submitted`                                |
| 3     | Archive and close server record for retention/reporting | IT admin custodian                                     | `D06-IT-IT-Admin`   | When `Status = Distributed` and archive condition met    |

---

## Role Matrix

| Domino Group                             | SharePoint Group    | Permission Level                                   |
| ---------------------------------------- | ------------------- | -------------------------------------------------- |
| `nmReqRecords` (record owner)            | `D06-IT-Initiators` | Contribute (create and edit own in Draft/Returned) |
| `AEditor1` (routed editor)               | `D06-IT-Editors-L1` | Contribute (assigned review/distribution actions)  |
| `ISAdmin` (IT admin owner)               | `D06-IT-IT-Admin`   | Full Control                                       |
| `ISGRecipients` (stakeholder recipients) | `D06-IT-Readers`    | Read                                               |

---

## Power Automate Actions

| Stage                | Flow Name                 | Trigger                                    | Actions                                                                                                          | Notification Target                    |
| -------------------- | ------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| Submit               | `IT_IAL4_Submit`          | SP - When item created (`FormCode = IAL4`) | Validate mandatory fields; set `Status=Submitted`; stamp `SubmittedBy/SubmittedDate`; normalize date/time fields | IT distribution owner and record owner |
| Distribution Approve | `IT_IAL4_Distribute`      | SP - When `Status=Submitted`               | Resolve recipient set; set `Status=Distributed`; stamp `ApprovedBy/ApprovedDate`; send server-record notice      | `ISGRecipients` and IT readers         |
| Distribution Reject  | `IT_IAL4_ReturnForRework` | SP - Rejection action at Stage 2           | Set `Status=Draft`; append rejection reason in `Comments`; notify owner for correction                           | Record owner (`PerformedBy`)           |
| Archive              | `IT_IAL4_Archive`         | Scheduled recurrence or admin close        | Set `Status=Closed`; set `CurrentAction=Archived`; stamp `ArchivedDate`; persist `WorkflowAuditJson`             | IT admin and reporting audience        |

---

## Screen Inventory

| Screen Name | Purpose                               | Visible To                  |
| ----------- | ------------------------------------- | --------------------------- |
| `IAL4_List` | Search and review server records      | IT readers, editors, admins |
| `IAL4_New`  | Create and submit server record       | IT initiators/editors       |
| `IAL4_View` | Read-only detail and workflow history | IT readers, editors, admins |
| `IAL4_Edit` | Complete distribution/closure updates | Editors and IT admins       |

---

## Navigation Map

`IAL4_List` -> `IAL4_New` (submit) -> `IAL4_View` (post-submit review) -> `IAL4_Edit`
(distribution/archive actions) -> `IAL4_List`.

---

## Migration Risks & Notes

- Risk: Data quality drift in root-cause and corrective-action fields due to optional narrative
  entry.
- Mitigation: Add flow validation for minimum content standards before distribution approval.
- Risk: Recipients may be incomplete when routing depends on environment configuration.
- Mitigation: Enforce non-empty resolved recipient set in stage-2 approval flow.

---

## v3 Impossibilities (if any)

| Domino Feature                                                                      | Reason Impossible in v3                                                              | Recommended Workaround                                                                                        |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Domino hidden-field recomputation on save (`CurrentAction`, editor routing helpers) | Canvas apps do not execute Domino form event lifecycle semantics                     | Move all stage transitions and routing logic to Power Automate with explicit SharePoint status columns        |
| In-form action link `Click here to create Server reboot log`                        | Direct Domino-to-Domino form action links are not available in Power Apps v3 runtime | Replace with a controlled command button to open/create linked `IAL1` item using deep-link and relational key |

---

## Reference PDF

- **Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/IAL4.pdf`
- **Subforms included:** none identified from extracted evidence
- **Page count:** 2

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
VERIFICATION CHECKLIST - Server Records (IAL4)

[✓] All fields identified: [25] fields found, [25] clarified
[✓] Zero unresolved CLARIFY markers: [0] remaining
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining
[✓] Zero unresolved MISSING markers: [0] remaining
[✓] Workflow stages fully mapped: [3] of [3] stages complete
[✓] Power Automate actions defined for each stage: [3] of [3] stages
[✓] Roles mapped to SharePoint groups: [4] of [4] roles mapped
[✓] All mandatory columns mapped: [8] of [8] columns

COMPLETION STATUS: COMPLETE
```

---

## Sentinel Validation Report

**Validation Date:** 2026-04-19T08:14:36Z **Validator Agent:** Sentinel v1.1 (Fallback Mode)
**Blueprint:** IAL4 (Server Records) **Input Status:** COMPLETE

### Validation Results

| Check # | Validation Item                                                   | Status  | Evidence / Comment                               |
| ------- | ----------------------------------------------------------------- | ------- | ------------------------------------------------ |
| 1       | YAML frontmatter removed — Form Identity table present            | ✅ PASS | Blueprint Status + Form Identity tables found    |
| 2       | Section order compliance (12 sections)                            | ✅ PASS | All required sections verified in order          |
| 3       | Workflow Stage Map formal table present                           | ✅ PASS | Pipe-delimited trigger-condition table confirmed |
| 4       | Role Matrix mapped to SP security groups                          | ✅ PASS | D06-IT-[Role] groups mapped                      |
| 5       | Power Automate flow names follow [DEPT]_[FORM]_[Event] convention | ✅ PASS | IT*IAL4*[Event] naming confirmed                 |
| 6       | Zero CLARIFY / TODO / UNCLEAR / MISSING / NEEDS REVIEW markers    | ✅ PASS | check-markers.sh EXIT 0                          |
| 7       | Architect Verification Checklist status = COMPLETE                | ✅ PASS | COMPLETION STATUS: COMPLETE found                |
| 8       | Blueprint Status table present with all lifecycle fields          | ✅ PASS | All 6 status fields present                      |

### Validation Verdict

**GATE STATUS:** ✅ **PASS** — Blueprint meets all compliance requirements. Lifecycle Status updated
to VALIDATED. Ready for Requirement Synthesizer dispatch.

---

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:14:36Z
