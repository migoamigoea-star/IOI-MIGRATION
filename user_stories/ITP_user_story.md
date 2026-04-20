# User Story — ISG Documentation register form used to store and manage IT/ISG documentation metadata, revision info, attachments, and reader/edit permissions (`ITP`)

> **Department:** IT  
> **Module:** M5 - Documentation & Policies  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `ITP`

---

## 1. App Overview & Purpose

ITP is the ISG documentation register form for maintaining controlled IT documentation metadata,
ownership, revision history, publication state, and reader permissions. The target implementation
uses `MainDB_IT` as the live submission store, with routing based on `FormCode=ITP`.

### Source Evidence

- PDF checked first and used as primary source:
  `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/IT/ITP.pdf`
- Metadata confirmed: Title `isgdoc - Form`, Pages `2`, printed PDF (`Form: none`)
- AcroForm/XFA detection: AcroForm field count `0`, `HasAcroForm=False`
- Visible text evidence used for mapping: `type`, `doctitle`, `verno`, `datelast`, `revision`,
  `Owner`, `att`, `ApplicableTo`, `Comments`, `Authors`, `MachineAuthor/DateModified`,
  `MachineCreationDate`, `MachineModificationDate`, `Readers`, `Status`

Supplemental references used after PDF verification:

- `docs/migration-analysis/Department_06_IT/ITP_analysis.md`
- `docs/Archive_analysy/Depratment/IT/ITP2_2_2.md`

---

### DEC-001 / DEC-004 / DEC-005 Control Notes

- DEC-001 (live submissions): all new ITP submissions write to `MainDB_IT` only. Any form-specific
  list such as `IT_ITP_List` is historical import/staging only and must not receive live
  submissions.
- DEC-004 (environment strategy): environment-variant values (review/publish approver aliases,
  notification sender profile, reminder cadence, archive recipients) must be loaded from
  `Config_AppSettings_IT` and promoted through `DEV -> TEST -> PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is the sole authoritative
  source for column definitions and is available in this workspace for schema reconciliation.

---

---

## 2. User Stories

**US-01: Create draft and submit**
> As a **Documentation PIC (`Authors`)** (member of ``D06-IT-Editors``),  
> I want to **create draft and submit** in the `ITP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created (`FormCode=ITP`)

**US-02: Review metadata, scope, and attachments**
> As a **Document Owner (`Owner`)** (member of ``D06-IT-Owners``),  
> I want to **review metadata, scope, and attachments** in the `ITP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `CurrentAction=UnderOwnerReview`

**US-03: Approve/publish and distribute to readers**
> As a **ISG Admin / IT Manager** (member of ``D06-IT-Managers``),  
> I want to **approve/publish and distribute to readers** in the `ITP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When owner decision = Approve

**US-LIST: Search and filter ISG Documentation register form used to store and manage IT/ISG documentation metadata, revision info, attachments, and reader/edit permissions records**
> As an **authorized user**,  
> I want to search, filter, and view ISG Documentation register form used to store and manage IT/ISG documentation metadata, revision info, attachments, and reader/edit permissions records in the list screen,  
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

| Column Name             | SP Type                 | Required | Choices / Source                                  | Notes                                            |
| ----------------------- | ----------------------- | -------- | ------------------------------------------------- | ------------------------------------------------ |
| Title                   | Single line of text     | Yes      | Auto-generated display ID (`ITP-YYYYMM-####`)     | Primary identifier                               |
| FormCode                | Single line of text     | Yes      | Constant `ITP`                                    | Routing/filter key                               |
| type                    | Choice                  | Yes      | SOP; WI; Policy; TrainingManual; Guideline; Other | Domino `type`                                    |
| doctitle                | Single line of text     | Yes      | User input                                        | Domino `doctitle`                                |
| verno                   | Single line of text     | Yes      | Governed format (for example `V1.0`)              | Domino `verno`                                   |
| datelast                | Date and Time           | Yes      | User/flow managed                                 | Domino `datelast`                                |
| revision                | Single line of text     | No       | User/flow managed                                 | Domino `revision`                                |
| Owner                   | Person or Group (multi) | Yes      | Directory selection                               | Domino `Owner` (edit rights)                     |
| att                     | Hyperlink or Picture    | No       | SharePoint attachment/document link               | Domino `att`; use native attachment storage      |
| ApplicableTo            | Multiple lines of text  | No       | User input                                        | Domino `ApplicableTo`                            |
| Comments                | Multiple lines of text  | No       | User/approver comments                            | Domino `Comments`                                |
| Authors                 | Person or Group         | Yes      | System/user context                               | Domino `Authors` (creator owner)                 |
| MachineAuthor           | Person or Group         | No       | Flow/system update                                | Split from `MachineAuthor/DateModified` evidence |
| DateModified            | Date and Time           | No       | Flow/system update                                | Split from `MachineAuthor/DateModified` evidence |
| MachineCreationDate     | Date and Time           | No       | Flow/system update                                | Domino hidden metadata                           |
| MachineModificationDate | Date and Time           | No       | Flow/system update                                | Domino hidden metadata                           |
| Readers                 | Person or Group (multi) | No       | Directory groups/users                            | Domino `Readers` (PATTERN-F access control)      |
| CurrentAction           | Choice                  | Yes      | Draft; UnderOwnerReview; Published; Archived      | Workflow stage state                             |
| Status                  | Choice                  | Yes      | Draft; Submitted; Approved; Rejected; Archived    | Cross-form lifecycle status                      |
| SubmittedBy             | Person or Group         | Yes      | System context                                    | Mandatory live-submission audit column           |
| SubmittedDate           | Date and Time           | Yes      | System timestamp                                  | Mandatory live-submission audit column           |
| ApprovedBy              | Person or Group         | No       | Workflow approver                                 | Publish/approval actor                           |
| ApprovedDate            | Date and Time           | No       | Workflow timestamp                                | Publish/approval timestamp                       |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `ITP_List` | Search and filter ITP records | IT readers, owners, admins |
| `ITP_New` | Create a new documentation register entry | IT initiators/editors |
| `ITP_View` | Read-only details and publication metadata | IT readers, owners, admins |
| `ITP_Edit` | Update metadata, ownership, status, and reader assignment | Owners and IT admins |

### Screen Interaction Details

**ITP_List Screen**
- Gallery displaying all `ITP` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ITP_New` (visible to Initiator role only).
- Tap a row to navigate to `ITP_View`.

**ITP_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ITP_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ITP-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(type) Or
    IsBlank(doctitle) Or
    IsBlank(verno) Or
    IsBlank(datelast) Or
    IsBlank(Owner) Or
    IsBlank(Authors),
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
Navigate(ITP_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ITP_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ITP",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ITP_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ITP" &&
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
- **Stage 1:** `Create draft and submit` — performed by `Documentation PIC (`Authors`)`
- **Stage 2:** `Review metadata, scope, and attachments` — performed by `Document Owner (`Owner`)`
- **Stage 3:** `Approve/publish and distribute to readers` — performed by `ISG Admin / IT Manager`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Domino Group / Field | Permission Level |
| `Authors` | Contribute |
| `Owner` | Edit/Approve at Stage 2 |
| ISG Admin (publication authority) | Approve/Full Control |
| `Readers` | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `ITP` (system-enforced constant).
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

| Stage        | Flow Name            | Trigger                                  | Actions                                                                                           | Notification Target             |
| ------------ | -------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------- |
| Submit       | `IT_ITP_Submit`      | SharePoint item created (`FormCode=ITP`) | Set `Status=Submitted`; set `CurrentAction=UnderOwnerReview`; stamp `SubmittedBy/SubmittedDate`   | `Owner`                         |
| Owner Review | `IT_ITP_OwnerReview` | Item modified with owner decision        | Approve: set `Status=Approved`; reject: set `Status=Rejected`; write review comment               | `Authors` and `D06-IT-Managers` |
| Publish      | `IT_ITP_Publish`     | `Status=Approved`                        | Set `CurrentAction=Published`; stamp `ApprovedBy/ApprovedDate`; apply reader/editor access policy | `Readers`                       |
| Archive      | `IT_ITP_Archive`     | Scheduled or manual archive signal       | Set `Status=Archived`; set `CurrentAction=Archived`; notify owner/readers                         | `Owner`, `Readers`              |

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
- [ ] Canvas App screens (`ITP_List`, `ITP_New`, `ITP_View`, `ITP_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
