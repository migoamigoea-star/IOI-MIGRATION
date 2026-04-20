# User Story — Night Duty Manager's Findings (`NDF`)

> **Department:** HR  
> **Module:** Operations — Night Duty Reporting  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "NDF"`  
> **Form Code:** `NDF`

---

## 1. App Overview & Purpose

NDF records structured findings made by the Night Duty Manager during plant inspection rounds. Each
report captures the inspection team composition, date, time, and up to 10 individual findings, each
assigned to a responsible department and PIC with a category and acknowledgement status. Findings
are distributed to named recipients for follow-up. The migrated solution must preserve the multi-row
findings structure via a child table and maintain the original distributon trail.

---

---

## 2. User Stories

**US-01: Create Draft**
> As a **Night Duty Manager** (member of `D05-HR-Staff`),  
> I want to **create draft** in the `NDF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created — NDF record initialised

**US-02: Submit**
> As a **Night Duty Manager** (member of `D05-HR-Staff`),  
> I want to **submit** in the `NDF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Draft' and manager submits

**US-03: Distribute**
> As a **System** (member of `—`),  
> I want to **distribute** in the `NDF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Submitted' → PA sends to SendTo addresses, sets IsLocked=Yes

**US-LIST: Search and filter Night Duty Manager's Findings records**
> As an **authorized user**,  
> I want to search, filter, and view Night Duty Manager's Findings records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "NDF"`

| #   | SP Internal Name | Display Label           | Column Type         | Required | Classification   | Source Mapping / Notes                                  |
| --- | ---------------- | ----------------------- | ------------------- | -------- | ---------------- | ------------------------------------------------------- |
| 1   | Title            | Title                   | Single line text    | Yes      | SYSTEM-COMPUTED  | NDF prefix + INNumber                                   |
| 2   | FormCode         | Form Code               | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value NDF                                         |
| 3   | INNumber         | IN Number               | Single line text    | No       | SYSTEM-COMPUTED  | `txtINNumberC` — auto-generated                         |
| 4   | TeamMembers      | Inspection Team Members | Multiple lines text | Yes      | USER-ENTERED     | `TeamMembers`                                           |
| 5   | DateVisit        | Inspection Date         | Date and Time       | Yes      | USER-ENTERED     | `DateVisit`                                             |
| 6   | InspectionTime   | Inspection Time         | Single line text    | Yes      | USER-ENTERED     | `Time`                                                  |
| 7   | SendTo           | Send To                 | Multiple lines text | No       | USER-ENTERED     | `SendTo` — distribution list (email addresses or names) |
| 8   | CurrentStatus    | Current Status          | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, Distributed                           |
| 9   | WorkflowStage    | Workflow Stage          | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=Distributed                       |
| 10  | EnvironmentTag   | Environment             | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                         |
| 11  | IsLocked         | Is Locked               | Yes/No              | No       | WORKFLOW-MANAGED | True after distribution                                 |


| #   | SP Internal Name | Display Label       | Column Type         | Required | Notes                                                        |
| --- | ---------------- | ------------------- | ------------------- | -------- | ------------------------------------------------------------ |
| 1   | NDFRef           | NDF Reference       | Lookup (MainDB_HR)  | Yes      | Links to parent NDF record                                   |
| 2   | FindingSeq       | Finding No          | Number              | Yes      | Sequence 1–10; order within report                           |
| 3   | Description      | Finding Description | Multiple lines text | Yes      | `Desc` — what was observed                                   |
| 4   | Department       | Department          | Single line text    | Yes      | `Dept` — responsible department                              |
| 5   | PIC              | Person in Charge    | Single line text    | Yes      | `PIC`                                                        |
| 6   | Category         | Category            | Choice              | Yes      | `Category` — Safety, Housekeeping, Equipment, Process, Other |
| 7   | Acknowledged     | Acknowledged        | Yes/No              | No       | `Att` — acknowledgement flag                                 |
| 8   | FindingRemarks   | Remarks             | Multiple lines text | No       | Review feedback on this finding                              |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| NDF_List | Gallery | List all NDF reports with date and status filter |
| NDF_New | Form | New NDF: header fields + editable findings child gallery |
| NDF_View | Read-only | View full NDF report with all findings rows |
| NDF_Edit | Form | Edit draft NDF (header + findings) |

### Screen Interaction Details

**NDF_List Screen**
- Gallery displaying all `NDF` records from `MainDB_HR **Form Discriminator:** FormCode = "NDF"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `NDF_New` (visible to Initiator role only).
- Tap a row to navigate to `NDF_View`.

**NDF_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "NDF"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**NDF_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "NDF-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(NDF_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(NDF_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "NDF",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(NDF_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "NDF" &&
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
- **Stage 1:** `Create Draft` — performed by `Night Duty Manager`
- **Stage 2:** `Submit` — performed by `Night Duty Manager`
- **Stage 3:** `Distribute` — performed by `System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Night Duty Managers | D05-HR-Staff |
| HR Manager | D05-HR-Manager |

### 3. Data Integrity Rules

- `FormCode` must always equal `NDF` (system-enforced constant).
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

| Flow Name         | Trigger                              | Action                                                                          |
| ----------------- | ------------------------------------ | ------------------------------------------------------------------------------- |
| HR_NDF_OnSubmit   | When Status='Draft' → item submitted | Generate INNumber, stamp date, set Stage=2, trigger distribution                |
| HR_NDF_Distribute | When Status='Submitted'              | Email SendTo list with NDF summary; set CurrentStatus=Distributed, IsLocked=Yes |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "NDF"` are created with correct types and required flags.
- [ ] Canvas App screens (`NDF_List`, `NDF_New`, `NDF_View`, `NDF_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
