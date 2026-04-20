# User Story — HR Notice / Information (`HRINFO`)

> **Department:** HR (Department_05)  
> **Module:** M1 — General Administration & Facilities  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_HR (Department_05)`  
> **Form Code:** `HRINFO`

---

## 1. App Overview & Purpose

`HRINFO` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `HR (Department_05)` department at the PRAI site.

---

## 2. User Stories

**US-LIST: Search and filter HR Notice / Information records**
> As an **authorized user**,  
> I want to search, filter, and view HR Notice / Information records in the list screen,  
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

**Target List:** `MainDB_HR (Department_05)`

| #   | Column Name      | SP Type                 | Required | Choices / Source         | Notes                                                                                                |
| --- | ---------------- | ----------------------- | -------- | ------------------------ | ---------------------------------------------------------------------------------------------------- |
| 1   | Title            | Single line of text     | Yes      | —                        | Auto-populated: `"HRINFO-" & INO`; display name in gallery                                           |
| 2   | INO              | Single line of text     | Yes      | —                        | System-computed via Power Automate (format: `HR-INF-YYMM-NNNN`); **PATTERN-E** — never set in canvas |
| 3   | FormType         | Single line of text     | Yes      | HRINFO                   | Fixed value to distinguish HRINFO records in shared MainDB_HR                                        |
| 4   | Subject          | Single line of text     | Yes      | —                        | Notice headline / subject (Domino: Subject)                                                          |
| 5   | Recipients       | Person or Group (multi) | Yes      | —                        | Primary target staff/departments (Domino: Send)                                                      |
| 6   | CC               | Person or Group (multi) | No       | —                        | Secondary notification recipients (Domino: CC)                                                       |
| 7   | Body             | Multiple lines of text  | Yes      | —                        | Announcement message body with rich text (Domino: Body/Announcement)                                 |
| 8   | ContactExt       | Single line of text     | No       | —                        | HR contact extension number (Domino: Ext)                                                            |
| 9   | Attachment       | Attachment              | No       | —                        | Supporting image or PDF notice (Domino: Att)                                                         |
| 10  | ReadCount        | Number                  | No       | —                        | Running count of staff who clicked "Read" (Domino: CtrLst; PA-incremented)                           |
| 11  | BeneficialUsers  | Person or Group (multi) | No       | —                        | Staff who clicked "Beneficial" engagement action (Domino: LkLst)                                     |
| 12  | DisseminateUsers | Person or Group (multi) | No       | —                        | Staff who clicked "Disseminate" engagement action (Domino: DslkLst)                                  |
| 13  | TotalViews       | Number                  | No       | —                        | Persistence view counter (Domino: Viewed; PA-incremented on each view)                               |
| 14  | HRHOD            | Person or Group         | Yes      | —                        | HR Manager / final admin sign-off (Domino: HRHOD)                                                    |
| 15  | HRAuthor         | Person or Group         | Yes      | —                        | HR Author who published the notice (Domino: HR/DocAuthor; auto-populated from logged-in user)        |
| 16  | PublishedDate    | Date and Time           | No       | —                        | Date notice was posted/broadcast (PA-set on post action)                                             |
| 17  | LockDate         | Date and Time           | No       | —                        | Auto-lock date = PublishedDate + 30 days (PA-set on post)                                            |
| 18  | IsLocked         | Yes/No                  | No       | —                        | Record locked flag (Domino: Lock; PA-set on auto-lock trigger)                                       |
| 19  | CurrentStatus    | Choice                  | Yes      | Draft; Published; Locked | Master workflow status (PA-managed)                                                                  |
| 20  | CurrentAction    | Choice                  | Yes      | Draft; Publish; Lock     | Active workflow action (PA-managed; sourced from Domino CurrentAction)                               |
| 21  | EnvironmentTag   | Choice                  | No       | DEV; TEST; PROD          | Three-tier environment strategy (DEC-004)                                                            |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| HRINFO_Feed | Social-style newsfeed of published notices | Gallery/Carousel, filter by date, search by subject, engagement badges |
| HRINFO_Detail | Immersive notice reading view | Display form with Body, Attachment viewer, Engagement action buttons (Read / Beneficial / Disseminate), view counter |
| HRINFO_New | New notice composer | Edit form: Subject, Recipients, CC, Body (rich text editor), Attachment, ContactExt |
| HRINFO_Analytics | Engagement analytics for HR management | View count, Beneficial list, Disseminate list, Read count per notice |

### Screen Interaction Details

**HRINFO_List Screen**
- Gallery displaying all `HRINFO` records from `MainDB_HR (Department_05)`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `HRINFO_New` (visible to Initiator role only).
- Tap a row to navigate to `HRINFO_View`.

**HRINFO_New / _Edit Screen**
- Data entry form bound to `MainDB_HR (Department_05)`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**HRINFO_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "HRINFO-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(HRINFO_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(HRINFO_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "HRINFO",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(HRINFO_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "HRINFO" &&
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

- `FormCode` must always equal `HRINFO` (system-enforced constant).
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

| Flow                        | Trigger                                                  | Actions                                                                                                                                                                             |
| --------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HRINFO_OnPublish            | Item created/updated with CurrentAction = Publish        | Generate INO (HR-INF-YYMM-NNNN), set PublishedDate, set LockDate (+30d), set CurrentStatus = Published, send personalised email to each recipient in Recipients + CC with deep-link |
| HRINFO_OnEngage_Read        | HTTP trigger from Power App (staff clicks "Read")        | Increment ReadCount on MainDB_HR record                                                                                                                                             |
| HRINFO_OnEngage_Beneficial  | HTTP trigger from Power App (staff clicks "Beneficial")  | Append current user to BeneficialUsers                                                                                                                                              |
| HRINFO_OnEngage_Disseminate | HTTP trigger from Power App (staff clicks "Disseminate") | Append current user to DisseminateUsers                                                                                                                                             |
| HRINFO_OnView               | HTTP trigger from Power App (record opened)              | Increment TotalViews                                                                                                                                                                |
| HRINFO_AutoLock             | Scheduled daily — check LockDate                         | If LockDate ≤ Today and IsLocked = false, set IsLocked = true, set CurrentStatus = Locked                                                                                           |

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

- [ ] All SharePoint columns in `MainDB_HR (Department_05)` are created with correct types and required flags.
- [ ] Canvas App screens (`HRINFO_List`, `HRINFO_New`, `HRINFO_View`, `HRINFO_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
