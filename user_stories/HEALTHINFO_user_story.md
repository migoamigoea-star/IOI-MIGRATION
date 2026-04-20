# User Story — Health & Title Information Broadcast (`HEALTHINFO`)

> **Department:** HR  
> **Module:** HR Administration — Internal Communications  
> **Site(s):** PRAI, JOHOR  
> **SharePoint List:** `MainDB_HR **Form Discriminator:** FormCode = "HEALTHINFO"`  
> **Form Code:** `HEALTHINFO`

---

## 1. App Overview & Purpose

HEALTHINFO is an internal broadcast form allowing HR administrators to publish health-related
notices, policy title updates, and informational announcements to staff. There is no approval
workflow — only an admin-publish action that creates the record and notifies designated recipients.
The migrated solution must preserve the category-based routing, the send target selection,
attachment support, and the read-only broadcast experience for recipients.

---

---

## 2. User Stories

**US-01: Create & Publish**
> As a **HR Admin** (member of `D05-HR-Manager`),  
> I want to **create & publish** in the `HEALTHINFO` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status='Draft' → HR Admin publishes

**US-02: Notify Recipients**
> As a **System** (member of `—`),  
> I want to **notify recipients** in the `HEALTHINFO` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* When Status changes to 'Published' → send email to SendTo group

**US-LIST: Search and filter Health & Title Information Broadcast records**
> As an **authorized user**,  
> I want to search, filter, and view Health & Title Information Broadcast records in the list screen,  
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

**Target List:** `MainDB_HR **Form Discriminator:** FormCode = "HEALTHINFO"`

| #   | SP Internal Name | Display Label         | Column Type         | Required | Classification   | Source Mapping / Notes                               |
| --- | ---------------- | --------------------- | ------------------- | -------- | ---------------- | ---------------------------------------------------- |
| 1   | Title            | Title                 | Single line text    | Yes      | SYSTEM-COMPUTED  | HEALTHINFO prefix + Subject                          |
| 2   | FormCode         | Form Code             | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value HEALTHINFO                               |
| 3   | Category         | Category              | Choice              | Yes      | USER-ENTERED     | `Category` — Health, Title, General, Policy          |
| 4   | SendTo           | Send To               | Person or Group     | Yes      | USER-ENTERED     | `Send` — recipients or group to notify               |
| 5   | Subject          | Subject               | Single line text    | Yes      | USER-ENTERED     | `Subject`                                            |
| 6   | Body             | Message Body          | Multiple lines text | Yes      | USER-ENTERED     | `Body` — HTML-capable announcement body              |
| 7   | Attachment       | Attachment            | Hyperlink           | No       | USER-ENTERED     | `Att` — optional supporting document                 |
| 8   | ExtensionInfo    | Extension / Reference | Single line text    | No       | USER-ENTERED     | `Ext` — phone/ext number or reference code           |
| 9   | PublishStatus    | Status                | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Published                                     |
| 10  | Author           | Published By          | Person or Group     | Yes      | SYSTEM-COMPUTED  | `Author` — HR admin who published                    |
| 11  | DateSent         | Date Published        | Date and Time       | Yes      | SYSTEM-COMPUTED  | `DateSent`                                           |
| 12  | IsLocked         | Is Locked             | Yes/No              | No       | WORKFLOW-MANAGED | `Lock` — true after publish                          |
| 13  | CurrentAction    | Current Action        | Single line text    | No       | WORKFLOW-MANAGED | `CurrentAction` — internal workflow state descriptor |
| 14  | IsAdmin          | Is Admin              | Yes/No              | No       | USER-ENTERED     | `ISADMIN` — flag for admin-only visibility features  |
| 15  | EnvironmentTag   | Environment           | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                      |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| HEALTHINFO_List | Gallery | List all published health/title broadcasts with category filter |
| HEALTHINFO_New | Form | Create and publish new broadcast |
| HEALTHINFO_View | Read-only | View full broadcast details with attachment |

### Screen Interaction Details

**HEALTHINFO_List Screen**
- Gallery displaying all `HEALTHINFO` records from `MainDB_HR **Form Discriminator:** FormCode = "HEALTHINFO"`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `HEALTHINFO_New` (visible to Initiator role only).
- Tap a row to navigate to `HEALTHINFO_View`.

**HEALTHINFO_New / _Edit Screen**
- Data entry form bound to `MainDB_HR **Form Discriminator:** FormCode = "HEALTHINFO"`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**HEALTHINFO_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "HEALTHINFO-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(HEALTHINFO_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(HEALTHINFO_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "HEALTHINFO",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(HEALTHINFO_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "HEALTHINFO" &&
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
- **Stage 1:** `Create & Publish` — performed by `HR Admin`
- **Stage 2:** `Notify Recipients` — performed by `System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| HR Admins | D05-HR-Manager |
| All Staff | D05-HR-Staff |

### 3. Data Integrity Rules

- `FormCode` must always equal `HEALTHINFO` (system-enforced constant).
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

| Flow Name               | Trigger                            | Action                                                                      |
| ----------------------- | ---------------------------------- | --------------------------------------------------------------------------- |
| HR_HEALTHINFO_OnPublish | When Status changes to 'Published' | Send email to SendTo recipients with Subject, Body, Attachment; lock record |

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

- [ ] All SharePoint columns in `MainDB_HR **Form Discriminator:** FormCode = "HEALTHINFO"` are created with correct types and required flags.
- [ ] Canvas App screens (`HEALTHINFO_List`, `HEALTHINFO_New`, `HEALTHINFO_View`, `HEALTHINFO_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
