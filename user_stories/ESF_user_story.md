# User Story — ESF Form (`ESF`)

> **Department:** HR (Department_05)  
> **Module:** M3 - Employee Records & Information  
> **Site(s):** PRAI (Penang)  
> **SharePoint List:** `MainDB_HR`  
> **Form Code:** `ESF`

---

## 1. App Overview & Purpose

ESF enables HR record submission and approval routing with standardized status control and
auditability.

---

## 2. User Stories

**US-01: Create draft**
> As a **Initiator** (member of `D05-HR-Initiators`),  
> I want to **create draft** in the `ESF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* On create

**US-02: Review**
> As a **HR Reviewer** (member of `D05-HR-Editors-L1`),  
> I want to **review** in the `ESF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus=Submitted

**US-03: Final decision**
> As a **HR Manager** (member of `D05-HR-Manager`),  
> I want to **final decision** in the `ESF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When review outcome submitted

**US-LIST: Search and filter ESF Form records**
> As an **authorized user**,  
> I want to search, filter, and view ESF Form records in the list screen,  
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

**Target List:** `MainDB_HR`

| #   | SP Internal Name | Display Label  | Column Type     | Required | Notes             |
| --- | ---------------- | -------------- | --------------- | -------- | ----------------- |
| 1   | FormType         | Form Type      | Choice          | Yes      | Fixed value `ESF` |
| 2   | INO              | Reference No.  | Single line     | Yes      | Flow-generated    |
| 3   | CurrentStatus    | Current Status | Choice          | Yes      | Workflow-managed  |
| 4   | Requester        | Requester      | Person or Group | Yes      | Initiator         |
| 5   | Department       | Department     | Single line     | Yes      | HR department     |
| 6   | Remarks          | Remarks        | Multiple lines  | No       | Optional notes    |

---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| ESF_List | List records | All authorized users |
| ESF_New | Create request | Initiator |
| ESF_Edit | Update request | Initiator and reviewer |
| ESF_View | Read-only view | All authorized users |
| ESF_Approval | Final decision | Manager |

### Screen Interaction Details

**ESF_List Screen**
- Gallery displaying all `ESF` records from `MainDB_HR`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ESF_New` (visible to Initiator role only).
- Tap a row to navigate to `ESF_View`.

**ESF_New / _Edit Screen**
- Data entry form bound to `MainDB_HR`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ESF_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ESF-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(ESF_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ESF_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ESF",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ESF_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ESF" &&
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
- **Stage 1:** `Create draft` — performed by `Initiator`
- **Stage 2:** `Review` — performed by `HR Reviewer`
- **Stage 3:** `Final decision` — performed by `HR Manager`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Initiator | Contribute |
| Reviewer | Contribute |
| Manager | Contribute |
| Admin | Full Control |
| Reader | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `ESF` (system-enforced constant).
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

| Stage  | Flow Name         | Trigger        | Action Summary                   |
| ------ | ----------------- | -------------- | -------------------------------- |
| Submit | HR_ESF_OnSubmit   | Item created   | Set status and notify reviewer   |
| Review | HR_ESF_OnReview   | Status updated | Route to manager                 |
| Final  | HR_ESF_OnDecision | Manager action | Lock record and notify requester |

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

- [ ] All SharePoint columns in `MainDB_HR` are created with correct types and required flags.
- [ ] Canvas App screens (`ESF_List`, `ESF_New`, `ESF_View`, `ESF_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
