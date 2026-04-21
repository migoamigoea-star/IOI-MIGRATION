# User Story — Resource Supply Estimation Sheet (`RSES`)

> **Department:** FIN` (Department_04)  
> **Module:** M3 — Resource Planning & Analysis  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_FIN`  
> **Form Code:** `RSES`

---

## 1. App Overview & Purpose

Resource Supply Estimation Sheet (RSES) forecasts resource requirements and supply plans for
upcoming periods. Submitted by department heads, reviewed by finance and operations for resource
capacity planning. Migrated to MainDB_FIN with FormCode=RSES, supporting resource planning, budget
forecasting, and capacity analysis workflows.

---

---

## 2. User Stories

**US-01: Create & submit RSES**
> As a **Item created (FormCode=RSES)** (member of `Department Head`),  
> I want to **create & submit rses** in the `RSES` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-Submitters`

**US-02: Finance review**
> As a **Status=Submitted** (member of `Finance Analyst`),  
> I want to **finance review** in the `RSES` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-Reviewers`

**US-03: Operations approval**
> As a **Status=Pending Review** (member of `Operations Manager`),  
> I want to **operations approval** in the `RSES` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-Approvers`

**US-04: Archive**
> As a **Status=Approved** (member of `System`),  
> I want to **archive** in the `RSES` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-Admins`

**US-LIST: Search and filter Resource Supply Estimation Sheet records**
> As an **authorized user**,  
> I want to search, filter, and view Resource Supply Estimation Sheet records in the list screen,  
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

**Target List:** `MainDB_FIN`

| #   | Column Name    | SP Type                | Required | Choices / Source                            | Notes                                    |
| --- | -------------- | ---------------------- | -------- | ------------------------------------------- | ---------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                           | Auto-populated from RSES tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: RSES                              | Shared list discriminator                |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Review; Approve; Complete | Workflow routing state                   |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Review; Approved; Archived   | Lifecycle status                         |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                           | Department head submitter                |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                           | Submission timestamp                     |
| 7   | ApprovedBy     | Person or Group        | No       | —                                           | Finance approver (workflow-set)          |
| 8   | ApprovedDate   | Date and Time          | No       | —                                           | Approval timestamp                       |
| 9   | Comments       | Multiple lines of text | No       | —                                           | Finance and operations remarks           |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                             | DEC-004 environment tier                 |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| RSES_List | Search and filter RSES records | All FIN roles |
| RSES_New | Create new resource supply estimate | `D04-FIN-Submitters` |
| RSES_View | Read-only detail view | All authorized users |
| RSES_Edit | Edit in Draft state | Department heads and reviewers |

### Screen Interaction Details

**RSES_List Screen**
- Gallery displaying all `RSES` records from `MainDB_FIN`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `RSES_New` (visible to Initiator role only).
- Tap a row to navigate to `RSES_View`.

**RSES_New / _Edit Screen**
- Data entry form bound to `MainDB_FIN`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**RSES_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "RSES-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(RSES_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(RSES_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "RSES",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(RSES_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "RSES" &&
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
- **Stage 1:** `Create & submit RSES` — performed by `Item created (FormCode=RSES)`
- **Stage 2:** `Finance review` — performed by `Status=Submitted`
- **Stage 3:** `Operations approval` — performed by `Status=Pending Review`
- **Stage 4:** `Archive` — performed by `Status=Approved`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Department Head / Submitter | Contribute |
| Finance Analyst / Reviewer | Contribute |
| Operations Manager / Approver | Approve |
| System Admin | Full Control |

### 3. Data Integrity Rules

- `FormCode` must always equal `RSES` (system-enforced constant).
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

| Flow Name          | Trigger                      | Actions                                                                                                                                               |
| ------------------ | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_RSES_Submit`  | Item created (FormCode=RSES) | 1. Validate resource forecast fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify finance reviewer. 5. Set CurrentAction=Review. |
| `FIN_RSES_Approve` | Status updated to Approved   | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Archived. 3. Archive record to planning database. 4. Send approval notification.                     |
| `FIN_RSES_Return`  | Status updated to Returned   | 1. Set Status=Draft; CurrentAction=Draft. 2. Append return notes to Comments. 3. Route back to department for revision.                               |

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

- [ ] All SharePoint columns in `MainDB_FIN` are created with correct types and required flags.
- [ ] Canvas App screens (`RSES_List`, `RSES_New`, `RSES_View`, `RSES_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
