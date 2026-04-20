# User Story — Notes ID Request (`NIR`)

> **Department:** IT (Department_06)  
> **Module:** M1 — User & Access Management  
> **Site(s):** PRAI (primary)  
> **SharePoint List:** `MainDB_IT (Department_06)`  
> **Form Code:** `NIR`

---

## 1. App Overview & Purpose

`NIR` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `IT (Department_06)` department at the PRAI (primary) site.

---

## 2. User Stories

**US-01: Request Submission**
> As a **New item created in `MainDB_IT`** (member of `Requestor (employee/HOD representative)`),  
> I want to **request submission** in the `NIR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* D06-IT-Initiators

**US-02: HOD Approval**
> As a **`CurrentAction` = RequestSubmitted; Item waiting for HOD review** (member of `HOD (per HODApprover column)`),  
> I want to **hod approval** in the `NIR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* D06-IT-HOD

**US-03: Notes Admin Provisioning**
> As a **`CurrentAction` = HODApproved; Item assigned to Notes admin** (member of `Notes Administrator`),  
> I want to **notes admin provisioning** in the `NIR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* D06-IT-Editors-L1

**US-04: IT Hardware Completion**
> As a **`CurrentAction` = NotesAdminCompleted; Item awaiting hardware setup** (member of `IT Hardware/Support owner`),  
> I want to **it hardware completion** in the `NIR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* D06-IT-Editors-L2

**US-05: Closed**
> As a **`CurrentAction` = Closed; No further action required** (member of `System (read-only)`),  
> I want to **closed** in the `NIR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* D06-IT-Readers

**US-LIST: Search and filter Notes ID Request records**
> As an **authorized user**,  
> I want to search, filter, and view Notes ID Request records in the list screen,  
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

**Target List:** `MainDB_IT (Department_06)`

| #   | Domino Field | SP Column Name                          | SP Type                | Required | Choices / Source                                                         | Notes (Source)                                                                                     |
| --- | ------------ | --------------------------------------- | ---------------------- | -------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| 1   | EmailType    | EmailType                               | Choice                 | Yes      | New Email; Replacement                                                   | Request type [USER-ENTERED]                                                                        |
| 2   | Company      | Company                                 | Choice                 | Yes      | IOI Oleochemical; IOI Acidchem                                           | Company selector [USER-ENTERED]                                                                    |
| 3   | Emailid      | ExistingEmailAddress                    | Single line of text    | No       | —                                                                        | Existing address for replacement [USER-ENTERED]                                                    |
| 4   | FullName     | FullName                                | Single line of text    | Yes      | —                                                                        | User full name [USER-ENTERED]                                                                      |
| 5   | EmpNo        | EmployeeNumber                          | Single line of text    | Yes      | —                                                                        | Employee ID [USER-ENTERED]                                                                         |
| 6   | Department   | Department                              | Choice                 | Yes      | _lookup to Department list_                                              | Requestor department [USER-ENTERED]                                                                |
| 7   | Designation  | Designation                             | Single line of text    | No       | —                                                                        | Job title [USER-ENTERED]                                                                           |
| 8   | Extension    | PhoneExtension                          | Single line of text    | No       | —                                                                        | Contact extension [USER-ENTERED]                                                                   |
| 9   | Type         | `[IN-PROGRESS: See CLARIFY note below]` | `PENDING`              | No       | —                                                                        | Secondary classification. **[CLARIFY: Verify if "Type" differs from "EmailType" or is redundant]** |
| 10  | HOD          | HODApprover                             | Person or Group        | Yes      | _D06-IT-Initiators (submitter populates)_                                | Head-of-Department approver [USER-ENTERED]                                                         |
| 11  | Remark       | Remarks                                 | Multiple lines of text | No       | —                                                                        | Business note, replacement details [USER-ENTERED]                                                  |
| 12  | Requestor    | Requestor                               | Person or Group        | No       | _Computed: User.FullName_                                                | Request initiator [SYSTEM-COMPUTED]                                                                |
| 13  | DateSent     | SubmittedDate                           | Date and Time          | No       | _Computed: NOW()_                                                        | Submission timestamp [SYSTEM-COMPUTED]                                                             |
| 14  | HODName      | HODName                                 | Person or Group        | No       | —                                                                        | Recorded HOD approver [WORKFLOW-MANAGED]                                                           |
| 15  | HodDate      | HODApprovalDate                         | Date and Time          | No       | —                                                                        | HOD decision timestamp [SYSTEM-COMPUTED]                                                           |
| 16  | HodStatus    | HODApprovalStatus                       | Choice                 | No       | Pending; Approved; Rejected                                              | HOD decision state [WORKFLOW-MANAGED]                                                              |
| 17  | HodComment   | HODComment                              | Multiple lines of text | No       | —                                                                        | HOD remarks [USER-ENTERED]                                                                         |
| 18  | PICName      | NotesAdministrator                      | Person or Group        | No       | _D06-IT-Editors-L1_                                                      | Notes admin handling provisioning [WORKFLOW-MANAGED]                                               |
| 19  | PICDate      | NotesAdminDate                          | Date and Time          | No       | —                                                                        | Notes admin action timestamp [SYSTEM-COMPUTED]                                                     |
| 20  | PICTask      | NotesAdminTask                          | Multiple lines of text | No       | —                                                                        | Provisioning task detail [USER-ENTERED]                                                            |
| 21  | ID           | InternalNotesID                         | Single line of text    | No       | —                                                                        | Internal Notes ID produced [WORKFLOW-MANAGED]                                                      |
| 22  | ID2          | ExternalNotesID                         | Single line of text    | No       | —                                                                        | External Notes ID or routing value [WORKFLOW-MANAGED]                                              |
| 23  | PICRemark    | NotesAdminRemark                        | Multiple lines of text | No       | —                                                                        | Notes admin remarks [USER-ENTERED]                                                                 |
| 24  | AccName      | ITHardwareOwner                         | Person or Group        | No       | _D06-IT-Editors-L2_                                                      | IT hardware/support actor [WORKFLOW-MANAGED]                                                       |
| 25  | AccDate      | ITHardwareDate                          | Date and Time          | No       | —                                                                        | IT hardware action timestamp [SYSTEM-COMPUTED]                                                     |
| 26  | AccTask      | ITHardwareTask                          | Multiple lines of text | No       | —                                                                        | Hardware or downstream IT task [USER-ENTERED]                                                      |
| 27  | AccStatus    | ITHardwareStatus                        | Choice                 | No       | Pending; In Progress; Completed                                          | Downstream IT completion status [WORKFLOW-MANAGED]                                                 |
| 28  | AccComment   | ITHardwareComment                       | Multiple lines of text | No       | —                                                                        | Hardware/support remarks [USER-ENTERED]                                                            |
| 29  | CA           | CurrentAction                           | Choice                 | No       | RequestSubmitted; HODPending; NotesAdminPending; HardwarePending; Closed | Hidden workflow state [WORKFLOW-MANAGED]                                                           |
| 30  | ITHOD        | ITHODRoutingField                       | Person or Group        | No       | —                                                                        | Hidden IT HOD routing field [WORKFLOW-MANAGED]                                                     |


| Domino Hidden Field | Purpose                  | Power Automate Replacement                                                     |
| ------------------- | ------------------------ | ------------------------------------------------------------------------------ |
| PIC                 | Notes PIC routing hint   | Lookup in IT routing matrix → populate `NotesAdministrator` column             |
| ISG                 | ISG team assignment      | Lookup in IT routing matrix → populate `ITTeamAssigned` column                 |
| HW                  | Penang hardware routing  | Lookup in Penang IT support routing → populate `ITHardwareOwner` (Penang)      |
| HW2                 | Johor hardware routing   | Lookup in Johor IT support routing → populate `ITHardwareOwner` (Johor)        |
| SW                  | Software team assignment | Evaluate in routing logic; cascade to `ITTeamAssigned`                         |
| HRE                 | HR Executive routing     | Conditional: if HR approvals needed, route to HR-Exec group                    |
| HRNE                | HR Non-Executive routing | Conditional: if HR approvals needed, route to HR-NonExec group                 |
| HR                  | HR general assignment    | Conditional: fallback HR team assignment                                       |
| ITHOD               | IT HOD routing field     | Lookup in IT management matrix → populate `HODApprover` or `ITHODRoutingField` |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `NIR_List` | Browse and search all NIR records | All authorized users |
| `NIR_New` | Create a new Notes ID Request request | Initiator / Requestor |
| `NIR_View` | Read-only detail view of a record | All authorized users |
| `NIR_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `NIR_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**NIR_List Screen**
- Gallery displaying all `NIR` records from `MainDB_IT (Department_06)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `NIR_New` (visible to Initiator role only).
- Tap a row to navigate to `NIR_View`.

**NIR_New / _Edit Screen**
- Data entry form bound to `MainDB_IT (Department_06)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**NIR_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "NIR-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(NIR_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(NIR_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "NIR",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(NIR_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "NIR" &&
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
- **Stage 1:** `Request Submission` — performed by `New item created in `MainDB_IT``
- **Stage 2:** `HOD Approval` — performed by ``CurrentAction` = RequestSubmitted; Item waiting for HOD review`
- **Stage 3:** `Notes Admin Provisioning` — performed by ``CurrentAction` = HODApproved; Item assigned to Notes admin`
- **Stage 4:** `IT Hardware Completion` — performed by ``CurrentAction` = NotesAdminCompleted; Item awaiting hardware setup`
- **Stage 5:** `Closed` — performed by ``CurrentAction` = Closed; No further action required`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|

### 3. Data Integrity Rules

- `FormCode` must always equal `NIR` (system-enforced constant).
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

| Step | Logic                    | Action                                                                        | Target                                                     |
| ---- | ------------------------ | ----------------------------------------------------------------------------- | ---------------------------------------------------------- |
| 1    | Validate required fields | Check: `EmailType`, `Company`, `FullName`, `EmpNo`, `HODApprover` all present | Fail → send validation error email to requestor; stop flow |
| 2    | Populate computed fields | Set `Requestor` = CurrentUser. Set `SubmittedDate` = NOW().                   | Update item                                                |
| 3    | Route to HOD             | Lookup `HODApprover` person record → resolve email                            | Send email with approval link                              |
| 4    | Set initial state        | Set `CurrentAction` = 'RequestSubmitted'; `HODApprovalStatus` = 'Pending'     | Update item                                                |
| 5    | Tag environment          | Set `EnvironmentTag` from `Config_AppSettings` (based on site URL)            | Update item (DEC-004)                                      |

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

- [ ] All SharePoint columns in `MainDB_IT (Department_06)` are created with correct types and required flags.
- [ ] Canvas App screens (`NIR_List`, `NIR_New`, `NIR_View`, `NIR_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
