# User Story — CWR (`CWR`)

> **Department:** Human Resources (D05)  
> **Module:** M2 — Recruitment & Hiring  
> **Site(s):** PRAI, Johor  
> **SharePoint List:** `MainDB_Human Resources (D05)`  
> **Form Code:** `CWR`

---

## 1. App Overview & Purpose

`CWR` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `Human Resources (D05)` department at the PRAI, Johor site.

---

## 2. User Stories

**US-LIST: Search and filter CWR records**
> As an **authorized user**,  
> I want to search, filter, and view CWR records in the list screen,  
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

| #   | SP Internal Name | Display Label                | Column Type    | Required | Classification   | Notes                                                                  |
| --- | ---------------- | ---------------------------- | -------------- | -------- | ---------------- | ---------------------------------------------------------------------- |
| 1   | FormType         | Form Type                    | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "CWR"                                                           |
| 2   | INO              | Reference No.                | Single line    | Yes      | SYSTEM-COMPUTED  | HR-CWR-YYMM-NNNN via PA                                                |
| 3   | CurrentStatus    | Current Status               | Choice         | Yes      | WORKFLOW-MANAGED | Draft/Submitted/HODEndorsed/DivApproved/HRAcknowledged/Rejected/Closed |
| 4   | EnvironmentTag   | Environment                  | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                                          |
| 5   | IssueNo          | Issue No.                    | Single line    | No       | USER-ENTERED     | Legacy issue reference                                                 |
| 6   | SendTo           | Initiation Category/To (HOD) | Single line    | Yes      | USER-ENTERED     | Recipient HOD or category                                              |
| 7   | DivHead          | Division Head                | Person         | Yes      | USER-ENTERED     | Division Head name                                                     |
| 8   | DocAuthor        | Requested By                 | Person         | Yes      | SYSTEM-COMPUTED  | Auto-filled from login                                                 |
| 9   | Designation      | Designation                  | Single line    | Yes      | USER-ENTERED     | Requestor's designation                                                |
| 10  | DateIssued       | Date Issued                  | Date           | Yes      | USER-ENTERED     | Form issue date                                                        |
| 11  | WorkerName       | From (Name)                  | Single line    | Yes      | USER-ENTERED     | Requesting person name                                                 |
| 12  | ContractType     | Type of Contract Workers     | Choice         | Yes      | USER-ENTERED     | Permanent/Temporary                                                    |
| 13  | PermCategory     | Category                     | Choice         | Yes      | USER-ENTERED     | Permanent/Temporary                                                    |
| 14  | SiteA            | Site (Section A)             | Choice         | Yes      | USER-ENTERED     | PRAI/Johor                                                             |
| 15  | NoWorkersA       | No. of Workers (Section A)   | Number         | Yes      | USER-ENTERED     | Count required                                                         |
| 16  | WorkstationA     | Section/Workstation (A)      | Single line    | Yes      | USER-ENTERED     | Workstation or section                                                 |
| 17  | JDA              | Job Description (A)          | Multiple lines | Yes      | USER-ENTERED     | JD for Perm/Temp workers                                               |
| 18  | WorkingHour      | Working Hour                 | Single line    | No       | USER-ENTERED     | Shift hours                                                            |
| 19  | CurrentNoWorkers | Current No. of Workers       | Number         | No       | USER-ENTERED     | Existing headcount at station                                          |
| 20  | EffDate          | Effective Date               | Date           | No       | USER-ENTERED     | Date workers needed                                                    |
| 21  | Justification    | Justification                | Multiple lines | Yes      | USER-ENTERED     | Business justification                                                 |
| 22  | RequiredPeriodsA | Required Periods (Section A) | Multiple lines | No       | USER-ENTERED     | JSON: [{from,to,days}×3]                                               |
| 23  | SiteB            | Site (Section B — Shutdown)  | Choice         | No       | USER-ENTERED     | PRAI/Johor                                                             |
| 24  | NoWorkersB       | No. of Workers (Section B)   | Number         | No       | USER-ENTERED     | Shutdown workers needed                                                |
| 25  | WorkstationB     | Section/Workstation (B)      | Single line    | No       | USER-ENTERED     | Shutdown workstation                                                   |
| 26  | JDB              | Job Description (B)          | Multiple lines | No       | USER-ENTERED     | JD for shutdown workers                                                |
| 27  | RequiredPeriodsB | Required Periods (Section B) | Multiple lines | No       | USER-ENTERED     | JSON: [{from,to,days}×3]                                               |
| 28  | HODApp           | HOD Endorsement              | Choice         | No       | WORKFLOW-MANAGED | Approved/Rejected                                                      |
| 29  | HODName          | HOD Name                     | Single line    | No       | WORKFLOW-MANAGED | Filled on endorsement                                                  |
| 30  | HODDate          | HOD Date                     | Date           | No       | WORKFLOW-MANAGED | Endorsement date                                                       |
| 31  | HODRemark        | HOD Remark                   | Multiple lines | No       | WORKFLOW-MANAGED | HOD comments                                                           |
| 32  | DivApp           | Division Head Decision       | Choice         | No       | WORKFLOW-MANAGED | Approved/Rejected                                                      |
| 33  | HODName3         | Division Head Name           | Single line    | No       | WORKFLOW-MANAGED | Filled on approval                                                     |
| 34  | HODDate3         | Division Head Date           | Date           | No       | WORKFLOW-MANAGED | Approval date                                                          |
| 35  | HODRemark3       | Division Head Remark         | Multiple lines | No       | WORKFLOW-MANAGED | Division Head comments                                                 |
| 36  | HRName           | HR Name                      | Single line    | No       | WORKFLOW-MANAGED | HR acknowledging officer                                               |
| 37  | HRPosition       | HR Position                  | Single line    | No       | WORKFLOW-MANAGED | HR officer position                                                    |
| 38  | HRDate           | HR Acknowledged Date         | Date           | No       | WORKFLOW-MANAGED | Acknowledgement date                                                   |
| 39  | Attachments      | Supporting Documents         | Attachment     | No       | USER-ENTERED     | Supporting files                                                       |
| 40  | IsLocked         | Is Locked                    | Yes/No         | No       | WORKFLOW-MANAGED | Lock after HRAcknowledged                                              |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `CWR_List` | Gallery of all requisitions, filterable by site/status | Gallery, search, status chips |
| `CWR_New` | New requisition form — both sections | Tabbed container (Section A / Section B), person pickers |
| `CWR_View` | Read-only detail with full approval timeline | Display form, approval timeline component |
| `CWR_Edit` | Edit by DocAuthor while in Draft | Edit form, section toggle |
| `CWR_HODReview` | HOD endorsement screen | Read-only summary + Approve/Reject radios + Remark field |
| `CWR_DivReview` | Division Head approval screen | Read-only summary + Approve/Reject radios + Remark field |
| `CWR_HRAck` | HR acknowledgement screen | Summary + HRName/Position/Date fields |

### Screen Interaction Details

**CWR_List Screen**
- Gallery displaying all `CWR` records from `MainDB_Human Resources (D05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `CWR_New` (visible to Initiator role only).
- Tap a row to navigate to `CWR_View`.

**CWR_New / _Edit Screen**
- Data entry form bound to `MainDB_Human Resources (D05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**CWR_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "CWR-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(CWR_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(CWR_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "CWR",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(CWR_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "CWR" &&
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
| Requestor (DocAuthor) | List, New, View, Edit (Draft) |
| HOD | List, View, HODReview |
| Division Head | List, View, DivReview |
| HR Officer | List, View, HRAck |
| HR Admin | All |
| Reader | List, View |

### 3. Data Integrity Rules

- `FormCode` must always equal `CWR` (system-enforced constant).
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
- [ ] Canvas App screens (`CWR_List`, `CWR_New`, `CWR_View`, `CWR_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
