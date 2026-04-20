# User Story — Job Description Documentation Control (`JD`)

> **Department:** HR  
> **Module:** HR Administration — Document Control  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "JD"`  
> **Form Code:** `JD`

---

## 1. App Overview & Purpose

JD manages the controlled authoring, versioning, and approval of Job Descriptions within IOI
Acidchem. HR creates a JD record capturing position details, reporting structure, job summary, and
up to 26 individual duty statements. The form is approved by the HOD and becomes the controlled
document for the position. The migrated solution must normalize the duty statements into a child
table, preserve revision numbering, and maintain a locked final state after HOD approval.

---

---

## 2. User Stories

**US-01: Create & Submit**
> As a **HR Staff** (member of `D05-HR-Staff`),  
> I want to **create & submit** in the `JD` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Draft' and item created

**US-02: HOD Review**
> As a **HOD** (member of `D05-HR-HOD`),  
> I want to **hod review** in the `JD` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Submitted' — notify HOD for approval

**US-03: Approve / Lock**
> As a **System** (member of `—`),  
> I want to **approve / lock** in the `JD` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When HOD approves → IsLocked=Yes, HoldingStatus=Active

**US-LIST: Search and filter Job Description Documentation Control records**
> As an **authorized user**,  
> I want to search, filter, and view Job Description Documentation Control records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "JD"`

| #   | SP Internal Name | Display Label      | Column Type         | Required | Classification   | Source Mapping / Notes                                   |
| --- | ---------------- | ------------------ | ------------------- | -------- | ---------------- | -------------------------------------------------------- |
| 1   | Title            | Title              | Single line text    | Yes      | SYSTEM-COMPUTED  | JD prefix + JobNo                                        |
| 2   | FormCode         | Form Code          | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value JD                                           |
| 3   | JDCategory       | Category           | Choice              | Yes      | USER-ENTERED     | `category` — Executive, Manager, Supervisor, Staff, etc. |
| 4   | HoldingStatus    | Holding Status     | Choice              | No       | USER-ENTERED     | `HStatus` — Active, Superseded, Draft                    |
| 5   | Division         | Division           | Single line text    | Yes      | USER-ENTERED     | `div1`                                                   |
| 6   | Department       | Department         | Single line text    | Yes      | USER-ENTERED     | `department1`                                            |
| 7   | Section          | Section            | Single line text    | No       | USER-ENTERED     | `section`                                                |
| 8   | Company          | Company            | Choice              | Yes      | USER-ENTERED     | `Company` — IOI Oleochemical, IOI Acidchem               |
| 9   | JobNo            | Job No             | Single line text    | Yes      | USER-ENTERED     | `jobno`                                                  |
| 10  | EffectiveDate    | Effective Date     | Date and Time       | Yes      | USER-ENTERED     | `effectdate`                                             |
| 11  | RevisionNo       | Revision Number    | Single line text    | No       | USER-ENTERED     | `revnum` — e.g. Rev.01, Rev.02                           |
| 12  | JobTitle         | Job Title          | Single line text    | Yes      | USER-ENTERED     | `jobtitle`                                               |
| 13  | ReportsTo        | Reports To         | Single line text    | No       | USER-ENTERED     | `repno` — reporting position code                        |
| 14  | JobSummary       | Job Summary        | Multiple lines text | Yes      | USER-ENTERED     | `jobsum`                                                 |
| 15  | HOD              | Head of Department | Person or Group     | Yes      | USER-ENTERED     | HOD approver                                             |
| 16  | CurrentStatus    | Current Status     | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HOD_Approved, Superseded               |
| 17  | WorkflowStage    | Workflow Stage     | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=HOD_Review 4=Approved              |
| 18  | CurrentAction    | Current Action     | Choice              | Yes      | WORKFLOW-MANAGED | Hidden routing field                                     |
| 19  | EnvironmentTag   | Environment        | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                          |
| 20  | IsLocked         | Is Locked          | Yes/No              | No       | WORKFLOW-MANAGED | True after HOD approval                                  |


| #   | SP Internal Name | Display Label    | Column Type         | Required | Notes                                            |
| --- | ---------------- | ---------------- | ------------------- | -------- | ------------------------------------------------ |
| 1   | JDRef            | JD Reference     | Lookup (MainDB_HR)  | Yes      | Links to parent JD record                        |
| 2   | DutySeq          | Duty No          | Number              | Yes      | Sequence 1–26; display order                     |
| 3   | DutyDescription  | Duty Description | Multiple lines text | Yes      | `duties_N` — the duty statement text             |
| 4   | DutyCategory     | Duty Category    | Choice              | No       | Core Duty, Secondary Duty, Administrative, Other |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| JD_List | Gallery | List all JD records with department and status filter |
| JD_New | Form | Create new JD: header + duties child gallery |
| JD_View | Read-only | View full JD with all duty statements |
| JD_Edit | Form | Edit draft JD (header + duties) |
| JD_HODApproval | Approval | HOD approval screen |

### Screen Interaction Details

**JD_List Screen**
- Gallery displaying all `JD` records from `MainDB_HR **Form Discriminator:** FormCode = "JD"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `JD_New` (visible to Initiator role only).
- Tap a row to navigate to `JD_View`.

**JD_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "JD"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**JD_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "JD-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(JD_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(JD_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "JD",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(JD_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "JD" &&
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
- **Stage 1:** `Create & Submit` — performed by `HR Staff`
- **Stage 2:** `HOD Review` — performed by `HOD`
- **Stage 3:** `Approve / Lock` — performed by `System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| HR Admins | D05-HR-Staff |
| HOD group | D05-HR-HOD |
| HR Manager | D05-HR-Manager |

### 3. Data Integrity Rules

- `FormCode` must always equal `JD` (system-enforced constant).
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

| Flow Name         | Trigger                                  | Action                                                                     |
| ----------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| HR_JD_OnSubmit    | When Status='Draft' → item submitted     | Stamp effective date, set Stage=2, notify HOD                              |
| HR_JD_HODDecision | When Status='Submitted' and HOD responds | If Approve: IsLocked=Yes, HoldingStatus=Active; if Reject: return to Draft |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "JD"` are created with correct types and required flags.
- [ ] Canvas App screens (`JD_List`, `JD_New`, `JD_View`, `JD_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
