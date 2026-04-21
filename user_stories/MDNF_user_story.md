# User Story — Material Disposal Notification Form (`MDNF`)

> **Department:** STR (Department_13_STR)  
> **Module:** M2 - Material Disposal  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_STR`  
> **Form Code:** `MDNF`

---

## 1. App Overview & Purpose

MDNF governs end-to-end material disposal from request initiation through procurement, collection,
finance completion, and controlled withdrawal closure. The migration preserves attributable
approvals, evidence capture, and auditable state transitions for disposal actions that affect
inventory and financial traceability.

---

## 2. User Stories

**US-01: Create and submit disposal request**
> As a **Requestor** (member of `D13-STR-Users`),  
> I want to **create and submit disposal request** in the `MDNF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Item created with `FormCode=MDNF`

**US-02: Review and approve/reject request**
> As a **HOD/Division Reviewer** (member of `D13-STR-Reviewers`),  
> I want to **review and approve/reject request** in the `MDNF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CurrentAction=Review`

**US-03: Record procurement and buyer processing**
> As a **Procurement** (member of `D13-STR-Procurement`),  
> I want to **record procurement and buyer processing** in the `MDNF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CurrentStatus=Procurement`

**US-04: Confirm disposal collection evidence**
> As a **Store/Collection** (member of `D13-STR-StoreOps`),  
> I want to **confirm disposal collection evidence** in the `MDNF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CollectionDate` updated

**US-05: Complete finance closure**
> As a **Finance** (member of `D13-STR-Finance`),  
> I want to **complete finance closure** in the `MDNF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `FinanceStatus=Completed`

**US-LIST: Search and filter Material Disposal Notification Form records**
> As an **authorized user**,  
> I want to search, filter, and view Material Disposal Notification Form records in the list screen,  
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

**Target List:** `MainDB_STR`

| #   | SP Internal Name     | Display Label          | Column Type     | Required | Classification   | Notes                                                                 |
| --- | -------------------- | ---------------------- | --------------- | -------- | ---------------- | --------------------------------------------------------------------- |
| 1   | FormCode             | Form Code              | Single line     | Yes      | SYSTEM-COMPUTED  | Fixed `MDNF`                                                          |
| 2   | INO                  | Disposal Ref No        | Single line     | Yes      | SYSTEM-COMPUTED  | Format `STR-MDNF-YYMM-NNNN` via flow                                  |
| 3   | CurrentStatus        | Workflow Status        | Choice          | Yes      | WORKFLOW-MANAGED | Draft, Submitted, Procurement, Collection, Finance, Closed, Withdrawn |
| 4   | CurrentAction        | Current Action         | Choice          | Yes      | WORKFLOW-MANAGED | Submit, Review, Approve, Complete, Withdraw                           |
| 5   | RequestDate          | Request Date           | Date and Time   | Yes      | USER-ENTERED     | Disposal request date                                                 |
| 6   | Requestor            | Requestor              | Person or Group | Yes      | USER-ENTERED     | Disposal initiator                                                    |
| 7   | RequestDept          | Requesting Department  | Single line     | Yes      | USER-ENTERED     | Origin department                                                     |
| 8   | ItemDescription      | Item Description       | Multiple lines  | Yes      | USER-ENTERED     | Material/item being disposed                                          |
| 9   | QtyToDispose         | Quantity to Dispose    | Number          | Yes      | USER-ENTERED     | Disposal quantity                                                     |
| 10  | DisposalReason       | Disposal Reason        | Multiple lines  | Yes      | USER-ENTERED     | Reason/justification                                                  |
| 11  | ProcurementAction    | Procurement Action     | Multiple lines  | No       | WORKFLOW-MANAGED | Buyer/procurement details                                             |
| 12  | CollectionDate       | Collection Date        | Date and Time   | No       | WORKFLOW-MANAGED | Disposal collection evidence                                          |
| 13  | FinanceStatus        | Finance Status         | Choice          | No       | WORKFLOW-MANAGED | Pending, Completed                                                    |
| 14  | FinanceCompletedDate | Finance Completed Date | Date and Time   | No       | WORKFLOW-MANAGED | Finance closure timestamp                                             |
| 15  | WithdrawalFlag       | Withdrawal Flag        | Yes/No          | No       | WORKFLOW-MANAGED | Indicates withdrawn request                                           |
| 16  | WithdrawalReason     | Withdrawal Reason      | Multiple lines  | No       | USER-ENTERED     | Mandatory when withdrawn                                              |
| 17  | SubmittedBy          | Submitted By           | Person or Group | Yes      | SYSTEM-COMPUTED  | Captured on submit                                                    |
| 18  | SubmittedDate        | Submitted Date         | Date and Time   | Yes      | SYSTEM-COMPUTED  | Captured on submit                                                    |
| 19  | ApprovedBy           | Approved By            | Person or Group | No       | WORKFLOW-MANAGED | Final approver actor                                                  |
| 20  | ApprovedDate         | Approved Date          | Date and Time   | No       | WORKFLOW-MANAGED | Final approval timestamp                                              |
| 21  | EnvironmentTag       | Environment            | Choice          | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                       |
| 22  | IsLocked             | Is Locked              | Yes/No          | No       | WORKFLOW-MANAGED | Set Yes at closure                                                    |

---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| MDNF_List | Filter/search disposal requests | STR users, reviewers, finance |
| MDNF_New | New disposal request entry | STR users |
| MDNF_View | Read-only record and audit trail | All authorized users |
| MDNF_Edit | Draft/returned edit screen | Requestor |
| MDNF_Review | Review and decision screen | Reviewers |
| MDNF_Closure | Finance closure and finalization | Finance |

### Screen Interaction Details

**MDNF_List Screen**
- Gallery displaying all `MDNF` records from `MainDB_STR`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `MDNF_New` (visible to Initiator role only).
- Tap a row to navigate to `MDNF_View`.

**MDNF_New / _Edit Screen**
- Data entry form bound to `MainDB_STR`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**MDNF_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "MDNF-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(MDNF_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(MDNF_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "MDNF",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(MDNF_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "MDNF" &&
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
- **Stage 1:** `Create and submit disposal request` — performed by `Requestor`
- **Stage 2:** `Review and approve/reject request` — performed by `HOD/Division Reviewer`
- **Stage 3:** `Record procurement and buyer processing` — performed by `Procurement`
- **Stage 4:** `Confirm disposal collection evidence` — performed by `Store/Collection`
- **Stage 5:** `Complete finance closure` — performed by `Finance`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Requestor | Contribute |
| Reviewer (HOD/Division) | Contribute |
| Procurement Processor | Contribute |
| Finance Completer | Contribute |
| Admin | Full Control |
| Reader | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `MDNF` (system-enforced constant).
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

| Stage       | Flow Name                    | Trigger                           | Actions                                                                                    |
| ----------- | ---------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------ |
| Submit      | STR_MDNF_OnSubmit            | Item created with `FormCode=MDNF` | Generate INO, set SubmittedBy/SubmittedDate, set CurrentStatus=Submitted, notify reviewers |
| Approve     | STR_MDNF_OnReviewDecision    | Reviewer action recorded          | Set approval decision, route to Procurement or Rejected state, persist remarks             |
| Procurement | STR_MDNF_OnProcurementUpdate | `CurrentStatus=Procurement`       | Persist procurement details, notify collection owner                                       |
| Collection  | STR_MDNF_OnCollection        | `CollectionDate` populated        | Capture collection completion and notify Finance                                           |
| Close       | STR_MDNF_OnFinanceComplete   | `FinanceStatus=Completed`         | Set CurrentStatus=Closed, stamp closure, set IsLocked=Yes                                  |
| Withdraw    | STR_MDNF_OnWithdraw          | `WithdrawalFlag=true`             | Require reason, set CurrentStatus=Withdrawn, notify stakeholders                           |

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

- [ ] All SharePoint columns in `MainDB_STR` are created with correct types and required flags.
- [ ] Canvas App screens (`MDNF_List`, `MDNF_New`, `MDNF_View`, `MDNF_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
