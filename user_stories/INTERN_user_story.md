# User Story — INTERN (`INTERN`)

> **Department:** Human Resources (D05)  
> **Module:** M2 — Recruitment & Hiring  
> **Site(s):**   
> **SharePoint List:** `MainDB_Human Resources (D05)`  
> **Form Code:** `INTERN`

---

## 1. App Overview & Purpose

`INTERN` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `Human Resources (D05)` department at the  site.

---

## 2. User Stories

**US-LIST: Search and filter INTERN records**
> As an **authorized user**,  
> I want to search, filter, and view INTERN records in the list screen,  
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

| #   | SP Internal Name    | Display Label               | Column Type    | Required | Classification   | Notes                                             |
| --- | ------------------- | --------------------------- | -------------- | -------- | ---------------- | ------------------------------------------------- |
| 1   | FormType            | Form Type                   | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "INTERN"                                   |
| 2   | INO                 | Reference No.               | Single line    | Yes      | SYSTEM-COMPUTED  | HR-TRA-YYMM-NNNN via PA                           |
| 3   | CurrentStatus       | Current Status              | Choice         | Yes      | WORKFLOW-MANAGED | Enrolled/Monitoring/Converted/Completed/Withdrawn |
| 4   | EnvironmentTag      | Environment                 | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                     |
| 5   | TraineeName         | Scholar Name                | Single line    | Yes      | USER-ENTERED     | Full name of trainee                              |
| 6   | University          | University / College        | Single line    | Yes      | USER-ENTERED     | Academic institution                              |
| 7   | CourseTitle         | Course Title                | Single line    | No       | USER-ENTERED     | Field of study                                    |
| 8   | TrainingStart       | Training Start              | Date           | Yes      | USER-ENTERED     | Placement start date                              |
| 9   | TrainingEnd         | Training End                | Date           | Yes      | USER-ENTERED     | Placement end date                                |
| 10  | Bond                | Bond Period (Years)         | Number         | Yes      | USER-ENTERED     | 1–5 years typical                                 |
| 11  | HOD                 | Supervisor / HOD            | Person         | Yes      | USER-ENTERED     | Assigned department supervisor                    |
| 12  | Department          | Placement Department        | Single line    | No       | USER-ENTERED     | Department hosting the trainee                    |
| 13  | Company             | Company Entity              | Choice         | Yes      | USER-ENTERED     | PCO/PCEO/ECM                                      |
| 14  | EmpStatus           | Employment Status           | Choice         | Yes      | WORKFLOW-MANAGED | Trainee/Staff/CompletedBonded/Resigned/Offboarded |
| 15  | DateJoin            | Actual Join Date            | Date           | No       | USER-ENTERED     | Only set when EmpStatus → Staff                   |
| 16  | ExpDateJoin         | Expected Joining Date       | Date           | No       | USER-ENTERED     | Projected join date for funnel                    |
| 17  | LastDay             | Last Day of Service         | Date           | No       | WORKFLOW-MANAGED | Set when trainee exits without joining            |
| 18  | JobPosting          | Job Posting Notes           | Multiple lines | No       | USER-ENTERED     | Ad-hoc placement notes                            |
| 19  | DocAuthor           | Created By (HR Coordinator) | Person         | Yes      | SYSTEM-COMPUTED  | Auto-filled from login                            |
| 20  | Attachment          | CV / Certificates           | Attachment     | No       | USER-ENTERED     | Supporting docs                                   |
| 21  | BondExpiryDate      | Bond Expiry Date            | Date           | No       | SYSTEM-COMPUTED  | PA-calculated: DateJoin + Bond years              |
| 22  | RetentionReviewDone | Retention Review Done       | Yes/No         | No       | WORKFLOW-MANAGED | Set by PA when review triggered                   |
| 23  | IsLocked            | Is Locked                   | Yes/No         | No       | WORKFLOW-MANAGED | Lock after Completed/Offboarded                   |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `INTERN_List` | Searchable trainee gallery, filterable by EmpStatus / University / Company | Gallery, status chips, university filter |
| `INTERN_New` | New trainee entry | Person picker (HOD), date pickers, company/entity choice |
| `INTERN_View` | Read-only detail with bond status indicator | Display form, bond countdown gauge, employment timeline |
| `INTERN_Edit` | Edit whilst in Enrolled/Monitoring stage | Edit form |
| `INTERN_Convert` | Employment conversion action | EmpStatus choice, DateJoin picker, "Generate PAF" button |

### Screen Interaction Details

**INTERN_List Screen**
- Gallery displaying all `INTERN` records from `MainDB_Human Resources (D05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `INTERN_New` (visible to Initiator role only).
- Tap a row to navigate to `INTERN_View`.

**INTERN_New / _Edit Screen**
- Data entry form bound to `MainDB_Human Resources (D05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**INTERN_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "INTERN-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(INTERN_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(INTERN_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "INTERN",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(INTERN_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "INTERN" &&
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
| HR Coordinator (DocAuthor) | List, New, View, Edit, Convert |
| HOD (Supervisor) | List, View |
| HR Manager | All |
| IT / Facilities (offboarding) | View only (triggered by PA) |
| Reader | List, View |

### 3. Data Integrity Rules

- `FormCode` must always equal `INTERN` (system-enforced constant).
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
- [ ] Canvas App screens (`INTERN_List`, `INTERN_New`, `INTERN_View`, `INTERN_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
