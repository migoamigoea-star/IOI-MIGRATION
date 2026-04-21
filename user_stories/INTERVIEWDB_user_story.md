# User Story — INTERVIEWDB (`INTERVIEWDB`)

> **Department:** Human Resources (D05)  
> **Module:** M2 — Recruitment & Hiring  
> **Site(s):**   
> **SharePoint List:** `MainDB_Human Resources (D05)`  
> **Form Code:** `INTERVIEWDB`

---

## 1. App Overview & Purpose

`INTERVIEWDB` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `Human Resources (D05)` department at the  site.

---

## 2. User Stories

**US-LIST: Search and filter INTERVIEWDB records**
> As an **authorized user**,  
> I want to search, filter, and view INTERVIEWDB records in the list screen,  
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

| #   | SP Internal Name | Display Label             | Column Type    | Required | Classification   | Notes                                                |
| --- | ---------------- | ------------------------- | -------------- | -------- | ---------------- | ---------------------------------------------------- |
| 1   | FormType         | Form Type                 | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "INTERVIEWDB"                                 |
| 2   | INO              | Batch Reference           | Single line    | Yes      | SYSTEM-COMPUTED  | HR-INT-YYMM-NNNN via PA                              |
| 3   | CurrentStatus    | Current Status            | Choice         | Yes      | WORKFLOW-MANAGED | Sourcing/Interviewing/Verifying/Communicating/Closed |
| 4   | EnvironmentTag   | Environment               | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                        |
| 5   | VacancyTitle     | Vacancy Title             | Single line    | Yes      | USER-ENTERED     | Job position being filled                            |
| 6   | LinkedSRRef      | Linked SR Reference       | Lookup         | No       | USER-ENTERED     | Link to approving SR record                          |
| 7   | LinkedJDRef      | Linked JD Reference       | Lookup         | No       | USER-ENTERED     | Pull required competencies from JD                   |
| 8   | InDate           | Interview Date            | Date           | Yes      | USER-ENTERED     | Date of interview                                    |
| 9   | InName           | Interviewer / Evaluator   | Person         | Yes      | USER-ENTERED     | Lead interviewer                                     |
| 10  | VrName           | Verifier                  | Person         | No       | WORKFLOW-MANAGED | HR Manager verifying results                         |
| 11  | HRE              | HR PIC (Executive)        | Person         | Yes      | WORKFLOW-MANAGED | HR Exec lead for communication                       |
| 12  | HRN              | HR PIC (Non-Executive)    | Person         | No       | WORKFLOW-MANAGED | HR support staff                                     |
| 13  | InRemarks        | Interview Remarks         | Multiple lines | No       | USER-ENTERED     | General batch-level notes                            |
| 14  | VrRemarks        | Verification Notes        | Multiple lines | No       | USER-ENTERED     | Auditor observations                                 |
| 15  | DocAuthor        | Created By                | Person         | Yes      | SYSTEM-COMPUTED  | HR Recruiter                                         |
| 16  | CA               | Current Action            | Choice         | No       | WORKFLOW-MANAGED | Stage control                                        |
| 17  | TotalCandidates  | Total Candidates in Batch | Number         | No       | SYSTEM-COMPUTED  | Count of child rows                                  |
| 18  | EmailDate        | HR Notification Date      | Date           | No       | SYSTEM-COMPUTED  | When communications sent                             |
| 19  | Attachment       | CV Batch (PDF)            | Attachment     | No       | USER-ENTERED     | Consolidated candidate CV file                       |
| 20  | IsLocked         | Is Locked                 | Yes/No         | No       | WORKFLOW-MANAGED | Lock after Closed                                    |


| #   | SP Internal Name | Display Label              | Column Type        | Required | Notes                               |
| --- | ---------------- | -------------------------- | ------------------ | -------- | ----------------------------------- |
| 1   | BatchINO         | Batch Reference            | Lookup (MainDB_HR) | Yes      | Parent record link                  |
| 2   | SlotNo           | Candidate Slot #           | Number             | Yes      | 1–30                                |
| 3   | CandidateName    | Candidate Name             | Single line        | Yes      | USER-ENTERED                        |
| 4   | EvalScore        | Evaluation Score (A-score) | Number             | No       | Average of A1–A10 scores            |
| 5   | EvalBreakdown    | Score Breakdown            | Multiple lines     | No       | JSON: {a1..a10} per quality         |
| 6   | CandidateStatus  | Status                     | Choice             | Yes      | Selected/Rejected/Reserved/Pending  |
| 7   | EmailStatus      | Email Status               | Choice             | No       | Pending/SentOffer/SentRegret        |
| 8   | EmailSentDate    | Email Sent Date            | Date               | No       | WORKFLOW-MANAGED                    |
| 9   | Remarks          | Candidate Remarks          | Multiple lines     | No       | Interviewer notes on this candidate |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `INTERVIEWDB_List` | Gallery of all interview batches | Search by vacancy/date/status; RAG status indicator |
| `INTERVIEWDB_New` | New batch header + candidate entry | Header fields + editable candidate gallery (up to 30 rows) |
| `INTERVIEWDB_View` | Read-only batch detail with candidate table | Batch header, sortable candidate gallery with scores and status |
| `INTERVIEWDB_Edit` | Edit batch header while in Sourcing stage | Header + candidate add/edit |
| `INTERVIEWDB_Score` | Interviewer scoring portal | Per-candidate score sliders (A1–A10); read-only candidate list; submit for verification |
| `INTERVIEWDB_Verify` | HR Manager verification portal | Candidate list + status choice per row (Selected/Rejected/Reserved) |
| `INTERVIEWDB_Communicate` | HR Specialist communication hub | Batch summary; "Send All Regrets" toggle; individual override per candidate |

### Screen Interaction Details

**INTERVIEWDB_List Screen**
- Gallery displaying all `INTERVIEWDB` records from `MainDB_Human Resources (D05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `INTERVIEWDB_New` (visible to Initiator role only).
- Tap a row to navigate to `INTERVIEWDB_View`.

**INTERVIEWDB_New / _Edit Screen**
- Data entry form bound to `MainDB_Human Resources (D05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**INTERVIEWDB_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "INTERVIEWDB-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(INTERVIEWDB_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(INTERVIEWDB_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "INTERVIEWDB",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(INTERVIEWDB_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "INTERVIEWDB" &&
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
| HR Recruiter (DocAuthor) | List, New, View, Edit |
| Interviewer (InName) | List, View, Score |
| HR Manager (VrName) | List, View, Verify |
| HR Specialist (HRE) | List, View, Communicate |
| HR Admin | All |
| Reader | List, View |

### 3. Data Integrity Rules

- `FormCode` must always equal `INTERVIEWDB` (system-enforced constant).
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
- [ ] Canvas App screens (`INTERVIEWDB_List`, `INTERVIEWDB_New`, `INTERVIEWDB_View`, `INTERVIEWDB_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
