# Technical Blueprint: HR Applications Problem Reporting (HRAPR)

<!-- Architect: HRAPR form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

## Form Identity

| Field                      | Value                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| Form Code                  | `HRAPR`                                                                                                |
| Official Name              | HR Applications Problem Reporting                                                                      |
| Department                 | HR (Department_05)                                                                                     |
| Module                     | M1 — General Administration & Facilities                                                               |
| Site(s)                    | PRAI                                                                                                   |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/HR/HRAPR.pdf`                                |
| Domino Database            | HR.nsf                                                                                                 |
| Official Name Claim Status | Claimed — "HR Applications Problem" (source: `Department_05_HR/HRAPR_analysis.md` extraction evidence) |
| Blueprint Version          | 1.0                                                                                                    |
| Blueprint Date             | 2026-04-14                                                                                             |
| Architect                  | GitHub Copilot (Architect Agent)                                                                       |
| DQ_REQUIRED                | NO                                                                                                     |
| GxP Class                  | Non-GxP                                                                                                |
| Complexity                 | Medium                                                                                                 |

---

## Business Purpose

HR staff and end users use this form to report problems encountered in HR Domino/system
applications. The reporter submits a problem description, identifies the system and module affected,
and sends it to a GHR (Group HR) Personnel contact. The IS Group (ISG) resolves the issue, records
the solution and date. The workflow supports three outcome paths: **Resolve** (ISG provides
solution, reporter accepts), **Reject** (ISG cannot resolve or rejects request), and **KIV/Archive**
(Keep In View — deferred or archived). The Case Number (DisplayCaseNo) is system-generated per the
`Year-Month-CaseNo` format.

---

## SharePoint Schema

### Primary Table: `MainDB_HR`

**URL:** `https://ioioi.sharepoint.com/sites/HR/Lists/MainDB_HR`

**Architecture Method:** DEC-001 (Live Submission Architecture)  
All HRAPR form submissions → `MainDB_HR`. A `FormType` column = `"HRAPR"` distinguishes records
within the shared list.

| #   | Column Name        | SP Type                 | Required | Choices / Source                                                                                      | Notes                                                                                                    |
| --- | ------------------ | ----------------------- | -------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1   | Title              | Single line of text     | Yes      | —                                                                                                     | Auto-populated: `"HRAPR-" & CaseNo`; display name                                                        |
| 2   | CaseNo             | Single line of text     | Yes      | —                                                                                                     | System-computed via Power Automate (format: `HR-APR-YYMM-NNNN`); **PATTERN-E** INO — never set in canvas |
| 3   | FormType           | Single line of text     | Yes      | HRAPR                                                                                                 | Fixed value to distinguish HRAPR records in shared MainDB_HR                                             |
| 4   | SentDate           | Date and Time           | Yes      | —                                                                                                     | Date the report was sent (Domino: DateCreated; PA-set on submit)                                         |
| 5   | SendTo             | Person or Group         | Yes      | —                                                                                                     | GHR Personnel recipient (Domino: SendTo)                                                                 |
| 6   | Company            | Single line of text     | Yes      | —                                                                                                     | Reporter's company/entity (Domino: companyname; e.g., ACM/DCM/AES)                                       |
| 7   | ReportedBy         | Person or Group         | Yes      | —                                                                                                     | Reporter identity (Domino: ReportedBy; auto-populated from logged-in user)                               |
| 8   | Department         | Single line of text     | Yes      | —                                                                                                     | Reporter's department (Domino: Dept)                                                                     |
| 9   | EmployeeNo         | Single line of text     | No       | —                                                                                                     | Reporter's employee number (Domino: EmpNo)                                                               |
| 10  | Section            | Single line of text     | No       | —                                                                                                     | Reporter's section (Domino: Section)                                                                     |
| 11  | ExtensionNo        | Single line of text     | No       | —                                                                                                     | Reporter's phone extension (Domino: ExtNo)                                                               |
| 12  | System             | Choice                  | Yes      | HR Module; Payroll; Leave; Recruitment; Training; Other                                               | System affected (Domino: System)                                                                         |
| 13  | Module1            | Single line of text     | No       | —                                                                                                     | First module specification (Domino: Module)                                                              |
| 14  | Module2            | Single line of text     | No       | —                                                                                                     | Second module specification if multiple (Domino: Module2)                                                |
| 15  | ProblemDescription | Multiple lines of text  | Yes      | —                                                                                                     | Detailed problem description (Domino: ProblemDesc)                                                       |
| 16  | Attachment         | Attachment              | No       | —                                                                                                     | Supporting screenshots or documents (Domino: Attach)                                                     |
| 17  | CC                 | Person or Group (multi) | No       | —                                                                                                     | CC recipients (Domino: CC)                                                                               |
| 18  | ISGEngineer        | Person or Group         | No       | —                                                                                                     | ISG engineer assigned to resolve (Domino: ISGName; set by ISG)                                           |
| 19  | Solution           | Multiple lines of text  | No       | —                                                                                                     | Proposed/applied solution (Domino: Solution; set by ISG in Resolve stage)                                |
| 20  | CaseStatus         | Choice                  | No       | Open; In Progress; Resolved; Rejected; KIV; Closed; Archived                                          | ISG case status (Domino: CaseStatus)                                                                     |
| 21  | DateStarted        | Date and Time           | No       | —                                                                                                     | Date ISG started working on the case (Domino: StartDate)                                                 |
| 22  | DateClosed         | Date and Time           | No       | —                                                                                                     | Date ISG completed resolution (Domino: DateClosed)                                                       |
| 23  | ISGRemarks         | Multiple lines of text  | No       | —                                                                                                     | ISG description and remarks on the resolution (Domino: ISGRemarks)                                       |
| 24  | ISGAttachment      | Attachment              | No       | —                                                                                                     | ISG supporting documents (Domino: Attachment2)                                                           |
| 25  | RejectedByISG      | Person or Group         | No       | —                                                                                                     | ISG person who rejected the case (Domino: ISGName_1; set on Reject path)                                 |
| 26  | RejectStatus       | Choice                  | No       | Rejected                                                                                              | Rejection status (Domino: CaseStatus_1; PA-set on rejection)                                             |
| 27  | DateRejected       | Date and Time           | No       | —                                                                                                     | Rejection date (Domino: DateReject)                                                                      |
| 28  | RejectRemarks      | Multiple lines of text  | No       | —                                                                                                     | ISG rejection explanation (Domino: ISRemarks)                                                            |
| 29  | AcceptanceStatus   | Choice                  | No       | Accepted; Not Accepted                                                                                | Reporter's acceptance of resolution (Domino: Status)                                                     |
| 30  | DateAccepted       | Date and Time           | No       | —                                                                                                     | Date reporter accepted the resolution (Domino: DateAccept)                                               |
| 31  | AcceptanceComment  | Multiple lines of text  | No       | —                                                                                                     | Reporter's acceptance comment (Domino: Comment)                                                          |
| 32  | KIVBy              | Person or Group         | No       | —                                                                                                     | Person who set case to KIV/Archive (Domino: KIVBy)                                                       |
| 33  | KIVStatus          | Choice                  | No       | KIV; Archived                                                                                         | Keep-in-view or archive disposition (Domino: KIVStatus)                                                  |
| 34  | KIVDate            | Date and Time           | No       | —                                                                                                     | Date of KIV/Archive action (Domino: KIVDate)                                                             |
| 35  | ExpireDate         | Date and Time           | No       | —                                                                                                     | Auto-close expiry date (Domino: AutoClosedDate; PA-set 30 days after DateClosed)                         |
| 36  | ReminderDate       | Date and Time           | No       | —                                                                                                     | Reminder trigger date for escalation (Domino: RemDate)                                                   |
| 37  | CurrentStatus      | Choice                  | Yes      | Draft; Submitted; ISGAssigned; Resolved; Rejected; PendingAcceptance; Accepted; KIV; Archived; Closed | Master workflow status (PA-managed)                                                                      |
| 38  | CurrentAction      | Choice                  | Yes      | Create; Submit; Assign; Resolve; Reject; Accept; KIV; Close; Archive                                  | Active workflow action (PA-managed; sourced from Domino CurrentAction)                                   |
| 39  | ISGGroup           | Person or Group         | No       | —                                                                                                     | IS Group admin recipients (Domino: ISG; hidden field)                                                    |
| 40  | GHRPerson          | Person or Group         | No       | —                                                                                                     | GHR contact (Domino: GHR; hidden field)                                                                  |
| 41  | GHR2Person         | Person or Group         | No       | —                                                                                                     | GHR secondary contact (Domino: GHR2; hidden field — HR LMS contact)                                      |
| 42  | HRHODPerson        | Person or Group         | No       | —                                                                                                     | HR HOD (Domino: HRHOD; hidden field for escalation)                                                      |
| 43  | MailingList        | Person or Group (multi) | No       | —                                                                                                     | Full notification mailing list (Domino: MailingList; PA-computed)                                        |
| 44  | LastModifiedBy     | Person or Group         | No       | —                                                                                                     | Last modifier for audit (Domino: LastModifiedBy; PA-tracked)                                             |
| 45  | EnvironmentTag     | Choice                  | No       | DEV; TEST; PROD                                                                                       | Three-tier environment strategy (DEC-004)                                                                |

---

### Staging Table (Historical Import Only): `HR_HRAPR_List`

Historical Domino HRAPR records imported for read-only reference. No live submissions target this
table.

---

## Field Inventory Summary

| Category       | Domino Fields                                                                 | Disposition               |
| -------------- | ----------------------------------------------------------------------------- | ------------------------- |
| Reference      | DateCreated, DisplayCaseNo                                                    | Mapped → columns 4, 2     |
| Reporter       | SendTo, companyname, ReportedBy, Dept, EmpNo, Section, ExtNo, CC              | Mapped → columns 5–11, 17 |
| Problem        | System, Module, Module2, ProblemDesc, Attach                                  | Mapped → columns 12–16    |
| ISG Resolution | ISGName, Solution, CaseStatus, StartDate, DateClosed, ISGRemarks, Attachment2 | Mapped → columns 18–24    |
| Rejection path | ISGName_1, CaseStatus_1, DateReject, ISRemarks                                | Mapped → columns 25–28    |
| Acceptance     | Status, DateAccept, Comment                                                   | Mapped → columns 29–31    |
| KIV/Archive    | KIVBy, KIVStatus, KIVDate                                                     | Mapped → columns 32–34    |
| Automation     | AutoClosedDate, RemDate                                                       | Mapped → columns 35–36    |
| Workflow state | CurrentAction                                                                 | Mapped → columns 37–38    |
| Access/routing | ISG, PIC, GHR, GHR2, HRHOD, AEditor1, AEditor2, AEditor3, MailingList         | Mapped → columns 39–43    |
| Audit          | LastModifiedBy, AuthorsList                                                   | Mapped → column 44        |

---

## Workflow

### Summary

3-path medium-complexity lifecycle: **Submission → ISG Assignment → [Resolve / Reject / KIV] →
Acceptance / Archive → Close**

### Stage Map

| Stage | Name                          | Trigger                  | Actor                 | Actions                                      | Next Stage   | Notifications                |
| ----- | ----------------------------- | ------------------------ | --------------------- | -------------------------------------------- | ------------ | ---------------------------- |
| 1     | Draft / Submission            | Item created             | Reporter (ReportedBy) | Fill problem details, Submit                 | 2            | SendTo (GHR), ISGGroup       |
| 2     | ISG Assignment & Resolution   | Submission received      | ISGEngineer           | Assign self, enter solution OR Reject OR KIV | 3a / 3b / 3c | Reporter, GHR                |
| 3a    | Resolved — Pending Acceptance | ISG marks Resolved       | Reporter              | Accept or Not Accept                         | 4            | Reporter email with solution |
| 3b    | Rejected                      | ISG marks Rejected       | PA (auto)             | Set status Rejected, notify reporter         | End          | Reporter: rejection notice   |
| 3c    | KIV / Archive                 | ISG or GHR sets KIV      | KIVBy                 | Archive or re-open                           | End          | Reporter: KIV notice         |
| 4     | Accepted / Closed             | Reporter accepts         | PA (auto)             | Set status Closed                            | End          | ISG, GHR confirmation        |
| Auto  | Auto-Close                    | 30 days after DateClosed | PA scheduled          | Set status Archived if no acceptance         | End          | Reporter reminder            |

### Power Automate Flows Required

| Flow            | Trigger                               | Actions                                                                                                    |
| --------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| HRAPR_OnSubmit  | Item created, CurrentAction = Submit  | Generate CaseNo (HR-APR-YYMM-NNNN), set SentDate, set CurrentStatus = Submitted, notify SendTo/ISGGroup/CC |
| HRAPR_OnResolve | Item updated, CurrentAction = Resolve | Set DateClosed, set CurrentStatus = Resolved, set ExpireDate = DateClosed + 30 days, notify Reporter       |
| HRAPR_OnReject  | Item updated, CurrentAction = Reject  | Set DateRejected, set CurrentStatus = Rejected, notify Reporter with rejection remarks                     |
| HRAPR_OnAccept  | Item updated, CurrentAction = Accept  | Set DateAccepted, set CurrentStatus = Accepted → Closed, notify ISGGroup                                   |
| HRAPR_OnKIV     | Item updated, CurrentAction = KIV     | Set KIVDate, set CurrentStatus = KIV, notify Reporter                                                      |
| HRAPR_AutoClose | Scheduled daily — check ExpireDate    | If ExpireDate < Today and CurrentStatus = Resolved, set CurrentStatus = Archived                           |
| HRAPR_Reminder  | Scheduled — ReminderDate              | Notify ISGGroup to act on pending cases                                                                    |

---

## Screen Inventory

| Screen Name     | Purpose                                       | Key Controls                                                     | Visible To            |
| --------------- | --------------------------------------------- | ---------------------------------------------------------------- | --------------------- |
| HRAPR_List      | Gallery of all HR application problem records | Gallery, filter by status/system, search by CaseNo               | HR staff, ISG         |
| HRAPR_New       | New problem report                            | Edit form: problem details, system, module, attachments, send-to | Reporters (all staff) |
| HRAPR_View      | Read-only case detail with full timeline      | DisplayForm, ISG resolution section, acceptance section          | All parties           |
| HRAPR_ISGAction | ISG work screen                               | Resolve/Reject/KIV action buttons, solution entry, ISG remarks   | ISG engineers         |
| HRAPR_Accept    | Reporter acceptance confirmation              | Accept/Not Accept buttons, comment field                         | Reporter              |

---

## Navigation Map

```
HRAPR_List  ──[New]──►  HRAPR_New  ──[Submit]──►  HRAPR_View
HRAPR_List  ──[Open]──►  HRAPR_View
HRAPR_View  ──[ISG Action]─►  HRAPR_ISGAction  ──[Resolve/Reject/KIV]──►  HRAPR_View
HRAPR_View  ──[Accept]──►  HRAPR_Accept  ──[Confirm]──►  HRAPR_View
```

---

## Role & Permission Matrix

| Role          | Description                                  | SharePoint Group | PA Access                                     |
| ------------- | -------------------------------------------- | ---------------- | --------------------------------------------- |
| Reporter      | Any HR staff member reporting system problem | D05-HR-Staff     | Create / Edit own (Stage 1, Stage Acceptance) |
| ISG Engineer  | IS Group support engineer working the case   | D02-IT-ISG       | Edit (Stage 2 — Resolution/Reject/KIV)        |
| GHR Personnel | GHR recipient and oversight                  | D05-HR-GHR       | Read / Edit oversight                         |
| HR HOD        | Escalation path                              | D05-HR-HOD       | Approve / Override                            |
| IT Admin      | System administrator                         | D02-IT-Admins    | Full control                                  |

---

## Related Lists / Dependencies

- Shared lookup: `Config_HR_Systems` (System choices: HR Module, Payroll, Leave, Recruitment,
  Training, Other)
- Shared people: `HR_ISGDirectory` for ISG engineer assignment
- No parent-child record structure; all data in MainDB_HR with FormType = HRAPR
- CaseNo INO pattern: `HR-APR-[YY][MM]-[NNNN sequential]`

---

## Migration Notes

- KIVDate field in Domino is named `KIVDate` (not in field list but referenced in extraction
  evidence: "Date :" under "KIV/ARCHIVED by"); map to KIVDate column.
- Multiple editing roles (AEditor1, AEditor2, AEditor3) in Domino map to ISG access control only —
  not separate approval stages.
- Reminder date (RemDate) used for PA scheduled reminder flows; not user-editable in canvas.
- Historical migration: import last 3 years of HRAPR records to `HR_HRAPR_List` staging (3-year HR
  retention policy applies).
- The `Year - Month - CaseNo` INO pattern from Domino maps to `HR-APR-YYMM-NNNN` in M365.
