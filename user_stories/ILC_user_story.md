# User Story — Ilc (`ILC`)

> **Department:** SA  
> **Module:** Johor Migration Wave  
> **Site(s):** JOHOR  
> **SharePoint List:** `MainDB_SA`  
> **Form Code:** `ILC`

---

## 1. App Overview & Purpose

This blueprint defines the migration baseline for Ilc from Johor site source forms into
Microsoft 365. The target implementation will use Power Apps canvas screens and SharePoint
list-backed storage with environment-safe automation flow controls.

---

---

## 2. User Stories

**US-01: Draft entry**
> As a **Initiator** (member of `SA-Initiators`),  
> I want to **draft entry** in the `ILC` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Record created in app draft state

**US-02: Submit**
> As a **Initiator** (member of `SA-Initiators`),  
> I want to **submit** in the `ILC` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* CurrentStatus set to Submitted

**US-03: Review**
> As a **Department reviewer** (member of `SA-Reviewers`),  
> I want to **review** in the `ILC` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* CurrentStatus is Submitted

**US-04: Final decision**
> As a **Department approver** (member of `SA-Approvers`),  
> I want to **final decision** in the `ILC` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Decision action updates final status

**US-LIST: Search and filter Ilc records**
> As an **authorized user**,  
> I want to search, filter, and view Ilc records in the list screen,  
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

**Target List:** `MainDB_SA`

| #   | Column Name    | Type                | Required | Domino Mapping      | Notes                                        |
| --- | -------------- | ------------------- | -------- | ------------------- | -------------------------------------------- |
| 1   | Title          | Single line of text | Yes      | Document identifier | Primary title key                            |
| 2   | FormCode       | Single line of text | Yes      | Form code           | Fixed value ILC                              |
| 3   | CurrentStatus  | Choice              | Yes      | Workflow status     | Draft, Submitted, Approved, Rejected, Closed |
| 4   | DocAuthor      | Person or Group     | Yes      | Creator             | Submission owner                             |
| 5   | CDate          | Date and Time       | Yes      | Created date        | Submission timestamp                         |
| 6   | Modified       | Date and Time       | No       | Modified date       | Last update timestamp                        |
| 7   | UpdatedBy      | Person or Group     | No       | Modified by         | Last editor                                  |
| 8   | EnvironmentTag | Choice              | Yes      | Environment marker  | DEV, TEST, PROD                              |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| ILC_List | Record listing and search | All authenticated roles |
| ILC_New | New submission form | Initiators |
| ILC_View | Read-only details | All authenticated roles |
| ILC_Edit | Editable review form | Reviewers and approvers |

### Screen Interaction Details

**ILC_List Screen**
- Gallery displaying all `ILC` records from `MainDB_SA`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ILC_New` (visible to Initiator role only).
- Tap a row to navigate to `ILC_View`.

**ILC_New / _Edit Screen**
- Data entry form bound to `MainDB_SA`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ILC_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ILC-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(ILC_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ILC_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ILC",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ILC_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ILC" &&
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
- **Stage 1:** `Draft entry` — performed by `Initiator`
- **Stage 2:** `Submit` — performed by `Initiator`
- **Stage 3:** `Review` — performed by `Department reviewer`
- **Stage 4:** `Final decision` — performed by `Department approver`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Initiator | SA-Initiators |
| Reviewer | SA-Reviewers |
| Approver | SA-Approvers |
| Reader | SA-Readers |
| Admin | SA-Admins |

### 3. Data Integrity Rules

- `FormCode` must always equal `ILC` (system-enforced constant).
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

| Flow Name              | Trigger                  | Core Actions                                                 |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| SA_ILC_OnSubmit        | SharePoint item created  | Normalize fields, set FormCode, set CDate, notify reviewer   |
| SA_ILC_OnReview        | SharePoint item modified | Track review decision, append audit fields, notify approver  |
| SA_ILC_OnFinalDecision | SharePoint item modified | Apply final status and lock rules, send closure notification |

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

- [ ] All SharePoint columns in `MainDB_SA` are created with correct types and required flags.
- [ ] Canvas App screens (`ILC_List`, `ILC_New`, `ILC_View`, `ILC_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
