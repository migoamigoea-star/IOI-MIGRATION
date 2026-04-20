# User Story — SR (`SR`)

> **Department:** Human Resources (D05)  
> **Module:** M2 — Recruitment & Hiring  
> **Site(s):**   
> **SharePoint List:** `MainDB_Human Resources (D05)`  
> **Form Code:** `SR`

---

## 1. App Overview & Purpose

`SR` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `Human Resources (D05)` department at the  site.

---

## 2. User Stories

**US-LIST: Search and filter SR records**
> As an **authorized user**,  
> I want to search, filter, and view SR records in the list screen,  
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

**Target List:** `MainDB_Human Resources (D05)`

| #   | SP Internal Name | Display Label              | Column Type | Required | Classification   | Notes                                                       |
| --- | ---------------- | -------------------------- | ----------- | -------- | ---------------- | ----------------------------------------------------------- |
| 1   | FormType         | Form Type                  | Choice      | Yes      | SYSTEM-COMPUTED  | Fixed: "SR"                                                 |
| 2   | INO              | SR Ref No.                 | Single line | Yes      | SYSTEM-COMPUTED  | HR-SR-YYMM-NNNN via PA                                      |
| 3   | CurrentStatus    | Workflow Status            | Choice      | Yes      | WORKFLOW-MANAGED | Proposing/Authorizing/Finalizing/Commencing/Rejected/Closed |
| 4   | EnvironmentTag   | Environment                | Choice      | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                               |
| 5   | DocNo            | SR Reference No. (Legacy)  | Single line | No       | SYSTEM-COMPUTED  | Legacy DocNo from Domino                                    |
| 6   | DocAuthor        | Created By (Requisitioner) | Person      | Yes      | SYSTEM-COMPUTED  | Auto-filled from login                                      |
| 7   | ReqDept          | Requesting Department      | Single line | Yes      | USER-ENTERED     | Department with vacancy                                     |
| 8   | VacancyTitle     | Vacancy Title              | Single line | Yes      | USER-ENTERED     | Job title required                                          |
| 9   | Grade            | Grade / Band               | Single line | Yes      | USER-ENTERED     | Salary band                                                 |
| 10  | VacancyReason    | Reason for Vacancy         | Choice      | Yes      | USER-ENTERED     | New Headcount/Replacement/Promotion                         |
| 11  | ReplacingName    | Replacing (Name)           | Single line | No       | USER-ENTERED     | Only if Reason=Replacement                                  |
| 12  | LinkedJDRef      | Linked JD Reference        | Lookup      | No       | USER-ENTERED     | Link to approved JD record                                  |
| 13  | AdChannel        | Advertisement Channel      | Choice      | Yes      | USER-ENTERED     | Internal/External/JobsDB/LinkedIn/Multiple                  |
| 14  | InternalAdDate   | Internal Ad Posted Date    | Date        | No       | WORKFLOW-MANAGED | Set by PA on internal posting                               |
| 15  | ExternalAdDate   | External Ad Posted Date    | Date        | No       | WORKFLOW-MANAGED | Set by PA — only after 5-day lockout                        |
| 16  | hodName          | GHR Reviewer (HR Manager)  | Person      | Yes      | WORKFLOW-MANAGED | Final HR verifier                                           |
| 17  | hodStatus        | GHR Status                 | Choice      | Yes      | WORKFLOW-MANAGED | Pending/Acknowledged/Rejected                               |
| 18  | Editor1          | HOD Approver               | Person      | Yes      | WORKFLOW-MANAGED | Stage 2 actor                                               |
| 19  | Editor2          | Reserve Approver           | Person      | No       | WORKFLOW-MANAGED | Backup for Editor1                                          |
| 20  | Editor3          | Division Head              | Person      | No       | WORKFLOW-MANAGED | Stage 3 actor                                               |
| 21  | Editor4          | Executive Director         | Person      | No       | WORKFLOW-MANAGED | Stage 3 ED if needed                                        |
| 22  | Editor5          | CFO (New HC only)          | Person      | No       | WORKFLOW-MANAGED | Only triggered for new headcount                            |
| 23  | DateModified     | Last Revised               | Date        | No       | SYSTEM-COMPUTED  | Auto-updated by SP                                          |
| 24  | NextRemDate      | SLA Nudge Date             | Date        | No       | SYSTEM-COMPUTED  | Computed: Submitted + 5 working days                        |
| 25  | Attachment       | Supporting Documents       | Attachment  | No       | USER-ENTERED     | JD copies, org charts                                       |
| 26  | IsLocked         | Is Locked                  | Yes/No      | No       | WORKFLOW-MANAGED | Lock after Closed                                           |


| #   | SP Internal Name | Display Label          | Column Type        | Required | Notes                          |
| --- | ---------------- | ---------------------- | ------------------ | -------- | ------------------------------ |
| 1   | SRRef            | SR Reference           | Lookup (MainDB_HR) | Yes      | Parent SR record               |
| 2   | BatchNo          | Batch / Cycle No.      | Number             | Yes      | 1–10                           |
| 3   | InterviewDate    | Interview Date         | Date               | No       | USER-ENTERED                   |
| 4   | NoApplicants     | No. of Applicants      | Number             | No       | USER-ENTERED                   |
| 5   | NoShortlisted    | No. Shortlisted        | Number             | No       | USER-ENTERED                   |
| 6   | LinkedINTRef     | Linked INTERVIEWDB Ref | Lookup             | No       | Link to INTERVIEWDB batch      |
| 7   | Outcome          | Outcome                | Choice             | No       | OngoingSearch/Filled/Withdrawn |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `SR_List` | Active recruitment funnel dashboard | Gallery with funnel status chips, vacancy age indicator |
| `SR_New` | New SR entry form | Vacancy fields, JD lookup, reason choice, approver chain auto-fill |
| `SR_View` | Full read-only detail with interview log | Display form + child gallery (interview batches) + approval timeline |
| `SR_Edit` | Edit while in Proposing stage | Edit form |
| `SR_HODReview` | HOD approval screen | Vacancy summary + Approve/Reject |
| `SR_DivReview` | Division Head review | Business impact summary (org chart context) + Approve/Reject |
| `SR_EDReview` | ED strategic clearance | Executive summary with budget context + Approve/Reject |
| `SR_HRCommence` | HR acknowledgement and ad posting | Final checklist + Acknowledge + ad channel confirmation |
| `SR_AuditView` | Interview tracking summary table | Grid of interview batches, applicants/shortlisted counts + INTERVIEWDB links |

### Screen Interaction Details

**SR_List Screen**
- Gallery displaying all `SR` records from `MainDB_Human Resources (D05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `SR_New` (visible to Initiator role only).
- Tap a row to navigate to `SR_View`.

**SR_New / _Edit Screen**
- Data entry form bound to `MainDB_Human Resources (D05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**SR_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "SR-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(SR_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(SR_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "SR",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(SR_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "SR" &&
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
| Role | Screen Access |
| Requisitioner (DocAuthor) | List, New, View, Edit |
| HOD (Editor1) | List, View, HODReview |
| Division Head (Editor3) | List, View, DivReview |
| CFO (Editor5) | List, View, CFO panel |
| ED (Editor4) | List, View, EDReview |
| HR Manager (hodName) | List, View, HRCommence, AuditView |
| HR Admin | All |
| Reader | List, View |

### 3. Data Integrity Rules

- `FormCode` must always equal `SR` (system-enforced constant).
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

*(Power Automate flows to be defined per workflow stage — see Workflow Stage Map)*

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

- [ ] All SharePoint columns in `MainDB_Human Resources (D05)` are created with correct types and required flags.
- [ ] Canvas App screens (`SR_List`, `SR_New`, `SR_View`, `SR_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
