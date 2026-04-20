# User Story — Outsource Worker Database (`OWP`)

> **Department:** HR  
> **Module:** Employee Lifecycle — Contractor & Outsource Tracking  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "OWP"`  
> **Form Code:** `OWP`

---

## 1. App Overview & Purpose

OWP is a registry database form for tracking outsourced and contract workers engaged by IOI
Acidchem. It stores personal details, immigration documents (passport, work permit), employment
status, and separation date. There is no approval workflow — HR staff perform direct CRUD operations
to maintain accurate headcount records for compliance, permit renewal monitoring, and workforce
reporting.

---

---

## 2. User Stories

**US-01: Create record**
> As a **HR Staff** (member of `D05-HR-Staff`),  
> I want to **create record** in the `OWP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* HR creates new outsource worker entry

**US-02: Update record**
> As a **HR Staff** (member of `D05-HR-Staff`),  
> I want to **update record** in the `OWP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* HR edits permit/document details

**US-03: Set exit status**
> As a **HR Staff** (member of `D05-HR-Staff`),  
> I want to **set exit status** in the `OWP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* HR sets Status=Resigned/Terminated + date

**US-LIST: Search and filter Outsource Worker Database records**
> As an **authorized user**,  
> I want to search, filter, and view Outsource Worker Database records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "OWP"`

| #   | SP Internal Name | Display Label           | Column Type         | Required | Classification  | Source Mapping / Notes                           |
| --- | ---------------- | ----------------------- | ------------------- | -------- | --------------- | ------------------------------------------------ |
| 1   | Title            | Title                   | Single line text    | Yes      | SYSTEM-COMPUTED | OWP prefix + EmpNo                               |
| 2   | FormCode         | Form Code               | Single line text    | Yes      | SYSTEM-COMPUTED | Fixed value OWP                                  |
| 3   | Company          | Company                 | Choice              | Yes      | USER-ENTERED    | `Company` — IOI Oleochemical, IOI Acidchem       |
| 4   | WorkerStatus     | Status                  | Choice              | Yes      | USER-ENTERED    | `Status` — Active, Resigned, Expired, Terminated |
| 5   | EmpName          | Worker Name             | Single line text    | Yes      | USER-ENTERED    | `Name`                                           |
| 6   | EmpNo            | Employee No             | Single line text    | Yes      | USER-ENTERED    | `EmpNo`                                          |
| 7   | Section          | Section                 | Single line text    | No       | USER-ENTERED    | `Section`                                        |
| 8   | DateOfBirth      | Date of Birth           | Date and Time       | Yes      | USER-ENTERED    | `DOB`                                            |
| 9   | DateOfJoining    | Date of Joining         | Date and Time       | Yes      | USER-ENTERED    | `DOJ`                                            |
| 10  | PassportNo       | Passport Number         | Single line text    | Yes      | USER-ENTERED    | `PassportNo`                                     |
| 11  | PassportExpiry   | Passport Expiry Date    | Date and Time       | Yes      | USER-ENTERED    | `PassportExpiryDate`                             |
| 12  | Nationality      | Nationality             | Single line text    | Yes      | USER-ENTERED    | `Nationality`                                    |
| 13  | WPExpiryDate     | Work Permit Expiry Date | Date and Time       | Yes      | USER-ENTERED    | `WorkPermitExpiryDate`                           |
| 14  | WorkPermitNo     | Work Permit Number      | Single line text    | Yes      | USER-ENTERED    | `WorkPermitNo`                                   |
| 15  | WPEmployed       | Work Permit Employed By | Choice              | No       | USER-ENTERED    | `WPEmployed` — IOI Acidchem, Contractor company  |
| 16  | WPEmployer       | Employer Name           | Single line text    | No       | USER-ENTERED    | `WPEmployer`                                     |
| 17  | ResignDate       | Resignation / Exit Date | Date and Time       | No       | USER-ENTERED    | `ResignDate`                                     |
| 18  | ExitReason       | Exit Reason             | Multiple lines text | No       | USER-ENTERED    | `Reason`                                         |
| 19  | EnvironmentTag   | Environment             | Choice              | Yes      | SYSTEM-COMPUTED | DEV, TEST, PROD                                  |
| 20  | IsLocked         | Is Locked               | Yes/No              | No       | USER-MANAGED    | Lock on resignation/termination                  |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| OWP_List | Gallery | List all outsource workers with status/company filter |
| OWP_New | Form | Register new outsource worker |
| OWP_View | Read-only | View worker record (documents + status) |
| OWP_Edit | Form | Edit worker details |

### Screen Interaction Details

**OWP_List Screen**
- Gallery displaying all `OWP` records from `MainDB_HR **Form Discriminator:** FormCode = "OWP"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `OWP_New` (visible to Initiator role only).
- Tap a row to navigate to `OWP_View`.

**OWP_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "OWP"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**OWP_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "OWP-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(OWP_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(OWP_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "OWP",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(OWP_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "OWP" &&
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
- **Stage 1:** `Create record` — performed by `HR Staff`
- **Stage 2:** `Update record` — performed by `HR Staff`
- **Stage 3:** `Set exit status` — performed by `HR Staff`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| HR Admins | D05-HR-Staff |
| HR Manager | D05-HR-Manager |

### 3. Data Integrity Rules

- `FormCode` must always equal `OWP` (system-enforced constant).
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

| Flow Name                  | Trigger         | Action                                                          |
| -------------------------- | --------------- | --------------------------------------------------------------- |
| HR_OWP_ExpiryAlertPassport | Scheduled daily | Alert HR 60/30/14 days before PassportExpiry for Active workers |
| HR_OWP_ExpiryAlertWP       | Scheduled daily | Alert HR 60/30/14 days before WPExpiryDate for Active workers   |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "OWP"` are created with correct types and required flags.
- [ ] Canvas App screens (`OWP_List`, `OWP_New`, `OWP_View`, `OWP_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
