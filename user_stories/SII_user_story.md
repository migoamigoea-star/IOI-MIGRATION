# User Story — Stock Item Inclusion (`SII`)

> **Department:** STR (Department_13_STR)  
> **Module:** M1 - Stock Item Management  
> **Site(s):** PRAI  
> **SharePoint List:** `MainDB_STR`  
> **Form Code:** `SII`

---

## 1. App Overview & Purpose

SII controls master-data onboarding for new stock items, including requestor details, sourcing and
cost review, HOD/materials/finance/executive approvals, warehouse-MRP-accounting completion, and
final material-code traceability. The workflow ensures that no stock item is activated without
controlled approvals and attributable completion records.

---

## 2. User Stories

**US-01: Submit stock item inclusion request**
> As a **Requestor** (member of `D13-STR-Users`),  
> I want to **submit stock item inclusion request** in the `SII` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* Item created with `FormCode=SII`

**US-02: Approve/reject business need**
> As a **HOD** (member of `D13-STR-HOD-Reviewers`),  
> I want to **approve/reject business need** in the `SII` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CurrentStatus=Submitted`

**US-03: Approve/reject materials suitability**
> As a **Materials** (member of `D13-STR-Materials`),  
> I want to **approve/reject materials suitability** in the `SII` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CurrentStatus=HODApproved`

**US-04: Approve/reject cost and control**
> As a **Finance** (member of `D13-STR-Finance`),  
> I want to **approve/reject cost and control** in the `SII` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CurrentStatus=MaterialsApproved`

**US-05: Final executive decision**
> As a **ED** (member of `D13-STR-Executive-Approvers`),  
> I want to **final executive decision** in the `SII` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CurrentStatus=FinanceApproved`

**US-06: Complete warehouse/MRP/accounting and assign material code**
> As a **Master Data Team** (member of `D13-STR-MasterData`),  
> I want to **complete warehouse/mrp/accounting and assign material code** in the `SII` application,  
> So that the workflow advances to the next approval stage.  
>
> *Trigger:* `CurrentStatus=EDApproved`

**US-LIST: Search and filter Stock Item Inclusion records**
> As an **authorized user**,  
> I want to search, filter, and view Stock Item Inclusion records in the list screen,  
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

**Target List:** `MainDB_STR`

| #   | SP Internal Name       | Display Label            | Column Type     | Required | Classification   | Notes                                                                                                         |
| --- | ---------------------- | ------------------------ | --------------- | -------- | ---------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | FormCode               | Form Code                | Single line     | Yes      | SYSTEM-COMPUTED  | Fixed `SII`                                                                                                   |
| 2   | INO                    | Inclusion Ref No         | Single line     | Yes      | SYSTEM-COMPUTED  | `STR-SII-YYMM-NNNN` via flow                                                                                  |
| 3   | CurrentStatus          | Workflow Status          | Choice          | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HODApproved, MaterialsApproved, FinanceApproved, EDApproved, Completed, Rejected, Discarded |
| 4   | CurrentAction          | Current Action           | Choice          | Yes      | WORKFLOW-MANAGED | Submit, Review, Approve, Complete, Discard                                                                    |
| 5   | RequestDate            | Request Date             | Date and Time   | Yes      | USER-ENTERED     | Request initiation date                                                                                       |
| 6   | Requestor              | Requestor                | Person or Group | Yes      | USER-ENTERED     | Initiator                                                                                                     |
| 7   | RequestDept            | Requesting Department    | Single line     | Yes      | USER-ENTERED     | Requesting unit                                                                                               |
| 8   | ItemDescription        | Item Description         | Multiple lines  | Yes      | USER-ENTERED     | Technical item description                                                                                    |
| 9   | ItemCategory           | Item Category            | Choice          | Yes      | USER-ENTERED     | Raw Material, Packaging, Spare, Consumable, Other                                                             |
| 10  | BuyerAssessment        | Buyer Assessment         | Multiple lines  | No       | USER-ENTERED     | Sourcing suitability                                                                                          |
| 11  | EstimatedCost          | Estimated Cost           | Currency        | No       | USER-ENTERED     | Estimated item cost                                                                                           |
| 12  | TotalHoldingCost       | Total Holding Cost       | Currency        | No       | SYSTEM-COMPUTED  | Cost roll-up or entered summary                                                                               |
| 13  | HODDecision            | HOD Decision             | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 14  | MaterialsDecision      | Materials Decision       | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 15  | FinanceDecision        | Finance Decision         | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 16  | EDDecision             | ED Decision              | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 17  | WarehouseDataComplete  | Warehouse Data Complete  | Yes/No          | No       | USER-ENTERED     | Master data completion check                                                                                  |
| 18  | MRPDataComplete        | MRP Data Complete        | Yes/No          | No       | USER-ENTERED     | Master data completion check                                                                                  |
| 19  | AccountingDataComplete | Accounting Data Complete | Yes/No          | No       | USER-ENTERED     | Master data completion check                                                                                  |
| 20  | MaterialCode           | Material Code            | Single line     | No       | WORKFLOW-MANAGED | Final code at completion                                                                                      |
| 21  | PRCreated              | PR Created               | Yes/No          | No       | WORKFLOW-MANAGED | Purchase requisition generated                                                                                |
| 22  | DiscardFlag            | Discard Flag             | Yes/No          | No       | WORKFLOW-MANAGED | Discard workflow route                                                                                        |
| 23  | DiscardReason          | Discard Reason           | Multiple lines  | No       | USER-ENTERED     | Mandatory when discarded                                                                                      |
| 24  | SubmittedBy            | Submitted By             | Person or Group | Yes      | SYSTEM-COMPUTED  | Submission actor                                                                                              |
| 25  | SubmittedDate          | Submitted Date           | Date and Time   | Yes      | SYSTEM-COMPUTED  | Submission timestamp                                                                                          |
| 26  | EnvironmentTag         | Environment              | Choice          | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                                                               |
| 27  | IsLocked               | Is Locked                | Yes/No          | No       | WORKFLOW-MANAGED | Set after completion/discard                                                                                  |

---

## 4. Screen Requirements

| Screen | Purpose | Visible To |
|--------|---------|------------|
| SII_List | Search and filter SII requests | STR users and reviewers |
| SII_New | New inclusion request | Requestor |
| SII_View | Read-only request details and approvals | Authorized users |
| SII_Edit | Draft/returned edits | Requestor |
| SII_Approval | Multi-stage review actions | HOD, Materials, Finance, ED |
| SII_Completion | Master data completion and code issuance | Master Data Team |

### Screen Interaction Details

**SII_List Screen**
- Gallery displaying all `SII` records from `MainDB_STR`.
- Search box filters by `Title` and `Status`.
- Status badge shows colour-coded current state (Draft = grey, Submitted = blue, Approved = green, Rejected = red).
- `+ New` button navigates to `SII_New` (visible to Initiator role only).
- Tap a row to navigate to `SII_View`.

**SII_New / _Edit Screen**
- Data entry form bound to `MainDB_STR`.
- Required fields highlighted in red when empty.
- `Save as Draft` button: patches record with `Status = Draft`.
- `Submit` button: disabled until all required fields are filled; on press patches `Status = Submitted` and triggers the Submit flow.
- `Cancel` button: discards changes and navigates back.

**SII_View Screen**
- All fields displayed in read-only mode.
- `Edit` button visible to Initiator when `Status = Draft` or `Returned`.
- `Approve` / `Reject` buttons visible to Approver role when `Status = Submitted` or `InApproval`.

---

## 5. Formula Requirements (Power Fx)

The following Power Fx formulas must be implemented in the Canvas App:

### 1. Title / Record ID Auto-Generation

```powerfx
// On form open for new record, set a unique display ID
Set(varTitle, "SII-" & Text(Now(), "YYYYMMDD-HHMMSS"))
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
Navigate(SII_New, ScreenTransition.Slide)

// Navigate from List to View screen for selected record
Navigate(SII_View, ScreenTransition.None, {varRecord: ThisItem})

// Save (Patch) and navigate back to list
Patch(MainDB, {
    Title: varTitle,
    FormCode: "SII",
    Status: "Draft",
    SubmittedBy: User(),
    SubmittedDate: Now()
});
Navigate(SII_List, ScreenTransition.Back)
```

### 5. List Screen Search & Filter

```powerfx
// Gallery Items formula — filter by FormCode and search text
Filter(
    MainDB,
    FormCode = "SII" &&
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
- **Stage 1:** `Submit stock item inclusion request` — performed by `Requestor`
- **Stage 2:** `Approve/reject business need` — performed by `HOD`
- **Stage 3:** `Approve/reject materials suitability` — performed by `Materials`
- **Stage 4:** `Approve/reject cost and control` — performed by `Finance`
- **Stage 5:** `Final executive decision` — performed by `ED`
- **Stage 6:** `Complete warehouse/MRP/accounting and assign material code` — performed by `Master Data Team`

> ⚠️ **Status must never be changed directly by end-users.** All status transitions are managed exclusively by Power Automate flows.

### 2. Role-Based Access Control

| Role | Allowed Actions |
|------|----------------|
| Requestor | Contribute |
| HOD Reviewer | Contribute |
| Materials Reviewer | Contribute |
| Finance Reviewer | Contribute |
| Executive Approver | Contribute |
| Master Data Team | Contribute |
| Admin | Full Control |
| Reader | Read |

### 3. Data Integrity Rules

- `FormCode` must always equal `SII` (system-enforced constant).
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

| Stage            | Flow Name                    | Trigger                          | Actions                                                                    |
| ---------------- | ---------------------------- | -------------------------------- | -------------------------------------------------------------------------- |
| Submit           | STR_SII_OnSubmit             | Item created with `FormCode=SII` | Generate INO, set CurrentStatus=Submitted, stamp SubmittedBy/SubmittedDate |
| HOD Review       | STR_SII_OnHODDecision        | `HODDecision` updated            | Route to Materials or reject path                                          |
| Materials Review | STR_SII_OnMaterialsDecision  | `MaterialsDecision` updated      | Route to Finance or reject path                                            |
| Finance Review   | STR_SII_OnFinanceDecision    | `FinanceDecision` updated        | Route to ED or reject path                                                 |
| Executive Review | STR_SII_OnEDDecision         | `EDDecision` updated             | Route to Master Data completion                                            |
| Complete         | STR_SII_OnMasterDataComplete | All completion flags true        | Set MaterialCode, PRCreated, CurrentStatus=Completed, IsLocked=Yes         |
| Discard          | STR_SII_OnDiscard            | `DiscardFlag=true`               | Enforce reason, set CurrentStatus=Discarded, notify stakeholders           |

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

- [ ] All SharePoint columns in `MainDB_STR` are created with correct types and required flags.
- [ ] Canvas App screens (`SII_List`, `SII_New`, `SII_View`, `SII_Edit`) are functional.
- [ ] All required field validations prevent submission of incomplete forms.
- [ ] Status field is read-only in the Canvas App; transitions are flow-only.
- [ ] All Power Automate flows are tested end-to-end in TEST environment.
- [ ] Notification emails are received by correct recipients at each stage.
- [ ] Approved records are fully locked (no edits possible).
- [ ] Role-based visibility is enforced: Initiators cannot approve their own records.
- [ ] Audit trail is complete and immutable for all status transitions.
- [ ] `EnvironmentTag` correctly isolates DEV / TEST / PROD data.
