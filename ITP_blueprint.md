## Blueprint Status

| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | VALIDATED   |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PASS        |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

---

## Form Identity

| Field                      | Value                                                                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Form Code                  | `ITP`                                                                                                                                             |
| Official Name              | `ISG Documentation register form used to store and manage IT/ISG documentation metadata, revision info, attachments, and reader/edit permissions` |
| Department                 | `IT`                                                                                                                                              |
| Module                     | `M5 - Documentation & Policies`                                                                                                                   |
| Site(s)                    | `PRAI`                                                                                                                                            |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/ITP.pdf`                                                                                    |
| Domino Database            | `PRAI_DB_Design_Original_File/IT`                                                                                                                 |
| Official Name Claim Status | `Claimed` (validated against source PDF in client drop)                                                                                           |
| Blueprint Version          | `1.0`                                                                                                                                             |
| Blueprint Date             | `2026-04-13`                                                                                                                                      |
| Architect                  | `GitHub Copilot (GPT-5.3-Codex)`                                                                                                                  |

---

## Purpose

ITP is the ISG documentation register form for maintaining controlled IT documentation metadata,
ownership, revision history, publication state, and reader permissions. The target implementation
uses `MainDB_IT` as the live submission store, with routing based on `FormCode=ITP`.

### Source Evidence

- PDF checked first and used as primary source:
  `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/ITP.pdf`
- Metadata confirmed: Title `isgdoc - Form`, Pages `2`, printed PDF (`Form: none`)
- AcroForm/XFA detection: AcroForm field count `0`, `HasAcroForm=False`
- Visible text evidence used for mapping: `type`, `doctitle`, `verno`, `datelast`, `revision`,
  `Owner`, `att`, `ApplicableTo`, `Comments`, `Authors`, `MachineAuthor/DateModified`,
  `MachineCreationDate`, `MachineModificationDate`, `Readers`, `Status`

Supplemental references used after PDF verification:

- `docs/migration-analysis/Department_06_IT/ITP_analysis.md`
- `docs/Archive_analysy/Depratment/IT/ITP2_2_2.md`

---

### DEC-001 / DEC-004 / DEC-005 Control Notes

- DEC-001 (live submissions): all new ITP submissions write to `MainDB_IT` only. Any form-specific
  list such as `IT_ITP_List` is historical import/staging only and must not receive live
  submissions.
- DEC-004 (environment strategy): environment-variant values (review/publish approver aliases,
  notification sender profile, reminder cadence, archive recipients) must be loaded from
  `Config_AppSettings_IT` and promoted through `DEV -> TEST -> PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is the sole authoritative
  source for column definitions and is available in this workspace for schema reconciliation.

---

## SharePoint Schema

**Target List:** `MainDB_IT`  
**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal-it/Lists/MainDB_IT`

| Column Name             | SP Type                 | Required | Choices / Source                                  | Notes                                            |
| ----------------------- | ----------------------- | -------- | ------------------------------------------------- | ------------------------------------------------ |
| Title                   | Single line of text     | Yes      | Auto-generated display ID (`ITP-YYYYMM-####`)     | Primary identifier                               |
| FormCode                | Single line of text     | Yes      | Constant `ITP`                                    | Routing/filter key                               |
| type                    | Choice                  | Yes      | SOP; WI; Policy; TrainingManual; Guideline; Other | Domino `type`                                    |
| doctitle                | Single line of text     | Yes      | User input                                        | Domino `doctitle`                                |
| verno                   | Single line of text     | Yes      | Governed format (for example `V1.0`)              | Domino `verno`                                   |
| datelast                | Date and Time           | Yes      | User/flow managed                                 | Domino `datelast`                                |
| revision                | Single line of text     | No       | User/flow managed                                 | Domino `revision`                                |
| Owner                   | Person or Group (multi) | Yes      | Directory selection                               | Domino `Owner` (edit rights)                     |
| att                     | Hyperlink or Picture    | No       | SharePoint attachment/document link               | Domino `att`; use native attachment storage      |
| ApplicableTo            | Multiple lines of text  | No       | User input                                        | Domino `ApplicableTo`                            |
| Comments                | Multiple lines of text  | No       | User/approver comments                            | Domino `Comments`                                |
| Authors                 | Person or Group         | Yes      | System/user context                               | Domino `Authors` (creator owner)                 |
| MachineAuthor           | Person or Group         | No       | Flow/system update                                | Split from `MachineAuthor/DateModified` evidence |
| DateModified            | Date and Time           | No       | Flow/system update                                | Split from `MachineAuthor/DateModified` evidence |
| MachineCreationDate     | Date and Time           | No       | Flow/system update                                | Domino hidden metadata                           |
| MachineModificationDate | Date and Time           | No       | Flow/system update                                | Domino hidden metadata                           |
| Readers                 | Person or Group (multi) | No       | Directory groups/users                            | Domino `Readers` (PATTERN-F access control)      |
| CurrentAction           | Choice                  | Yes      | Draft; UnderOwnerReview; Published; Archived      | Workflow stage state                             |
| Status                  | Choice                  | Yes      | Draft; Submitted; Approved; Rejected; Archived    | Cross-form lifecycle status                      |
| SubmittedBy             | Person or Group         | Yes      | System context                                    | Mandatory live-submission audit column           |
| SubmittedDate           | Date and Time           | Yes      | System timestamp                                  | Mandatory live-submission audit column           |
| ApprovedBy              | Person or Group         | No       | Workflow approver                                 | Publish/approval actor                           |
| ApprovedDate            | Date and Time           | No       | Workflow timestamp                                | Publish/approval timestamp                       |

PATTERN-F mapping note: `Owner` and `Readers` are retained as primary access-control columns for
item-level visibility/edit policies.

---

## Workflow Stage Map

```
[Stage 1: Documentation Authoring] -> [Stage 2: Owner Review] -> [Stage 3: ISG Publish]
          ^                                    |                     |
          |---------- reject/rework -----------|----- archive ------|
```

| Stage | Action                                    | Actor Role                    | SP Group          | Power Automate Trigger                |
| ----- | ----------------------------------------- | ----------------------------- | ----------------- | ------------------------------------- |
| 1     | Create draft and submit                   | Documentation PIC (`Authors`) | `D06-IT-Editors`  | When item created (`FormCode=ITP`)    |
| 2     | Review metadata, scope, and attachments   | Document Owner (`Owner`)      | `D06-IT-Owners`   | When `CurrentAction=UnderOwnerReview` |
| 3     | Approve/publish and distribute to readers | ISG Admin / IT Manager        | `D06-IT-Managers` | When owner decision = Approve         |

Reject path: owner rejection sets `Status=Rejected`, returns `CurrentAction=Draft`, and notifies
`Authors`.

---

## Role Matrix

| Domino Group / Field              | SharePoint Group  | Permission Level        |
| --------------------------------- | ----------------- | ----------------------- |
| `Authors`                         | `D06-IT-Editors`  | Contribute              |
| `Owner`                           | `D06-IT-Owners`   | Edit/Approve at Stage 2 |
| ISG Admin (publication authority) | `D06-IT-Managers` | Approve/Full Control    |
| `Readers`                         | `D06-IT-Readers`  | Read                    |

---

## Power Automate Actions

| Stage        | Flow Name            | Trigger                                  | Actions                                                                                           | Notification Target             |
| ------------ | -------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------- |
| Submit       | `IT_ITP_Submit`      | SharePoint item created (`FormCode=ITP`) | Set `Status=Submitted`; set `CurrentAction=UnderOwnerReview`; stamp `SubmittedBy/SubmittedDate`   | `Owner`                         |
| Owner Review | `IT_ITP_OwnerReview` | Item modified with owner decision        | Approve: set `Status=Approved`; reject: set `Status=Rejected`; write review comment               | `Authors` and `D06-IT-Managers` |
| Publish      | `IT_ITP_Publish`     | `Status=Approved`                        | Set `CurrentAction=Published`; stamp `ApprovedBy/ApprovedDate`; apply reader/editor access policy | `Readers`                       |
| Archive      | `IT_ITP_Archive`     | Scheduled or manual archive signal       | Set `Status=Archived`; set `CurrentAction=Archived`; notify owner/readers                         | `Owner`, `Readers`              |

Environment binding (DEC-004): sender profile, manager fallback, escalation window, and
archive-notification list are read from `Config_AppSettings_IT` by key per environment.

---

## Screen Inventory

| Screen Name | Purpose                                                   | Visible To                 |
| ----------- | --------------------------------------------------------- | -------------------------- |
| `ITP_List`  | Search and filter ITP records                             | IT readers, owners, admins |
| `ITP_New`   | Create a new documentation register entry                 | IT initiators/editors      |
| `ITP_View`  | Read-only details and publication metadata                | IT readers, owners, admins |
| `ITP_Edit`  | Update metadata, ownership, status, and reader assignment | Owners and IT admins       |

---

## Navigation Map

`ITP_List` -> `ITP_New` (create) -> `ITP_View` (after submit) -> `ITP_Edit` (owner/admin updates) ->
back to `ITP_List`.

---

## Migration Risks & Notes

- Risk: Reader/author behavior from Domino may not match SharePoint item-level permissions
  one-to-one.
- Mitigation: Enforce permission synchronization in publish/archive flows using `Owner` and
  `Readers` columns.
- Risk: Manual status updates can bypass expected lifecycle transitions.
- Mitigation: Restrict status edits to approved roles and flow-owned actions.

---

## v3 Impossibilities (if any)

No blocking v3 impossibilities identified for this form pattern.

| Domino Feature                                 | Reason Impossible in v3                                                            | Recommended Workaround                                                                    |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Domino Reader/Author runtime security formulas | Domino formula-driven security is not directly portable to Canvas runtime formulas | Use SharePoint item permissions + `Owner`/`Readers` columns + flow-driven permission sync |

---

## Reference PDF

- **Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/ITP.pdf`
- **Subforms included:** None explicitly indicated in the printed source
- **Page count:** 2

---

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - ISG Documentation register form (ITP)

[✓] All fields identified: [15] fields found from PDF evidence, [15] clarified
[✓] Zero unresolved CLARIFY markers: [0] remaining
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining
[✓] Zero unresolved MISSING markers: [0] remaining
[✓] Zero unresolved NEEDS REVIEW markers: [0] remaining
[✓] Workflow stages fully mapped: [3] of [3] stages complete
[✓] Power Automate actions defined for each stage: [4] of [4] stage actions
[✓] Roles mapped to SharePoint groups: [4] of [4] roles mapped
[✓] All mandatory columns mapped: [8] of [8] columns

COMPLETION STATUS: COMPLETE
```

---

## Sentinel Validation Report

**Validation Date:** 2026-04-19T08:14:36Z **Validator Agent:** Sentinel v1.1 (Fallback Mode)
**Blueprint:** ITP (ISG Documentation register form used to store and manage IT/ISG documentation
metadata, revision info, attachments, and reader/edit permissions) **Input Status:** COMPLETE

### Validation Results

| Check # | Validation Item                                                   | Status  | Evidence / Comment                               |
| ------- | ----------------------------------------------------------------- | ------- | ------------------------------------------------ |
| 1       | YAML frontmatter removed — Form Identity table present            | ✅ PASS | Blueprint Status + Form Identity tables found    |
| 2       | Section order compliance (12 sections)                            | ✅ PASS | All required sections verified in order          |
| 3       | Workflow Stage Map formal table present                           | ✅ PASS | Pipe-delimited trigger-condition table confirmed |
| 4       | Role Matrix mapped to SP security groups                          | ✅ PASS | D06-IT-[Role] groups mapped                      |
| 5       | Power Automate flow names follow [DEPT]_[FORM]_[Event] convention | ✅ PASS | IT*ITP*[Event] naming confirmed                  |
| 6       | Zero CLARIFY / TODO / UNCLEAR / MISSING / NEEDS REVIEW markers    | ✅ PASS | check-markers.sh EXIT 0                          |
| 7       | Architect Verification Checklist status = COMPLETE                | ✅ PASS | COMPLETION STATUS: COMPLETE found                |
| 8       | Blueprint Status table present with all lifecycle fields          | ✅ PASS | All 6 status fields present                      |

### Validation Verdict

**GATE STATUS:** ✅ **PASS** — Blueprint meets all compliance requirements. Lifecycle Status updated
to VALIDATED. Ready for Requirement Synthesizer dispatch.

---

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:14:36Z
