# User Story — Backup Staff Database (`BSD`)

> **Department:** HR (Department_05)  
> **Module:** M3 - Employee Records & Information  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_HR`  
> **Form Code:** `BSD`

---

## 1. App Overview & Purpose

BSD records primary role ownership and the nominated backup staff structure for business continuity.
It captures a primary person-in-charge (PIC) and up to three backup nominees, routing through
department head review and division-level approval. Used for workforce succession planning and
emergency coverage management.

---

---

## 2. User Stories

**US-01: Create and nominate backup staff**
> As a **Initiator / HOD** (member of `D05-HR-Initiators`),  
> I want to **create and nominate backup staff** in the `BSD` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created (CurrentStatus=Draft)

**US-02: Review nomination and request revision or approve**
> As a **Department Head (HOD)** (member of `D05-HR-HOD-Reviewers`),  
> I want to **review nomination and request revision or approve** in the `BSD` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus=Submitted

**US-03: Final approval or rejection**
> As a **Head of Division** (member of `D05-HR-Division-Approvers`),  
> I want to **final approval or rejection** in the `BSD` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus=Revision_Requested OR approved by HOD

**US-LIST: Search and filter Backup Staff Database records**
> As an **authorized user**,  
> I want to search, filter, and view Backup Staff Database records in the list screen,  
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

**Target List:** `MainDB_HR`

| #   | SP Internal Name | Display Label               | Column Type     | Required | Classification   | Notes                                                                  |
| --- | ---------------- | --------------------------- | --------------- | -------- | ---------------- | ---------------------------------------------------------------------- |
| 1   | FormType         | Form Type                   | Choice          | Yes      | SYSTEM-COMPUTED  | Fixed value BSD                                                        |
| 2   | INO              | Reference No.               | Single line     | Yes      | SYSTEM-COMPUTED  | HR-BSD-YYMM-NNNN                                                       |
| 3   | CurrentStatus    | Current Status              | Choice          | Yes      | WORKFLOW-MANAGED | Draft; Submitted; Revision_Requested; Approved; Rejected               |
| 4   | EnvironmentTag   | Environment                 | Choice          | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                                          |
| 5   | Division         | Division                    | Single line     | Yes      | USER-ENTERED     | Organization division; maps Domino Division field                      |
| 6   | Dept             | Department                  | Single line     | Yes      | USER-ENTERED     | Department within division; maps Domino Dept field                     |
| 7   | Section          | Section                     | Single line     | No       | USER-ENTERED     | Sub-section identifier if applicable; maps Domino Section              |
| 8   | PIC              | Main PIC Name               | Single line     | Yes      | USER-ENTERED     | Primary person-in-charge; maps Domino PIC field                        |
| 9   | EmpNo            | Main PIC Employee No        | Single line     | Yes      | USER-ENTERED     | Employee number of main PIC; maps Domino EmpNo                         |
| 10  | Position         | Main PIC Position           | Single line     | Yes      | USER-ENTERED     | Job title/position of main PIC; maps Domino Position                   |
| 11  | Responsibility   | Main PIC Responsibility     | Multiple lines  | Yes      | USER-ENTERED     | Role and responsibility scope; maps Domino Responsibility              |
| 12  | HOD              | Dept Head                   | Person or Group | Yes      | USER-ENTERED     | Department head who nominates; maps Domino HOD field                   |
| 13  | SubmittedBy      | Submitted By                | Person or Group | Yes      | SYSTEM-COMPUTED  | User who submitted the BSD record; system-set on submit                |
| 14  | SubmitDate       | Date Submitted              | Date and Time   | Yes      | SYSTEM-COMPUTED  | Timestamp of submission; system-set                                    |
| 15  | Remark           | Submission Remark           | Multiple lines  | No       | USER-ENTERED     | Comments by initiator/department head; maps Domino Remark              |
| 16  | Revision         | Revision Required           | Yes/No          | No       | WORKFLOW-MANAGED | Set to Yes when HOD requests rework; maps Domino Revision flag         |
| 17  | UpdatedBy        | Updated By                  | Person or Group | No       | SYSTEM-COMPUTED  | Person who performed last revision; system-set                         |
| 18  | UpdatedDt        | Updated Date                | Date and Time   | No       | SYSTEM-COMPUTED  | Timestamp of last update; system-set                                   |
| 19  | Status           | HOD Decision Status         | Choice          | No       | WORKFLOW-MANAGED | Approved; Rejected; Pending; maps Domino Status field                  |
| 20  | StaRem           | HOD Review Remarks          | Multiple lines  | No       | USER-ENTERED     | Comments from HOD during review; maps Domino StaRem                    |
| 21  | HODName          | Division Head Name          | Person or Group | No       | WORKFLOW-MANAGED | Division head who makes final decision; workflow-set at approval stage |
| 22  | HODPost          | Division Head Position      | Single line     | No       | SYSTEM-COMPUTED  | Job title of division head; system-set from directory                  |
| 23  | HODDate          | Division Head Decision Date | Date and Time   | No       | SYSTEM-COMPUTED  | Timestamp of division head approval/rejection; system-set              |
| 24  | HODRemarks       | Division Head Comments      | Multiple lines  | No       | USER-ENTERED     | Approval/rejection remarks from division head; maps Domino HODRemarks  |
| 25  | DocAuthor        | Created By                  | Person or Group | Yes      | SYSTEM-COMPUTED  | Original author/creator; system-set when form initiated                |
| 26  | IsLocked         | Is Locked                   | Yes/No          | No       | WORKFLOW-MANAGED | Set to Yes when approved; prevents further edits                       |


| #   | SP Internal Name     | Display Label         | Column Type        | Required | Notes                                                    |
| --- | -------------------- | --------------------- | ------------------ | -------- | -------------------------------------------------------- |
| 1   | BSDRef               | BSD Reference         | Lookup (MainDB_HR) | Yes      | Parent BSD record pointer; lookup column                 |
| 2   | BackupSeq            | Backup Sequence       | Number             | Yes      | 1, 2, or 3 — ordered sequence                            |
| 3   | BackupName           | Backup Name           | Single line        | Yes      | Backup nominee name; maps Domino PIC_1/2/3 fields        |
| 4   | BackupPosition       | Backup Position       | Single line        | Yes      | Job title of backup; maps Domino Position_1/2/3          |
| 5   | BackupResponsibility | Backup Responsibility | Multiple lines     | Yes      | Scope of backup duties; maps Domino Responsibility_1/2/3 |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| BSD_List | Index of all BSD records with filters | Gallery by division/department/status, search by PIC name |
| BSD_New | Create new BSD record with backup nominees | Header form (Division, Dept, PIC info), child gallery for 3 backup rows |
| BSD_View | Read-only detail view with audit trail | Display form, backup nominees table, readonly approval history |
| BSD_Edit | Stage-specific editing (initiator rework, HOD review, division approval) | Role-based conditional visibility: editable sections for current stage only |
| BSD_Approval | Division approver final decision interface | Approve/Reject buttons, comment input, read-only backup data |

### Screen Interaction Details

**BSD_List Screen**
- Gallery displaying all `BSD` records from `MainDB_HR`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `BSD_New` (visible to Initiator role only).
- Tap a row to navigate to `BSD_View`.

**BSD_New / _Edit Screen**
- Data entry form bound to `MainDB_HR`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**BSD_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "BSD-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(BSD_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(BSD_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "BSD",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(BSD_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "BSD" &&
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
- **Stage 1:** `Create and nominate backup staff` — performed by `Initiator / HOD`
- **Stage 2:** `Review nomination and request revision or approve` — performed by `Department Head (HOD)`
- **Stage 3:** `Final approval or rejection` — performed by `Head of Division`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Domino Field | Permission Level |
| Initiator / HOD nominator | Contribute |
| Department Head (HOD) | Contribute |
| Head of Division | Contribute |
| HR Administrator | Full Control |
| Readers / Viewers | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `BSD` (system-enforced constant).
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

| Stage              | Flow Name              | Trigger                                                                  | Actions                                                                                                             | Notification Target         |
| ------------------ | ---------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| Submit             | HR_BSD_OnSubmit        | SP when item created                                                     | Generate INO (HR-BSD-YYMM-NNNN), set Title from PIC name, set CurrentStatus=Submitted, set SubmitDate               | HOD, division approver      |
| HOD Review Approve | HR_BSD_HODApprove      | SP when CurrentStatus=Submitted and HOD decision=Approve                 | Set Status=Approved (or leave blank), persist HOD remarks in StaRem                                                 | Division Approver           |
| HOD Review Reject  | HR_BSD_HODReject       | SP when CurrentStatus=Submitted and HOD decision=Reject                  | Set Revision=Yes, set CurrentStatus=Revision_Requested, notify Initiator                                            | Initiator                   |
| Division Approve   | HR_BSD_DivisionApprove | SP when CurrentStatus=Revision_Requested OR Status=Approved (HOD signed) | Set CurrentStatus=Approved, set HODName (division approver), set HODDate, set IsLocked=Yes, notify all stakeholders | Initiator, HOD, All Readers |
| Division Reject    | HR_BSD_DivisionReject  | SP when CurrentStatus=Revision_Requested AND division decision=Reject    | Set CurrentStatus=Rejected, set HODName (rejecter), persist HODRemarks, notify Initiator                            | Initiator, HOD              |

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

- [ ] All SharePoint columns in `MainDB_HR` are created with correct types and required flags.
- [ ] Canvas App screens (`BSD_List`, `BSD_New`, `BSD_View`, `BSD_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
