# Technical Blueprint — EAF

## Form Identity

| Field                      | Value                                                                       |
| -------------------------- | --------------------------------------------------------------------------- |
| Form Code                  | `EAF`                                                                       |
| Official Name              | `External Access Form (VPN & Citrix)`                                       |
| Department                 | `IT`                                                                        |
| Module                     | `M1 - User & Access Management`                                             |
| Site(s)                    | `PRAI`                                                                      |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/EAF.pdf`       |
| Domino Database            | `IT.nsf` (department database)                                              |
| Official Name Claim Status | `Claimed` (exact inventory name aligned in `official_name_claim_status.md`) |
| Blueprint Version          | `1.0`                                                                       |
| Blueprint Date             | `2026-04-13`                                                                |
| Architect                  | `Architect Agent`                                                           |

---

## DEC-001 / DEC-004 / DEC-005 Control Notes

- DEC-001 (live submissions): all new EAF submissions write to `MainDB_IT` only. Any form-specific
  list (for example `IT_EAF_List`) is import/staging for historical Domino records only.
- DEC-004 (environment strategy): approver routing aliases, reminder cadence, sender identity, and
  escalation recipients are environment-driven through `Config_AppSettings` for `DEV`, `TEST`, and
  `PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is authoritative for
  column definitions. This workspace does not currently include a discoverable local copy, so this
  blueprint is aligned to DEC-005 governance and must be reconciled against the canonical enhanced
  schema before production promotion.

---

## SharePoint Schema

**Target List:** `MainDB_IT`  
**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal-it/Lists/MainDB_IT`

| Column Name           | SP Type                 | Required | Choices / Source                                        | Notes                          |
| --------------------- | ----------------------- | -------- | ------------------------------------------------------- | ------------------------------ |
| Title                 | Single line of text     | Yes      | Auto-generated (`EAF-YYYYMM-####`)                      | Display identifier             |
| FormCode              | Single line of text     | Yes      | Constant `EAF`                                          | Routing and filtering key      |
| Company               | Choice                  | Yes      | Company master list                                     | Domino `Company`               |
| Requestor             | Person or Group         | Yes      | User picker                                             | Domino `req`                   |
| SubmittedOn           | Date and Time           | Yes      | System timestamp                                        | Domino `date1`                 |
| TargetUser            | Person or Group         | Yes      | User picker                                             | Domino `User`                  |
| Application           | Choice                  | Yes      | Citrix; VPN; Other                                      | Domino `App`                   |
| SystemName            | Choice                  | Yes      | System lookup list                                      | Domino `system`                |
| Justification         | Multiple lines of text  | Yes      | User input                                              | Domino `justification`         |
| DepartmentHead        | Person or Group         | Yes      | Approver matrix                                         | Domino `depthead`              |
| CCRecipients          | Person or Group (multi) | No       | User/flow populated                                     | Domino `CC`                    |
| DeptHeadStatus        | Choice                  | No       | Pending; Approved; Rejected                             | Domino `status1`               |
| DeptHeadApprovedBy    | Person or Group         | No       | Workflow managed                                        | Domino `HODNAME`               |
| DeptHeadApprovedDate  | Date and Time           | No       | Workflow managed                                        | Domino `date2`                 |
| DeptHeadComment       | Multiple lines of text  | No       | Approver input                                          | Domino `comment1`              |
| DDAppStatus           | Choice                  | No       | Pending; Approved; Rejected                             | Domino `status2`               |
| DDAppApprovedBy       | Person or Group         | No       | Workflow managed                                        | Domino `DIVNAME`               |
| DDAppApprovedDate     | Date and Time           | No       | Workflow managed                                        | Domino `date3`                 |
| DDAppComment          | Multiple lines of text  | No       | Approver input                                          | Domino `comment2`              |
| ITManagerStatus       | Choice                  | No       | Pending; Approved; Rejected                             | Domino `status3`               |
| ITManagerApprovedBy   | Person or Group         | No       | Workflow managed                                        | Domino `name4`                 |
| ITManagerApprovedDate | Date and Time           | No       | Workflow managed                                        | Domino `date4`                 |
| ITManagerComment      | Multiple lines of text  | No       | Approver input                                          | Domino `comment3`              |
| ITCompletionStatus    | Choice                  | No       | Pending; Completed; Rework                              | Domino `status4`               |
| ITCompletedBy         | Person or Group         | No       | Workflow managed                                        | Domino `name5`                 |
| ITCompletedDate       | Date and Time           | No       | Workflow managed                                        | Domino `date5`                 |
| ITCompletionRemarks   | Multiple lines of text  | No       | IT input                                                | Domino `comment4`              |
| ITInternalRemarks     | Multiple lines of text  | No       | IT input                                                | Domino `remarks`               |
| FinalStatus           | Choice                  | No       | Open; Approved; Rejected; Closed                        | Domino `Status`                |
| CurrentAction         | Choice                  | Yes      | Requestor; HOD; DDApp; ITManager; ITComplete; Closed    | Domino `CurrentAction`         |
| RouteACMIT            | Person or Group         | No       | Workflow managed                                        | Domino `ACMIT`                 |
| RoutePCNIT            | Person or Group         | No       | Workflow managed                                        | Domino `PCNIT`                 |
| RoutePCNIT2           | Person or Group         | No       | Workflow managed                                        | Domino `PCNIT2`                |
| IsPCN                 | Yes/No                  | No       | Computed from company                                   | Domino `isPCN`                 |
| ITPIC                 | Person or Group         | No       | Workflow managed                                        | Domino `ITPIC`                 |
| ITPIC2                | Person or Group         | No       | Workflow managed                                        | Domino `ITPIC2`                |
| ExecutiveDirector     | Person or Group         | No       | Workflow managed                                        | Domino `ED`                    |
| HeadOfOperation       | Person or Group         | No       | Workflow managed                                        | Domino `HOO`                   |
| HigherApprover        | Person or Group         | No       | Workflow managed                                        | Domino `HApp`                  |
| RecipientRouting      | Person or Group (multi) | No       | Workflow managed                                        | Domino `SendTo`                |
| ISManager             | Person or Group         | No       | Workflow managed                                        | Domino `IsMgr`                 |
| ITAdmin               | Person or Group         | No       | Workflow managed                                        | Domino `ITADMIN`               |
| ReminderTo            | Person or Group (multi) | No       | Flow managed                                            | Domino `RemTo`                 |
| ReminderSubject       | Single line of text     | No       | Flow generated                                          | Domino `RemSubject`            |
| Status                | Choice                  | Yes      | Draft; Submitted; InReview; Completed; Rejected; Closed | Cross-form workflow state      |
| SubmittedBy           | Person or Group         | Yes      | System                                                  | Mandatory governance column    |
| SubmittedDate         | Date and Time           | Yes      | System                                                  | Mandatory governance column    |
| ApprovedBy            | Person or Group         | No       | Workflow managed                                        | Final approval actor           |
| ApprovedDate          | Date and Time           | No       | Workflow managed                                        | Final approval timestamp       |
| Comments              | Multiple lines of text  | No       | User/flow notes                                         | Consolidated remarks trail     |
| WorkflowAuditJson     | Multiple lines of text  | No       | Flow-generated JSON                                     | Optional troubleshooting trail |

Attachment handling: use native SharePoint list attachments on `MainDB_IT`; do not create a separate
attachment-hyperlink column for live submissions.

---

## Workflow Stage Map

```
[Stage 1: Requestor Submission] --> [Stage 2: Department Head Review] --> [Stage 3: DDApp Review] --> [Stage 4: IT Manager Review] --> [Stage 5: IT Completion]
           ^                                                                                                                         |
           |--------------------------------------------------------- reject/rework -------------------------------------------------|
```

| Stage | Action                                     | Actor Role              | SP Group                         | Power Automate Trigger                                             |
| ----- | ------------------------------------------ | ----------------------- | -------------------------------- | ------------------------------------------------------------------ |
| 1     | Create and submit external access request  | Requestor               | `D06-IT-Initiators`              | When item created in `MainDB_IT` where `FormCode = EAF`            |
| 2     | Approve/reject request at department level | Department Head         | `D06-IT-HOD`                     | When `CurrentAction = HOD`                                         |
| 3     | Approve/reject higher-level business gate  | DDApp / Higher Approver | `D06-IT-Editors-L3`              | When `DeptHeadStatus = Approved` and `CurrentAction = DDApp`       |
| 4     | Approve/reject technical manager gate      | IT Manager              | `D06-IT-IT-Admin`                | When `DDAppStatus = Approved` and `CurrentAction = ITManager`      |
| 5     | Execute provisioning and close request     | IT PIC / IT Admin       | `D06-IT-PIC` + `D06-IT-IT-Admin` | When `ITManagerStatus = Approved` and `CurrentAction = ITComplete` |

---

## Role Matrix

| Domino Group                               | SharePoint Group                  | Permission Level                                  |
| ------------------------------------------ | --------------------------------- | ------------------------------------------------- |
| `req` / `Requestor` / `AEditor1`           | `D06-IT-Initiators`               | Contribute (create/edit own before final closure) |
| `depthead` / `HODNAME`                     | `D06-IT-HOD`                      | Approve/Reject                                    |
| `DIVNAME` / `HApp`                         | `D06-IT-Editors-L3`               | Approve/Reject                                    |
| `IsMgr` / `name4`                          | `D06-IT-IT-Admin`                 | Approve/Reject + workflow admin                   |
| `ITPIC` / `ITPIC2` / `name5`               | `D06-IT-PIC`                      | Contribute (execution and completion update)      |
| `ITADMIN`                                  | `D06-IT-IT-Admin`                 | Full Control                                      |
| `SendTo` / `CC` / informational recipients | `D06-IT-Readers`                  | Read                                              |
| `ACMIT` / `PCNIT` / `PCNIT2`               | `D06-IT-ACM-IT` / `D06-IT-PCN-IT` | Approve (company-specific route)                  |

---

## Power Automate Actions

| Stage         | Flow Name                  | Trigger                                        | Actions                                                                                                                                     | Notification Target               |
| ------------- | -------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| Submit        | `IT_EAF_Submit`            | SP item created (`FormCode = EAF`)             | Validate required fields; stamp `SubmittedBy/SubmittedDate`; set `Status=Submitted`; set `CurrentAction=HOD`; compute route flags (`IsPCN`) | Department Head + CC              |
| HOD           | `IT_EAF_HODDecision`       | Item modified where `CurrentAction=HOD`        | Branch approve/reject; update `DeptHeadStatus`, `DeptHeadApprovedBy`, `DeptHeadApprovedDate`; on approve move to DDApp                      | Requestor + DDApp/Higher approver |
| DDApp         | `IT_EAF_DDAppDecision`     | Item modified where `CurrentAction=DDApp`      | Branch approve/reject; update `DDAppStatus`, `DDAppApprovedBy`, `DDAppApprovedDate`; on approve move to IT Manager                          | Requestor + IT Manager            |
| IT Manager    | `IT_EAF_ITManagerDecision` | Item modified where `CurrentAction=ITManager`  | Branch approve/reject; update `ITManagerStatus`, `ITManagerApprovedBy`, `ITManagerApprovedDate`; on approve move to IT completion           | IT PIC/IT Admin + requestor       |
| IT Completion | `IT_EAF_Complete`          | Item modified where `CurrentAction=ITComplete` | Update `ITCompletionStatus`, `ITCompletedBy`, `ITCompletedDate`, `FinalStatus`, `Status=Closed`; append audit JSON                          | Requestor + recipients            |

Reminder/escalation behavior: use a recurrence branch inside each flow family (or dedicated
`IT_EAF_Reminder`) to notify `ReminderTo` based on configurable SLA keys in `Config_AppSettings`.

---

## v3 Impossibilities (if any)

| Domino Feature                                                              | Reason Impossible in v3                                                      | Recommended Workaround                                                        |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Domino hidden-field formula transitions (`CurrentAction`, route identities) | Domino formula lifecycle does not execute natively in SharePoint list forms  | Move all state transitions to explicit Power Automate updates                 |
| Embedded Domino rich attachment behavior                                    | Domino-style rich text attachment embedding is not preserved in Canvas forms | Use SharePoint native list attachments and store metadata in standard columns |

---

## Reference PDF

- **Path:** `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/EAF.pdf`
- **Subforms included:** No separate external subform PDF identified in source package; workflow
  sections are embedded in main form
- **Page count:** 3 (based on extracted evidence in `EAF_analysis.md`)

---

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - External Access Form (VPN & Citrix)

[✓] All fields identified: [46] fields found, [46] clarified
[✓] Zero unresolved CLARIFY markers: [0] remaining
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining
[✓] Zero unresolved MISSING markers: [0] remaining
[✓] Workflow stages fully mapped: [5] of [5] stages complete
[✓] Power Automate actions defined for each stage: [5] of [5] stages
[✓] Roles mapped to SharePoint groups: [8] of [8] roles mapped
[✓] All mandatory columns mapped: [51] of [51] columns

COMPLETION STATUS: COMPLETE
```

Additional unresolved-marker audit:

- Zero unresolved NEEDS REVIEW markers: [0] remaining
