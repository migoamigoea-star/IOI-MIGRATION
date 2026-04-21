# User Story — FTCR (`FTCR`)

> **Department:** Human Resources (D05)  
> **Module:** M2 — Recruitment & Hiring  
> **Site(s):** PRAI, Johor  
> **SharePoint List:** `MainDB_Human Resources (D05)`  
> **Form Code:** `FTCR`

---

## 1. App Overview & Purpose

`FTCR` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `Human Resources (D05)` department at the PRAI, Johor site.

---

## 2. User Stories

**US-LIST: Search and filter FTCR records**
> As an **authorized user**,  
> I want to search, filter, and view FTCR records in the list screen,  
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

| #   | SP Internal Name  | Display Label               | Column Type    | Required | Classification   | Notes                                                                         |
| --- | ----------------- | --------------------------- | -------------- | -------- | ---------------- | ----------------------------------------------------------------------------- |
| 1   | FormType          | Form Type                   | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "FTCR"                                                                 |
| 2   | INO               | Reference No.               | Single line    | Yes      | SYSTEM-COMPUTED  | HR-FTC-YYMM-NNNN via PA                                                       |
| 3   | CurrentStatus     | Current Status              | Choice         | Yes      | WORKFLOW-MANAGED | Draft/Submitted/EndorsedHOD/ApprovedHR/ApprovedCOO/ApprovedED/Rejected/Closed |
| 4   | EnvironmentTag    | Environment                 | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                                                 |
| 5   | EmpName           | Employee Name               | Single line    | Yes      | USER-ENTERED     | Subject employee                                                              |
| 6   | EmpNo             | Employee No.                | Single line    | Yes      | USER-ENTERED     | Staff ID                                                                      |
| 7   | DOB               | Date of Birth               | Date           | Yes      | USER-ENTERED     | For age calculation                                                           |
| 8   | EmpAge            | Age                         | Number         | No       | SYSTEM-COMPUTED  | PA-calculated from DOB                                                        |
| 9   | EmpPost           | Position                    | Single line    | Yes      | USER-ENTERED     | Current title                                                                 |
| 10  | Dept              | Department/Section          | Single line    | Yes      | USER-ENTERED     | Employee's dept                                                               |
| 11  | JoinDate          | Date Joined                 | Date           | Yes      | USER-ENTERED     | Original join date                                                            |
| 12  | RetDate           | Retirement Date             | Date           | Yes      | USER-ENTERED     | Scheduled retirement                                                          |
| 13  | DivHead           | HOD/Division Head           | Person         | Yes      | USER-ENTERED     | Form initiator                                                                |
| 14  | Attachment        | Supporting Documents        | Attachment     | No       | USER-ENTERED     | Contract docs, CV                                                             |
| 15  | CPeriod           | Contract Period (Months)    | Number         | Yes      | USER-ENTERED     | No. of months for extension                                                   |
| 16  | Others            | Period Notes                | Single line    | No       | USER-ENTERED     | Specify if "Others" selected                                                  |
| 17  | DivHeadJust       | Division Head Justification | Multiple lines | Yes      | USER-ENTERED     | Business case                                                                 |
| 18  | InSuccess         | Identified Successor        | Choice         | Yes      | USER-ENTERED     | Yes/No                                                                        |
| 19  | Ext               | For External Advertisement  | Choice         | No       | USER-ENTERED     | Yes/No                                                                        |
| 20  | SucName           | Successor Name              | Single line    | No       | USER-ENTERED     | Required if InSuccess=Yes                                                     |
| 21  | SucEmpNo          | Successor Emp. No.          | Single line    | No       | USER-ENTERED     | Required if InSuccess=Yes                                                     |
| 22  | SucPost           | Successor Position          | Single line    | No       | USER-ENTERED     |                                                                               |
| 23  | SucAge            | Successor Age               | Number         | No       | SYSTEM-COMPUTED  |                                                                               |
| 24  | SucDept           | Successor Dept/Section      | Single line    | No       | USER-ENTERED     |                                                                               |
| 25  | SucDate           | Successor Start Date        | Date           | No       | USER-ENTERED     | When successor takes over                                                     |
| 26  | TrReq             | Training Required           | Choice         | No       | USER-ENTERED     | Yes/No                                                                        |
| 27  | TrList            | Training List               | Multiple lines | No       | USER-ENTERED     | List if TrReq=Yes                                                             |
| 28  | Remarks           | Remarks/Attachment Notes    | Multiple lines | No       | USER-ENTERED     | General comments                                                              |
| 29  | SubBy             | Submitted By (Dept Head)    | Single line    | No       | USER-ENTERED     | Department/Section Head name                                                  |
| 30  | SubDesg           | Submission Designation      | Single line    | No       | USER-ENTERED     | Submitter's title                                                             |
| 31  | SubDate           | Submission Date             | Date           | No       | USER-ENTERED     | Date submitted by Dept Head                                                   |
| 32  | EndBy             | Endorsed By (Div Head)      | Single line    | No       | WORKFLOW-MANAGED | Division/Dept Head name                                                       |
| 33  | EndDesg           | Endorser Designation        | Single line    | No       | WORKFLOW-MANAGED |                                                                               |
| 34  | EndDate           | Endorsement Date            | Date           | No       | WORKFLOW-MANAGED |                                                                               |
| 35  | AppHR             | Approved By HR              | Person         | No       | WORKFLOW-MANAGED | HR approver                                                                   |
| 36  | AppCOO            | Approved By COO             | Person         | No       | WORKFLOW-MANAGED | COO approver                                                                  |
| 37  | AppED             | Approved By ED              | Person         | No       | WORKFLOW-MANAGED | Exec Director (if required)                                                   |
| 38  | Fixed             | Contract Renewed            | Choice         | No       | WORKFLOW-MANAGED | Yes/No — final outcome                                                        |
| 39  | CaseStatus        | Case Status                 | Choice         | No       | WORKFLOW-MANAGED | Open/Approved/Rejected                                                        |
| 40  | AppFor            | Approved For (Period)       | Single line    | No       | WORKFLOW-MANAGED | Final approved period                                                         |
| 41  | NotHOD            | Notify HOD                  | Yes/No         | No       | WORKFLOW-MANAGED | Flag to send HOD notification                                                 |
| 42  | Remarks2          | HR Remarks                  | Multiple lines | No       | WORKFLOW-MANAGED | HR additional comments                                                        |
| 43  | CA                | Current Action              | Choice         | No       | WORKFLOW-MANAGED | Stage tracking                                                                |
| 44  | BackgroundHistory | Employee Background History | Multiple lines | No       | USER-ENTERED     | JSON: 6-year rolling table                                                    |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `FTCR_List` | Gallery of all FTCR records, filterable by dept/status | Gallery, date range filter, status chips |
| `FTCR_New` | New FTCR form entry | Employee picker, date pickers, JD fields, Background History table entry |
| `FTCR_View` | Read-only view with full approval chain | Display form, 6-year history table, approval timeline |
| `FTCR_Edit` | Edit while in Draft/pending submission | Editable form, history table grid |
| `FTCR_EndorseReview` | Division Head endorsement | Summary + Endorse button + date auto-fill |
| `FTCR_HRReview` | HR approval screen | Summary + history table + Approve/Reject |
| `FTCR_COOReview` | COO approval screen | Executive summary + Approve/Reject |
| `FTCR_EDReview` | ED approval (conditional) | Executive summary + Approve/Reject |

### Screen Interaction Details

**FTCR_List Screen**
- Gallery displaying all `FTCR` records from `MainDB_Human Resources (D05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `FTCR_New` (visible to Initiator role only).
- Tap a row to navigate to `FTCR_View`.

**FTCR_New / _Edit Screen**
- Data entry form bound to `MainDB_Human Resources (D05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**FTCR_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "FTCR-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(FTCR_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(FTCR_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "FTCR",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(FTCR_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "FTCR" &&
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
| Initiator (DivHead) | List, New, View, Edit |
| Dept/Section Head | List, View, EndorseReview |
| Division Head | List, View, EndorseReview |
| HR Officer | List, View, HRReview |
| COO | List, View, COOReview |
| Executive Director | List, View, EDReview |
| HR Admin | All |
| Reader | List, View |

### 3. Data Integrity Rules

- `FormCode` must always equal `FTCR` (system-enforced constant).
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
- [ ] Canvas App screens (`FTCR_List`, `FTCR_New`, `FTCR_View`, `FTCR_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
