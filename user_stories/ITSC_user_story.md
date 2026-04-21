# User Story — IT Server Checklist 2025 (`ITSC`)

> **Department:** IT (Department 06)  
> **Module:** M3 – Hardware & Infrastructure  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_IT (Department 06)`  
> **Form Code:** `ITSC`

---

## 1. App Overview & Purpose

`ITSC` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `IT (Department 06)` department at the PRAI site.

---

## 2. User Stories

**US-LIST: Search and filter IT Server Checklist 2025 records**
> As an **authorized user**,  
> I want to search, filter, and view IT Server Checklist 2025 records in the list screen,  
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

**Target List:** `MainDB_IT (Department 06)`

| Column Name  | SP Type         | Required | Notes                                                                         |
| ------------ | --------------- | -------- | ----------------------------------------------------------------------------- |
| ID           | Number          | Yes      | SharePoint system key (auto)                                                  |
| RequestNo    | Text            | Yes      | Business reference: auto-generated as `SC-[YYYY]-[WW]-[INO]`                  |
| FormType     | Choice          | Yes      | Fixed value: `ITSC`                                                           |
| Title        | Text            | Yes      | Auto-mapped from RequestNo or audit date                                      |
| Status       | Choice          | Yes      | Values: `Draft`, `Submitted`, `Under Review`, `Approved`, `Flagged`, `Closed` |
| CurrentStage | Choice          | Yes      | Values: `Stage-1-Monitoring`, `Stage-2-Review`, `Completed`                   |
| Requestor    | Lookup (Person) | Yes      | IT Technician performing the audit (CreatedBy from Domino)                    |
| CreatedOn    | Text            | Yes      | Audit initiation timestamp                                                    |
| CreatedBy    | Lookup (Person) | Yes      | System actor recording submission                                             |
| ModifiedOn   | Text            | No       | Last update timestamp                                                         |
| ModifiedBy   | Lookup (Person) | No       | Last update actor                                                             |


| Column Name               | SP Type | Required | Notes                                                           | Domino Source             |
| ------------------------- | ------- | -------- | --------------------------------------------------------------- | ------------------------- |
| ITSC_ServerName           | Text    | Yes      | Primary server/host name                                        | `svrname`                 |
| ITSC_ServerName2          | Text    | No       | Secondary server name (if multi-node)                           | `svrname2`                |
| ITSC_CPUPercent           | Number  | Yes      | CPU utilization at audit time (0–100)                           | `CPU`                     |
| ITSC_MemoryTotalGB        | Number  | Yes      | Total installed RAM in GB                                       | `FullMemory`              |
| ITSC_Drive1Status         | Text    | Yes      | Drive C: space status (e.g., "120GB Free")                      | `Drive1` / `Size1`        |
| ITSC_Drive2Status         | Text    | No       | Drive D: space status                                           | (Additional drive field)  |
| ITSC_Drive3Status         | Text    | No       | Drive E: space status                                           | (Additional drive field)  |
| ITSC_DiskCleanup          | Choice  | Yes      | Disk cleanup performed? Values: `Yes`, `No`, `Pending`          | `diskcleanup`             |
| ITSC_Defrag               | Choice  | Yes      | Defragmentation needed? Values: `Yes`, `No`, `N/A`              | `Defrag`                  |
| ITSC_WindowsUpdate        | Text    | Yes      | Last Windows Update date/time                                   | `WinUpd`                  |
| ITSC_EventViewerStatus    | Choice  | No       | Event Viewer status: `OK`, `Warnings`, `Critical`               | `Event`                   |
| ITSC_HANAMemoryMB         | Number  | No       | SAP HANA memory usage in MB                                     | `MDC` / `Tenant`          |
| ITSC_HANATenantID         | Text    | No       | HANA Tenant ID or node identifier                               | `Tenant`                  |
| ITSC_HANAVolume1GB        | Number  | No       | HANA Data volume size (GB)                                      | `Volume1`                 |
| ITSC_HANAVolume2GB        | Number  | No       | HANA Log volume size (GB)                                       | `Volume2`                 |
| ITSC_HANAVolume3GB        | Number  | No       | HANA Trace volume size (GB)                                     | `Volume3`                 |
| ITSC_BackupStartDateTime  | Text    | Yes      | Weekly backup start timestamp (ISO 8601)                        | `DateStart` / `TimeStart` |
| ITSC_BackupEndDateTime    | Text    | Yes      | Weekly backup end timestamp (ISO 8601)                          | `DateEnd` / `TimeEnd`     |
| ITSC_NetworkWindowsDomain | Choice  | No       | Windows domain accessible? Values: `Yes`, `No`, `Offline`       | `NW`                      |
| ITSC_VirusDefStatus       | Choice  | No       | Virus definition status: `Current`, `OutOfDate`, `Scan Pending` | `nav`                     |
| ITSC_Remarks              | Text    | No       | Audit notes and observations                                    | `remarks`                 |
| ITSC_AttachmentUrl        | Text    | No       | Link to health dashboard PDF or screenshot                      | `Attachment`              |
| ITSC_CurrencyYear         | Number  | No       | Current business year                                           | `CurrYear`                |
| ITSC_WeekEndDate          | Text    | Yes      | Week ending date (ISO 8601, auto computed)                      | `WeekEndDate`             |
| ITSC_YearStartDate        | Text    | No       | Fiscal year start date                                          | `YearStartDate`           |
| ITSC_WeekNum              | Number  | Yes      | ISO week number (auto computed from `CreatedOn`)                | `Week`                    |
| ITSC_WeekDay              | Choice  | No       | Day of week: `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`, `Sun`    | `WkDay`                   |
| ITSC_OrganizationalUnit   | Text    | No       | OU designation for AD/infrastructure context                    | `OU`                      |


| Column Name              | SP Type         | Required | Notes                                               |
| ------------------------ | --------------- | -------- | --------------------------------------------------- |
| ITSC_Stage1SubmittedBy   | Lookup (Person) | No       | IT Technician who submitted audit                   |
| ITSC_Stage1SubmittedDate | Text            | No       | Submission timestamp                                |
| ITSC_Stage2ReviewedBy    | Lookup (Person) | No       | Systems Manager who reviewed                        |
| ITSC_Stage2ReviewDate    | Text            | No       | Review completion date                              |
| ITSC_Stage2Approval      | Choice          | No       | Stage 2 decision: `Approved`, `Flagged`, `Rejected` |
| ITSC_FlaggedReason       | Text            | No       | If flagged, capture issue description               |
| ITSC_ApprovedForArchive  | Choice          | No       | Final archival decision: `Yes`, `No`                |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `ITSC_List` | Browse and search all ITSC records | All authorized users |
| `ITSC_New` | Create a new IT Server Checklist 2025 request | Initiator / Requestor |
| `ITSC_View` | Read-only detail view of a record | All authorized users |
| `ITSC_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `ITSC_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**ITSC_List Screen**
- Gallery displaying all `ITSC` records from `MainDB_IT (Department 06)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ITSC_New` (visible to Initiator role only).
- Tap a row to navigate to `ITSC_View`.

**ITSC_New / _Edit Screen**
- Data entry form bound to `MainDB_IT (Department 06)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ITSC_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ITSC-" & Text(Now(), "YYYYMMDD-HHMMSS"))
```

### 2. Required Field Validation

```powerfx
// Submit button IsDisplayMode check — disable if any required field is empty
DisplayMode: If(
    IsBlank(ID) Or
    IsBlank(RequestNo) Or
    IsBlank(Status) Or
    IsBlank(CurrentStage) Or
    IsBlank(Requestor) Or
    IsBlank(CreatedOn),
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
Navigate(ITSC_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ITSC_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ITSC",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ITSC_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ITSC" &&
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

### 3. Data Integrity Rules

- `FormCode` must always equal `ITSC` (system-enforced constant).
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

- [ ] All SharePoint columns in `MainDB_IT (Department 06)` are created with correct types and required flags.
- [ ] Canvas App screens (`ITSC_List`, `ITSC_New`, `ITSC_View`, `ITSC_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
