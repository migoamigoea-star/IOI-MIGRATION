# User Story — IOIOI POLICY (`IOIP`)

> **Department:** IT  
> **Module:** M5 - Documentation & Policies  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `IOIP`

---

## 1. App Overview & Purpose

`IOIP` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `IT` department at the PRAI site.

---

## 2. User Stories

**US-01: Create draft policy and submit**
> As a **Document Author (`DocAuthor`)** (member of ``D06-IT-Initiators``),  
> I want to **create draft policy and submit** in the `IOIP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created or modified (`Status=Draft`)

**US-02: Collect authority approvals**
> As a **Policy Owner + routed authorities** (member of ``D06-IT-HOD`, `D06-IT-Editors-L1``),  
> I want to **collect authority approvals** in the `IOIP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `Status=Submitted`

**US-03: Publish and distribute policy**
> As a **Policy Admin / Editor** (member of ``D06-IT-Editors-L1``),  
> I want to **publish and distribute policy** in the `IOIP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When all `cr_approvalrecord` rows are approved

**US-04: Update revision and resubmit**
> As a **Editors** (member of ``D06-IT-Editors-L1``),  
> I want to **update revision and resubmit** in the `IOIP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When revision metadata/content changes

**US-05: Archive superseded policy**
> As a **IT Admin / Policy Admin** (member of ``D06-IT-IT-Admin``),  
> I want to **archive superseded policy** in the `IOIP` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `FinalStatus=Archived`

**US-LIST: Search and filter IOIOI POLICY records**
> As an **authorized user**,  
> I want to search, filter, and view IOIOI POLICY records in the list screen,  
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

| Column Name          | SP Type                 | Required | Choices / Source                                            | Notes                                                |
| -------------------- | ----------------------- | -------- | ----------------------------------------------------------- | ---------------------------------------------------- |
| Title                | Single line of text     | Yes      | Auto-generated display ID                                   | Primary display value                                |
| FormCode             | Single line of text     | Yes      | Constant `IOIP`                                             | Routing/filter key                                   |
| PolicyNo             | Single line of text     | Yes      | User input (controlled numbering)                           | Domino `PolicyNo`                                    |
| RevNo                | Single line of text     | Yes      | Flow-managed or governed input                              | Domino `RevNo`                                       |
| DateIssue            | Date and Time           | Yes      | User input                                                  | Domino `DateIssue`                                   |
| Subject              | Single line of text     | Yes      | User input                                                  | Domino `Subject`                                     |
| ReviNum              | Single line of text     | Yes      | User input                                                  | Domino `ReviNum`                                     |
| PolicyOwner          | Person or Group         | Yes      | Directory lookup                                            | Domino `PolicyOwner`                                 |
| DocAuthor            | Person or Group         | Yes      | User/directory context                                      | Domino `DocAuthor`                                   |
| Editors              | Person or Group (multi) | No       | Directory lookup                                            | Domino `Editors`                                     |
| Authors              | Person or Group (multi) | No       | Flow-captured                                               | Domino `Authors`                                     |
| Readers              | Person or Group (multi) | No       | Directory lookup                                            | Domino `Readers`                                     |
| Sendto               | Person or Group (multi) | No       | Distribution list or directory                              | Domino `Sendto`                                      |
| FinalStatus          | Choice                  | Yes      | Draft; PendingApproval; Active; Superseded; Archived        | Domino lifecycle status                              |
| DateArchived         | Date and Time           | No       | Flow-managed                                                | Domino `DateArchived`                                |
| FormName             | Single line of text     | No       | Constant/template name                                      | Domino `FormName`                                    |
| RevisionHistoryJson  | Multiple lines of text  | No       | Flow-managed serialized history                             | Replaces embedded Domino revision grid (`R`,`D`,`U`) |
| DistributionListName | Single line of text     | No       | Lookup-derived                                              | Domino `DistributionList`/`DefaultList` evidence     |
| CurrentAction        | Choice                  | Yes      | Draft; Submitted; InApproval; Published; Revision; Archived | Workflow stage state                                 |
| Status               | Choice                  | Yes      | Draft; Submitted; Approved; Rejected; Archived              | Cross-form workflow status                           |
| SubmittedBy          | Person or Group         | Yes      | System/user context                                         | Mandatory cross-form                                 |
| SubmittedDate        | Date and Time           | Yes      | System timestamp                                            | Mandatory cross-form                                 |
| ApprovedBy           | Person or Group         | No       | Stage actor stamp                                           | Last approval actor                                  |
| ApprovedDate         | Date and Time           | No       | Flow-managed                                                | Last approval timestamp                              |
| Comments             | Multiple lines of text  | No       | User/flow notes                                             | Decision remarks                                     |


| Column Name      | SP Type                | Required | Notes                       |
| ---------------- | ---------------------- | -------- | --------------------------- |
| ParentItemId     | Lookup (`MainDB_IT`)   | Yes      | Parent IOIP record          |
| ApprovalStage    | Number                 | Yes      | 1..N sequence               |
| ApproverRole     | Single line of text    | Yes      | Authority role label        |
| ApproverPerson   | Person or Group        | Yes      | Routed approver             |
| ApprovalRequired | Yes/No                 | Yes      | Domino `Req*` mapping       |
| ApprovalStatus   | Choice                 | Yes      | Pending; Approved; Rejected |
| ApprovalDate     | Date and Time          | No       | Approver action date        |
| ApprovalComment  | Multiple lines of text | No       | Approver remarks            |
| RepliedFlag      | Yes/No                 | Yes      | Domino `A*replied` mapping  |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `IOIP_List` | Browse and search all IOIP records | All authorized users |
| `IOIP_New` | Create a new IOIOI POLICY request | Initiator / Requestor |
| `IOIP_View` | Read-only detail view of a record | All authorized users |
| `IOIP_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `IOIP_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**IOIP_List Screen**
- Gallery displaying all `IOIP` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `IOIP_New` (visible to Initiator role only).
- Tap a row to navigate to `IOIP_View`.

**IOIP_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**IOIP_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "IOIP-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(PolicyNo) Or
    IsBlank(RevNo) Or
    IsBlank(DateIssue) Or
    IsBlank(Subject) Or
    IsBlank(ReviNum) Or
    IsBlank(PolicyOwner),
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
Navigate(IOIP_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(IOIP_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "IOIP",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(IOIP_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "IOIP" &&
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
- **Stage 1:** `Create draft policy and submit` — performed by `Document Author (`DocAuthor`)`
- **Stage 2:** `Collect authority approvals` — performed by `Policy Owner + routed authorities`
- **Stage 3:** `Publish and distribute policy` — performed by `Policy Admin / Editor`
- **Stage 4:** `Update revision and resubmit` — performed by `Editors`
- **Stage 5:** `Archive superseded policy` — performed by `IT Admin / Policy Admin`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| `DocAuthor` | Contribute |
| `PolicyOwner` | Approve/Edit |
| `Editors` | Edit |
| `Readers` | Read |
| `Sendto` recipients | Read |
| `IT/ISAdmin` | Full Control |

### 3. Data Integrity Rules

- `FormCode` must always equal `IOIP` (system-enforced constant).
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

| Stage   | Flow Name          | Trigger                                                                                 | Actions                                                                                                         | Notification Target            |
| ------- | ------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| Submit  | `IT_IOIP_Submit`   | SharePoint item created/updated with `Status=Draft` and required header fields complete | Validate required fields; set `Status=Submitted`; set `CurrentAction=InApproval`; seed `cr_approvalrecord` rows | Policy owner + first approvers |
| Approve | `IT_IOIP_Approval` | Child approval row action in `cr_approvalrecord`                                        | Update child status/date; evaluate all required approvals; if complete set parent `Status=Approved`             | Document author + editors      |
| Reject  | `IT_IOIP_Reject`   | Any required child approval row rejected                                                | Set parent `Status=Rejected`; set `CurrentAction=Revision`; capture rejection comment                           | Document author + policy owner |
| Publish | `IT_IOIP_Publish`  | Parent `Status=Approved` and distribution fields complete                               | Set `FinalStatus=Active`; set `CurrentAction=Published`; send issue/distribution notification                   | `Sendto`, `Readers`            |
| Archive | `IT_IOIP_Archive`  | Parent `FinalStatus=Archived`                                                           | Stamp `DateArchived`; set `Status=Archived`; disable active reminders; write audit note                         | Policy owner + IT admin        |

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
- [ ] Canvas App screens (`IOIP_List`, `IOIP_New`, `IOIP_View`, `IOIP_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
