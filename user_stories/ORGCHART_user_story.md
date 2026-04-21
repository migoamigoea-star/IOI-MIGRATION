# User Story — Organisation Charts Documentation Control (`ORGCHART`)

> **Department:** HR  
> **Module:** HR Administration — Document Control  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "ORGCHART"`  
> **Form Code:** `ORGCHART`

---

## 1. App Overview & Purpose

ORGCHART governs the controlled submission, review, and approval of organisation chart documents
within IOI Acidchem. A department submits a new or revised org chart with attached document file,
which is then reviewed by a Verifier, endorsed by an Endorser, and approved by a final Approver.
Each authority level is identified by name, designation, and date. The migrated solution must
preserve the 4-level approval chain, attachment handling, chart numbering, and the final
locked/archived state.

---

---

## 2. User Stories

**US-01: Create & Submit**
> As a **HR Staff** (member of `D05-HR-Staff`),  
> I want to **create & submit** in the `ORGCHART` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Draft' and item submitted

**US-02: Verify / Reject**
> As a **Verifier** (member of `D05-HR-Verifiers`),  
> I want to **verify / reject** in the `ORGCHART` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Submitted' — notify Verifier

**US-03: Endorse / Reject**
> As a **Endorser** (member of `D05-HR-Endorsers`),  
> I want to **endorse / reject** in the `ORGCHART` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Verification' and Verifier approves — notify Endorser

**US-04: Final Approve/Rej**
> As a **Approver** (member of `D05-HR-Approvers`),  
> I want to **final approve/rej** in the `ORGCHART` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Endorsement' and Endorser approves — notify Approver

**US-05: Close**
> As a **System** (member of `—`),  
> I want to **close** in the `ORGCHART` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Approver approves → assign OrgNum, IsLocked=Yes, archive

**US-LIST: Search and filter Organisation Charts Documentation Control records**
> As an **authorized user**,  
> I want to search, filter, and view Organisation Charts Documentation Control records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "ORGCHART"`

| #   | SP Internal Name | Display Label             | Column Type         | Required | Classification   | Source Mapping / Notes                                                 |
| --- | ---------------- | ------------------------- | ------------------- | -------- | ---------------- | ---------------------------------------------------------------------- |
| 1   | Title            | Title                     | Single line text    | Yes      | SYSTEM-COMPUTED  | ORGCHART prefix + OrgChartNum                                          |
| 2   | FormCode         | Form Code                 | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value ORGCHART                                                   |
| 3   | OrgChartNum      | Org Chart Number          | Single line text    | Yes      | USER-ENTERED     | `OrgChartNum` — document control number                                |
| 4   | Division         | Division                  | Single line text    | Yes      | USER-ENTERED     | `div`                                                                  |
| 5   | Department       | Department                | Single line text    | Yes      | USER-ENTERED     | `dept`                                                                 |
| 6   | Section          | Section                   | Single line text    | No       | USER-ENTERED     | `sect`                                                                 |
| 7   | PIC              | Person in Charge          | Single line text    | Yes      | USER-ENTERED     | `pic`                                                                  |
| 8   | Retention        | Retention Period          | Single line text    | No       | USER-ENTERED     | `ret`                                                                  |
| 9   | Attachment       | Org Chart Attachment      | Hyperlink           | Yes      | USER-ENTERED     | `attach` — primary org chart file                                      |
| 10  | Attachment2      | Supporting Attachment     | Hyperlink           | No       | USER-ENTERED     | `attach_1` — supplementary file                                        |
| 11  | PreparedByName   | Prepared By (Name)        | Single line text    | Yes      | USER-ENTERED     | Preparer name                                                          |
| 12  | PreparedByDesig  | Prepared By (Designation) | Single line text    | Yes      | USER-ENTERED     | Preparer designation                                                   |
| 13  | PreparedDate     | Prepared Date             | Date and Time       | Yes      | USER-ENTERED     | Prepared date                                                          |
| 14  | DraftSubBy       | Draft Submitted By        | Person or Group     | Yes      | USER-ENTERED     | `DraftSubBy`                                                           |
| 15  | dtSubmitted      | Date Submitted            | Date and Time       | Yes      | SYSTEM-COMPUTED  | `dtSubmitted`                                                          |
| 16  | ChangesRequired  | Changes Required?         | Yes/No              | No       | USER-ENTERED     | `rbChangesRequired`                                                    |
| 17  | DraftRemarks     | Draft Remarks             | Multiple lines text | No       | USER-ENTERED     | `DraftRemarks`                                                         |
| 18  | DraftRevBy       | Draft Reviewed By         | Person or Group     | No       | USER-ENTERED     | `DraftRevBy`                                                           |
| 19  | OrgSelection     | Org Selection             | Choice              | No       | USER-ENTERED     | `OrgSelection` — type of org chart                                     |
| 20  | Changes          | Changes Summary           | Multiple lines text | No       | USER-ENTERED     | `Changes` — description of changes from prior version                  |
| 21  | HRRemarks        | HR Remarks                | Multiple lines text | No       | WORKFLOW-MANAGED | `HRRem`                                                                |
| 22  | OrgNum           | Final Org Number          | Single line text    | No       | WORKFLOW-MANAGED | `OrgNum` — assigned on approval                                        |
| 23  | VerifiedByName   | Verified By (Name)        | Single line text    | No       | WORKFLOW-MANAGED | Verifier name — Stage 2                                                |
| 24  | VerifiedByDesig  | Verified By (Designation) | Single line text    | No       | WORKFLOW-MANAGED | Verifier designation                                                   |
| 25  | VerifiedDate     | Verified Date             | Date and Time       | No       | WORKFLOW-MANAGED | Verification stamp date                                                |
| 26  | EndorsedByName   | Endorsed By (Name)        | Single line text    | No       | WORKFLOW-MANAGED | Endorser name — Stage 3                                                |
| 27  | EndorsedByDesig  | Endorsed By (Designation) | Single line text    | No       | WORKFLOW-MANAGED | Endorser designation                                                   |
| 28  | EndorsedDate     | Endorsed Date             | Date and Time       | No       | WORKFLOW-MANAGED | Endorsement stamp date                                                 |
| 29  | ApprovedByName   | Approved By (Name)        | Single line text    | No       | WORKFLOW-MANAGED | Approver name — Stage 4                                                |
| 30  | ApprovedByDesig  | Approved By (Designation) | Single line text    | No       | WORKFLOW-MANAGED | Approver designation                                                   |
| 31  | ApprovedDate     | Approved Date             | Date and Time       | No       | WORKFLOW-MANAGED | Approval stamp date                                                    |
| 32  | CurrentStatus    | Current Status            | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, Verification, Endorsement, Approval, Approved        |
| 33  | WorkflowStage    | Workflow Stage            | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=Verification 4=Endorsement 5=Approval 6=Approved |
| 34  | EnvironmentTag   | Environment               | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                        |
| 35  | IsLocked         | Is Locked                 | Yes/No              | No       | WORKFLOW-MANAGED | True after final approval                                              |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| ORGCHART_List | Gallery | List all ORGCHART records with department and status filter |
| ORGCHART_New | Form | Create new org chart submission with attachment upload |
| ORGCHART_View | Read-only | View full record with all approval stages and attachments |
| ORGCHART_Edit | Form | Edit draft before submission |
| ORGCHART_Verify | Approval | Verifier review screen |
| ORGCHART_Endorse | Approval | Endorser review screen |
| ORGCHART_Approve | Approval | Final approver screen |

### Screen Interaction Details

**ORGCHART_List Screen**
- Gallery displaying all `ORGCHART` records from `MainDB_HR **Form Discriminator:** FormCode = "ORGCHART"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ORGCHART_New` (visible to Initiator role only).
- Tap a row to navigate to `ORGCHART_View`.

**ORGCHART_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "ORGCHART"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ORGCHART_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ORGCHART-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(ORGCHART_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ORGCHART_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ORGCHART",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ORGCHART_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ORGCHART" &&
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
- **Stage 2:** `Verify / Reject` — performed by `Verifier`
- **Stage 3:** `Endorse / Reject` — performed by `Endorser`
- **Stage 4:** `Final Approve/Rej` — performed by `Approver`
- **Stage 5:** `Close` — performed by `System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| HR Admins | D05-HR-Staff |
| Verifiers group | D05-HR-Verifiers |
| Endorsers group | D05-HR-Endorsers |
| Approvers group | D05-HR-Approvers |
| HR Manager | D05-HR-Manager |

### 3. Data Integrity Rules

- `FormCode` must always equal `ORGCHART` (system-enforced constant).
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

| Flow Name                    | Trigger                                          | Action                                                                           |
| ---------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------- |
| HR_ORGCHART_OnSubmit         | When Status='Draft' → item submitted             | Stamp dtSubmitted, set Stage=2, notify Verifier group                            |
| HR_ORGCHART_VerifierDecision | When Status='Submitted' and Verifier responds    | If Verify: set Stage=3, notify Endorser; if Reject: return to Draft + notify HR  |
| HR_ORGCHART_EndorserDecision | When Status='Verification' and Endorser responds | If Endorse: set Stage=4, notify Approver; if Reject: return to Draft + notify HR |
| HR_ORGCHART_ApproverDecision | When Status='Endorsement' and Approver responds  | If Approve: assign OrgNum, IsLocked=Yes, Status=Approved; if Reject: → Draft     |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "ORGCHART"` are created with correct types and required flags.
- [ ] Canvas App screens (`ORGCHART_List`, `ORGCHART_New`, `ORGCHART_View`, `ORGCHART_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
