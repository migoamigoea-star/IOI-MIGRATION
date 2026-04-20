# User Story — Program Request Form (PRF) 2025 (`PRF`)

> **Department:** 06 - IT  
> **Module:** M2 - Service Management & Requests  
> **Site(s):** PRAI` (primary), `Johor` (secondary)  
> **SharePoint List:** `MainDB_06 - IT`  
> **Form Code:** `PRF`

---

## 1. App Overview & Purpose

`PRF` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `06 - IT` department at the PRAI` (primary), `Johor` (secondary) site.

---

## 2. User Stories

**US-01: Requesting**
> As a **Manual form create + submit** (member of `Requestor`),  
> I want to **requesting** in the `PRF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D[Dept]-Staff`

**US-02: Authorizing**
> As a **Status=Submitted** (member of `HOD / Dept Manager`),  
> I want to **authorizing** in the `PRF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D06-IT-Managers`

**US-03: Triaging**
> As a **Approval Stage 1 = Approved** (member of `IT Manager`),  
> I want to **triaging** in the `PRF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D06-IT-Managers`

**US-04: FunctionReview**
> As a **PRF_IsSAP = Yes; (Optional)** (member of `SAP Functional Lead`),  
> I want to **functionreview** in the `PRF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D02-SAP-Leads` (or similar)

**US-05: Processing**
> As a **Stage 3/4 Complete; PRF_AssignedITOwner assigned** (member of `IT Support Staff`),  
> I want to **processing** in the `PRF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D06-IT-ServiceDesk`

**US-06: Validating**
> As a **Tasks Completed; PRF_ApprovalStatus2 = Approved** (member of `Requestor`),  
> I want to **validating** in the `PRF` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `D[Dept]-Staff`

**US-LIST: Search and filter Program Request Form (PRF) 2025 records**
> As an **authorized user**,  
> I want to search, filter, and view Program Request Form (PRF) 2025 records in the list screen,  
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

**Target List:** `MainDB_06 - IT`

| #   | Column Name   | SP Type      | Required | Lookup / Choice Values                                                                          | Mapped From Domino | Notes                                |
| --- | ------------- | ------------ | -------- | ----------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------ |
| 1   | ID            | Number       | Yes      | —                                                                                               | System auto        | SharePoint system key                |
| 2   | Title         | Single line  | Yes      | —                                                                                               | `ReqNo`            | Business reference visible in search |
| 3   | FormType      | Choice       | Yes      | `PRF`, `SAPAMR`, `ITDR`, `ITSSR`                                                                | Form input         | Determines which columns are active  |
| 4   | Status        | Choice       | Yes      | `Draft`, `Submitted`, `Approved-L1`, `Approved-L2`, `In Progress`, `Completed`, `Rejected`      | Workflow           | Workflow-managed                     |
| 5   | CurrentStage  | Choice       | Yes      | `Requesting`, `Authorizing`, `Triaging`, `Processing`, `FunctionReview`, `Validating`, `Closed` | Workflow           | Workflow engine state                |
| 6   | CreatedOn     | Single line  | Yes      | —                                                                                               | System             | ISO 8601 datetime                    |
| 7   | CreatedBy     | Person/Group | No       | —                                                                                               | System             | Requestor identity                   |
| 8   | ModifiedOn    | Single line  | No       | —                                                                                               | System             | Last edit timestamp                  |
| 9   | ModifiedBy    | Person/Group | No       | —                                                                                               | System             | Last editor identity                 |
| 10  | FinalStatus   | Choice       | No       | `Completed`, `Completed-AutoAccepted`, `Rejected`, `Withdrawn`                                  | Workflow           | Final closure state                  |
| 11  | CurrentAction | Choice       | No       | [Power Automate internal state]                                                                 | Workflow           | Not user-visible                     |


| #                                                        | Column Name                 | SP Type              | Required | Lookup / Source                                     | Domino Field                          | Approval Pattern | Notes                                                    |
| -------------------------------------------------------- | --------------------------- | -------------------- | -------- | --------------------------------------------------- | ------------------------------------- | ---------------- |
| **Request Identification**                               |                             |                      |          |                                                     |                                       |                  |                                                          |
| 12                                                       | PRF_RequestNo               | Single line          | Yes      | —                                                   | `ReqNo` (computed: `PRF-YYYY-MM-INO`) | —                | System-assigned request number                           |
| 13                                                       | PRF_Requestor               | Person/Group         | Yes      | —                                                   | `requestor`                           | —                | User who initiated the request                           |
| 14                                                       | PRF_RequestorOU             | Single line          | No       | —                                                   | `OU` (computed from AD sync)          | —                | Organizational Unit from Active Directory                |
| **Department & Contact Context**                         |                             |                      |          |                                                     |                                       |                  |                                                          |
| 15                                                       | PRF_DeptManager             | Person/Group         | Yes      | —                                                   | `deptmanager`                         | PATTERN-C        | Approver at stage 2; written by workflow                 |
| 16                                                       | PRF_Dept                    | Choice               | Yes      | Lookup: `LK_IT_Department`                          | `dept`                                | —                | Requesting department (e.g. HR, FIN, LOG)                |
| 17                                                       | PRF_ExtNo                   | Single line          | No       | —                                                   | `ExtNo`                               | —                | Phone extension for follow-up                            |
| 18                                                       | PRF_CCList                  | Person/Group (Multi) | No       | —                                                   | `cc`                                  | —                | Notification recipients (multi-select)                   |
| **Request Details**                                      |                             |                      |          |                                                     |                                       |                  |                                                          |
| 19                                                       | PRF_System                  | Choice               | Yes      | Lookup: `LK_IT_System`                              | `system`                              | —                | Target system (SAP, Windows, Notes, etc.)                |
| 20                                                       | PRF_RequestType             | Choice               | Yes      | Lookup: `LK_IT_RequestType`                         | `type`                                | —                | Hardware / Software / Access / Project                   |
| 21                                                       | PRF_Site                    | Choice               | Yes      | Lookup: `LK_IT_Site`                                | `site`                                | —                | PRAI / Johor / Both                                      |
| 22                                                       | PRF_Module                  | Single line          | No       | —                                                   | `module`                              | —                | Business module name (optional descriptor)               |
| 23                                                       | PRF_Objective               | Multi-line           | Yes      | —                                                   | `objective`                           | —                | What is the request intended to accomplish?              |
| 24                                                       | PRF_ChangeDescription       | Multi-line           | Yes      | —                                                   | `Remarks`                             | —                | Detailed description of requested change                 |
| 25                                                       | PRF_Implementation          | Single line          | No       | —                                                   | `Implementation`                      | —                | Where/how to apply (e.g., "Production", "Test")          |
| **Access/Security Controls**                             |                             |                      |          |                                                     |                                       |                  |                                                          |
| 26                                                       | PRF_GroupName               | Single line          | No       | —                                                   | `grpname`                             | —                | If requesting group creation, group name                 |
| 27                                                       | PRF_GroupMembers            | Multi-line           | No       | —                                                   | `grpmembers`                          | —                | If group request, list of members to add                 |
| 28                                                       | PRF_Validity                | Choice               | Yes      | `Permanent`, `Temporary`                            | `validity`                            | —                | Is the access/resource permanent or time-bound?          |
| 29                                                       | PRF_ValidTill               | Single line          | No       | Date format `YYYY-MM-DD`                            | `validtill`                           | —                | Expiry date (if Temporary selected)                      |
| **Business Justification**                               |                             |                      |          |                                                     |                                       |                  |                                                          |
| 30                                                       | PRF_Reason                  | Multi-line           | Yes      | —                                                   | `reason`                              | —                | Why is this request needed?                              |
| 31                                                       | PRF_Benefits                | Multi-line           | Yes      | —                                                   | `benefits`                            | —                | What are the business benefits?                          |
| 32                                                       | PRF_ExpectedUsers           | Number               | No       | —                                                   | `noofusers`                           | —                | How many users will use this resource?                   |
| **Submission Tracking**                                  |                             |                      |          |                                                     |                                       |                  |                                                          |
| 33                                                       | PRF_AttachmentUrl           | Single line          | No       | —                                                   | `att`                                 | —                | Main supporting document (e.g., change spec)             |
| 34                                                       | PRF_DateSubmitted           | Single line          | No       | —                                                   | `datesent` (computed: now)            | —                | Timestamp when form submitted                            |
| **Stage 2: HOD/Manager Approval**                        |                             |                      |          |                                                     |                                       |                  |                                                          |
| 35                                                       | PRF_AcceptedBy              | Person/Group         | No       | —                                                   | `depthead`                            | PATTERN-C        | HOD/Manager who approved stage 2                         |
| 36                                                       | PRF_ApprovalStatus1         | Choice               | Yes      | `Pending`, `Approved`, `Rejected`, `Pending-Rework` | `status1`                             | PATTERN-C        | Stage 2 approval outcome                                 |
| 37                                                       | PRF_ApprovalDate1           | Single line          | No       | —                                                   | `dateapp1`                            | PATTERN-C        | When stage 2 approval completed                          |
| 38                                                       | PRF_ApprovalComments1       | Multi-line           | No       | —                                                   | `comments1`                           | PATTERN-C        | Approval remarks or rejection reason                     |
| **Stage 3-4: IT Manager & Technical Assignment**         |                             |                      |          |                                                     |                                       |                  |                                                          |
| 39                                                       | PRF_AssignedITOwner         | Person/Group         | No       | —                                                   | `isg` (IT Support Group lead)         | PATTERN-C        | IT staff assigned to execute                             |
| 40                                                       | PRF_CC_ITAssignment         | Person/Group (Multi) | No       | —                                                   | `CC_ISG`                              | —                | Copy to other IT staff                                   |
| 41                                                       | PRF_IsSAP                   | Choice               | Yes      | `Yes`, `No`                                         | Implied from `isSAP` hidden field     | —                | Does this request involve SAP changes?                   |
| 42                                                       | PRF_RFCNumber               | Single line          | No       | —                                                   | `RFC` (if SAP)                        | —                | RFC ticket number if applicable                          |
| **Stage 4: Functional Submission (if SAP/RFC Required)** |                             |                      |          |                                                     |                                       |                  |                                                          |
| 43                                                       | PRF_FunctionalAttachmentUrl | Single line          | No       | —                                                   | `Attachment_SAP`                      | —                | Mandatory if `IsSAP='Yes'`; contains SAP functional spec |
| 44                                                       | PRF_FunctionalRemarks       | Multi-line           | No       | —                                                   | `Remarks_SAP`                         | —                | Functional notes/validation comments                     |
| 45                                                       | PRF_AttachedBy              | Single line          | No       | —                                                   | `AttachedBy`                          | —                | Staff member who submitted functional docs               |
| 46                                                       | PRF_FunctionalDateSubmitted | Single line          | No       | —                                                   | `dtSubmitted`                         | —                | Timestamp of SAP submission                              |
| **Stage 5: IT Execution & Support**                      |                             |                      |          |                                                     |                                       |                  |                                                          |
| 47                                                       | PRF_ApprovalStatus2         | Choice               | Yes      | `Pending`, `Approved`, `Rejected`, `In Progress`    | `status2`                             | PATTERN-C        | IT acceptance/approval stage                             |
| 48                                                       | PRF_ApprovalBy_ISG          | Person/Group         | No       | —                                                   | `AppBy_ISG`                           | PATTERN-C        | IT staff who approved                                    |
| 49                                                       | PRF_ApprovalDate2           | Single line          | No       | —                                                   | `dateapp2`                            | PATTERN-C        | When IT approval completed                               |
| 50                                                       | PRF_ApprovalComments2       | Multi-line           | No       | —                                                   | `comments2`                           | PATTERN-C        | IT comments or action summary                            |
| 51                                                       | PRF_TaskAttachmentUrl       | Single line          | No       | —                                                   | `TasksAtt`                            | —                | Task work log attachment                                 |
| **Stage 6: User Acceptance & Closure**                   |                             |                      |          |                                                     |                                       |                  |                                                          |
| 52                                                       | PRF_ExpectedCompletionDate  | Single line          | No       | —                                                   | `requiredby`                          | —                | Target completion date (from "Update by IT Approver")    |
| 53                                                       | PRF_CompletionRemarks       | Multi-line           | No       | —                                                   | `remark`                              | —                | IT completion notes                                      |
| 54                                                       | PRF_UpdatedBy               | Single line          | No       | —                                                   | `updby`                               | —                | Last status updater                                      |
| 55                                                       | PRF_UpdatedDate             | Single line          | No       | —                                                   | `upddt`                               | —                | Last update timestamp                                    |
| 56                                                       | PRF_ITReason                | Multi-line           | No       | —                                                   | `ITReason`                            | —                | Reason for delay (if applicable)                         |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `PRF_List` | Browse and search all PRF records | All authorized users |
| `PRF_New` | Create a new Program Request Form (PRF) 2025 request | Initiator / Requestor |
| `PRF_View` | Read-only detail view of a record | All authorized users |
| `PRF_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `PRF_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**PRF_List Screen**
- Gallery displaying all `PRF` records from `MainDB_06 - IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `PRF_New` (visible to Initiator role only).
- Tap a row to navigate to `PRF_View`.

**PRF_New / _Edit Screen**
- Data entry form bound to `MainDB_06 - IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**PRF_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "PRF-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(PRF_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(PRF_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "PRF",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(PRF_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "PRF" &&
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
- **Stage 1:** `Requesting` — performed by `Manual form create + submit`
- **Stage 2:** `Authorizing` — performed by `Status=Submitted`
- **Stage 3:** `Triaging` — performed by `Approval Stage 1 = Approved`
- **Stage 4:** `FunctionReview` — performed by `PRF_IsSAP = Yes; (Optional)`
- **Stage 5:** `Processing` — performed by `Stage 3/4 Complete; PRF_AssignedITOwner assigned`
- **Stage 6:** `Validating` — performed by `Tasks Completed; PRF_ApprovalStatus2 = Approved`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|

### 3. Data Integrity Rules

- `FormCode` must always equal `PRF` (system-enforced constant).
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

- [ ] All SharePoint columns in `MainDB_06 - IT` are created with correct types and required flags.
- [ ] Canvas App screens (`PRF_List`, `PRF_New`, `PRF_View`, `PRF_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
