# User Story — IT Support & Service Request (SSR) 2025 (`ITSSR`)

> **Department:** Department_06_IT (IT)  
> **Module:** M2 - IT Support & Service Requests  
> **Site(s):** PRAI / Both (Johor routing via hidden fields)  
> **SharePoint List:** `MainDB_IT`  
> **Form Code:** `ITSSR`

---

## 1. App Overview & Purpose

`ITSSR` is migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online). The app supports standardized submission, review, and approval workflows for the `Department_06_IT (IT)` department at the PRAI / Both (Johor routing via hidden fields) site.

---

## 2. User Stories

**US-01: Create & Submit SSR**
> As a **Requestor** (member of ``D06-IT-Initiators``),  
> I want to **create & submit ssr** in the `ITSSR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* New item created with mandatory fields (Company, ServiceType, ProblemDesc, ReportedBy)

**US-02: Triage & Assign**
> As a **IT Admin** (member of ``D06-IT-IT-Admin``),  
> I want to **triage & assign** in the `ITSSR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Status = Submitted

**US-03: Execute Resolution**
> As a **IT Executor** (member of ``D06-IT-Editors-L1` + site-team routers (HWP/HWJ)`),  
> I want to **execute resolution** in the `ITSSR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Status = InProgress + ITName assigned

**US-04: Requestor Accept & Rate**
> As a **Requestor** (member of ``D06-IT-Initiators``),  
> I want to **requestor accept & rate** in the `ITSSR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Status = Resolved + DateClosed filled

**US-05: Final Closure & Archive**
> As a **IT Admin / System** (member of ``D06-IT-IT-Admin``),  
> I want to **final closure & archive** in the `ITSSR` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Status = Accepted OR 30 days elapsed since Resolved

**US-LIST: Search and filter IT Support & Service Request (SSR) 2025 records**
> As an **authorized user**,  
> I want to search, filter, and view IT Support & Service Request (SSR) 2025 records in the list screen,  
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

**Target List:** `MainDB_IT`

| #   | Column Name (SharePoint) | SP Type                 | Required | Choices / Source                                         | Domino Field     | Notes                                                             |
| --- | ------------------------ | ----------------------- | -------- | -------------------------------------------------------- | ---------------- | ----------------------------------------------------------------- |
| 1   | Title                    | Single line of text     | Yes      | —                                                        | `CaseNo`         | Auto-mapped case identifier; system-computed in Domino            |
| 2   | FormType                 | Single line of text     | Yes      | Choice: ITSSR                                            | —                | Distinguishes form type within MainDB_IT parent table (DEC-001)   |
| 3   | CaseNo                   | Single line of text     | Yes      | —                                                        | `CaseNo`         | Domino case reference; stored redundantly for reporting access    |
| 4   | Company                  | Choice                  | Yes      | [List from Domino]                                       | `Company`        | Requesting company/entity                                         |
| 5   | Department               | Choice                  | Yes      | [List from Domino]                                       | `Dept`           | Requesting department                                             |
| 6   | ServiceType              | Choice                  | Yes      | [List from Domino]                                       | `Type`           | Support category (Hardware/Software/Network/etc.)                 |
| 7   | Hardware                 | Choice                  | No       | [List from Domino]                                       | `HWare`          | Hardware category selector (if Type=Hardware)                     |
| 8   | Application              | Choice                  | No       | [List from Domino]                                       | `App`            | Application/service selector (if Type=Application)                |
| 9   | Module                   | Choice                  | No       | [List from Domino]                                       | `Module`         | Module or subsystem                                               |
| 10  | SAPModule                | Choice                  | No       | [List from Domino]                                       | `SAPModule`      | SAP-specific category (if applicable)                             |
| 11  | BankModule               | Choice                  | No       | [List from Domino]                                       | `BankModule`     | Bank module selector (if applicable)                              |
| 12  | ReportedByEmail          | Person or Group         | Yes      | —                                                        | `ReportedBy`     | Requestor (originator); auto-populated from user                  |
| 13  | PhoneExtension           | Single line of text     | No       | —                                                        | `ExtNo`          | Contact number for requestor callback                             |
| 14  | SendToEmail              | Person or Group         | Yes      | —                                                        | `SendTo`         | Main IT routing recipient (initial assignment)                    |
| 15  | CCEmail                  | Person or Group (multi) | No       | —                                                        | `CC`             | Additional copy recipients                                        |
| 16  | ProblemDescription       | Multi-line text         | Yes      | —                                                        | `ProblemDesc`    | Core issue/request narrative, at least 10 chars                   |
| 17  | RequestorAttachment      | Hyperlink               | No       | —                                                        | `Attach`         | Requestor evidence URL or document library reference              |
| 18  | CaseStatus               | Choice                  | Yes      | Draft; Submitted; InProgress; Resolved; Accepted; Closed | —                | Workflow state (DEC-001 / live PA submission logic)               |
| 19  | SubmittedBy              | Person or Group         | Yes      | —                                                        | —                | Auto-populated by Power Apps when item created                    |
| 20  | SubmittedDate            | Date and Time           | Yes      | —                                                        | `DateCreated`    | Creation timestamp                                                |
| 21  | AssignedToEmail          | Person or Group         | No       | —                                                        | `ITName`         | IT executor assigned during triage stage                          |
| 22  | DateStarted              | Date and Time           | No       | —                                                        | `StartDate`      | Start of IT work (once assigned)                                  |
| 23  | Solution                 | Multi-line text         | No       | —                                                        | `Solution`       | Resolution details recorded by IT executor                        |
| 24  | ITAttachment             | Hyperlink               | No       | —                                                        | `Attachment2`    | IT evidence URL or document library reference                     |
| 25  | ProblemCategory          | Choice                  | No       | [List from Domino]                                       | `ProbCat`        | Primary issue category (set by IT during resolution)              |
| 26  | SecondaryCategory        | Choice                  | No       | [List from Domino]                                       | `ProbCat2`       | Secondary issue category (if applicable)                          |
| 27  | Classification           | Choice                  | No       | [List from Domino]                                       | `Classification` | Severity/priority (set by IT: High/Medium/Low)                    |
| 28  | SupportMethod            | Choice                  | No       | [List from Domino]                                       | `Support`        | Support channel/method (OnSite/Remote/Phone/etc.)                 |
| 29  | DateResolved             | Date and Time           | No       | —                                                        | `DateClosed`     | Resolution completion timestamp (system-set when Status→Resolved) |
| 30  | DateNotifiedRequestor    | Date and Time           | No       | —                                                        | `DateNotified`   | Timestamp when requestor was notified of resolution               |
| 31  | ApprovedBy               | Person or Group         | No       | —                                                        | —                | Applicable if multi-level approval required (see Workflow)        |
| 32  | ApprovedDate             | Date and Time           | No       | —                                                        | —                | Timestamp of approval                                             |
| 33  | DateAccepted             | Date and Time           | No       | —                                                        | `DateAccept`     | Requestor acceptance/sign-off timestamp                           |
| 34  | SatisfactionRating       | Number                  | No       | 1–10 scale                                               | `RatingCom`      | User satisfaction rating (1=Dissatisfied, 8–10=Delighted)         |
| 35  | RequestorComment         | Multi-line text         | No       | —                                                        | `Comment`        | Requestor feedback and comments                                   |
| 36  | ITRemarks                | Multi-line text         | No       | —                                                        | `ITRemarks`      | IT executor remarks during resolution                             |
| 37  | ITNotifyRemarks          | Multi-line text         | No       | —                                                        | `ITRemark`       | IT notification/follow-up remarks                                 |
| 38  | DateNotifyFollowUp       | Date and Time           | No       | —                                                        | `datenotify`     | IT notification follow-up timestamp                               |
| 39  | CurrentAction            | Choice                  | Yes      | [State machine keys]                                     | `CA`             | Hidden workflow state machine key; Power Automate managed         |
| 40  | RoutingOU                | Person or Group (multi) | No       | —                                                        | `OU`             | Hidden requestor org unit(s); Power Automate routing              |
| 41  | ITAdminEmail             | Person or Group (multi) | No       | —                                                        | `ITADMIN`        | Hidden IT admin distribution; workflow routing                    |
| 42  | MKTCFOEmail              | Person or Group (multi) | No       | —                                                        | `MKT`            | Hidden MKT/CFO routing (if cross-functional); workflow managed    |
| 43  | DefaultMailingList       | Distribution List       | No       | —                                                        | `Defcc`          | Hidden default distribution; workflow managed                     |
| 44  | PenangTeam               | Person or Group (multi) | No       | —                                                        | `HWP`            | Hidden Penang IT team routing (site-based)                        |
| 45  | JohorTeam                | Person or Group (multi) | No       | —                                                        | `HWJ`            | Hidden Johor IT team routing (site-based)                         |
| 46  | HardwareTeam             | Person or Group (multi) | No       | —                                                        | `ALLHW`          | Hidden hardware team assignment; workflow managed                 |
| 47  | SoftwareTeam             | Person or Group (multi) | No       | —                                                        | `ALLSW`          | Hidden software team assignment; workflow managed                 |
| 48  | AllITReaders             | Person or Group (multi) | No       | —                                                        | `AllIT`          | Hidden IT reader distribution list                                |
| 49  | Editor1–4                | Person or Group (multi) | No       | —                                                        | `Editor1–4`      | Hidden editor escalation/approval chain slots                     |
| 50  | ComputedCategory         | Single line of text     | No       | —                                                        | `Category`       | Hidden computed subject category field                            |
| 51  | ComputedSAPSubject       | Single line of text     | No       | —                                                        | `dsSAPSubject`   | Hidden computed SAP module subject line                           |
| 52  | ReminderSubject          | Single line of text     | No       | —                                                        | `RemSubject`     | Hidden computed reminder subject for escalation                   |
| 53  | MailingList              | Distribution List       | No       | —                                                        | `MailingList`    | Hidden mailing list for result broadcast                          |
| 54  | DocAuthor                | Single line of text     | No       | —                                                        | `DocAuthor`      | Audit: creator metadata                                           |
| 55  | CreationDate             | Date and Time           | No       | —                                                        | `CreationDate`   | Audit: form creation timestamp                                    |
| 56  | ApprovedApprovalRecord   | Lookup                  | No       | Lookup to child table                                    | —                | [CHILD TABLE] Links to approval/activity audit log (if used)      |



---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| `ITSSR_List` | Browse and search all ITSSR records | All authorized users |
| `ITSSR_New` | Create a new IT Support & Service Request (SSR) 2025 request | Initiator / Requestor |
| `ITSSR_View` | Read-only detail view of a record | All authorized users |
| `ITSSR_Edit` | Edit a draft or returned record | Initiator / Reviewer |
| `ITSSR_Approval` | Approve or reject the record | Approver / Manager |

### Screen Interaction Details

**ITSSR_List Screen**
- Gallery displaying all `ITSSR` records from `MainDB_IT`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `ITSSR_New` (visible to Initiator role only).
- Tap a row to navigate to `ITSSR_View`.

**ITSSR_New / _Edit Screen**
- Data entry form bound to `MainDB_IT`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**ITSSR_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "ITSSR-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(ITSSR_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(ITSSR_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "ITSSR",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(ITSSR_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "ITSSR" &&
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
- **Stage 1:** `Create & Submit SSR` — performed by `Requestor`
- **Stage 2:** `Triage & Assign` — performed by `IT Admin`
- **Stage 3:** `Execute Resolution` — performed by `IT Executor`
- **Stage 4:** `Requestor Accept & Rate` — performed by `Requestor`
- **Stage 5:** `Final Closure & Archive` — performed by `IT Admin / System`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Domino Group / Field | Permission Level |
| Requestor (`ReportedBy`) | Contribute |
| IT Admin (`ITADMIN`) | Contribute |
| Hardware Team (`ALLHW`) | Contribute |
| Software Team (`ALLSW`) | Contribute |
| Penang IT Senior (`HWP`) | Contribute |
| Johor IT Senior (`HWJ`) | Contribute |
| IT Executor (`ITName`) | Contribute |
| IT Readers (`CC`, `AllIT`) | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `ITSSR` (system-enforced constant).
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

| Stage       | Flow Name                    | Trigger                                       | Primary Actions                                                                                                                                                                                                                       | Condition Checks                                                      | Notification Target                            |
| ----------- | ---------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| 1 (Submit)  | `IT_ITSSR_SubmitIntake`      | SP: When item created                         | ✓ Set Status = Submitted; ✓ Validate mandatory fields; ✓ Log CreateDate; ✓ Route based on Company + Site                                                                                                                              | Company not empty AND ServiceType selected AND ProblemDesc ≥ 10 chars | IT Admin (ITADMIN) and SendTo recipient        |
| 2 (Assign)  | `IT_ITSSR_TriageAssign`      | SP: When Status = Submitted                   | ✓ Validate Service Type; ✓ Route to Hardware/Software/Site team based on Type + Site; ✓ Assign ITName from pool; ✓ Set Status = InProgress; ✓ Set DateStarted; ✓ Escalate if no assignment within 2 hrs                               | Type field populated AND site identified (PRAI/Johor)                 | Assigned IT executor + requestor notification  |
| 3 (Resolve) | `IT_ITSSR_ExecuteResolution` | SP: When Status = InProgress                  | ✓ Monitor assignment; ✓ Accept solution input; ✓ Validate Solution field ≥ 50 chars if problem cat set; ✓ Set Status = Resolved; ✓ Set DateClosed = today; ✓ Notify requestor for acceptance                                          | Solution not empty AND (ProblemCategory OR SupportMethod) set         | Requestor (ReportedBy) + IT stakeholders       |
| 4 (Accept)  | `IT_ITSSR_RequestorAccept`   | SP: When Status = Resolved                    | ✓ Notify requestor deadline (72 hrs to accept); ✓ Accept rating/comment input; ✓ Validate: if Rating < 8 then Comment mandatory; ✓ If accepted: Set Status = Accepted + DateAccepted; ✓ If rejected/no-response: escalate to IT Admin | Rating present if DateAccepted populated OR 72 hrs elapsed            | IT Admin (if no response) + requestor reminder |
| 5 (Archive) | `IT_ITSSR_FinalArchive`      | SP: When Status = Accepted OR daily scheduled | ✓ If Status = Accepted: Set Status = Closed, DateClosed final, archive; ✓ Compute satisfaction metrics; ✓ Publish result to ITRemarks + team reporting; ✓ If 30 days elapsed on Resolved: auto-close with reminder                    | No open acceptance work remains                                       | IT Admin + reporting audience                  |

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

- [ ] All SharePoint columns in `MainDB_IT` are created with correct types and required flags.
- [ ] Canvas App screens (`ITSSR_List`, `ITSSR_New`, `ITSSR_View`, `ITSSR_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
