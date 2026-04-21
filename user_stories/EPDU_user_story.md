# User Story — Employee Personal Detail Update (`EPDU`)

> **Department:** HR  
> **Module:** Employee Lifecycle — Personal Data Management  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "EPDU"`  
> **Form Code:** `EPDU`

---

## 1. App Overview & Purpose

EPDU allows employees to submit updates to their personal data stored in the HR system — including
address, emergency contacts, marital status, statutory numbers (EPF/SOCSO/income tax), education
history, children details, and family emergency contacts. HR reviews the submission and confirms the
update in the HR master record. The migrated solution must normalize the repeating education,
children, and family sections into child tables and preserve the 2-stage submit-and-review flow.

---

---

## 2. User Stories

**US-01: Create & Submit**
> As a **Employee** (member of `D05-HR-Staff`),  
> I want to **create & submit** in the `EPDU` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Draft' and employee submits

**US-02: HR Review**
> As a **HR Admin** (member of `D05-HR-Manager`),  
> I want to **hr review** in the `EPDU` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Submitted' — notify HR for review

**US-03: Confirm / Reject**
> As a **System** (member of `—`),  
> I want to **confirm / reject** in the `EPDU` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When HR confirms: IsLocked=Yes, Status=Updated; if Reject: notify employee

**US-LIST: Search and filter Employee Personal Detail Update records**
> As an **authorized user**,  
> I want to search, filter, and view Employee Personal Detail Update records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "EPDU"`

| #   | SP Internal Name | Display Label        | Column Type         | Required | Classification   | Source Mapping / Notes                             |
| --- | ---------------- | -------------------- | ------------------- | -------- | ---------------- | -------------------------------------------------- |
| 1   | Title            | Title                | Single line text    | Yes      | SYSTEM-COMPUTED  | EPDU prefix + EmpNo                                |
| 2   | FormCode         | Form Code            | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value EPDU                                   |
| 3   | EmpNo            | Employee No          | Single line text    | Yes      | USER-ENTERED     | `EmpNo`                                            |
| 4   | Company          | Company              | Choice              | Yes      | USER-ENTERED     | `Company` — IOI Oleochemical, IOI Acidchem         |
| 5   | EmpName          | Employee Name        | Single line text    | Yes      | USER-ENTERED     | `EmpName`                                          |
| 6   | NRIC_Old         | NRIC (Old)           | Single line text    | No       | USER-ENTERED     | `NRIC_O`                                           |
| 7   | NRIC_New         | NRIC (New/Current)   | Single line text    | Yes      | USER-ENTERED     | `NRIC_N`                                           |
| 8   | MaritalStatus    | Marital Status       | Choice              | Yes      | USER-ENTERED     | `Marital` — Single, Married, Divorced, Widowed     |
| 9   | Disabilities     | Disabilities         | Single line text    | No       | USER-ENTERED     | `Disabilities`                                     |
| 10  | Address1         | Address Line 1       | Single line text    | Yes      | USER-ENTERED     | `Address1`                                         |
| 11  | Address2         | Address Line 2       | Single line text    | No       | USER-ENTERED     | `Address2`                                         |
| 12  | Postcode1        | Postcode (Permanent) | Single line text    | No       | USER-ENTERED     | `Poscode1`                                         |
| 13  | Postcode2        | Postcode (Mailing)   | Single line text    | No       | USER-ENTERED     | `Poscode2`                                         |
| 14  | TelNo1           | Tel No 1             | Single line text    | No       | USER-ENTERED     | `TelNo1`                                           |
| 15  | TelNo2           | Tel No 2             | Single line text    | No       | USER-ENTERED     | `TelNo2`                                           |
| 16  | EPFNo            | EPF Number           | Single line text    | No       | USER-ENTERED     | `EPF`                                              |
| 17  | SOCSONo          | SOCSO Number         | Single line text    | No       | USER-ENTERED     | `SOCSO`                                            |
| 18  | IncomeTaxNo      | Income Tax Number    | Single line text    | No       | USER-ENTERED     | `ITAX`                                             |
| 19  | SpouseName       | Spouse Name          | Single line text    | No       | USER-ENTERED     | `SpName`                                           |
| 20  | SpouseNRIC       | Spouse NRIC          | Single line text    | No       | USER-ENTERED     | `SpNRIC_N`                                         |
| 21  | SpouseWork       | Spouse Workplace     | Single line text    | No       | USER-ENTERED     | `SpWork`                                           |
| 22  | SpouseOccupation | Spouse Occupation    | Single line text    | No       | USER-ENTERED     | `SpOccupation`                                     |
| 23  | HRRemarks        | HR Review Remarks    | Multiple lines text | No       | WORKFLOW-MANAGED | HR comments on update request                      |
| 24  | CurrentStatus    | Current Status       | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HR_Review, Updated, Rejected     |
| 25  | WorkflowStage    | Workflow Stage       | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=HR_Review 4=Updated/Rejected |
| 26  | EnvironmentTag   | Environment          | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                    |
| 27  | IsLocked         | Is Locked            | Yes/No              | No       | WORKFLOW-MANAGED | True after HR confirms update                      |


| #   | SP Internal Name | Display Label    | Column Type        | Required | Notes                       |
| --- | ---------------- | ---------------- | ------------------ | -------- | --------------------------- |
| 1   | EPDURef          | EPDU Reference   | Lookup (MainDB_HR) | Yes      | Links to parent EPDU record |
| 2   | EduSeq           | Entry No         | Number             | Yes      | Sequence 1–5                |
| 3   | Institution      | Institution Name | Single line text   | Yes      | School/university name      |
| 4   | Qualification    | Qualification    | Single line text   | Yes      | Degree/cert obtained        |
| 5   | FieldOfStudy     | Field of Study   | Single line text   | No       | Major/specialisation        |
| 6   | YearCompleted    | Year Completed   | Number             | No       | 4-digit year                |
| 7   | Grade            | Grade / CGPA     | Single line text   | No       | Result/grade/CGPA           |


| #   | SP Internal Name | Display Label  | Column Type        | Required | Notes                       |
| --- | ---------------- | -------------- | ------------------ | -------- | --------------------------- |
| 1   | EPDURef          | EPDU Reference | Lookup (MainDB_HR) | Yes      | Links to parent EPDU record |
| 2   | ChildSeq         | Child No       | Number             | Yes      | Sequence 1–8                |
| 3   | ChildName        | Child Name     | Single line text   | Yes      |                             |
| 4   | ChildNRIC        | Child NRIC     | Single line text   | No       |                             |
| 5   | ChildDOB         | Date of Birth  | Date and Time      | No       |                             |
| 6   | ChildGender      | Gender         | Choice             | No       | Male, Female                |


| #   | SP Internal Name | Display Label  | Column Type        | Required | Notes                          |
| --- | ---------------- | -------------- | ------------------ | -------- | ------------------------------ |
| 1   | EPDURef          | EPDU Reference | Lookup (MainDB_HR) | Yes      | Links to parent EPDU record    |
| 2   | FamilySeq        | Entry No       | Number             | Yes      | Sequence 1–10                  |
| 3   | FamilyName       | Name           | Single line text   | Yes      |                                |
| 4   | FamilyNRIC       | NRIC           | Single line text   | No       |                                |
| 5   | Relationship     | Relationship   | Choice             | Yes      | Parent, Sibling, Spouse, Other |
| 6   | ContactNo        | Contact Number | Single line text   | No       |                                |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| EPDU_List | Gallery | List employee's own EPDU records with status filter |
| EPDU_New | Form | New personal detail update with child section galleries |
| EPDU_View | Read-only | View submitted/confirmed personal detail update |
| EPDU_Edit | Form | Edit draft before submission |
| EPDU_HRReview | Approval | HR review and confirmation screen |

### Screen Interaction Details

**EPDU_List Screen**
- Gallery displaying all `EPDU` records from `MainDB_HR **Form Discriminator:** FormCode = "EPDU"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `EPDU_New` (visible to Initiator role only).
- Tap a row to navigate to `EPDU_View`.

**EPDU_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "EPDU"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**EPDU_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "EPDU-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(EPDU_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(EPDU_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "EPDU",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(EPDU_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "EPDU" &&
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
- **Stage 1:** `Create & Submit` — performed by `Employee`
- **Stage 2:** `HR Review` — performed by `HR Admin`
- **Stage 3:** `Confirm / Reject` — performed by `System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| All Employees | D05-HR-Staff |
| HR Admins | D05-HR-Manager |

### 3. Data Integrity Rules

- `FormCode` must always equal `EPDU` (system-enforced constant).
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

| Flow Name        | Trigger                                 | Action                                                               |
| ---------------- | --------------------------------------- | -------------------------------------------------------------------- |
| HR_EPDU_OnSubmit | When Status='Draft' → employee submits  | Stamp date, set Stage=2, notify HR Admin                             |
| HR_EPDU_HRReview | When Status='Submitted' and HR responds | If Confirm: IsLocked=Yes, Status=Updated; if Reject: notify employee |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "EPDU"` are created with correct types and required flags.
- [ ] Canvas App screens (`EPDU_List`, `EPDU_New`, `EPDU_View`, `EPDU_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
