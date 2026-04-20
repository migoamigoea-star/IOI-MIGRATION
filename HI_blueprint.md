# Technical Blueprint - HI

## Form Identity

| Field                      | Value                                                                |
| -------------------------- | -------------------------------------------------------------------- |
| Form Code                  | `HI`                                                                 |
| Official Name              | `Hardware Inventory`                                                 |
| Department                 | `IT`                                                                 |
| Module                     | `M3 - Hardware & Infrastructure`                                     |
| Site(s)                    | `PRAI`                                                               |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/HI.pdf` |
| Domino Database            | `IT.nsf` (department database)                                       |
| Official Name Claim Status | `Claimed`                                                            |
| Blueprint Version          | `1.0`                                                                |
| Blueprint Date             | `2026-04-13`                                                         |
| Architect                  | `Architect Agent`                                                    |

---

## DEC-001 / DEC-004 / DEC-005 Control Notes

- DEC-001 (live submissions): all new HI submissions write to `MainDB_IT` only. Any form-specific
  list (for example `IT_HI_List`) is import/staging for historical Domino records only.
- DEC-004 (environment strategy): environment-variant values (recipient groups, reminder intervals,
  archive thresholds, and sender identity) are loaded from `Config_AppSettings` for `DEV`, `TEST`,
  and `PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is authoritative for
  column definitions. A discoverable local copy is not currently present in this workspace, so this
  blueprint is aligned to DEC-005 governance and must be reconciled against the canonical enhanced
  schema before production promotion.

---

## SharePoint Schema

**Target List:** `MainDB_IT`  
**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal-it/Lists/MainDB_IT`

| Column Name         | SP Type                | Required | Choices / Source                              | Notes                               |
| ------------------- | ---------------------- | -------- | --------------------------------------------- | ----------------------------------- |
| Title               | Single line of text    | Yes      | Auto-generated                                | Display identifier for HI record    |
| FormCode            | Single line of text    | Yes      | Constant `HI`                                 | Routing/filter key                  |
| machineid           | Single line of text    | Yes      | System/flow generated or governed format      | Domino `machineid`                  |
| TagNo               | Single line of text    | Yes      | User input                                    | Domino `TagNo`                      |
| status              | Choice                 | Yes      | Active; InUse; Returned; Disposed; Archived   | Domino `status` lifecycle           |
| type                | Choice                 | Yes      | Hardware type catalog                         | Domino `type`                       |
| DeskType            | Choice                 | No       | Access type catalog                           | Domino `DeskType`                   |
| compname            | Single line of text    | Yes      | User input                                    | Domino `compname`                   |
| compmodel           | Single line of text    | No       | User input                                    | Domino `compmodel`                  |
| srvrmodel           | Single line of text    | No       | User input                                    | Domino `srvrmodel`                  |
| comp                | Choice                 | Yes      | Company master list                           | Domino `comp`                       |
| usedby              | Person or Group        | Yes      | Directory lookup                              | Domino `usedby`                     |
| prevusedby          | Person or Group        | No       | Directory lookup                              | Domino `prevusedby`                 |
| loc                 | Choice                 | Yes      | Location master list                          | Domino `loc`                        |
| dept                | Choice                 | Yes      | Department master list                        | Domino `dept`                       |
| Notes               | Multiple lines of text | No       | User input                                    | Domino `Notes`                      |
| cpusno              | Single line of text    | No       | User input                                    | Domino `cpusno`                     |
| ramsize             | Single line of text    | No       | User input                                    | Domino `ramsize`                    |
| ram                 | Single line of text    | No       | User input                                    | Domino `ram`                        |
| ramtype             | Choice                 | No       | RAM type catalog                              | Domino `ramtype`                    |
| hddsize             | Single line of text    | No       | User input                                    | Domino `hddsize`                    |
| hddtype             | Choice                 | No       | Disk type catalog                             | Domino `hddtype`                    |
| inch                | Single line of text    | No       | User input                                    | Domino `inch` (monitor)             |
| winversion          | Choice                 | No       | OS version catalog                            | Domino `winversion`                 |
| winsvrversion       | Choice                 | No       | Server OS version catalog                     | Domino `winsvrversion`              |
| msversion           | Choice                 | No       | Office version catalog                        | Domino `msversion`                  |
| MSEmail             | Single line of text    | No       | User input                                    | Domino `MSEmail`                    |
| MSEmailPswd         | Single line of text    | No       | Restricted; masked in app UI                  | Domino `MSEmailPswd` (sensitive)    |
| MSOfficeKey         | Single line of text    | No       | Restricted; masked in app UI                  | Domino `MSOfficeKey` (sensitive)    |
| notesver            | Choice                 | No       | Notes version catalog                         | Domino `notesver`                   |
| PoNumber            | Single line of text    | No       | User input                                    | Domino `PoNumber`                   |
| AssetNo             | Single line of text    | Yes      | User input with uniqueness check              | Domino `AssetNo`                    |
| Vendor              | Lookup                 | No       | Vendor master list                            | Domino `Vendor`                     |
| Authors             | Person or Group        | Yes      | System/user context                           | Domino `Authors`                    |
| MachineCreationDate | Date and Time          | Yes      | System timestamp                              | Domino `MachineCreationDate`        |
| MachineAuthor       | Person or Group        | No       | Workflow managed                              | Domino `MachineAuthor`              |
| DateModified        | Date and Time          | No       | Workflow managed                              | Domino `DateModified`               |
| LastAuditedBy       | Person or Group        | No       | Workflow managed                              | Domino `LastAuditedBy`              |
| LastAuditedOn       | Date and Time          | No       | Workflow managed                              | Domino `LastAuditedOn`              |
| IT                  | Person or Group        | No       | IT owner directory                            | Domino `IT`                         |
| Year                | Number                 | No       | Flow generated                                | Domino `Year`                       |
| Month               | Number                 | No       | Flow generated                                | Domino `Month`                      |
| INO                 | Number                 | No       | Flow generated                                | Domino `INO`                        |
| Status              | Choice                 | Yes      | Draft; Registered; Updated; Audited; Archived | Cross-form workflow status          |
| SubmittedBy         | Person or Group        | Yes      | System/user context                           | Live submission owner               |
| SubmittedDate       | Date and Time          | Yes      | System timestamp                              | Live submission timestamp           |
| ApprovedBy          | Person or Group        | No       | Reserved for governance extension             | Not used in current HI flow         |
| ApprovedDate        | Date and Time          | No       | Reserved for governance extension             | Not used in current HI flow         |
| Comments            | Multiple lines of text | No       | User/flow notes                               | Reserved comments/audit note column |

Attachment handling: use native SharePoint list attachments on `MainDB_IT` to store HI evidence
files corresponding to Domino field `a`.

---

## Workflow Stage Map

```
[Stage 1: Asset Registration] --submit--> [Stage 2: Operational Update]
    |                                             |
    |                                   periodic audit --> [Stage 3: Audit and History]
```

| Stage | Action                                          | Actor Role                             | SP Group            | Power Automate Trigger                                            |
| ----- | ----------------------------------------------- | -------------------------------------- | ------------------- | ----------------------------------------------------------------- |
| 1     | Register new hardware inventory record          | Initiator / IT owner (`Authors`, `IT`) | `D06-IT-Initiators` | When item created in `MainDB_IT` where `FormCode = HI`            |
| 2     | Update ownership/configuration/status fields    | IT editor (`MachineAuthor`)            | `D06-IT-Editors-L1` | When HI item modified and record is not archived                  |
| 3     | Perform periodic audit and stamp audit metadata | IT auditor (`LastAuditedBy`)           | `D06-IT-Editors-L3` | Scheduled recurrence for due assets or manual audit action update |

Workflow routing is IT-owned operational governance; no separate HOD approval is evidenced in the
source form.

---

## Role Matrix

| Domino Group                         | SharePoint Group    | Permission Level |
| ------------------------------------ | ------------------- | ---------------- |
| `Authors` (creator)                  | `D06-IT-Initiators` | Contribute       |
| `MachineAuthor` (operational editor) | `D06-IT-Editors-L1` | Contribute       |
| `LastAuditedBy` (auditor)            | `D06-IT-Editors-L3` | Contribute       |
| `IT` (IT owner/admin)                | `D06-IT-IT-Admin`   | Full Control     |
| Read-only stakeholders               | `D06-IT-Readers`    | Read             |

---

## Power Automate Actions

| Stage    | Flow Name        | Trigger                                              | Actions                                                                                                                               | Notification Target                        |
| -------- | ---------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Register | `IT_HI_Register` | SharePoint - item created (`FormCode = HI`)          | Set `SubmittedBy`, `SubmittedDate`, initialize `Status`, validate mandatory identity fields, generate/validate `Year`, `Month`, `INO` | IT owner group and initiator               |
| Update   | `IT_HI_Update`   | SharePoint - item modified                           | Stamp `MachineAuthor` and `DateModified`, validate operational edits, maintain lifecycle `status`                                     | IT owner and relevant `usedby` stakeholder |
| Audit    | `IT_HI_Audit`    | Scheduled recurrence + optional manual audit trigger | Identify due assets, stamp `LastAuditedBy`/`LastAuditedOn`, set `Status = Audited` or keep current state, log audit notes             | IT governance/auditor group                |

Environment-configurable values must be loaded from `Config_AppSettings` keys (for example
`HI.AuditIntervalDays`, `HI.UpdateNotificationGroup`, and `HI.SenderProfile`) per DEC-004.

---

## v3 Impossibilities (if any)

| Domino Feature                                                           | Reason Impossible in v3                                                                     | Recommended Workaround                                                                                                                                                           |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Domino-style inline secret retention for `MSEmailPswd` and `MSOfficeKey` | Storing credentials in plain text fields is not acceptable in modern M365 security controls | Mask fields in Canvas UI, restrict field-level visibility to IT admin roles, and store sensitive values in secure store where possible; retain only compliant references in list |

---

## Reference PDF

- Path: `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/HI.pdf`
- Source analysis in department folder: `docs/migration-analysis/Department_06_IT/HI_analysis.md`
- Subforms included: None identified from extracted evidence
- Page count: 3 (form layout and history block)

---

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - Hardware Inventory (HI)

[✓] All fields identified: [42] fields found, [42] clarified
[✓] Zero unresolved CLARIFY markers: [0] remaining
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining
[✓] Zero unresolved MISSING markers: [0] remaining
[✓] Workflow stages fully mapped: [3] of [3] stages complete
[✓] Power Automate actions defined for each stage: [3] of [3] stages
[✓] Roles mapped to SharePoint groups: [5] of [5] roles mapped
[✓] All mandatory columns mapped: [16] of [16] columns

COMPLETION STATUS: COMPLETE
```

Additional unresolved-marker audit:

- Zero unresolved NEEDS REVIEW markers: [0] remaining
