# User Story — ISG Documentation - Training Manual (`ITP2`)

> **Department:** IT (D06)  
> **Module:** M5 - Documentation & Policies  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `ITP2`

---

## 1. App Overview & Purpose

ITP2 is an internal training manual registration and publication form. It captures metadata (title,
version, revision, owner, attachments, applicability, readers, and status) for ISG training
documents. The form operates as a simple three-stage document lifecycle: **Registration →
Publication/Update → Archive**. Notably, this form is **NOT an approval workflow**—status and reader
access are managed by document owners and system administrators, not through escalation chains. All
new submissions will be recorded in `MainDB_IT` (per **DEC-001**), with form module table
`ITP2_List` reserved for historical Domino import only.

---

---

## 2. User Stories

**US-LIST: Search and filter ISG Documentation - Training Manual records**
> As an **authorized user**,  
> I want to search, filter, and view ISG Documentation - Training Manual records in the list screen,  
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

| #   | Column Name      | SP Type                 | Required | Choices / Source                       | Domino Field              | Notes                                                              |
| --- | ---------------- | ----------------------- | -------- | -------------------------------------- | ------------------------- | ------------------------------------------------------------------ |
| 1   | FormCode         | Single line of text     | Yes      | —                                      | [System]                  | Auto-populated as `ITP2` for all submissions (per DEC-001)         |
| 2   | TrainingType     | Choice                  | Yes      | Manual; Workshop; Procedure; Other     | `Trgtype`                 | Training/manual category; user-selected at entry                   |
| 3   | DocumentTitle    | Single line of text     | Yes      | —                                      | `TrgTitle`                | Training manual title; required for identification                 |
| 4   | VersionNumber    | Single line of text     | Yes      | —                                      | `Trgverno`                | Version identifier (e.g., "1.0", "2.1")                            |
| 5   | DateLastUpdated  | Date only               | Yes      | —                                      | `Trgdatelast`             | Date of the last update; user-entered                              |
| 6   | RevisionNumber   | Single line of text     | No       | —                                      | `Trgrevision`             | Revision identifier separate from version (e.g., "Rev A", "Rev 1") |
| 7   | DocumentOwner    | Person or Group (multi) | No       | —                                      | `TrgOwner`                | Users authorized to edit and maintain; supports multiple owners    |
| 8   | AttachmentURL    | Hyperlink               | No       | —                                      | `Trgatt`                  | Link or reference to the training manual file/attachment           |
| 9   | ApplicableTo     | Multiple lines of text  | No       | —                                      | `ApplicableTo`            | Scope or intended audience (e.g., "All IT Staff", "SAP Users")     |
| 10  | Comments         | Multiple lines of text  | No       | —                                      | `TrgComments`             | Instructional notes or additional context                          |
| 11  | CreatedBy        | Person or Group         | No       | —                                      | `Authors`                 | Original document creator; system-populated                        |
| 12  | LastModifiedBy   | Person or Group         | No       | —                                      | `MachineAuthor`           | Last editor; system-populated on any edit                          |
| 13  | LastModifiedDate | Date and Time           | No       | —                                      | `DateModified`            | Timestamp of final modification; system-populated                  |
| 14  | CreatedDate      | Date and Time           | No       | —                                      | `MachineCreationDate`     | Document creation timestamp; system-populated                      |
| 15  | ModificationDate | Date and Time           | No       | —                                      | `MachineModificationDate` | System record of last modification; system-populated               |
| 16  | AllowedReaders   | Person or Group (multi) | No       | —                                      | `Readers`                 | Users permitted to view the published document; workflow-managed   |
| 17  | Status           | Choice                  | No       | Draft; Published; Archived; Superseded | `Status`                  | Document publication/lifecycle status; updated by owner or admin   |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `EntryEdit_IT_ITP2_New` | Initial training document registration | ITP2 |
| `EntryEdit_IT_ITP2_Edit` | Owner/admin edit existing document metadata | ITP2 |
| `Display_IT_ITP2_Detail` | Read-only detail view of published document | ITP2 |
| `SearchArchive_IT_ITP2` | Search and filter training documents by title, owner, status | ITP2 |

### Screen Interaction Details

**ITP2_List Screen**
- Gallery displaying all `ITP2` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ITP2_New` (visible to Initiator role only).
- Tap a row to navigate to `ITP2_View`.

**ITP2_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ITP2_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ITP2-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(ITP2_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ITP2_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ITP2",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ITP2_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ITP2" &&
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
| Role Name | SharePoint Group |
| Author / Initiator | `D06-IT-Initiators` |
| Document Owner | `D06-IT-Editors-L1` |
| Authorized Readers | `D06-IT-Readers` |
| IT/IS Administrator | `D06-IT-IT-Admin` |

### 3. Data Integrity Rules

- `FormCode` must always equal `ITP2` (system-enforced constant).
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

| Stage        | Flow Name                   | Trigger                                                           | Actions                                                                    | Notification Target                         |
| ------------ | --------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------- |
| Registration | `IT_ITP2_DocumentCreated`   | SP — When item created in `MainDB_IT` (filter: `FormCode='ITP2'`) | Validate required fields (title, version); set timestamps                  | Optional: notify designated owner           |
| Publication  | `IT_ITP2_PublicationUpdate` | SP — When Status changes to "Published"                           | Send notification to `AllowedReaders`; log publication event to audit list | AllowedReaders distribution                 |
| Archive      | `IT_ITP2_Archival`          | SP — When Status changes to "Archived" or "Superseded"            | Preserve version history; log archival to audit list                       | Optional: notify readers of doc deprecation |

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
- [ ] Canvas App screens (`ITP2_List`, `ITP2_New`, `ITP2_View`, `ITP2_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
