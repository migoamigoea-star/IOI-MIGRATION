# User Story — Data Restoration Request (`IAL5`)

> **Department:** IT  
> **Module:** M2 - IT Support & Service Requests  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `IAL5`

---

## 1. App Overview & Purpose

IAL5 manages IT data restoration requests across submission, assignment, backup-administrator
processing, and closure stages while preserving auditability for requested assets, restoration
outcomes, and stakeholder notifications.

### Governance Notes

- DEC-001 (live submissions): all new IAL5 submissions must write to `MainDB_IT` only. Any
  form-specific list such as `IT_IAL5_List` is historical import/staging only and must not receive
  live submissions.
- DEC-004 (environment strategy): environment-specific values (backup administrator routing
  defaults, manager distribution groups, reminder/escalation windows, sender profile) must be loaded
  from `Config_AppSettings` for `DEV`, `TEST`, and `PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is the sole authoritative
  source for column definitions and is available in this workspace for schema reconciliation.

---

---

## 2. User Stories

**US-01: Create and submit restoration request**
> As a **Requestor (`RequestedBy`)** (member of ``D06-IT-Initiators``),  
> I want to **create and submit restoration request** in the `IAL5` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created in `MainDB_IT` where `FormCode = IAL5`

**US-02: Assign and process restoration details**
> As a **Backup Administrator (`BackupAdminAssignee`)** (member of ``D06-IT-Editors-L1``),  
> I want to **assign and process restoration details** in the `IAL5` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `Status = Submitted` or `CurrentAction = Assigned`

**US-03: Validate completion data and notify stakeholders**
> As a **IT Admin / Routed editor (`ITAdminOwner` / `SectionIIEditor`)** (member of ``D06-IT-IT-Admin``),  
> I want to **validate completion data and notify stakeholders** in the `IAL5` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `RestorationStatus` transitions to terminal state

**US-04: Retain record and close workflow**
> As a **System + IT admin custodian** (member of ``D06-IT-Readers` (read) and `D06-IT-IT-Admin` (close)`),  
> I want to **retain record and close workflow** in the `IAL5` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `Status = Completed` and closure action executed

**US-LIST: Search and filter Data Restoration Request records**
> As an **authorized user**,  
> I want to search, filter, and view Data Restoration Request records in the list screen,  
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

**Target List:** `MainDB_IT`

| Column Name           | SP Type                 | Required | Choices / Source                                                    | Notes                                                            |
| --------------------- | ----------------------- | -------- | ------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Title                 | Single line of text     | Yes      | Auto-generated display ID                                           | Display identifier for IAL5 item                                 |
| FormCode              | Single line of text     | Yes      | Constant `IAL5`                                                     | Routing/filter key                                               |
| INONumber             | Number                  | Yes      | Flow-generated sequence                                             | Domino `INO`; PATTERN-E auto-number via Power Automate only      |
| Site                  | Choice                  | Yes      | Site master list                                                    | Domino `rbSite`                                                  |
| RequestedBy           | Person or Group         | Yes      | User directory                                                      | Domino `nmRequestedBy`                                           |
| Department            | Choice                  | Yes      | Department master list                                              | Domino `lstDept`                                                 |
| RequestMediaReference | Single line of text     | No       | User input                                                          | Domino `txtMedia`                                                |
| ServerName            | Choice                  | Yes      | Server master list                                                  | Domino `lstServerName`                                           |
| RestorePath           | Single line of text     | Yes      | User input                                                          | Domino `txtFilePath`                                             |
| RequestedFileOrFolder | Single line of text     | Yes      | User input                                                          | Domino `txtFileName`                                             |
| RequestReason         | Multiple lines of text  | Yes      | User input                                                          | Domino `txtReason`                                               |
| RequestAttachmentLink | Hyperlink or Picture    | No       | User/flow managed                                                   | Domino `rtxtAttach`; prefer native SharePoint attachment storage |
| CCInternal            | Person or Group (multi) | No       | User directory                                                      | Domino `nmCC`                                                    |
| SubmittedBy           | Person or Group         | Yes      | System/user context                                                 | Domino `nmSubmitted` and mandatory cross-form column             |
| SubmittedDate         | Date and Time           | Yes      | System timestamp                                                    | Domino `dtSubmitted` and mandatory cross-form column             |
| BackupMediaName       | Single line of text     | No       | Backup admin input                                                  | Domino `txtMediaName`                                            |
| BackupMediaDate       | Date and Time           | No       | Backup admin input                                                  | Domino `dtMediadate`                                             |
| RestoredFileName      | Single line of text     | No       | Backup admin input                                                  | Domino `txtFileName1`                                            |
| BackupAdminRemarks    | Multiple lines of text  | No       | Backup admin input                                                  | Domino `Remark`                                                  |
| RestorationStatus     | Choice                  | Yes      | Pending Assignment; In Progress; Completed; Failed; Returned        | Domino `rbStatus`                                                |
| PerformedBy           | Person or Group         | No       | User directory                                                      | Domino `nmPerformed`                                             |
| PerformedDate         | Date and Time           | No       | Flow stamp                                                          | Domino `dtPerformed`                                             |
| CreatorPerson         | Person or Group         | Yes      | System/user context                                                 | Domino `nmRequestor`                                             |
| CreatedOn             | Date and Time           | Yes      | System timestamp                                                    | Domino `dtCreatedOn`                                             |
| ITAdminOwner          | Person or Group         | No       | Config/routing matrix                                               | Domino `ISAdmin`                                                 |
| DisplayServerName     | Single line of text     | No       | Derived helper                                                      | Domino `dsSvrName`                                               |
| MailPenangMgr         | Person or Group (multi) | No       | Routing matrix by site                                              | Domino `MailP_Mgr`                                               |
| MailJohorMgr          | Person or Group (multi) | No       | Routing matrix by site                                              | Domino `MailJ_Mgr`                                               |
| CurrentAction         | Choice                  | Yes      | Draft; Submitted; Assigned; Processing; Completed; Returned; Closed | Domino `CurrentAction`                                           |
| SectionIEditor        | Person or Group         | No       | Workflow managed                                                    | Domino `AEditor1`                                                |
| BackupAdminAssignee   | Person or Group         | No       | Routing matrix                                                      | Domino `nmBKAdmin`                                               |
| SectionIIEditor       | Person or Group         | No       | Workflow managed                                                    | Domino `AEditor2`                                                |
| Status                | Choice                  | Yes      | Draft; Submitted; In Review; Completed; Rejected; Closed            | Workflow control status                                          |
| ApprovedBy            | Person or Group         | No       | Stage actor stamp                                                   | Stage 2/3 approval actor                                         |
| ApprovedDate          | Date and Time           | No       | Flow stamp                                                          | Stage 2/3 approval timestamp                                     |
| Comments              | Multiple lines of text  | No       | User/flow note                                                      | Workflow comments and return reasons                             |
| WorkflowAuditJson     | Multiple lines of text  | No       | Flow-generated JSON                                                 | Optional troubleshooting/audit trace                             |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `IAL5_List` | Search and track restoration requests | IT readers, editors, admins |
| `IAL5_New` | Submit restoration request | IT initiators |
| `IAL5_View` | Review request details and status history | Requestors, assignees, admins |
| `IAL5_Edit` | Process assignment, restoration details, and closure | Backup admins and IT admins |

### Screen Interaction Details

**IAL5_List Screen**
- Gallery displaying all `IAL5` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `IAL5_New` (visible to Initiator role only).
- Tap a row to navigate to `IAL5_View`.

**IAL5_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**IAL5_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "IAL5-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(INONumber) Or
    IsBlank(Site) Or
    IsBlank(RequestedBy) Or
    IsBlank(Department) Or
    IsBlank(ServerName) Or
    IsBlank(RestorePath),
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
Navigate(IAL5_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(IAL5_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "IAL5",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(IAL5_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "IAL5" &&
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
- **Stage 1:** `Create and submit restoration request` — performed by `Requestor (`RequestedBy`)`
- **Stage 2:** `Assign and process restoration details` — performed by `Backup Administrator (`BackupAdminAssignee`)`
- **Stage 3:** `Validate completion data and notify stakeholders` — performed by `IT Admin / Routed editor (`ITAdminOwner` / `SectionIIEditor`)`
- **Stage 4:** `Retain record and close workflow` — performed by `System + IT admin custodian`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| `nmRequestedBy` / `nmSubmitted` (requestor/submitter) | Contribute (create/edit own before assignment) |
| `nmBKAdmin` / `AEditor2` (backup administrator processing) | Contribute (assigned processing actions) |
| `ISAdmin` / `AEditor1` (IT admin/routing owner) | Full Control |
| `nmCC` / `MailP_Mgr` / `MailJ_Mgr` (stakeholders/managers) | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `IAL5` (system-enforced constant).
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

| Stage             | Flow Name          | Trigger                                                       | Actions                                                                                                                                            | Notification Target                |
| ----------------- | ------------------ | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Submit            | `IT_IAL5_Submit`   | SP - When item created (`FormCode = IAL5`)                    | Validate mandatory fields; generate `INONumber`; set `Status=Submitted`; stamp `SubmittedBy/SubmittedDate`; set `CurrentAction=Submitted`          | Backup administrator and requestor |
| Backup Processing | `IT_IAL5_Process`  | SP - When `Status=Submitted` or assignment action invoked     | Resolve backup admin assignee by site/server matrix; set `CurrentAction=Processing`; capture media/restoration details; update `RestorationStatus` | Requestor, CC, site managers       |
| Finalization      | `IT_IAL5_Finalize` | SP - When `RestorationStatus` becomes `Completed` or `Failed` | Enforce performed-by/date checks; stamp `ApprovedBy/ApprovedDate`; set `Status=Completed` or `Rejected`; append audit remarks                      | Requestor, CC, IT admin, managers  |
| Closure           | `IT_IAL5_Close`    | SP - When final state confirmed                               | Set `Status=Closed`; set `CurrentAction=Closed`; persist `WorkflowAuditJson`; retention tagging/reporting flag                                     | IT admin and reporting audience    |

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

- [ ] All SharePoint columns in `MainDB_IT` are created with correct types and required flags.
- [ ] Canvas App screens (`IAL5_List`, `IAL5_New`, `IAL5_View`, `IAL5_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
