# User Story — Hardware Inventory (`HI`)

> **Department:** IT  
> **Module:** M3 - Hardware & Infrastructure  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `HI`

---

## 1. App Overview & Purpose

`HI` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `IT` department at the PRAI site.

---

## 2. User Stories

**US-01: Register new hardware inventory record**
> As a **Initiator / IT owner (`Authors`, `IT`)** (member of ``D06-IT-Initiators``),  
> I want to **register new hardware inventory record** in the `HI` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created in `MainDB_IT` where `FormCode = HI`

**US-02: Update ownership/configuration/status fields**
> As a **IT editor (`MachineAuthor`)** (member of ``D06-IT-Editors-L1``),  
> I want to **update ownership/configuration/status fields** in the `HI` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When HI item modified and record is not archived

**US-03: Perform periodic audit and stamp audit metadata**
> As a **IT auditor (`LastAuditedBy`)** (member of ``D06-IT-Editors-L3``),  
> I want to **perform periodic audit and stamp audit metadata** in the `HI` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Scheduled recurrence for due assets or manual audit action update

**US-LIST: Search and filter Hardware Inventory records**
> As an **authorized user**,  
> I want to search, filter, and view Hardware Inventory records in the list screen,  
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

| Column Name         | SP Type                | Required | Choices / Source                              | Notes                               |
| ------------------- | ---------------------- | -------- | --------------------------------------------- | ----------------------------------- |
| Title               | Single line of text    | Yes      | Auto-generated                                | Display identifier for HI record    |
| FormCode            | Single line of text    | Yes      | Constant `HI`                                 | Routing/filter key                  |
| machineid           | Single line of text    | Yes      | System/flow generated or governed format      | Domino `machineid`                  |
| TagNo               | Single line of text    | Yes      | User input                                    | Domino `TagNo`                      |
| status              | Choice                 | Yes      | Active; InUse; Returned; Disposed; Archived   | Domino `status` lifecycle           |
| type                | Choice                 | Yes      | Hardware type catalog                         | Domino `type`                       |
| DeskType            | Choice                 | No       | Access type catalog                           | Domino `DeskType`                   |
| compname            | Single line of text    | Yes      | User input                                    | Domino `compname`                   |
| compmodel           | Single line of text    | No       | User input                                    | Domino `compmodel`                  |
| srvrmodel           | Single line of text    | No       | User input                                    | Domino `srvrmodel`                  |
| comp                | Choice                 | Yes      | Company master list                           | Domino `comp`                       |
| usedby              | Person or Group        | Yes      | Directory lookup                              | Domino `usedby`                     |
| prevusedby          | Person or Group        | No       | Directory lookup                              | Domino `prevusedby`                 |
| loc                 | Choice                 | Yes      | Location master list                          | Domino `loc`                        |
| dept                | Choice                 | Yes      | Department master list                        | Domino `dept`                       |
| Notes               | Multiple lines of text | No       | User input                                    | Domino `Notes`                      |
| cpusno              | Single line of text    | No       | User input                                    | Domino `cpusno`                     |
| ramsize             | Single line of text    | No       | User input                                    | Domino `ramsize`                    |
| ram                 | Single line of text    | No       | User input                                    | Domino `ram`                        |
| ramtype             | Choice                 | No       | RAM type catalog                              | Domino `ramtype`                    |
| hddsize             | Single line of text    | No       | User input                                    | Domino `hddsize`                    |
| hddtype             | Choice                 | No       | Disk type catalog                             | Domino `hddtype`                    |
| inch                | Single line of text    | No       | User input                                    | Domino `inch` (monitor)             |
| winversion          | Choice                 | No       | OS version catalog                            | Domino `winversion`                 |
| winsvrversion       | Choice                 | No       | Server OS version catalog                     | Domino `winsvrversion`              |
| msversion           | Choice                 | No       | Office version catalog                        | Domino `msversion`                  |
| MSEmail             | Single line of text    | No       | User input                                    | Domino `MSEmail`                    |
| MSEmailPswd         | Single line of text    | No       | Restricted; masked in app UI                  | Domino `MSEmailPswd` (sensitive)    |
| MSOfficeKey         | Single line of text    | No       | Restricted; masked in app UI                  | Domino `MSOfficeKey` (sensitive)    |
| notesver            | Choice                 | No       | Notes version catalog                         | Domino `notesver`                   |
| PoNumber            | Single line of text    | No       | User input                                    | Domino `PoNumber`                   |
| AssetNo             | Single line of text    | Yes      | User input with uniqueness check              | Domino `AssetNo`                    |
| Vendor              | Lookup                 | No       | Vendor master list                            | Domino `Vendor`                     |
| Authors             | Person or Group        | Yes      | System/user context                           | Domino `Authors`                    |
| MachineCreationDate | Date and Time          | Yes      | System timestamp                              | Domino `MachineCreationDate`        |
| MachineAuthor       | Person or Group        | No       | Workflow managed                              | Domino `MachineAuthor`              |
| DateModified        | Date and Time          | No       | Workflow managed                              | Domino `DateModified`               |
| LastAuditedBy       | Person or Group        | No       | Workflow managed                              | Domino `LastAuditedBy`              |
| LastAuditedOn       | Date and Time          | No       | Workflow managed                              | Domino `LastAuditedOn`              |
| IT                  | Person or Group        | No       | IT owner directory                            | Domino `IT`                         |
| Year                | Number                 | No       | Flow generated                                | Domino `Year`                       |
| Month               | Number                 | No       | Flow generated                                | Domino `Month`                      |
| INO                 | Number                 | No       | Flow generated                                | Domino `INO`                        |
| Status              | Choice                 | Yes      | Draft; Registered; Updated; Audited; Archived | Cross-form workflow status          |
| SubmittedBy         | Person or Group        | Yes      | System/user context                           | Live submission owner               |
| SubmittedDate       | Date and Time          | Yes      | System timestamp                              | Live submission timestamp           |
| ApprovedBy          | Person or Group        | No       | Reserved for governance extension             | Not used in current HI flow         |
| ApprovedDate        | Date and Time          | No       | Reserved for governance extension             | Not used in current HI flow         |
| Comments            | Multiple lines of text | No       | User/flow notes                               | Reserved comments/audit note column |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `HI_List` | Browse and search all HI records | All authorized users |
| `HI_New` | Create a new Hardware Inventory request | Initiator / Requestor |
| `HI_View` | Read-only detail view of a record | All authorized users |
| `HI_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `HI_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**HI_List Screen**
- Gallery displaying all `HI` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `HI_New` (visible to Initiator role only).
- Tap a row to navigate to `HI_View`.

**HI_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**HI_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "HI-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(machineid) Or
    IsBlank(TagNo) Or
    IsBlank(status) Or
    IsBlank(type) Or
    IsBlank(compname) Or
    IsBlank(comp),
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
Navigate(HI_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(HI_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "HI",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(HI_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "HI" &&
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
- **Stage 1:** `Register new hardware inventory record` — performed by `Initiator / IT owner (`Authors`, `IT`)`
- **Stage 2:** `Update ownership/configuration/status fields` — performed by `IT editor (`MachineAuthor`)`
- **Stage 3:** `Perform periodic audit and stamp audit metadata` — performed by `IT auditor (`LastAuditedBy`)`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| `Authors` (creator) | Contribute |
| `MachineAuthor` (operational editor) | Contribute |
| `LastAuditedBy` (auditor) | Contribute |
| `IT` (IT owner/admin) | Full Control |
| Read-only stakeholders | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `HI` (system-enforced constant).
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

| Stage    | Flow Name        | Trigger                                              | Actions                                                                                                                               | Notification Target                        |
| -------- | ---------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Register | `IT_HI_Register` | SharePoint - item created (`FormCode = HI`)          | Set `SubmittedBy`, `SubmittedDate`, initialize `Status`, validate mandatory identity fields, generate/validate `Year`, `Month`, `INO` | IT owner group and initiator               |
| Update   | `IT_HI_Update`   | SharePoint - item modified                           | Stamp `MachineAuthor` and `DateModified`, validate operational edits, maintain lifecycle `status`                                     | IT owner and relevant `usedby` stakeholder |
| Audit    | `IT_HI_Audit`    | Scheduled recurrence + optional manual audit trigger | Identify due assets, stamp `LastAuditedBy`/`LastAuditedOn`, set `Status = Audited` or keep current state, log audit notes             | IT governance/auditor group                |

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
- [ ] Canvas App screens (`HI_List`, `HI_New`, `HI_View`, `HI_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
