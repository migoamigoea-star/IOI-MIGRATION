# User Story — SRS (`SRS`)

> **Department:** ADM (Department_01)  
> **Module:** ADM Module  
> **Site(s):** Prai  
> **SharePoint List:** `MainDB_ADM`  
> **Form Code:** `SRS`

---

## 1. App Overview & Purpose

SRS is an administration form migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online).
The form supports standardized administrative submission, review, and approval at the Prai site.
Detailed field-level extraction remains anchored in the source analysis artifact.

---

## 2. User Stories

**US-01: Submit SRS**
> As a **Initiator** (member of `D01-ADM-Users`),  
> I want to **submit srs** in the `SRS` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus = 'Submitted'

**US-02: Review SRS**
> As a **Reviewer** (member of `D01-ADM-Reviewers`),  
> I want to **review srs** in the `SRS` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus = 'Reviewed'

**US-03: Decide SRS**
> As a **Approver** (member of `D01-ADM-Approvers`),  
> I want to **decide srs** in the `SRS` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus = 'Approved' OR 'Rejected'

**US-LIST: Search and filter SRS records**
> As an **authorized user**,  
> I want to search, filter, and view SRS records in the list screen,  
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

**Target List:** `MainDB_ADM`

| # | Column (Internal) | Display Name    | Type                   | Required | Notes                                |
|---|-------------------|-----------------|------------------------|----------|--------------------------------------|
| 1 | Title             | Title           | Single line of text    | Yes      | Record identifier                    |
| 2 | FormType          | Form Type       | Single line of text    | Yes      | Fixed value: SRS                     |
| 3 | CurrentStatus     | Current Status  | Choice                 | Yes      | Draft, Submitted, Approved, Rejected |
| 4 | Requestor         | Requestor       | Person                 | Yes      | Initiator                            |
| 5 | RequestDate       | Request Date    | Date                   | Yes      | Created/submitted date               |
| 6 | ReviewComments    | Review Comments | Multiple lines of text | No       | Review notes                         |
| 7 | AttachmentLink    | Attachment Link | Hyperlink              | No       | Supporting reference                 |
| 8 | EnvironmentTag    | Environment Tag | Choice                 | Yes      | DEV, TEST, PROD                      |

---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| SRS_List | List all SRS records | Authenticated users |
| SRS_New | Create SRS request | D01-ADM-Users+ |
| SRS_View | View SRS detail | Authenticated users |
| SRS_Edit | Edit SRS draft/review | Initiator + reviewers |
| SRS_Approval | Approve/reject SRS | D01-ADM-Approvers |

### Screen Interaction Details

**SRS_List Screen**
- Gallery displaying all `SRS` records from `MainDB_ADM`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `SRS_New` (visible to Initiator role only).
- Tap a row to navigate to `SRS_View`.

**SRS_New / _Edit Screen**
- Data entry form bound to `MainDB_ADM`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**SRS_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "SRS-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(SRS_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(SRS_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "SRS",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(SRS_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "SRS" &&
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
- **Stage 1:** `Submit SRS` — performed by `Initiator`
- **Stage 2:** `Review SRS` — performed by `Reviewer`
- **Stage 3:** `Decide SRS` — performed by `Approver`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Initiator | Create, Read own |
| Reviewer | Read, Edit in review |
| Approver | Read, Approve, Reject |
| Admin | Full control |

### 3. Data Integrity Rules

- `FormCode` must always equal `SRS` (system-enforced constant).
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

| Flow Name         | Trigger                   | Action                                   |
|-------------------|---------------------------|------------------------------------------|
| ADM_SRS_OnSubmit  | CurrentStatus='Submitted' | Notify reviewer and stamp review stage   |
| ADM_SRS_OnReview  | CurrentStatus='Reviewed'  | Notify approver and stamp decision stage |
| ADM_SRS_OnApprove | CurrentStatus='Approved'  | Lock record and notify initiator         |
| ADM_SRS_OnReject  | CurrentStatus='Rejected'  | Return to initiator with reason          |

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

- [ ] All SharePoint columns in `MainDB_ADM` are created with correct types and required flags.
- [ ] Canvas App screens (`SRS_List`, `SRS_New`, `SRS_View`, `SRS_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
