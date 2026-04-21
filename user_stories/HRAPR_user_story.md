# User Story — HR Applications Problem Reporting (`HRAPR`)

> **Department:** HR (Department_05)  
> **Module:** M1 — General Administration & Facilities  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_HR (Department_05)`  
> **Form Code:** `HRAPR`

---

## 1. App Overview & Purpose

`HRAPR` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `HR (Department_05)` department at the PRAI site.

---

## 2. User Stories

**US-LIST: Search and filter HR Applications Problem Reporting records**
> As an **authorized user**,  
> I want to search, filter, and view HR Applications Problem Reporting records in the list screen,  
> So that I can quickly find the record I need to act on.

**US-NOTIFY: Receive workflow notifications**
> As a **workflow participant**,  
> I want to receive email notifications when the form status changes or requires my action,  
> So that I am always aware of pending tasks without checking the app manually.

**US-AUDIT: View audit trail and history**
> As an **Admin / Manager**,  
> I want to view a full audit trail of every status change and approver action,  
> So that I can meet compliance and traceability requirements.

---

## 3. SharePoint List Requirements

**Target List:** `MainDB_HR (Department_05)`

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

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| HRAPR_List | Gallery of all HR application problem records | Gallery, filter by status/system, search by CaseNo |
| HRAPR_New | New problem report | Edit form: problem details, system, module, attachments, send-to |
| HRAPR_View | Read-only case detail with full timeline | DisplayForm, ISG resolution section, acceptance section |
| HRAPR_ISGAction | ISG work screen | Resolve/Reject/KIV action buttons, solution entry, ISG remarks |
| HRAPR_Accept | Reporter acceptance confirmation | Accept/Not Accept buttons, comment field |

### Screen Interaction Details

**HRAPR_List Screen**
- Gallery displaying all `HRAPR` records from `MainDB_HR (Department_05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `HRAPR_New` (visible to Initiator role only).
- Tap a row to navigate to `HRAPR_View`.

**HRAPR_New / _Edit Screen**
- Data entry form bound to `MainDB_HR (Department_05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**HRAPR_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "HRAPR-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 3. Field Lock Based on Status

```powerfx
// Lock all editable fields once record is Approved or Closed
DisplayMode: If(
    ThisItem.Status in ["Approved", "Closed", "Archived"],
    DisplayMode.View,
    DisplayMode.Edit
)
```

### 4. Screen Navigation

```powerfx
// Navigate from List to New form
Navigate(HRAPR_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(HRAPR_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "HRAPR",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(HRAPR_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "HRAPR" &&
    (IsBlank(txtSearch.Text) ||
     StartsWith(Title, txtSearch.Text) ||
     StartsWith(Status, txtSearch.Text))
)
```


---

## 6. Business Logic Requirements

The following business rules and logic must be enforced:

### 1. Status Transition Rules

Status must only progress through the defined workflow stages in sequence:

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|

### 3. Data Integrity Rules

- `FormCode` must always equal `HRAPR` (system-enforced constant).
- `SubmittedBy` and `SubmittedDate` are system-stamped on first submission and must not be editable.
- `ApprovedBy` and `ApprovedDate` are set by the flow only when all required approvals are collected.
- Records in `Approved`, `Closed`, or `Archived` state must be fully read-only.
- `EnvironmentTag` must be set from `Config_AppSettings` and must match the deployment environment (DEV / TEST / PROD).

### 4. Notification Logic

- Notifications are sent via Power Automate (email / Teams adaptive card).
- Notification recipients are determined by the role matrix and workflow stage.
- All notifications must include: Record Title, Current Status, Action Required (if any), and deep-link URL to the record.

### 5. Audit & Traceability

- Every status change must be logged in the SharePoint item version history.
- Multi-stage approvals must write individual approval records to `cr_approvalrecord` child list (if applicable).
- Rejection comments must be captured and returned to the initiator.


---

## 7. Power Automate Requirements

| Flow            | Trigger                               | Actions                                                                                                    |
| --------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| HRAPR_OnSubmit  | Item created, CurrentAction = Submit  | Generate CaseNo (HR-APR-YYMM-NNNN), set SentDate, set CurrentStatus = Submitted, notify SendTo/ISGGroup/CC |
| HRAPR_OnResolve | Item updated, CurrentAction = Resolve | Set DateClosed, set CurrentStatus = Resolved, set ExpireDate = DateClosed + 30 days, notify Reporter       |
| HRAPR_OnReject  | Item updated, CurrentAction = Reject  | Set DateRejected, set CurrentStatus = Rejected, notify Reporter with rejection remarks                     |
| HRAPR_OnAccept  | Item updated, CurrentAction = Accept  | Set DateAccepted, set CurrentStatus = Accepted → Closed, notify ISGGroup                                   |
| HRAPR_OnKIV     | Item updated, CurrentAction = KIV     | Set KIVDate, set CurrentStatus = KIV, notify Reporter                                                      |
| HRAPR_AutoClose | Scheduled daily — check ExpireDate    | If ExpireDate < Today and CurrentStatus = Resolved, set CurrentStatus = Archived                           |
| HRAPR_Reminder  | Scheduled — ReminderDate              | Notify ISGGroup to act on pending cases                                                                    |

### Flow Design Principles

All Power Automate flows for this application must adhere to the following:

1. **Environment isolation:** Flows must read environment-specific settings (email recipients, approver groups, retry limits) from `Config_AppSettings` using the `EnvironmentTag` field. Never hard-code DEV/TEST/PROD-specific values.
2. **Idempotency:** Flows must handle duplicate triggers gracefully (do-until loops with condition checks).
3. **Error handling:** All HTTP actions and SharePoint calls must be wrapped in try/catch scope with failure notifications to the admin group.
4. **Status locking:** Only flows may update the `Status` and `CurrentAction` fields. Canvas App patches to these fields are blocked via SharePoint column validation or item-level permissions.
5. **Audit stamping:** Every flow must write a version comment to the SharePoint item history when changing status.
6. **Notification standard:** All emails / Teams cards must include: Record Title, Form Code, Current Status, Action Required, and a deep-link to the record in the Canvas App.

---

## 8. Acceptance Criteria

The following acceptance criteria must be met before this form can be promoted to PROD:

- [ ] All SharePoint columns in `MainDB_HR (Department_05)` are created with correct types and required flags.
- [ ] Canvas App screens (`HRAPR_List`, `HRAPR_New`, `HRAPR_View`, `HRAPR_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
