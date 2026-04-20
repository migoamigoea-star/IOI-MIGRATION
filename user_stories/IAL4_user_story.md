# User Story — Server Records (`IAL4`)

> **Department:** IT  
> **Module:** M2 - IT Support & Service Requests  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `IAL4`

---

## 1. App Overview & Purpose

IAL4 captures structured server-record entries for IT incident/service analysis, including
chronology, root-cause context, and corrective/preventive actions, then routes records through
distribution and archival stages in `MainDB_IT`.

### Governance Notes

- DEC-001 (live submissions): all new IAL4 submissions write to `MainDB_IT` only. Any form-specific
  list such as `IT_IAL4_List` is historical import/staging only and must not receive live
  submissions.
- DEC-004 (environment strategy): environment-variant values (distribution recipients, reminder
  windows, archive thresholds, sender profile, escalation owner) must be loaded from
  `Config_AppSettings` for `DEV`, `TEST`, and `PROD`.
- DEC-005 (schema authority): `FORM_COLUMN_DEFINITIONS_ENHANCED.json` v2.0 is the sole authoritative
  source for column definitions and is available in this workspace for schema reconciliation.

---

---

## 2. User Stories

**US-01: Create and submit server record**
> As a **Record owner (`PerformedBy`)** (member of ``D06-IT-Initiators``),  
> I want to **create and submit server record** in the `IAL4` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created in `MainDB_IT` where `FormCode = IAL4`

**US-02: Validate record completeness and approve distribution**
> As a **IT distribution owner (`ITAdminOwner` / routed editor)** (member of ``D06-IT-Editors-L1``),  
> I want to **validate record completeness and approve distribution** in the `IAL4` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `Status = Submitted`

**US-03: Archive and close server record for retention/reporting**
> As a **IT admin custodian** (member of ``D06-IT-IT-Admin``),  
> I want to **archive and close server record for retention/reporting** in the `IAL4` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `Status = Distributed` and archive condition met

**US-LIST: Search and filter Server Records records**
> As an **authorized user**,  
> I want to search, filter, and view Server Records records in the list screen,  
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

| Column Name          | SP Type                 | Required | Choices / Source                        | Notes                                                          |
| -------------------- | ----------------------- | -------- | --------------------------------------- | -------------------------------------------------------------- |
| Title                | Single line of text     | Yes      | Auto-generated display ID               | Display identifier for IAL4 item                               |
| FormCode             | Single line of text     | Yes      | Constant `IAL4`                         | Routing/filter key                                             |
| Site                 | Choice                  | Yes      | Site master list                        | Domino `rbSite`                                                |
| ServerName           | Choice                  | Yes      | Server master list                      | Domino `lstServerName`                                         |
| RecordType           | Choice                  | Yes      | Record-type list                        | Domino `lstRecType`                                            |
| Mode                 | Choice                  | Yes      | Mode/severity list                      | Domino `rbMode`                                                |
| DateFrom             | Date and Time           | Yes      | User input                              | Domino `dtFrom`                                                |
| DateTo               | Date and Time           | No       | User input                              | Domino `dtTo`                                                  |
| TimeFrom             | Date and Time           | Yes      | User input                              | Domino `tmFrom`                                                |
| TimeTo               | Date and Time           | No       | User input                              | Domino `tmTo`                                                  |
| Overview             | Multiple lines of text  | Yes      | User input                              | Domino `Summary`                                               |
| OverviewDetail       | Multiple lines of text  | No       | User input                              | Domino `txtSummary`                                            |
| Background           | Multiple lines of text  | No       | User input                              | Domino `txtBackground`                                         |
| Analysis             | Multiple lines of text  | No       | User input                              | Domino `txtAnalysis`                                           |
| RootCauseDescription | Multiple lines of text  | No       | User input                              | Domino `txtRootCause`                                          |
| CorrectiveActions    | Multiple lines of text  | No       | User input                              | Domino `txtCA`                                                 |
| PreventiveActions    | Multiple lines of text  | No       | User input                              | Domino `txtPA`                                                 |
| RequiredReboot       | Choice                  | No       | Yes; No                                 | Domino `YESNO`                                                 |
| AttachmentLink       | Hyperlink or Picture    | No       | User/flow managed                       | Domino `SvrAttach`; use native list attachment where available |
| PerformedBy          | Person or Group         | Yes      | User directory                          | Domino `nmReqRecords`                                          |
| CreatorPerson        | Person or Group         | Yes      | System/user context                     | Domino `nmRequestor`                                           |
| CreatedOn            | Date and Time           | Yes      | System timestamp                        | Domino `dtCreatedOn`                                           |
| RoutedEditor         | Person or Group         | No       | Workflow managed                        | Domino `AEditor1`                                              |
| CurrentAction        | Choice                  | Yes      | Draft; Submitted; Distributed; Archived | Domino `CurrentAction`                                         |
| ITAdminOwner         | Person or Group         | No       | Config-driven                           | Domino `ISAdmin`                                               |
| DisplayServerName    | Single line of text     | No       | Derived                                 | Domino `dsSvrName`                                             |
| ISGRecipients        | Person or Group (multi) | No       | Config or workflow resolved             | Domino `ISGRecipients`                                         |
| Status               | Choice                  | Yes      | Draft; Submitted; Distributed; Closed   | Workflow status                                                |
| SubmittedBy          | Person or Group         | Yes      | System/user context                     | Mandatory cross-form column                                    |
| SubmittedDate        | Date and Time           | Yes      | System timestamp                        | Mandatory cross-form column                                    |
| ApprovedBy           | Person or Group         | No       | Stage actor stamp                       | Stage 2 distribution approval stamp                            |
| ApprovedDate         | Date and Time           | No       | Flow managed                            | Stage 2 distribution approval timestamp                        |
| Comments             | Multiple lines of text  | No       | User/flow note                          | Workflow note and archive remarks                              |
| ArchivedDate         | Date and Time           | No       | Flow managed                            | Archive evidence timestamp                                     |
| WorkflowAuditJson    | Multiple lines of text  | No       | Flow generated                          | Optional troubleshooting trace                                 |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `IAL4_List` | Search and review server records | IT readers, editors, admins |
| `IAL4_New` | Create and submit server record | IT initiators/editors |
| `IAL4_View` | Read-only detail and workflow history | IT readers, editors, admins |
| `IAL4_Edit` | Complete distribution/closure updates | Editors and IT admins |

### Screen Interaction Details

**IAL4_List Screen**
- Gallery displaying all `IAL4` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `IAL4_New` (visible to Initiator role only).
- Tap a row to navigate to `IAL4_View`.

**IAL4_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**IAL4_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "IAL4-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(Site) Or
    IsBlank(ServerName) Or
    IsBlank(RecordType) Or
    IsBlank(Mode) Or
    IsBlank(DateFrom) Or
    IsBlank(TimeFrom),
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
Navigate(IAL4_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(IAL4_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "IAL4",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(IAL4_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "IAL4" &&
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
- **Stage 1:** `Create and submit server record` — performed by `Record owner (`PerformedBy`)`
- **Stage 2:** `Validate record completeness and approve distribution` — performed by `IT distribution owner (`ITAdminOwner` / routed editor)`
- **Stage 3:** `Archive and close server record for retention/reporting` — performed by `IT admin custodian`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| `nmReqRecords` (record owner) | Contribute (create and edit own in Draft/Returned) |
| `AEditor1` (routed editor) | Contribute (assigned review/distribution actions) |
| `ISAdmin` (IT admin owner) | Full Control |
| `ISGRecipients` (stakeholder recipients) | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `IAL4` (system-enforced constant).
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

| Stage                | Flow Name                 | Trigger                                    | Actions                                                                                                          | Notification Target                    |
| -------------------- | ------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| Submit               | `IT_IAL4_Submit`          | SP - When item created (`FormCode = IAL4`) | Validate mandatory fields; set `Status=Submitted`; stamp `SubmittedBy/SubmittedDate`; normalize date/time fields | IT distribution owner and record owner |
| Distribution Approve | `IT_IAL4_Distribute`      | SP - When `Status=Submitted`               | Resolve recipient set; set `Status=Distributed`; stamp `ApprovedBy/ApprovedDate`; send server-record notice      | `ISGRecipients` and IT readers         |
| Distribution Reject  | `IT_IAL4_ReturnForRework` | SP - Rejection action at Stage 2           | Set `Status=Draft`; append rejection reason in `Comments`; notify owner for correction                           | Record owner (`PerformedBy`)           |
| Archive              | `IT_IAL4_Archive`         | Scheduled recurrence or admin close        | Set `Status=Closed`; set `CurrentAction=Archived`; stamp `ArchivedDate`; persist `WorkflowAuditJson`             | IT admin and reporting audience        |

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
- [ ] Canvas App screens (`IAL4_List`, `IAL4_New`, `IAL4_View`, `IAL4_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
