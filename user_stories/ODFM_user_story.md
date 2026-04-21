# User Story — One-Off Deviation From Min/Max (`ODFM`)

> **Department:** STR  
> **Module:** M6 - Deviation & Safety Items  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_STR`  
> **Form Code:** `ODFM`

---

## 1. App Overview & Purpose

ODFM is migrated as a STR workflow form in MainDB_STR with FormCode=ODFM. The implementation
preserves submission, review/approval routing, auditability, and notification behavior for PRAI
operations.

---

## 2. User Stories

**US-01: Create and submit form**
> As a **Requestor** (member of `D20-STR-Users`),  
> I want to **create and submit form** in the `ODFM` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created with FormCode=ODFM

**US-02: Review submission and request revision if needed**
> As a **Reviewer** (member of `D20-STR-Reviewers`),  
> I want to **review submission and request revision if needed** in the `ODFM` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentAction=Review

**US-03: Approve/reject and finalize workflow**
> As a **Approver** (member of `D20-STR-Managers`),  
> I want to **approve/reject and finalize workflow** in the `ODFM` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When review decision recorded

**US-LIST: Search and filter One-Off Deviation From Min/Max records**
> As an **authorized user**,  
> I want to search, filter, and view One-Off Deviation From Min/Max records in the list screen,  
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

| Column Name    | SP Type                | Required | Notes                                                  |
| -------------- | ---------------------- | -------- | ------------------------------------------------------ |
| Title          | Single line of text    | Yes      | Display identifier                                     |
| FormCode       | Single line of text    | Yes      | Constant `ODFM`                                        |
| CurrentAction  | Choice                 | Yes      | Draft, Review, Approve, Return, Close                  |
| Status         | Choice                 | Yes      | Draft, Submitted, Approved, Rejected, Returned, Closed |
| SubmittedBy    | Person or Group        | Yes      | Submission audit                                       |
| SubmittedDate  | Date and Time          | Yes      | Submission timestamp                                   |
| ApprovedBy     | Person or Group        | No       | Final approver                                         |
| ApprovedDate   | Date and Time          | No       | Approval timestamp                                     |
| Comments       | Multiple lines of text | No       | Reviewer remarks                                       |
| EnvironmentTag | Choice                 | Yes      | DEV, TEST, PROD                                        |

---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| ODFM_List | Search and filter ODFM records | STR readers, reviewers, approvers |
| ODFM_New | Create new ODFM request | STR requestors |
| ODFM_View | Read-only detail view | All authorized users |
| ODFM_Edit | Edit in draft/returned state | Requestor and reviewers |

### Screen Interaction Details

**ODFM_List Screen**
- Gallery displaying all `ODFM` records from `MainDB_STR`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ODFM_New` (visible to Initiator role only).
- Tap a row to navigate to `ODFM_View`.

**ODFM_New / _Edit Screen**
- Data entry form bound to `MainDB_STR`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ODFM_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ODFM-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(CurrentAction) Or
    IsBlank(Status) Or
    IsBlank(SubmittedBy) Or
    IsBlank(SubmittedDate),
    DisplayMode.Disabled,
    DisplayMode.Edit
)
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
Navigate(ODFM_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ODFM_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ODFM",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ODFM_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ODFM" &&
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
- **Stage 1:** `Create and submit form` — performed by `Requestor`
- **Stage 2:** `Review submission and request revision if needed` — performed by `Reviewer`
- **Stage 3:** `Approve/reject and finalize workflow` — performed by `Approver`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Requestor | Contribute |
| Reviewer | Contribute |
| Approver | Approve |
| Admin | Full Control |
| Reader | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `ODFM` (system-enforced constant).
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

| Stage   | Flow Name        | Trigger                      | Actions                                                                  |
| ------- | ---------------- | ---------------------------- | ------------------------------------------------------------------------ |
| Submit  | STR_ODFM_Submit  | Item created (FormCode=ODFM) | Set Submitted status, stamp SubmittedBy/SubmittedDate, notify reviewers  |
| Review  | STR_ODFM_Review  | CurrentAction=Review         | Route for decision, persist reviewer comments, handle return/reject path |
| Approve | STR_ODFM_Approve | Reviewer decision=Approve    | Set Approved status, stamp ApprovedBy/ApprovedDate, notify stakeholders  |
| Close   | STR_ODFM_Close   | Final state reached          | Lock record and finalize notifications                                   |

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
- [ ] Canvas App screens (`ODFM_List`, `ODFM_New`, `ODFM_View`, `ODFM_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
