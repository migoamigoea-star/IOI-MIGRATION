# User Story — External Access Form (VPN & Citrix) (`EAF`)

> **Department:** IT  
> **Module:** M1 - User & Access Management  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `EAF`

---

## 1. App Overview & Purpose

`EAF` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `IT` department at the PRAI site.

---

## 2. User Stories

**US-01: Create and submit external access request**
> As a **Requestor** (member of ``D06-IT-Initiators``),  
> I want to **create and submit external access request** in the `EAF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created in `MainDB_IT` where `FormCode = EAF`

**US-02: Approve/reject request at department level**
> As a **Department Head** (member of ``D06-IT-HOD``),  
> I want to **approve/reject request at department level** in the `EAF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `CurrentAction = HOD`

**US-03: Approve/reject higher-level business gate**
> As a **DDApp / Higher Approver** (member of ``D06-IT-Editors-L3``),  
> I want to **approve/reject higher-level business gate** in the `EAF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `DeptHeadStatus = Approved` and `CurrentAction = DDApp`

**US-04: Approve/reject technical manager gate**
> As a **IT Manager** (member of ``D06-IT-IT-Admin``),  
> I want to **approve/reject technical manager gate** in the `EAF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `DDAppStatus = Approved` and `CurrentAction = ITManager`

**US-05: Execute provisioning and close request**
> As a **IT PIC / IT Admin** (member of ``D06-IT-PIC` + `D06-IT-IT-Admin``),  
> I want to **execute provisioning and close request** in the `EAF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When `ITManagerStatus = Approved` and `CurrentAction = ITComplete`

**US-LIST: Search and filter External Access Form (VPN & Citrix) records**
> As an **authorized user**,  
> I want to search, filter, and view External Access Form (VPN & Citrix) records in the list screen,  
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

| Column Name           | SP Type                 | Required | Choices / Source                                        | Notes                          |
| --------------------- | ----------------------- | -------- | ------------------------------------------------------- | ------------------------------ |
| Title                 | Single line of text     | Yes      | Auto-generated (`EAF-YYYYMM-####`)                      | Display identifier             |
| FormCode              | Single line of text     | Yes      | Constant `EAF`                                          | Routing and filtering key      |
| Company               | Choice                  | Yes      | Company master list                                     | Domino `Company`               |
| Requestor             | Person or Group         | Yes      | User picker                                             | Domino `req`                   |
| SubmittedOn           | Date and Time           | Yes      | System timestamp                                        | Domino `date1`                 |
| TargetUser            | Person or Group         | Yes      | User picker                                             | Domino `User`                  |
| Application           | Choice                  | Yes      | Citrix; VPN; Other                                      | Domino `App`                   |
| SystemName            | Choice                  | Yes      | System lookup list                                      | Domino `system`                |
| Justification         | Multiple lines of text  | Yes      | User input                                              | Domino `justification`         |
| DepartmentHead        | Person or Group         | Yes      | Approver matrix                                         | Domino `depthead`              |
| CCRecipients          | Person or Group (multi) | No       | User/flow populated                                     | Domino `CC`                    |
| DeptHeadStatus        | Choice                  | No       | Pending; Approved; Rejected                             | Domino `status1`               |
| DeptHeadApprovedBy    | Person or Group         | No       | Workflow managed                                        | Domino `HODNAME`               |
| DeptHeadApprovedDate  | Date and Time           | No       | Workflow managed                                        | Domino `date2`                 |
| DeptHeadComment       | Multiple lines of text  | No       | Approver input                                          | Domino `comment1`              |
| DDAppStatus           | Choice                  | No       | Pending; Approved; Rejected                             | Domino `status2`               |
| DDAppApprovedBy       | Person or Group         | No       | Workflow managed                                        | Domino `DIVNAME`               |
| DDAppApprovedDate     | Date and Time           | No       | Workflow managed                                        | Domino `date3`                 |
| DDAppComment          | Multiple lines of text  | No       | Approver input                                          | Domino `comment2`              |
| ITManagerStatus       | Choice                  | No       | Pending; Approved; Rejected                             | Domino `status3`               |
| ITManagerApprovedBy   | Person or Group         | No       | Workflow managed                                        | Domino `name4`                 |
| ITManagerApprovedDate | Date and Time           | No       | Workflow managed                                        | Domino `date4`                 |
| ITManagerComment      | Multiple lines of text  | No       | Approver input                                          | Domino `comment3`              |
| ITCompletionStatus    | Choice                  | No       | Pending; Completed; Rework                              | Domino `status4`               |
| ITCompletedBy         | Person or Group         | No       | Workflow managed                                        | Domino `name5`                 |
| ITCompletedDate       | Date and Time           | No       | Workflow managed                                        | Domino `date5`                 |
| ITCompletionRemarks   | Multiple lines of text  | No       | IT input                                                | Domino `comment4`              |
| ITInternalRemarks     | Multiple lines of text  | No       | IT input                                                | Domino `remarks`               |
| FinalStatus           | Choice                  | No       | Open; Approved; Rejected; Closed                        | Domino `Status`                |
| CurrentAction         | Choice                  | Yes      | Requestor; HOD; DDApp; ITManager; ITComplete; Closed    | Domino `CurrentAction`         |
| RouteACMIT            | Person or Group         | No       | Workflow managed                                        | Domino `ACMIT`                 |
| RoutePCNIT            | Person or Group         | No       | Workflow managed                                        | Domino `PCNIT`                 |
| RoutePCNIT2           | Person or Group         | No       | Workflow managed                                        | Domino `PCNIT2`                |
| IsPCN                 | Yes/No                  | No       | Computed from company                                   | Domino `isPCN`                 |
| ITPIC                 | Person or Group         | No       | Workflow managed                                        | Domino `ITPIC`                 |
| ITPIC2                | Person or Group         | No       | Workflow managed                                        | Domino `ITPIC2`                |
| ExecutiveDirector     | Person or Group         | No       | Workflow managed                                        | Domino `ED`                    |
| HeadOfOperation       | Person or Group         | No       | Workflow managed                                        | Domino `HOO`                   |
| HigherApprover        | Person or Group         | No       | Workflow managed                                        | Domino `HApp`                  |
| RecipientRouting      | Person or Group (multi) | No       | Workflow managed                                        | Domino `SendTo`                |
| ISManager             | Person or Group         | No       | Workflow managed                                        | Domino `IsMgr`                 |
| ITAdmin               | Person or Group         | No       | Workflow managed                                        | Domino `ITADMIN`               |
| ReminderTo            | Person or Group (multi) | No       | Flow managed                                            | Domino `RemTo`                 |
| ReminderSubject       | Single line of text     | No       | Flow generated                                          | Domino `RemSubject`            |
| Status                | Choice                  | Yes      | Draft; Submitted; InReview; Completed; Rejected; Closed | Cross-form workflow state      |
| SubmittedBy           | Person or Group         | Yes      | System                                                  | Mandatory governance column    |
| SubmittedDate         | Date and Time           | Yes      | System                                                  | Mandatory governance column    |
| ApprovedBy            | Person or Group         | No       | Workflow managed                                        | Final approval actor           |
| ApprovedDate          | Date and Time           | No       | Workflow managed                                        | Final approval timestamp       |
| Comments              | Multiple lines of text  | No       | User/flow notes                                         | Consolidated remarks trail     |
| WorkflowAuditJson     | Multiple lines of text  | No       | Flow-generated JSON                                     | Optional troubleshooting trail |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `EAF_List` | Browse and search all EAF records | All authorized users |
| `EAF_New` | Create a new External Access Form (VPN & Citrix) request | Initiator / Requestor |
| `EAF_View` | Read-only detail view of a record | All authorized users |
| `EAF_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `EAF_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**EAF_List Screen**
- Gallery displaying all `EAF` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `EAF_New` (visible to Initiator role only).
- Tap a row to navigate to `EAF_View`.

**EAF_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**EAF_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "EAF-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(Company) Or
    IsBlank(Requestor) Or
    IsBlank(SubmittedOn) Or
    IsBlank(TargetUser) Or
    IsBlank(Application) Or
    IsBlank(SystemName),
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
Navigate(EAF_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(EAF_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "EAF",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(EAF_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "EAF" &&
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
- **Stage 1:** `Create and submit external access request` — performed by `Requestor`
- **Stage 2:** `Approve/reject request at department level` — performed by `Department Head`
- **Stage 3:** `Approve/reject higher-level business gate` — performed by `DDApp / Higher Approver`
- **Stage 4:** `Approve/reject technical manager gate` — performed by `IT Manager`
- **Stage 5:** `Execute provisioning and close request` — performed by `IT PIC / IT Admin`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| `req` / `Requestor` / `AEditor1` | Contribute (create/edit own before final closure) |
| `depthead` / `HODNAME` | Approve/Reject |
| `DIVNAME` / `HApp` | Approve/Reject |
| `IsMgr` / `name4` | Approve/Reject + workflow admin |
| `ITPIC` / `ITPIC2` / `name5` | Contribute (execution and completion update) |
| `ITADMIN` | Full Control |
| `SendTo` / `CC` / informational recipients | Read |
| `ACMIT` / `PCNIT` / `PCNIT2` | Approve (company-specific route) |

### 3. Data Integrity Rules

- `FormCode` must always equal `EAF` (system-enforced constant).
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

| Stage         | Flow Name                  | Trigger                                        | Actions                                                                                                                                     | Notification Target               |
| ------------- | -------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| Submit        | `IT_EAF_Submit`            | SP item created (`FormCode = EAF`)             | Validate required fields; stamp `SubmittedBy/SubmittedDate`; set `Status=Submitted`; set `CurrentAction=HOD`; compute route flags (`IsPCN`) | Department Head + CC              |
| HOD           | `IT_EAF_HODDecision`       | Item modified where `CurrentAction=HOD`        | Branch approve/reject; update `DeptHeadStatus`, `DeptHeadApprovedBy`, `DeptHeadApprovedDate`; on approve move to DDApp                      | Requestor + DDApp/Higher approver |
| DDApp         | `IT_EAF_DDAppDecision`     | Item modified where `CurrentAction=DDApp`      | Branch approve/reject; update `DDAppStatus`, `DDAppApprovedBy`, `DDAppApprovedDate`; on approve move to IT Manager                          | Requestor + IT Manager            |
| IT Manager    | `IT_EAF_ITManagerDecision` | Item modified where `CurrentAction=ITManager`  | Branch approve/reject; update `ITManagerStatus`, `ITManagerApprovedBy`, `ITManagerApprovedDate`; on approve move to IT completion           | IT PIC/IT Admin + requestor       |
| IT Completion | `IT_EAF_Complete`          | Item modified where `CurrentAction=ITComplete` | Update `ITCompletionStatus`, `ITCompletedBy`, `ITCompletedDate`, `FinalStatus`, `Status=Closed`; append audit JSON                          | Requestor + recipients            |

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
- [ ] Canvas App screens (`EAF_List`, `EAF_New`, `EAF_View`, `EAF_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
