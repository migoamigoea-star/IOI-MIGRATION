# User Story — Employee Annual Review Form (`EARF`)

> **Department:** FIN` (Department_04)  
> **Module:** M1 — Financial Approvals & Requisitions  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_FIN`  
> **Form Code:** `EARF`

---

## 1. App Overview & Purpose

Employee Annual Review Form (EARF) captures performance appraisals and review data. Submitted by
managers, reviewed by department heads and HR, with final sign-off for record-keeping. Migrated to
MainDB_FIN with FormCode=EARF, preserving submission routing, multi-level approval, performance
scoring, and auditability.

---

---

## 2. User Stories

**US-01: Create & submit EARF**
> As a **Item created (FormCode=EARF)** (member of `Manager`),  
> I want to **create & submit earf** in the `EARF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-Submitters`

**US-02: Department head review**
> As a **Status=Submitted** (member of `Department Head`),  
> I want to **department head review** in the `EARF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-DeptHeads`

**US-03: HR/Finance sign-off**
> As a **Status=Pending Review** (member of `HR or Finance Manager`),  
> I want to **hr/finance sign-off** in the `EARF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-Signatories`

**US-04: Close workflow**
> As a **Final decision reached** (member of `System`),  
> I want to **close workflow** in the `EARF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D04-FIN-Admins`

**US-LIST: Search and filter Employee Annual Review Form records**
> As an **authorized user**,  
> I want to search, filter, and view Employee Annual Review Form records in the list screen,  
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

| #   | Column Name    | SP Type                | Required | Choices / Source                                              | Notes                                    |
| --- | -------------- | ---------------------- | -------- | ------------------------------------------------------------- | ---------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                                             | Auto-populated from EARF tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: EARF                                                | Shared list discriminator                |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Review; Finalize; Closed                    | Workflow routing state                   |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Review; Approved; Signed Off; Returned; Closed | Lifecycle status                         |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                                             | Manager submitter                        |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                                             | Submission timestamp                     |
| 7   | ApprovedBy     | Person or Group        | No       | —                                                             | Final approver (workflow-set)            |
| 8   | ApprovedDate   | Date and Time          | No       | —                                                             | Sign-off timestamp                       |
| 9   | Comments       | Multiple lines of text | No       | —                                                             | Reviewer remarks                         |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                                               | DEC-004 environment tier                 |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| EARF_List | Search and filter EARF records | All FIN roles |
| EARF_New | Create new annual review | `D04-FIN-Submitters` |
| EARF_View | Read-only detail view | All authorized users |
| EARF_Edit | Edit in Draft/Returned state | Manager and reviewers |

### Screen Interaction Details

**EARF_List Screen**
- Gallery displaying all `EARF` records from `MainDB_FIN`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `EARF_New` (visible to Initiator role only).
- Tap a row to navigate to `EARF_View`.

**EARF_New / _Edit Screen**
- Data entry form bound to `MainDB_FIN`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**EARF_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "EARF-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(EARF_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(EARF_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "EARF",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(EARF_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "EARF" &&
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
- **Stage 1:** `Create & submit EARF` — performed by `Item created (FormCode=EARF)`
- **Stage 2:** `Department head review` — performed by `Status=Submitted`
- **Stage 3:** `HR/Finance sign-off` — performed by `Status=Pending Review`
- **Stage 4:** `Close workflow` — performed by `Final decision reached`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Manager / Submitter | Contribute |
| Department Head / Reviewer | Contribute |
| HR/Finance Signatory | Approve |
| System Admin | Full Control |

### 3. Data Integrity Rules

- `FormCode` must always equal `EARF` (system-enforced constant).
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

| Flow Name          | Trigger                      | Actions                                                                                                                                     |
| ------------------ | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_EARF_Submit`  | Item created (FormCode=EARF) | 1. Validate required fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify department head. 5. Set CurrentAction=Review. |
| `FIN_EARF_SignOff` | Status updated to Approved   | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Signed Off; CurrentAction=Closed. 3. Notify manager. 4. Lock record.                       |
| `FIN_EARF_Return`  | Status updated to Rejected   | 1. Set Status=Returned; CurrentAction=Draft. 2. Append return reason to Comments. 3. Route back to manager for revision.                    |

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
- [ ] Canvas App screens (`EARF_List`, `EARF_New`, `EARF_View`, `EARF_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
