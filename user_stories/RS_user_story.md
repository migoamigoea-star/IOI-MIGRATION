# User Story — Reset Password/Unlock ID (`RS`)

> **Department:** IT (D06)  
> **Module:** M1 - User & Access Management  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT (D06)`  
> **Form Code:** `RS`

---

## 1. App Overview & Purpose

`RS` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `IT (D06)` department at the PRAI site.

---

## 2. User Stories

**US-LIST: Search and filter Reset Password/Unlock ID records**
> As an **authorized user**,  
> I want to search, filter, and view Reset Password/Unlock ID records in the list screen,  
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

**Target List:** `MainDB_IT (D06)`

| #   | Column Name | SP Type     | Required | Source Domino Field        | Notes                                        |
| --- | ----------- | ----------- | -------- | -------------------------- | -------------------------------------------- |
| 1   | ID          | Number      | Yes      | System                     | SharePoint system key                        |
| 2   | Title       | Single line | Yes      | FormType filled as "RS"    | Business reference (visible in search)       |
| 3   | FormType    | Choice      | Yes      | Fixed = "RS"               | Determines context for form-specific columns |
| 4   | Status      | Choice      | Yes      | `finalstatus` / `edstatus` | Workflow-managed across stages               |


| #   | Column Name        | SP Type     | Required | Source Domino Field | Choice Values / Notes                                         |
| --- | ------------------ | ----------- | -------- | ------------------- | ------------------------------------------------------------- |
| 5   | RS_EmployeeName    | Single line | Yes      | `empname`           | Requestor's full name                                         |
| 6   | RS_Designation     | Single line | Yes      | `designation`       | Job title of requestor                                        |
| 7   | RS_Company         | Choice      | Yes      | `coname`            | IOI entity (ACIDCHEM, IOI Oleochem, etc.)                     |
| 8   | RS_Department      | Choice      | Yes      | `dept`              | Department requesting reset                                   |
| 9   | RS_Phone           | Single line | No       | `phnum`             | Extension or direct dial                                      |
| 10  | RS_ApplicationType | Choice      | Yes      | `type`              | Acidchem Domain ID, SAP, Weighbridge, Sales Portal, HCL Notes |
| 11  | RS_ClientID        | Single line | No       | `Client`            | Client identifier if app requires it                          |
| 12  | RS_ClientNumber    | Single line | No       | `ClientName`        | Account/client number if app-specific                         |
| 13  | RS_Bank            | Choice      | No       | `Bank`              | Bank selector (if bank-related module involved)               |
| 14  | RS_Justification   | Multi-line  | Yes      | `Justification`     | Reason for password reset/unlock request                      |
| 15  | RS_Attachment      | Hyperlink   | No       | `Attachment`        | Supporting evidence/documentation                             |
| 16  | RS_LoginID         | Single line | Yes      | `LoginID`           | User ID to reset or unlock                                    |
| 17  | RS_UnlockType      | Choice      | No       | `Unlock`            | Reset, Unlock, or Reset+Unlock                                |
| 18  | RS_DateSubmitted   | Date/Time   | Yes      | `datecreated`       | System-captured submission timestamp                          |


| #   | Column Name        | SP Type      | Required | Source Domino Field | Notes                                                       |
| --- | ------------------ | ------------ | -------- | ------------------- | ----------------------------------------------------------- |
| 19  | RS_ITStatus        | Choice       | No       | `finalstatus`       | Pending, In Progress, Completed, Failed                     |
| 20  | RS_ITProcessedDate | Date/Time    | No       | `datecre`           | Date IT action was completed                                |
| 21  | RS_ITProcessedBy   | Person/Group | No       | `isname`            | IT admin who performed the reset                            |
| 22  | RS_ITRemarks       | Multi-line   | No       | `rem`               | IT notes (e.g., "Password reset successful", error details) |


| #   | Column Name        | SP Type      | Required | Source Domino Field | Notes                                        |
| --- | ------------------ | ------------ | -------- | ------------------- | -------------------------------------------- |
| 23  | RS_EDStatus        | Choice       | No       | `edstatus`          | Pending, Approved, Rejected (ED-only paths)  |
| 24  | RS_EDProcessedDate | Date/Time    | No       | `eddate`            | Date ED reviewer completed action            |
| 25  | RS_EDProcessedBy   | Person/Group | No       | `edname`            | ED actor (bank coordinator)                  |
| 26  | RS_EDRemarks       | Multi-line   | No       | `edrem`             | ED notes (compliance check, approval reason) |


| #   | Column Name         | SP Type              | Required | Source Domino Field | Notes                                                                               |
| --- | ------------------- | -------------------- | -------- | ------------------- | ----------------------------------------------------------------------------------- |
| 27  | RS_CurrentAction    | Choice               | Yes      | `CurrentAction`     | Hidden workflow state key; controls trigger routing                                 |
| 28  | RS_FinalStatus      | Choice               | Yes      | `status`            | Hidden terminal status (completed, failed, pending branch)                          |
| 29  | RS_DocumentAuthor   | Person/Group         | No       | `DocumentAuthor`    | System-captured original submitter                                                  |
| 30  | RS_Requestor        | Person/Group         | No       | `docauthor`         | Hidden requestor author reference                                                   |
| 31  | RS_Initiator        | Person/Group         | No       | `requestor`         | Hidden initiator role alias                                                         |
| 32  | RS_EmailRecipients  | Person/Group (multi) | No       | `receivers`         | Hidden recipient distribution list for notifications                                |
| 33  | RS_PasswordGuidance | Single line          | No       | `Pswd`              | Guidance text (never expose actual passwords; use Power Automate secret management) |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `RS_List` | Browse and search all RS records | All authorized users |
| `RS_New` | Create a new Reset Password/Unlock ID request | Initiator / Requestor |
| `RS_View` | Read-only detail view of a record | All authorized users |
| `RS_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `RS_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**RS_List Screen**
- Gallery displaying all `RS` records from `MainDB_IT (D06)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `RS_New` (visible to Initiator role only).
- Tap a row to navigate to `RS_View`.

**RS_New / _Edit Screen**
- Data entry form bound to `MainDB_IT (D06)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**RS_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "RS-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(RS_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(RS_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "RS",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(RS_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "RS" &&
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

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Domino Group/Role | HTTP Access |
| All authenticated users (Requestor) | Yes |
| IT Technical Staff | Yes |
| ED / Bank Coordinator | Yes |
| IT Administrator | Yes |
| Read-only Recipients | Yes |

### 3. Data Integrity Rules

- `FormCode` must always equal `RS` (system-enforced constant).
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

- [ ] All SharePoint columns in `MainDB_IT (D06)` are created with correct types and required flags.
- [ ] Canvas App screens (`RS_List`, `RS_New`, `RS_View`, `RS_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
