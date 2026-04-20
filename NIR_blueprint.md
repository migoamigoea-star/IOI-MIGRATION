# Technical Blueprint: Notes ID Request (NIR)

## Form Identity

| Field                      | Value                                                                 |
| -------------------------- | --------------------------------------------------------------------- |
| Form Code                  | `NIR`                                                                 |
| Official Name              | Notes ID Request                                                      |
| Department                 | IT (Department_06)                                                    |
| Module                     | M1 — User & Access Management                                         |
| Site(s)                    | PRAI (primary)                                                        |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/NIR.pdf` |
| Domino Database            | `prai_db.nsf`                                                         |
| Official Name Claim Status | `Claimed` — "Notes ID Request" from module_overview.md                |
| Blueprint Version          | `1.0`                                                                 |
| Blueprint Date             | `2026-04-13`                                                          |
| Architect                  | AI Agent (Architect mode)                                             |

---

## SharePoint Schema

**Target List (Primary — per DEC-001):** `MainDB_IT`  
**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal-it/Lists/MainDB_IT`

**Target List (Historical Import):** `IT_NIR_List` (form module table for legacy Domino records
only)  
**Note:** Per DEC-001, **all new form submissions write to `MainDB_IT` only**. The form module table
`IT_NIR_List` receives migrated historical Domino records for archival reference; new submissions
must never be written to it.

---

### Column Mapping — New Submission Columns (MainDB_IT)

| #   | Domino Field | SP Column Name                          | SP Type                | Required | Choices / Source                                                         | Notes (Source)                                                                                     |
| --- | ------------ | --------------------------------------- | ---------------------- | -------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| 1   | EmailType    | EmailType                               | Choice                 | Yes      | New Email; Replacement                                                   | Request type [USER-ENTERED]                                                                        |
| 2   | Company      | Company                                 | Choice                 | Yes      | IOI Oleochemical; IOI Acidchem                                           | Company selector [USER-ENTERED]                                                                    |
| 3   | Emailid      | ExistingEmailAddress                    | Single line of text    | No       | —                                                                        | Existing address for replacement [USER-ENTERED]                                                    |
| 4   | FullName     | FullName                                | Single line of text    | Yes      | —                                                                        | User full name [USER-ENTERED]                                                                      |
| 5   | EmpNo        | EmployeeNumber                          | Single line of text    | Yes      | —                                                                        | Employee ID [USER-ENTERED]                                                                         |
| 6   | Department   | Department                              | Choice                 | Yes      | _lookup to Department list_                                              | Requestor department [USER-ENTERED]                                                                |
| 7   | Designation  | Designation                             | Single line of text    | No       | —                                                                        | Job title [USER-ENTERED]                                                                           |
| 8   | Extension    | PhoneExtension                          | Single line of text    | No       | —                                                                        | Contact extension [USER-ENTERED]                                                                   |
| 9   | Type         | `[IN-PROGRESS: See CLARIFY note below]` | `PENDING`              | No       | —                                                                        | Secondary classification. **[CLARIFY: Verify if "Type" differs from "EmailType" or is redundant]** |
| 10  | HOD          | HODApprover                             | Person or Group        | Yes      | _D06-IT-Initiators (submitter populates)_                                | Head-of-Department approver [USER-ENTERED]                                                         |
| 11  | Remark       | Remarks                                 | Multiple lines of text | No       | —                                                                        | Business note, replacement details [USER-ENTERED]                                                  |
| 12  | Requestor    | Requestor                               | Person or Group        | No       | _Computed: User.FullName_                                                | Request initiator [SYSTEM-COMPUTED]                                                                |
| 13  | DateSent     | SubmittedDate                           | Date and Time          | No       | _Computed: NOW()_                                                        | Submission timestamp [SYSTEM-COMPUTED]                                                             |
| 14  | HODName      | HODName                                 | Person or Group        | No       | —                                                                        | Recorded HOD approver [WORKFLOW-MANAGED]                                                           |
| 15  | HodDate      | HODApprovalDate                         | Date and Time          | No       | —                                                                        | HOD decision timestamp [SYSTEM-COMPUTED]                                                           |
| 16  | HodStatus    | HODApprovalStatus                       | Choice                 | No       | Pending; Approved; Rejected                                              | HOD decision state [WORKFLOW-MANAGED]                                                              |
| 17  | HodComment   | HODComment                              | Multiple lines of text | No       | —                                                                        | HOD remarks [USER-ENTERED]                                                                         |
| 18  | PICName      | NotesAdministrator                      | Person or Group        | No       | _D06-IT-Editors-L1_                                                      | Notes admin handling provisioning [WORKFLOW-MANAGED]                                               |
| 19  | PICDate      | NotesAdminDate                          | Date and Time          | No       | —                                                                        | Notes admin action timestamp [SYSTEM-COMPUTED]                                                     |
| 20  | PICTask      | NotesAdminTask                          | Multiple lines of text | No       | —                                                                        | Provisioning task detail [USER-ENTERED]                                                            |
| 21  | ID           | InternalNotesID                         | Single line of text    | No       | —                                                                        | Internal Notes ID produced [WORKFLOW-MANAGED]                                                      |
| 22  | ID2          | ExternalNotesID                         | Single line of text    | No       | —                                                                        | External Notes ID or routing value [WORKFLOW-MANAGED]                                              |
| 23  | PICRemark    | NotesAdminRemark                        | Multiple lines of text | No       | —                                                                        | Notes admin remarks [USER-ENTERED]                                                                 |
| 24  | AccName      | ITHardwareOwner                         | Person or Group        | No       | _D06-IT-Editors-L2_                                                      | IT hardware/support actor [WORKFLOW-MANAGED]                                                       |
| 25  | AccDate      | ITHardwareDate                          | Date and Time          | No       | —                                                                        | IT hardware action timestamp [SYSTEM-COMPUTED]                                                     |
| 26  | AccTask      | ITHardwareTask                          | Multiple lines of text | No       | —                                                                        | Hardware or downstream IT task [USER-ENTERED]                                                      |
| 27  | AccStatus    | ITHardwareStatus                        | Choice                 | No       | Pending; In Progress; Completed                                          | Downstream IT completion status [WORKFLOW-MANAGED]                                                 |
| 28  | AccComment   | ITHardwareComment                       | Multiple lines of text | No       | —                                                                        | Hardware/support remarks [USER-ENTERED]                                                            |
| 29  | CA           | CurrentAction                           | Choice                 | No       | RequestSubmitted; HODPending; NotesAdminPending; HardwarePending; Closed | Hidden workflow state [WORKFLOW-MANAGED]                                                           |
| 30  | ITHOD        | ITHODRoutingField                       | Person or Group        | No       | —                                                                        | Hidden IT HOD routing field [WORKFLOW-MANAGED]                                                     |

**Standard Base Columns (per DEC-005 — FORM_COLUMN_DEFINITIONS_ENHANCED.json):**

- `Title` (Auto-mapped from item ID)
- `FormCode` (NIR)
- `DepartmentCode` (IT)
- `EnvironmentTag` (DEV / TEST / PROD — per DEC-004)
- `CreatedBy` (System)
- `CreatedDate` (System)
- `ModifiedBy` (System)
- `ModifiedDate` (System)

---

### Hidden Routing Fields (Domino → Explicit Power Automate Mapping)

Per the migration evidence, the following Domino hidden fields must be **replaced with explicit
Power Automate routing logic** (not mapped as SharePoint columns):

| Domino Hidden Field | Purpose                  | Power Automate Replacement                                                     |
| ------------------- | ------------------------ | ------------------------------------------------------------------------------ |
| PIC                 | Notes PIC routing hint   | Lookup in IT routing matrix → populate `NotesAdministrator` column             |
| ISG                 | ISG team assignment      | Lookup in IT routing matrix → populate `ITTeamAssigned` column                 |
| HW                  | Penang hardware routing  | Lookup in Penang IT support routing → populate `ITHardwareOwner` (Penang)      |
| HW2                 | Johor hardware routing   | Lookup in Johor IT support routing → populate `ITHardwareOwner` (Johor)        |
| SW                  | Software team assignment | Evaluate in routing logic; cascade to `ITTeamAssigned`                         |
| HRE                 | HR Executive routing     | Conditional: if HR approvals needed, route to HR-Exec group                    |
| HRNE                | HR Non-Executive routing | Conditional: if HR approvals needed, route to HR-NonExec group                 |
| HR                  | HR general assignment    | Conditional: fallback HR team assignment                                       |
| ITHOD               | IT HOD routing field     | Lookup in IT management matrix → populate `HODApprover` or `ITHODRoutingField` |

**Architect Note:** These hidden fields control conditional routing. They must be **materialized as
Power Automate decision branches**, not stored as SharePoint columns. The flow logic will read
request attributes (company, site, employee type) and make routing decisions without storing the
hidden field names.

---

## Workflow Stage Map

```
[Stage 1: Requestor Submits]
    ├─→ [Stage 2: HOD Approval]
    │   ├─→ Approved → [Stage 3: Notes Admin Provisioning]
    │   └─→ Rejected → [Stage 1: Requestor Rework] ◄─┐
    │                                                 │
    └─→ [Stage 3: Notes Admin Creates ID]            │
        ├─→ ID Created → [Stage 4: IT Hardware]      │
        └─→ Error → [Back to HOD/Requestor]            │
        │                                              │
        ├─→ [Stage 4: IT Hardware/Support Completion] │
            ├─→ Hardware Assigned → [Closed]           │
            └─→ Escalation → [Stage 3: Re-Route] ─────┘
```

| Stage # | Stage Name               | Trigger                                                             | Actor(s)                                | SP Group          | Actions Available                                                                               | Next Stage                   | Notifications                                   |
| ------- | ------------------------ | ------------------------------------------------------------------- | --------------------------------------- | ----------------- | ----------------------------------------------------------------------------------------------- | ---------------------------- | ----------------------------------------------- |
| 1       | Request Submission       | New item created in `MainDB_IT`                                     | Requestor (employee/HOD representative) | D06-IT-Initiators | Enter employee, company, request type, HOD selector                                             | 2                            | Email to HODApprover with link                  |
| 2       | HOD Approval             | `CurrentAction` = RequestSubmitted; Item waiting for HOD review     | HOD (per HODApprover column)            | D06-IT-HOD        | Approve with optional comment OR Reject with required comment                                   | 3 (Approved) or 1 (Rejected) | Email: Approved→Notes Admin; Rejected→Requestor |
| 3       | Notes Admin Provisioning | `CurrentAction` = HODApproved; Item assigned to Notes admin         | Notes Administrator                     | D06-IT-Editors-L1 | Create internal ID, populate `InternalNotesID`, `ExternalNotesID`, log task in `NotesAdminTask` | 4                            | Email to ITHardwareOwner; Copy to requestor     |
| 4       | IT Hardware Completion   | `CurrentAction` = NotesAdminCompleted; Item awaiting hardware setup | IT Hardware/Support owner               | D06-IT-Editors-L2 | Complete downstream task, set `ITHardwareStatus` = Completed, add remarks                       | Closed                       | Email: Requestor, HOD, stakeholder list         |
| 5       | Closed                   | `CurrentAction` = Closed; No further action required                | System (read-only)                      | D06-IT-Readers    | View only; Archive                                                                              | —                            | Confirmation email to all stakeholders          |

---

## Power Automate Flow Logic (Stage Actions)

### Flow 1: `IT_NIR_Submit` (Trigger: When item created)

**Activation Condition:** `FormCode` = 'NIR' AND `DepartmentCode` = 'IT'

| Step | Logic                    | Action                                                                        | Target                                                     |
| ---- | ------------------------ | ----------------------------------------------------------------------------- | ---------------------------------------------------------- |
| 1    | Validate required fields | Check: `EmailType`, `Company`, `FullName`, `EmpNo`, `HODApprover` all present | Fail → send validation error email to requestor; stop flow |
| 2    | Populate computed fields | Set `Requestor` = CurrentUser. Set `SubmittedDate` = NOW().                   | Update item                                                |
| 3    | Route to HOD             | Lookup `HODApprover` person record → resolve email                            | Send email with approval link                              |
| 4    | Set initial state        | Set `CurrentAction` = 'RequestSubmitted'; `HODApprovalStatus` = 'Pending'     | Update item                                                |
| 5    | Tag environment          | Set `EnvironmentTag` from `Config_AppSettings` (based on site URL)            | Update item (DEC-004)                                      |

**Notifications:**

- To: `HODApprover` email (from Person column)
- Subject: `[NIR] New Notes ID Request from {FullName} — Approval Needed`
- Body: Link to approval screen, requestor details, company, request type

---

### Flow 2: `IT_NIR_HODApprove` (Trigger: When HODApprovalStatus = Approved)

**Activation Condition:** Item Status changed manually OR Power Apps approval action

| Step | Logic                     | Action                                                                                                              | Target                         |
| ---- | ------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| 1    | Capture approval metadata | Set `HODName` = CurrentUser. Set `HODApprovalDate` = NOW().                                                         | Update item                    |
| 2    | Populate routing fields   | Lookup IT routing matrix: `Company`, `ExistingEmailAddress` (if replacement) → Route to Notes PIC email from matrix | Set `NotesAdministrator`       |
| 3    | Set next state            | Set `CurrentAction` = 'HODApproved'; `NotesAdminStatus` = 'Pending'                                                 | Update item                    |
| 4    | Notify Notes Admin        | Send email with provisioning task link                                                                              | To: `NotesAdministrator` email |
| 5    | Copy requestor            | Send approval confirmation                                                                                          | To: Requestor email            |

**Notifications:**

- To: NotesAdministrator (from routing lookup)
- CC: Requestor
- Subject: `[NIR] HOD Approved — Notes ID Provisioning Task`
- Body: Employee details, internal/external ID requirements, any special instructions

---

### Flow 3: `IT_NIR_HODReject` (Trigger: When HODApprovalStatus = Rejected)

| Step | Logic                      | Action                                                                             | Target                                     |
| ---- | -------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------ |
| 1    | Capture rejection metadata | Set `HODName` = CurrentUser. Set `HODApprovalDate` = NOW(). `HODComment` required. | Update item; validate HODComment not empty |
| 2    | Reset to draft             | Set `CurrentAction` = 'RequestRejected'; trigger requestor review flow             | Update item                                |
| 3    | Notify requestor           | Send rejection email with comment and rework instructions                          | To: Requestor email                        |
| 4    | Allow resubmission         | Requestor may edit and resubmit (returns to stage 1)                               | —                                          |

---

### Flow 4: `IT_NIR_NotesAdminComplete` (Trigger: When NotesAdminStatus = Completed)

| Step | Logic                        | Action                                                                                            | Target                                      |
| ---- | ---------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| 1    | Validate provisioning data   | Check: `InternalNotesID` and/or `ExternalNotesID` populated; `NotesAdminTask` contains action log | Fail → send error email; require correction |
| 2    | Capture Notes admin metadata | Set `NotesAdminDate` = NOW(); `NotesAdministrator` = CurrentUser                                  | Update item                                 |
| 3    | Route to IT Hardware         | Lookup site (PRAI/Johor) and hardware routing matrix → populate `ITHardwareOwner`                 | Set column; send to next actor              |
| 4    | Set next state               | Set `CurrentAction` = 'HardwarePending'; `ITHardwareStatus` = 'Pending'                           | Update item                                 |
| 5    | Notify hardware team         | Send hardware setup task link with ID details                                                     | To: `ITHardwareOwner` email                 |

---

### Flow 5: `IT_NIR_HardwareComplete` (Trigger: When ITHardwareStatus = Completed)

| Step | Logic                       | Action                                                                      | Target                                             |
| ---- | --------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------- |
| 1    | Capture hardware completion | Set `ITHardwareDate` = NOW(); `ITHardwareOwner` = CurrentUser               | Update item                                        |
| 2    | Validate closure readiness  | Check: `ITHardwareTask` or `ITHardwareComment` logged; no pending sub-tasks | If incomplete, ask for details                     |
| 3    | Close request               | Set `CurrentAction` = 'Closed'; email closure summary to all                | Update item                                        |
| 4    | Notify stakeholders         | Send closure notification                                                   | To: Requestor, HOD, Notes Admin, IT Hardware owner |
| 5    | Archive & audit log         | Record completion in audit log; item is read-only going forward             | —                                                  |

---

## Role & Permission Matrix

### Domino Group → SharePoint Group Mapping

| Domino Role / Group             | Description                                                         | SharePoint Group    | Permission Level | Power Apps Access                         |
| ------------------------------- | ------------------------------------------------------------------- | ------------------- | ---------------- | ----------------------------------------- |
| Requestor                       | Creates the Notes ID request; typically an employee or HOD delegate | `D06-IT-Initiators` | Contribute       | Create new + Edit own before HOD approval |
| HOD (Head of Department)        | Reviews and approves or rejects the request                         | `D06-IT-HOD`        | Contribute       | Edit Item (approval stage only) + View    |
| Notes PIC / Notes Administrator | Manages Notes ID provisioning                                       | `D06-IT-Editors-L1` | Contribute       | Edit Item (provisioning stage) + View     |
| IT Hardware/Support             | Completes hardware setup and downstream tasks                       | `D06-IT-Editors-L2` | Contribute       | Edit Item (hardware stage) + View         |
| IT / ISG Admin                  | List administrator; manages routing configs and settings            | `D06-IT-Admin`      | Full Control     | Full admin access                         |
| Readers / Stakeholders          | Visibility into completed requests; no edit rights                  | `D06-IT-Readers`    | Read             | View only                                 |

### Stage-Level Edit Security

| Stage                  | Role       | Can Create? | Can Edit This Stage?             | Can Read? | Can Approve?         |
| ---------------------- | ---------- | ----------- | -------------------------------- | --------- | -------------------- |
| 1 — Request Submission | Initiators | Yes         | Yes (own item only until submit) | Yes       | No                   |
| 2 — HOD Approval       | HOD        | No          | Yes (HODApprovalStatus; Comment) | Yes       | Yes                  |
| 3 — Notes Provisioning | Editors-L1 | No          | Yes (ID fields; Task/Remark)     | Yes       | No (workflow-driven) |
| 4 — IT Hardware        | Editors-L2 | No          | Yes (Task status; Comment)       | Yes       | No (workflow-driven) |
| 5 — Closed             | Admin only | No          | No (read-only)                   | Yes       | No                   |

---

## Cross-List Dependencies & Lookups

| Lookup / Reference           | Source List                       | Lookup Column                                              | Used For                                      | Notes                                |
| ---------------------------- | --------------------------------- | ---------------------------------------------------------- | --------------------------------------------- | ------------------------------------ |
| Employee Directory           | `HR_EmployeeDirectory`            | Employee Number → Name, Job Title, Department, Cost Center | Validate EmpNo; auto-populate Designation     | Optional: read-only display          |
| Company List                 | `Config_Companies`                | Choice list: IOI Oleochemical; IOI Acidchem                | Populate Company choice field                 | Must be in sync with valid companies |
| Department List              | `Config_Departments`              | Lookup: Set of IT departments                              | Department selector (optional; informational) | For filtering/reporting              |
| HOD Routing Matrix           | `Config_ApproverMatrix`           | Lookup by Company + Department → HOD email                 | Auto-suggest HODApprover in Submit flow       | PIC routing decision rules here      |
| Notes Admin Routing          | `Config_NotesAdminRouting`        | Lookup by Site (PRAI/Johor) → Notes PIC email              | Assign NotesAdministrator in Approval flow    | Site-specific; must be current       |
| IT Hardware Routing (Penang) | `Config_ITHardwareRouting_Penang` | Lookup by team → support contact                           | Assign ITHardwareOwner for Penang             | Site-specific; must be current       |
| IT Hardware Routing (Johor)  | `Config_ITHardwareRouting_Johor`  | Lookup by team → support contact                           | Assign ITHardwareOwner for Johor              | Site-specific; must be current       |

---

## SharePoint Site & List Inventory

| Asset                 | URL                                                | Notes                                                    |
| --------------------- | -------------------------------------------------- | -------------------------------------------------------- |
| **Department Portal** | `https://ioioi.sharepoint.com/sites/ioi-portal-it` | Primary IT site                                          |
| **Main List**         | `Lists/MainDB_IT`                                  | Live submissions; all forms in IT department             |
| **Form Module Table** | `Lists/IT_NIR_List`                                | Legacy Domino import only; new submissions never go here |
| **Config Lists**      | See Cross-List Dependencies above                  | Referenced by Power Apps and flows                       |

---

## v3 Architecture Alignment (DEC-001, DEC-004, DEC-005)

### DEC-001 — MainDB_IT Submission Architecture

✅ **Applied:** All new submissions write to `MainDB_IT`, not `IT_NIR_List`. Form module table is
import-only.

**Power Automate Trigger:**

```
When an item is created in MainDB_IT
Scope to: FormCode = 'NIR'
```

**Power Apps Entry Point:**

```
Primary: MainDB_IT
Lookup: IT_NIR_List (read-only, for historical reference only)
```

---

### DEC-004 — Three-Tier Environment Strategy

✅ **Applied:** `EnvironmentTag` column tracks DEV / TEST / PROD. Config values (approver emails,
routing tables) are read from `Config_AppSettings` list per environment.

**Environment Determination:**

```
Site URL contains: 'ioi-portal-it' → production environment (PROD)
Site URL contains: 'ioi-portal-it-test' → test environment (TEST)
Site URL contains: 'ioi-portal-it-dev' → dev environment (DEV)
```

**Config Overrides per Environment:**

- DEV: Test approvers, dummy routing (for screen preview)
- TEST: OQ/UAT approvers, shadow routing (for formal testing)
- PROD: Live approvers, live routing (users only)

---

### DEC-005 — FORM_COLUMN_DEFINITIONS_ENHANCED.json Authority

✅ **Referenced:** All column definitions in this blueprint are checked against
`FORM_COLUMN_DEFINITIONS_ENHANCED.json` (v2.0) for consistency. Field types, required flags, and
base columns conform to the authoritative schema.

**Provisioning Validation:**

```
Before list creation, validate:
- All columns exist in FORM_COLUMN_DEFINITIONS_ENHANCED.json
- No custom columns except those explicitly in the definition
- All choice fields match the defined value set
```

---

## Reference Documents

| Document           | Path                                                                  | Purpose                               |
| ------------------ | --------------------------------------------------------------------- | ------------------------------------- |
| Analysis Report    | `docs/migration-analysis/Department_06_IT/NIR_analysis.md`            | Source form structure & field listing |
| Module Overview    | `docs/migration-analysis/Department_06_IT/module_overview.md`         | Form placement in IT module framework |
| Feasibility Report | `docs/migration-analysis/Department_06_IT/NIR_feasibility.md`         | v3 impossibilities & workarounds      |
| Decision Log       | `DECISION_LOG.md`                                                     | DEC-001, DEC-004, DEC-005 full text   |
| Schema Authority   | `(FORM_COLUMN_DEFINITIONS_ENHANCED.json)`                             | Master column definitions (v2.0)      |
| Reference PDF      | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/IT/NIR.pdf` | Original Lotus Domino export          |

---

## Architect Verification Checklist

```
VERIFICATION CHECKLIST — Notes ID Request (NIR)

[✓] All fields identified: 30 fields found, 1 clarified [Type field ambiguity]
[✓] Zero unresolved CLARIFY markers: 1 remaining [Type vs EmailType — needs confirmation]
[✓] Zero unresolved TODO markers: 0 remaining
[✓] Zero unresolved UNCLEAR markers: 0 remaining
[✓] Zero unresolved MISSING markers: 0 remaining
[✓] Workflow stages fully mapped: 5 of 5 stages complete
[✓] Power Automate actions defined for each stage: 5 of 5 flows defined
[✓] Roles mapped to SharePoint groups: 6 of 6 roles mapped
[✓] All mandatory columns mapped: 28 of 30 mapped (2 pending clarification on Type field)

MARKER DETAIL:
- [CLARIFY: Field "Type" (row 9)]
  The NIR form displays both "EmailType" (request type: New Email / Replacement) and a secondary "Type" field.
  Current evidence does not clarify if Type is:
    a) A duplicate/alias of EmailType (should be removed)
    b) A separate classification field (should be mapped separately)
  RECOMMENDATION: Confirm in Domino form instructions or with IT subject matter expert before Craftsman begins screen build.

COMPLETION STATUS: INCOMPLETE — 1 unresolved CLARIFY marker remains
```

---

## Architect Notes

1. **Hidden Fields Materialization:** The 8 Domino hidden routing fields (PIC, ISG, HW, HW2, SW,
   HRE, HRNE, HR) are **not mapped as SharePoint columns**. Instead, Power Automate flows will read
   request attributes and route dynamically. This is the correct pattern for conditional assignment
   logic.

2. **Multi-Stage Edit Control:** Each workflow stage grants edit rights only to the assigned actor.
   For example, the HOD can only edit columns in Stage 2 (HODApprovalStatus, HODComment); the Notes
   admin can only edit Stage 3 columns (ID fields, Task, Remark). Power Apps view filtering and form
   controls must enforce this.

3. **Site-Specific Routing:** IT Hardware routing differs between Penang (HW) and Johor (HW2). The
   flow must check the site context to select the correct routing table.

4. **Official Name Clarification:** The form is claimed as "Notes ID Request" per the
   module_overview.md table. No inventory name conflict detected.

5. **Type Field Clarification Pending:** The CLARIFY marker blocks handoff to Craftsman. Once IT
   confirms whether Type is a duplicate or distinct field, update row 9 and remove the marker.
