# User Story — Typhoid & NPRA Medical Records Database (`TNPRA`)

> **Department:** HR  
> **Module:** HR Administration — Occupational Health & Compliance  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "TNPRA"`  
> **Form Code:** `TNPRA`

---

## 1. App Overview & Purpose

TNPRA is a medical compliance registry for tracking employee typhoid vaccination records, food
handler examination results, and NPRA (National Pharmaceutical Regulatory Agency) medical
examination records. HR admins create and maintain records for each employee, tracking vaccination
dates, next-due dates, hospital, doctor, and test results. There is no approval workflow — this is a
CRUD registry with scheduled expiry alerts. The migrated solution must normalize the 3 repeating
medical record sections into child tables and preserve expiry-based alerting.

---

---

## 2. User Stories

**US-01: Create / Edit Record**
> As a **HR Admin** (member of `D05-HR-Manager`),  
> I want to **create / edit record** in the `TNPRA` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* On item create or update

**US-02: Expiry Alert**
> As a **System** (member of `—`),  
> I want to **expiry alert** in the `TNPRA` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Daily scheduled — check NextDueDate < Today+30 → email HR Manager

**US-LIST: Search and filter Typhoid & NPRA Medical Records Database records**
> As an **authorized user**,  
> I want to search, filter, and view Typhoid & NPRA Medical Records Database records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "TNPRA"`

| #   | SP Internal Name | Display Label         | Column Type      | Required | Classification  | Source Mapping / Notes                                 |
| --- | ---------------- | --------------------- | ---------------- | -------- | --------------- | ------------------------------------------------------ |
| 1   | Title            | Title                 | Single line text | Yes      | SYSTEM-COMPUTED | TNPRA prefix + EmpNo                                   |
| 2   | FormCode         | Form Code             | Single line text | Yes      | SYSTEM-COMPUTED | Fixed value TNPRA                                      |
| 3   | Category         | Category              | Choice           | Yes      | USER-ENTERED    | `Category` — Food Handler, Non-Food Handler, NPRA-Only |
| 4   | Company          | Company               | Choice           | Yes      | USER-ENTERED    | `Company` — IOI Oleochemical, IOI Acidchem             |
| 5   | RecordStatus     | Record Status         | Choice           | Yes      | USER-ENTERED    | `Status` — Active, Inactive, Terminated                |
| 6   | ContractCompany  | Contract Company      | Single line text | No       | USER-ENTERED    | `ContractCompany` — if contractor                      |
| 7   | EmpName          | Employee Name         | Single line text | Yes      | USER-ENTERED    | `Name`                                                 |
| 8   | EmpNo            | Employee No           | Single line text | Yes      | USER-ENTERED    | `EmpNo`                                                |
| 9   | IdentityNo       | Identity No (NRIC/IC) | Single line text | Yes      | USER-ENTERED    | `IdentityNo`                                           |
| 10  | Gender           | Gender                | Choice           | Yes      | USER-ENTERED    | `Gender` — Male, Female                                |
| 11  | Designation      | Designation           | Single line text | No       | USER-ENTERED    | `Designation`                                          |
| 12  | Section          | Section               | Single line text | No       | USER-ENTERED    | `Section`                                              |
| 13  | Department       | Department            | Single line text | Yes      | USER-ENTERED    | `Department`                                           |
| 14  | Superior         | Immediate Superior    | Single line text | No       | USER-ENTERED    | `Superior`                                             |
| 15  | EnvironmentTag   | Environment           | Choice           | Yes      | SYSTEM-COMPUTED | DEV, TEST, PROD                                        |


| #   | SP Internal Name | Display Label     | Column Type        | Required | Notes                        |
| --- | ---------------- | ----------------- | ------------------ | -------- | ---------------------------- |
| 1   | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Links to parent TNPRA record |
| 2   | TyphoidSeq       | Record No         | Number             | Yes      | Sequence 1–10                |
| 3   | DateGiven        | Date Given        | Date and Time      | Yes      | Vaccination date             |
| 4   | Hospital         | Hospital / Clinic | Single line text   | Yes      | Where vaccination was given  |
| 5   | DoctorName       | Doctor Name       | Single line text   | No       |                              |
| 6   | NextDueDate      | Next Due Date     | Date and Time      | Yes      | For alert scheduling         |
| 7   | BatchNo          | Batch Number      | Single line text   | No       | Vaccine batch identifier     |


| #   | SP Internal Name | Display Label     | Column Type        | Required | Notes                        |
| --- | ---------------- | ----------------- | ------------------ | -------- | ---------------------------- |
| 1   | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Links to parent TNPRA record |
| 2   | ExamSeq          | Record No         | Number             | Yes      | Sequence 1–10                |
| 3   | ExamDate         | Exam Date         | Date and Time      | Yes      | Date of examination          |
| 4   | Hospital         | Hospital / Clinic | Single line text   | Yes      |                              |
| 5   | DoctorName       | Doctor Name       | Single line text   | No       |                              |
| 6   | ExamResult       | Result            | Choice             | Yes      | Pass, Fail                   |
| 7   | NextExamDate     | Next Exam Date    | Date and Time      | Yes      | For alert scheduling         |


| #   | SP Internal Name | Display Label     | Column Type        | Required | Notes                        |
| --- | ---------------- | ----------------- | ------------------ | -------- | ---------------------------- |
| 1   | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Links to parent TNPRA record |
| 2   | NPRASeq          | Record No         | Number             | Yes      | Sequence                     |
| 3   | DateExam         | Exam Date         | Date and Time      | Yes      |                              |
| 4   | Hospital         | Hospital / Clinic | Single line text   | Yes      |                              |
| 5   | DoctorName       | Doctor Name       | Single line text   | No       |                              |
| 6   | ExamResult       | Result            | Choice             | Yes      | Pass, Fail                   |
| 7   | NPRARefNo        | NPRA Reference No | Single line text   | No       | Regulatory reference number  |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| TNPRA_List | Gallery | List all TNPRA records with category/department/status filter |
| TNPRA_New | Form | Create new employee medical record with child table entry galleries |
| TNPRA_View | Read-only | View all sections: typhoid, food handler, NPRA records |
| TNPRA_Edit | Form | Edit existing record and add new rows to child galleries |

### Screen Interaction Details

**TNPRA_List Screen**
- Gallery displaying all `TNPRA` records from `MainDB_HR **Form Discriminator:** FormCode = "TNPRA"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `TNPRA_New` (visible to Initiator role only).
- Tap a row to navigate to `TNPRA_View`.

**TNPRA_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "TNPRA"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**TNPRA_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "TNPRA-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(TNPRA_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(TNPRA_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "TNPRA",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(TNPRA_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "TNPRA" &&
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
- **Stage 1:** `Create / Edit Record` — performed by `HR Admin`
- **Stage 2:** `Expiry Alert` — performed by `System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| HR Admins | D05-HR-Manager |
| All Staff | D05-HR-Staff |

### 3. Data Integrity Rules

- `FormCode` must always equal `TNPRA` (system-enforced constant).
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

| Flow Name            | Trigger                              | Action                                                                                                                                                     |
| -------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HR_TNPRA_ExpiryAlert | Scheduled daily (recurrence trigger) | Query HR_TNPRA_TyphoidRecords and HR_TNPRA_FoodHandlerExam for NextDueDate ≤ Today+30; send email to D05-HR-Manager with employee name, type, and due date |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "TNPRA"` are created with correct types and required flags.
- [ ] Canvas App screens (`TNPRA_List`, `TNPRA_New`, `TNPRA_View`, `TNPRA_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
