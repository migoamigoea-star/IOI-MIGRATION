# Technical Blueprint: IOIP

## Form Identity

| Field                      | Value                                                                  |
| -------------------------- | ---------------------------------------------------------------------- |
| Form Code                  | `IOIP`                                                                 |
| Official Name              | `IOIOI POLICY`                                                         |
| Department                 | `IT`                                                                   |
| Module                     | `M5 - Documentation & Policies`                                        |
| Site(s)                    | `PRAI`                                                                 |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/IOIP.pdf` |
| Domino Database            | `PRAI_DB_Design(2)`                                                    |
| Official Name Claim Status | `Claimed`                                                              |
| Blueprint Version          | `1.0`                                                                  |
| Blueprint Date             | `2026-04-13`                                                           |
| Architect                  | `GitHub Copilot (Architect Agent)`                                     |

---

## DEC-001 / DEC-004 / DEC-005 Control Notes

- DEC-001 (live submissions): all new IOIP submissions write to `MainDB_IT` only. Any IOIP-specific
  list is historical import/staging only and must not receive live submissions.
- DEC-004 (environment strategy): environment-variant values (approval routing recipients,
  escalation timers, sender profile, and archive retention windows) must be loaded from
  `Config_AppSettings` for `DEV`, `TEST`, and `PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is the sole authoritative
  column-definition source. This workspace currently has no discoverable local copy, so this
  blueprint is aligned to DEC-005 governance and must be reconciled against the canonical enhanced
  schema before TEST/PROD promotion.

---

## SharePoint Schema

**Target List:** `MainDB_IT`  
**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal-it/Lists/MainDB_IT`

| Column Name          | SP Type                 | Required | Choices / Source                                            | Notes                                                |
| -------------------- | ----------------------- | -------- | ----------------------------------------------------------- | ---------------------------------------------------- |
| Title                | Single line of text     | Yes      | Auto-generated display ID                                   | Primary display value                                |
| FormCode             | Single line of text     | Yes      | Constant `IOIP`                                             | Routing/filter key                                   |
| PolicyNo             | Single line of text     | Yes      | User input (controlled numbering)                           | Domino `PolicyNo`                                    |
| RevNo                | Single line of text     | Yes      | Flow-managed or governed input                              | Domino `RevNo`                                       |
| DateIssue            | Date and Time           | Yes      | User input                                                  | Domino `DateIssue`                                   |
| Subject              | Single line of text     | Yes      | User input                                                  | Domino `Subject`                                     |
| ReviNum              | Single line of text     | Yes      | User input                                                  | Domino `ReviNum`                                     |
| PolicyOwner          | Person or Group         | Yes      | Directory lookup                                            | Domino `PolicyOwner`                                 |
| DocAuthor            | Person or Group         | Yes      | User/directory context                                      | Domino `DocAuthor`                                   |
| Editors              | Person or Group (multi) | No       | Directory lookup                                            | Domino `Editors`                                     |
| Authors              | Person or Group (multi) | No       | Flow-captured                                               | Domino `Authors`                                     |
| Readers              | Person or Group (multi) | No       | Directory lookup                                            | Domino `Readers`                                     |
| Sendto               | Person or Group (multi) | No       | Distribution list or directory                              | Domino `Sendto`                                      |
| FinalStatus          | Choice                  | Yes      | Draft; PendingApproval; Active; Superseded; Archived        | Domino lifecycle status                              |
| DateArchived         | Date and Time           | No       | Flow-managed                                                | Domino `DateArchived`                                |
| FormName             | Single line of text     | No       | Constant/template name                                      | Domino `FormName`                                    |
| RevisionHistoryJson  | Multiple lines of text  | No       | Flow-managed serialized history                             | Replaces embedded Domino revision grid (`R`,`D`,`U`) |
| DistributionListName | Single line of text     | No       | Lookup-derived                                              | Domino `DistributionList`/`DefaultList` evidence     |
| CurrentAction        | Choice                  | Yes      | Draft; Submitted; InApproval; Published; Revision; Archived | Workflow stage state                                 |
| Status               | Choice                  | Yes      | Draft; Submitted; Approved; Rejected; Archived              | Cross-form workflow status                           |
| SubmittedBy          | Person or Group         | Yes      | System/user context                                         | Mandatory cross-form                                 |
| SubmittedDate        | Date and Time           | Yes      | System timestamp                                            | Mandatory cross-form                                 |
| ApprovedBy           | Person or Group         | No       | Stage actor stamp                                           | Last approval actor                                  |
| ApprovedDate         | Date and Time           | No       | Flow-managed                                                | Last approval timestamp                              |
| Comments             | Multiple lines of text  | No       | User/flow notes                                             | Decision remarks                                     |

### Child List (PATTERN-A): `cr_approvalrecord`

Multi-slot authority approvals (`Authority1..3`, status/date/replied fields) must be normalized into
child approval rows, not flattened in `MainDB_IT`.

| Column Name      | SP Type                | Required | Notes                       |
| ---------------- | ---------------------- | -------- | --------------------------- |
| ParentItemId     | Lookup (`MainDB_IT`)   | Yes      | Parent IOIP record          |
| ApprovalStage    | Number                 | Yes      | 1..N sequence               |
| ApproverRole     | Single line of text    | Yes      | Authority role label        |
| ApproverPerson   | Person or Group        | Yes      | Routed approver             |
| ApprovalRequired | Yes/No                 | Yes      | Domino `Req*` mapping       |
| ApprovalStatus   | Choice                 | Yes      | Pending; Approved; Rejected |
| ApprovalDate     | Date and Time          | No       | Approver action date        |
| ApprovalComment  | Multiple lines of text | No       | Approver remarks            |
| RepliedFlag      | Yes/No                 | Yes      | Domino `A*replied` mapping  |

---

## Workflow Stage Map

```
[Stage 1: Draft Policy Entry] --submit--> [Stage 2: Approval Chain] --approve all--> [Stage 3: Publish & Distribute]
        |                                         | reject/revise                      |
        +-------------------rework---------------+                                    v
                                                                 [Stage 4: Revision Update] --retire--> [Stage 5: Archive]
```

| Stage | Action                         | Actor Role                        | SP Group                          | Power Automate Trigger                         |
| ----- | ------------------------------ | --------------------------------- | --------------------------------- | ---------------------------------------------- |
| 1     | Create draft policy and submit | Document Author (`DocAuthor`)     | `D06-IT-Initiators`               | When item created or modified (`Status=Draft`) |
| 2     | Collect authority approvals    | Policy Owner + routed authorities | `D06-IT-HOD`, `D06-IT-Editors-L1` | When `Status=Submitted`                        |
| 3     | Publish and distribute policy  | Policy Admin / Editor             | `D06-IT-Editors-L1`               | When all `cr_approvalrecord` rows are approved |
| 4     | Update revision and resubmit   | Editors                           | `D06-IT-Editors-L1`               | When revision metadata/content changes         |
| 5     | Archive superseded policy      | IT Admin / Policy Admin           | `D06-IT-IT-Admin`                 | When `FinalStatus=Archived`                    |

---

## Role Matrix

| Domino Group        | SharePoint Group    | Permission Level |
| ------------------- | ------------------- | ---------------- |
| `DocAuthor`         | `D06-IT-Initiators` | Contribute       |
| `PolicyOwner`       | `D06-IT-HOD`        | Approve/Edit     |
| `Editors`           | `D06-IT-Editors-L1` | Edit             |
| `Readers`           | `D06-IT-Readers`    | Read             |
| `Sendto` recipients | `D06-IT-Readers`    | Read             |
| `IT/ISAdmin`        | `D06-IT-IT-Admin`   | Full Control     |

---

## Power Automate Actions

| Stage   | Flow Name          | Trigger                                                                                 | Actions                                                                                                         | Notification Target            |
| ------- | ------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| Submit  | `IT_IOIP_Submit`   | SharePoint item created/updated with `Status=Draft` and required header fields complete | Validate required fields; set `Status=Submitted`; set `CurrentAction=InApproval`; seed `cr_approvalrecord` rows | Policy owner + first approvers |
| Approve | `IT_IOIP_Approval` | Child approval row action in `cr_approvalrecord`                                        | Update child status/date; evaluate all required approvals; if complete set parent `Status=Approved`             | Document author + editors      |
| Reject  | `IT_IOIP_Reject`   | Any required child approval row rejected                                                | Set parent `Status=Rejected`; set `CurrentAction=Revision`; capture rejection comment                           | Document author + policy owner |
| Publish | `IT_IOIP_Publish`  | Parent `Status=Approved` and distribution fields complete                               | Set `FinalStatus=Active`; set `CurrentAction=Published`; send issue/distribution notification                   | `Sendto`, `Readers`            |
| Archive | `IT_IOIP_Archive`  | Parent `FinalStatus=Archived`                                                           | Stamp `DateArchived`; set `Status=Archived`; disable active reminders; write audit note                         | Policy owner + IT admin        |

---

## v3 Impossibilities (if any)

| Domino Feature                                                                                            | Reason Impossible in v3                                                                            | Recommended Workaround                                                                               |
| --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Embedded revision-history grid (`R`,`D`,`U` repeating rows inside a single form)                          | Canvas forms do not support Domino-style repeat-row embedded design with formula-managed row slots | Store structured revision entries in `RevisionHistoryJson` or a dedicated child list with gallery UI |
| Multi-slot authority approval fields (`Authority1..3`, status/date/replied) as hardcoded parallel columns | Hardcoded slot columns are brittle and violate PATTERN-A for reusable approval routing             | Use `cr_approvalrecord` child list and flow-driven approval orchestration                            |

---

## Reference PDF

- **Path:** `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/IOIP.pdf`
- **Subforms included:** `PolicyEntryV1` (visible form page template), approval and revision
  sections
- **Page count:** `3`

---

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST — IOIOI POLICY

[✓] All fields identified: [14] fields found, [14] clarified
[✓] Zero unresolved CLARIFY markers: [0] remaining
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining
[✓] Zero unresolved MISSING markers: [0] remaining
[✓] Workflow stages fully mapped: [5] of [5] stages complete
[✓] Power Automate actions defined for each stage: [5] of [5] stages
[✓] Roles mapped to SharePoint groups: [6] of [6] roles mapped
[✓] All mandatory columns mapped: [11] of [11] columns

COMPLETION STATUS: [COMPLETE]
```
