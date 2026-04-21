# User Story — Cafeteria Inspection Database (`CIR`)

> **Department:** HR (Department_05)  
> **Module:** M1 — General Administration & Facilities  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_HR (Department_05)`  
> **Form Code:** `CIR`

---

## 1. App Overview & Purpose

`CIR` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `HR (Department_05)` department at the PRAI site.

---

## 2. User Stories

**US-LIST: Search and filter Cafeteria Inspection Database records**
> As an **authorized user**,  
> I want to search, filter, and view Cafeteria Inspection Database records in the list screen,  
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

**Target List:** `MainDB_HR (Department_05)`

| #   | Column Name    | SP Type                 | Required | Choices / Source                                | Notes                                                                                                |
| --- | -------------- | ----------------------- | -------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1   | Title          | Single line of text     | Yes      | —                                               | Auto-populated: `"CIR-" & INO`; used as record display name                                          |
| 2   | INO            | Single line of text     | Yes      | —                                               | System-computed via Power Automate (format: `HR-CIR-YYMM-NNNN`); **PATTERN-E** — never set in canvas |
| 3   | Site           | Choice                  | Yes      | PRAI; Johor                                     | Cafeteria site location (Domino: Site)                                                               |
| 4   | InspectionDate | Date and Time           | Yes      | —                                               | Date of cafeteria inspection (Domino: InsDate)                                                       |
| 5   | InspectionTime | Single line of text     | No       | —                                               | Time of inspection (Domino: InsTime; stored as text HH:MM)                                           |
| 6   | Inspector      | Person or Group         | Yes      | —                                               | Primary inspector (Domino: Inspector)                                                                |
| 7   | TeamMembers    | Person or Group (multi) | No       | —                                               | Additional inspection team members (Domino: TeamMembers)                                             |
| 8   | SubmittedBy    | Person or Group         | Yes      | —                                               | Record initiator (Domino: SubmittedBy; auto-populated from logged-in user)                           |
| 9   | SubmittedDate  | Date and Time           | Yes      | —                                               | Submission timestamp (Domino: SubmittedDate; PA-set on submit)                                       |
| 10  | ReviewedBy     | Person or Group         | No       | —                                               | Corrective action reviewer (Domino: ReviewedBy; set during review stage)                             |
| 11  | ReviewedDate   | Date and Time           | No       | —                                               | Date review was completed (Domino: ReviewedDate; PA-set on review submit)                            |
| 12  | Remarks        | Multiple lines of text  | No       | —                                               | Corrective action review remarks (Domino: Remarks)                                                   |
| 13  | ACMCommittee   | Person or Group (multi) | No       | —                                               | ACM committee members for this inspection (Domino: ACMComm)                                          |
| 14  | ECMCommittee   | Person or Group (multi) | No       | —                                               | ECM committee members for this inspection (Domino: ECMComm)                                          |
| 15  | ITNotify       | Person or Group         | No       | —                                               | IT notification recipient (Domino: IT; for system-related issues flagged during inspection)          |
| 16  | CurrentStatus  | Choice                  | Yes      | Draft; Submitted; UnderReview; Reviewed; Closed | Master workflow status (PA-managed; sourced from Domino CurrentAction)                               |
| 17  | CurrentAction  | Choice                  | Yes      | Create; Submit; Review; Close                   | Active workflow action (PA-managed; sourced from Domino CurrentAction hidden field)                  |
| 18  | Editors        | Person or Group (multi) | No       | —                                               | Access control — editors group (Domino: Editors; Editor1; Editor2)                                   |
| 19  | EnvironmentTag | Choice                  | No       | DEV; TEST; PROD                                 | Three-tier environment strategy (DEC-004)                                                            |
| 20  | InitiatorEmail | Person or Group         | No       | —                                               | Requestor identity for audit trail (PA-set from Office 365 login)                                    |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| CIR_List | Gallery list of all cafeteria inspection records | Gallery, search by site/date, filter by status |
| CIR_New | New inspection data entry | Edit form: Site, InspectionDate, InspectionTime, Inspector, TeamMembers, ACMComm, ECMComm |
| CIR_View | Read-only record detail | Display form with all fields, status banner, timeline |
| CIR_Edit | Edit/review stage | Conditional fields: Remarks, ReviewedBy (only visible in Review stage) |

### Screen Interaction Details

**CIR_List Screen**
- Gallery displaying all `CIR` records from `MainDB_HR (Department_05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `CIR_New` (visible to Initiator role only).
- Tap a row to navigate to `CIR_View`.

**CIR_New / _Edit Screen**
- Data entry form bound to `MainDB_HR (Department_05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**CIR_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "CIR-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(CIR_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(CIR_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "CIR",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(CIR_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "CIR" &&
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

### 3. Data Integrity Rules

- `FormCode` must always equal `CIR` (system-enforced constant).
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

| Flow          | Trigger                                                    | Actions                                                                                         |
| ------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| CIR_OnSubmit  | Item created in MainDB_HR with CurrentAction = Submit      | Set INO (HR-CIR-YYMM-NNNN), set SubmittedDate, set CurrentStatus = Submitted, notify ReviewedBy |
| CIR_OnReview  | Item updated with CurrentAction = Review                   | Set ReviewedDate, set CurrentStatus = Reviewed, notify Initiator, notify ACMComm/ECMComm        |
| CIR_AutoClose | Scheduled — 7 days after ReviewedDate if no further action | Set CurrentStatus = Closed                                                                      |

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

- [ ] All SharePoint columns in `MainDB_HR (Department_05)` are created with correct types and required flags.
- [ ] Canvas App screens (`CIR_List`, `CIR_New`, `CIR_View`, `CIR_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
