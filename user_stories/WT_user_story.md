# User Story — Walkie Talkie Equipment Tracking (`WT`)

> **Department:** SEC (Department_18)  
> **Module:** M5 - Equipment Tracking & Maintenance  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_SEC`  
> **Form Code:** `WT`

---

## 1. App Overview & Purpose

WT tracks walkie-talkie equipment inventory, assignment, channel allocation, and access control
across departments for secure communications management. Captures equipment model, serial number,
frequency, location, and person-in-charge; implements approvals for new equipment or access changes;
maintains audit trail of usage and ownership. Used for regulatory compliance and equipment
accountability.

---

---

## 2. User Stories

**US-01: Register equipment and request approval**
> As a **Requester** (member of `D18-SEC-Staff`),  
> I want to **register equipment and request approval** in the `WT` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When item created (CurrentStatus=Registered)

**US-02: Security verify channel/access**
> As a **Security Verifier** (member of `D18-SEC-Verifiers`),  
> I want to **security verify channel/access** in the `WT` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus=Registered (CurrentAction=VERIFICATION)

**US-03: Final assignment to person-in-charge**
> As a **Security Manager** (member of `D18-SEC-Managers`),  
> I want to **final assignment to person-in-charge** in the `WT` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When CurrentStatus=Verified (CurrentAction=ASSIGNMENT)

**US-LIST: Search and filter Walkie Talkie Equipment Tracking records**
> As an **authorized user**,  
> I want to search, filter, and view Walkie Talkie Equipment Tracking records in the list screen,  
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

**Target List:** `MainDB_SEC`

| #   | SP Internal Name | Display Label         | Column Type     | Required | Classification   | Notes                                                          |
| --- | ---------------- | --------------------- | --------------- | -------- | ---------------- | -------------------------------------------------------------- |
| 1   | FormType         | Form Type             | Choice          | Yes      | SYSTEM-COMPUTED  | Fixed value WT                                                 |
| 2   | WTNo             | Walkie Talkie No      | Single line     | Yes      | WORKFLOW-MANAGED | Auto-generated (SEC-WT-YYMM-NNNN)                              |
| 3   | Group            | Department Group      | Single line     | Yes      | USER-ENTERED     | Department/group name; maps Domino Group field                 |
| 4   | Dept             | Specific Department   | Single line     | Yes      | USER-ENTERED     | Sub-department; maps Domino Dept field                         |
| 5   | PIC              | Person-in-Charge Name | Single line     | Yes      | USER-ENTERED     | Equipment owner/manager; maps Domino PIC field                 |
| 6   | Model            | Equipment Model       | Single line     | Yes      | USER-ENTERED     | Walkie-talkie model/type; maps Domino Model field              |
| 7   | SerialNo         | Serial Number         | Single line     | Yes      | USER-ENTERED     | Equipment serial number for traceability; maps Domino SerialNo |
| 8   | Qty              | Quantity              | Number          | Yes      | USER-ENTERED     | Number of units; maps Domino Qty field                         |
| 9   | Channel          | Assigned Channel      | Single line     | Yes      | USER-ENTERED     | Frequency/channel allocation; maps Domino Channel field        |
| 10  | Access           | Access Level          | Choice          | Yes      | USER-ENTERED     | Restricted, Standard, Full; maps Domino Access field           |
| 11  | Location         | Storage Location      | Single line     | No       | USER-ENTERED     | Equipment location/storage; maps Domino Location field         |
| 12  | Frequency        | Operating Frequency   | Single line     | No       | USER-ENTERED     | Technical frequency specification; maps Domino Frequency       |
| 13  | CurrentStatus    | Current Status        | Choice          | Yes      | WORKFLOW-MANAGED | Registered; Verified; Assigned; Recalled; Decommissioned       |
| 14  | CurrentAction    | Current Action        | Single line     | Yes      | WORKFLOW-MANAGED | REGISTRATION, VERIFICATION, ASSIGNMENT, RECALL                 |
| 15  | EnvironmentTag   | Environment           | Choice          | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                                  |
| 16  | DocAuthor        | Created By            | Person or Group | Yes      | SYSTEM-COMPUTED  | Originator of equipment request; system-set on creation        |
| 17  | CDate            | Created Date          | Date and Time   | Yes      | SYSTEM-COMPUTED  | System-set timestamp                                           |
| 18  | SubmitDate       | Submitted On          | Date and Time   | No       | SYSTEM-COMPUTED  | Timestamp when moved to Verification stage                     |
| 19  | ApprovedDate     | Approved On           | Date and Time   | No       | SYSTEM-COMPUTED  | Final approval timestamp                                       |
| 20  | ApprovedBy       | Approved By           | Person or Group | No       | WORKFLOW-MANAGED | Security manager who approved; workflow-set                    |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| WT_List | Browse all walkie-talkie equipment inventory | Gallery, filters by status/department/channel, search |
| WT_New | Register new equipment | Header form (Model, SerialNo, Channel, Access, etc.) |
| WT_View | Read-only equipment detail | Display form, verification/assignment history |
| WT_Edit | Update equipment info (conditional by stage) | Editable sections by role; locked when Assigned |
| WT_Approval | Security verification and assignment decision | Read-only equipment data, Verify/Reject/Assign actions |

### Screen Interaction Details

**WT_List Screen**
- Gallery displaying all `WT` records from `MainDB_SEC`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `WT_New` (visible to Initiator role only).
- Tap a row to navigate to `WT_View`.

**WT_New / _Edit Screen**
- Data entry form bound to `MainDB_SEC`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**WT_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "WT-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(WT_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(WT_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "WT",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(WT_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "WT" &&
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
- **Stage 1:** `Register equipment and request approval` — performed by `Requester`
- **Stage 2:** `Security verify channel/access` — performed by `Security Verifier`
- **Stage 3:** `Final assignment to person-in-charge` — performed by `Security Manager`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Requester / Staff | Contribute |
| Security Verifier | Contribute |
| Security Manager | Contribute |
| SEC Admin | Full Control |
| Reader | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `WT` (system-enforced constant).
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

| Stage        | Flow Name       | Trigger                                          | Actions                                                                                  | Notification Target         |
| ------------ | --------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- | --------------------------- |
| Submit       | SEC_WT_OnSubmit | SP when item created                             | Generate WTNo (SEC-WT-YYMM-NNNN), set CurrentStatus=Registered, set CurrentAction=VERIFY | Security Verifier, Manager  |
| Verify       | SEC_WT_OnVerify | SP when CurrentStatus=Registered and verified OK | Set CurrentStatus=Verified, capture verification metadata, set CurrentAction=ASSIGNMENT  | Security Manager            |
| Reject       | SEC_WT_OnReject | SP when verification fails or access denied      | Set CurrentStatus=Rejected, persist rejection reason, notify Requester                   | Requester, Manager          |
| Assign       | SEC_WT_OnAssign | SP when CurrentStatus=Verified                   | Set CurrentStatus=Assigned, set ApprovedBy & ApprovedDate, lock equipment record         | PIC, Requester, All Readers |
| Recall       | SEC_WT_OnRecall | SP when equipment return requested               | Set CurrentStatus=Recalled, capture return metadata, disable access flags                | PIC, Requester, Manager     |
| Decommission | SEC_WT_OnDecomm | SP when equipment lifecycle ends                 | Set CurrentStatus=Decommissioned, archive record, notify audit trail                     | Manager, Audit Trail        |

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

- [ ] All SharePoint columns in `MainDB_SEC` are created with correct types and required flags.
- [ ] Canvas App screens (`WT_List`, `WT_New`, `WT_View`, `WT_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
