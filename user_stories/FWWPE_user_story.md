# User Story — Foreign Worker Work Period Extension (`FWWPE`)

> **Department:** HR  
> **Module:** Employee Lifecycle — Foreign Worker Management  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "FWWPE"`  
> **Form Code:** `FWWPE`

---

## 1. App Overview & Purpose

FWWPE manages the process of extending a foreign worker's work permit period within IOI Acidchem. HR
or the immediate supervisor submits the extension request with passport and work permit details,
which is reviewed and signed off by the Head of Section (HOS) and Head of Department (HOD). The
migrated solution must preserve dual-approver attribution, work permit expiry date tracking, and a
final contractor status flag for compliance and permit renewal records.

---

---

## 2. User Stories

**US-01: Create & Submit**
> As a **HR or Supervisor** (member of `D05-HR-Staff`),  
> I want to **create & submit** in the `FWWPE` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Draft' and item created

**US-02: HOS Approve / Reject**
> As a **Head of Section** (member of `D05-HR-HOS`),  
> I want to **hos approve / reject** in the `FWWPE` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Submitted' — notify HOS via adaptive card

**US-03: HOD Approve / Reject**
> As a **Head of Department** (member of `D05-HR-HOD`),  
> I want to **hod approve / reject** in the `FWWPE` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='HOS_Review' and HOS approves — notify HOD

**US-04: Close**
> As a **System** (member of `—`),  
> I want to **close** in the `FWWPE` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When HOD approves → set ContStatus=Extended, IsLocked=Yes

**US-LIST: Search and filter Foreign Worker Work Period Extension records**
> As an **authorized user**,  
> I want to search, filter, and view Foreign Worker Work Period Extension records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "FWWPE"`

| #   | SP Internal Name  | Display Label           | Column Type         | Required | Classification   | Source Mapping / Notes                                            |
| --- | ----------------- | ----------------------- | ------------------- | -------- | ---------------- | ----------------------------------------------------------------- |
| 1   | Title             | Title                   | Single line text    | Yes      | SYSTEM-COMPUTED  | FWWPE prefix + EmpNo                                              |
| 2   | FormCode          | Form Code               | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value FWWPE                                                 |
| 3   | IssueNo           | Issue No                | Single line text    | No       | SYSTEM-COMPUTED  | `IssueNo` — auto-generated on submit                              |
| 4   | SendTo            | Send To                 | Person or Group     | No       | USER-ENTERED     | `SendTo` — notification recipient                                 |
| 5   | HOS               | Head of Section         | Person or Group     | Yes      | USER-ENTERED     | `HOS`                                                             |
| 6   | HOD               | Head of Department      | Person or Group     | Yes      | USER-ENTERED     | `HOD`                                                             |
| 7   | CC                | CC Recipients           | Multiple lines text | No       | USER-ENTERED     | `CC` — additional email addresses                                 |
| 8   | Company           | Company                 | Choice              | Yes      | USER-ENTERED     | `Company` — IOI Oleochemical, IOI Acidchem                        |
| 9   | EmpName           | Employee Name           | Single line text    | Yes      | USER-ENTERED     | `Name`                                                            |
| 10  | EmpNo             | Employee No             | Single line text    | Yes      | USER-ENTERED     | `EmpNo`                                                           |
| 11  | PassportNo        | Passport Number         | Single line text    | Yes      | USER-ENTERED     | `PassportNo`                                                      |
| 12  | Department        | Department              | Single line text    | Yes      | USER-ENTERED     | `Department`                                                      |
| 13  | Section           | Section                 | Single line text    | No       | USER-ENTERED     | `Section`                                                         |
| 14  | WPExpiryDate      | Work Permit Expiry Date | Date and Time       | Yes      | USER-ENTERED     | `WPExpDate`                                                       |
| 15  | ExtensionDateFrom | Extension From Date     | Date and Time       | Yes      | USER-ENTERED     | `DateF`                                                           |
| 16  | ExtensionDateTo   | Extension To Date       | Date and Time       | Yes      | USER-ENTERED     | `DateT`                                                           |
| 17  | ReplyRemark       | Reply Remarks           | Multiple lines text | No       | USER-ENTERED     | `ReplyRemark` — remarks on approval                               |
| 18  | HOSStatus         | HOS Status              | Choice              | No       | WORKFLOW-MANAGED | `HOSStatus` — Pending, Approved, Rejected                         |
| 19  | ContStatus        | Contractor Status       | Choice              | No       | WORKFLOW-MANAGED | `ContStatus` — Active, Expired, Extended                          |
| 20  | HODStatus         | HOD Status              | Choice              | No       | WORKFLOW-MANAGED | `HODStatus` — Pending, Approved, Rejected                         |
| 21  | CurrentStatus     | Current Status          | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HOS_Review, HOD_Review, Approved, Rejected      |
| 22  | WorkflowStage     | Workflow Stage          | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=HOS_Review 4=HOD_Review 5=Approved/Rejected |
| 23  | CurrentAction     | Current Action          | Choice              | Yes      | WORKFLOW-MANAGED | Hidden routing field                                              |
| 24  | EnvironmentTag    | Environment             | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                   |
| 25  | IsLocked          | Is Locked               | Yes/No              | No       | WORKFLOW-MANAGED | True after HOD decision                                           |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| FWWPE_List | Gallery | List all FWWPE records with status filter |
| FWWPE_New | Form | New extension request |
| FWWPE_View | Read-only | View extension record details |
| FWWPE_Edit | Form | Edit draft before submission |
| FWWPE_HOSApproval | Approval | HOS decision: Approve / Reject |
| FWWPE_HODApproval | Approval | HOD final decision |

### Screen Interaction Details

**FWWPE_List Screen**
- Gallery displaying all `FWWPE` records from `MainDB_HR **Form Discriminator:** FormCode = "FWWPE"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `FWWPE_New` (visible to Initiator role only).
- Tap a row to navigate to `FWWPE_View`.

**FWWPE_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "FWWPE"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**FWWPE_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "FWWPE-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(FWWPE_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(FWWPE_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "FWWPE",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(FWWPE_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "FWWPE" &&
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
- **Stage 1:** `Create & Submit` — performed by `HR or Supervisor`
- **Stage 2:** `HOS Approve / Reject` — performed by `Head of Section`
- **Stage 3:** `HOD Approve / Reject` — performed by `Head of Department`
- **Stage 4:** `Close` — performed by `System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| HR Admins | D05-HR-Staff |
| HOS group | D05-HR-HOS |
| HOD group | D05-HR-HOD |
| HR Manager | D05-HR-Manager |

### 3. Data Integrity Rules

- `FormCode` must always equal `FWWPE` (system-enforced constant).
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

| Flow Name            | Trigger                                   | Action                                                                          |
| -------------------- | ----------------------------------------- | ------------------------------------------------------------------------------- |
| HR_FWWPE_OnSubmit    | When Status='Draft' → item submitted      | Generate IssueNo, stamp date, set Stage=2, notify HOS                           |
| HR_FWWPE_HOSDecision | When Status='Submitted' and HOS responds  | If Approve: set HOSStatus=Approved, Stage=3, notify HOD; if Reject: lock+notify |
| HR_FWWPE_HODDecision | When Status='HOS_Review' and HOD responds | If Approve: set ContStatus=Extended, IsLocked=Yes; if Reject: notify submitter  |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "FWWPE"` are created with correct types and required flags.
- [ ] Canvas App screens (`FWWPE_List`, `FWWPE_New`, `FWWPE_View`, `FWWPE_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
