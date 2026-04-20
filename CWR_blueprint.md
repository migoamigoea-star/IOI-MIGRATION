<!-- Architect: CWR form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

---

form_code: CWR dept: HR official_name: "Contract Worker Requisition Form (Outsourcing)" owner: "HR
Department, D05" complexity: Medium DQ_REQUIRED: NO gxp_class: "—" status: BLUEPRINT_DRAFT date:
2026-04-14 ino_pattern: "HR-CWR-YYMM-NNNN" sp_list_primary: "MainDB_HR" sp_form_type_discriminator:
"CWR" sp_list_staging: "HR_CWR_List"

---

# CWR — Contract Worker Requisition Form (Outsourcing)

## 1. Form Identity

| Attribute       | Value                                              |
| --------------- | -------------------------------------------------- |
| Form Code       | CWR                                                |
| Full Name       | Contract Worker Requisition Form (Outsourcing)     |
| Department      | Human Resources (D05)                              |
| Module          | M2 — Recruitment & Hiring                          |
| Site(s)         | PRAI, Johor                                        |
| Complexity      | Medium                                             |
| DQ Required     | NO                                                 |
| INO Pattern     | `HR-CWR-YYMM-NNNN` (Power Automate — NEVER canvas) |
| SP Primary List | `MainDB_HR` (FormType = "CWR")                     |
| SP Staging List | `HR_CWR_List` (historical import)                  |

## 2. Business Purpose

The CWR form manages the formal requisition process for outsourced contract workers at IOI sites. It
covers two separate requirement sections:

- **Section A — Permanent/Temporary Contract Workers:** Day-to-day workforce needs including site,
  number of workers, workstation, job description, and working hours.
- **Section B — Plant Shutdown Contract Workers:** Temporary workforce specifically for planned
  plant shutdowns, covering multiple period slots.

The form routes through HOD endorsement, Division Head approval, and HR acknowledgement before
procurement of contract workers can commence. Company policy requires the form to be submitted to HR
a minimum of 2 months in advance.

## 3. SharePoint Schema

### 3a. Primary List — `MainDB_HR` (FormType discriminator: "CWR")

| #   | SP Internal Name | Display Label                | Column Type    | Required | Classification   | Notes                                                                  |
| --- | ---------------- | ---------------------------- | -------------- | -------- | ---------------- | ---------------------------------------------------------------------- |
| 1   | FormType         | Form Type                    | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "CWR"                                                           |
| 2   | INO              | Reference No.                | Single line    | Yes      | SYSTEM-COMPUTED  | HR-CWR-YYMM-NNNN via PA                                                |
| 3   | CurrentStatus    | Current Status               | Choice         | Yes      | WORKFLOW-MANAGED | Draft/Submitted/HODEndorsed/DivApproved/HRAcknowledged/Rejected/Closed |
| 4   | EnvironmentTag   | Environment                  | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                                          |
| 5   | IssueNo          | Issue No.                    | Single line    | No       | USER-ENTERED     | Legacy issue reference                                                 |
| 6   | SendTo           | Initiation Category/To (HOD) | Single line    | Yes      | USER-ENTERED     | Recipient HOD or category                                              |
| 7   | DivHead          | Division Head                | Person         | Yes      | USER-ENTERED     | Division Head name                                                     |
| 8   | DocAuthor        | Requested By                 | Person         | Yes      | SYSTEM-COMPUTED  | Auto-filled from login                                                 |
| 9   | Designation      | Designation                  | Single line    | Yes      | USER-ENTERED     | Requestor's designation                                                |
| 10  | DateIssued       | Date Issued                  | Date           | Yes      | USER-ENTERED     | Form issue date                                                        |
| 11  | WorkerName       | From (Name)                  | Single line    | Yes      | USER-ENTERED     | Requesting person name                                                 |
| 12  | ContractType     | Type of Contract Workers     | Choice         | Yes      | USER-ENTERED     | Permanent/Temporary                                                    |
| 13  | PermCategory     | Category                     | Choice         | Yes      | USER-ENTERED     | Permanent/Temporary                                                    |
| 14  | SiteA            | Site (Section A)             | Choice         | Yes      | USER-ENTERED     | PRAI/Johor                                                             |
| 15  | NoWorkersA       | No. of Workers (Section A)   | Number         | Yes      | USER-ENTERED     | Count required                                                         |
| 16  | WorkstationA     | Section/Workstation (A)      | Single line    | Yes      | USER-ENTERED     | Workstation or section                                                 |
| 17  | JDA              | Job Description (A)          | Multiple lines | Yes      | USER-ENTERED     | JD for Perm/Temp workers                                               |
| 18  | WorkingHour      | Working Hour                 | Single line    | No       | USER-ENTERED     | Shift hours                                                            |
| 19  | CurrentNoWorkers | Current No. of Workers       | Number         | No       | USER-ENTERED     | Existing headcount at station                                          |
| 20  | EffDate          | Effective Date               | Date           | No       | USER-ENTERED     | Date workers needed                                                    |
| 21  | Justification    | Justification                | Multiple lines | Yes      | USER-ENTERED     | Business justification                                                 |
| 22  | RequiredPeriodsA | Required Periods (Section A) | Multiple lines | No       | USER-ENTERED     | JSON: [{from,to,days}×3]                                               |
| 23  | SiteB            | Site (Section B — Shutdown)  | Choice         | No       | USER-ENTERED     | PRAI/Johor                                                             |
| 24  | NoWorkersB       | No. of Workers (Section B)   | Number         | No       | USER-ENTERED     | Shutdown workers needed                                                |
| 25  | WorkstationB     | Section/Workstation (B)      | Single line    | No       | USER-ENTERED     | Shutdown workstation                                                   |
| 26  | JDB              | Job Description (B)          | Multiple lines | No       | USER-ENTERED     | JD for shutdown workers                                                |
| 27  | RequiredPeriodsB | Required Periods (Section B) | Multiple lines | No       | USER-ENTERED     | JSON: [{from,to,days}×3]                                               |
| 28  | HODApp           | HOD Endorsement              | Choice         | No       | WORKFLOW-MANAGED | Approved/Rejected                                                      |
| 29  | HODName          | HOD Name                     | Single line    | No       | WORKFLOW-MANAGED | Filled on endorsement                                                  |
| 30  | HODDate          | HOD Date                     | Date           | No       | WORKFLOW-MANAGED | Endorsement date                                                       |
| 31  | HODRemark        | HOD Remark                   | Multiple lines | No       | WORKFLOW-MANAGED | HOD comments                                                           |
| 32  | DivApp           | Division Head Decision       | Choice         | No       | WORKFLOW-MANAGED | Approved/Rejected                                                      |
| 33  | HODName3         | Division Head Name           | Single line    | No       | WORKFLOW-MANAGED | Filled on approval                                                     |
| 34  | HODDate3         | Division Head Date           | Date           | No       | WORKFLOW-MANAGED | Approval date                                                          |
| 35  | HODRemark3       | Division Head Remark         | Multiple lines | No       | WORKFLOW-MANAGED | Division Head comments                                                 |
| 36  | HRName           | HR Name                      | Single line    | No       | WORKFLOW-MANAGED | HR acknowledging officer                                               |
| 37  | HRPosition       | HR Position                  | Single line    | No       | WORKFLOW-MANAGED | HR officer position                                                    |
| 38  | HRDate           | HR Acknowledged Date         | Date           | No       | WORKFLOW-MANAGED | Acknowledgement date                                                   |
| 39  | Attachments      | Supporting Documents         | Attachment     | No       | USER-ENTERED     | Supporting files                                                       |
| 40  | IsLocked         | Is Locked                    | Yes/No         | No       | WORKFLOW-MANAGED | Lock after HRAcknowledged                                              |

### 3b. Staging List — `HR_CWR_List`

Historical import from Lotus Domino. Mirrors `MainDB_HR` structure filtered to FormType=CWR. Last 24
months of records migrated.

## 4. Field Inventory Summary

| Category               | Count                                                                                                             |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Identity / System      | 4 (FormType, INO, CurrentStatus, EnvironmentTag)                                                                  |
| Requestor Details      | 6 (SendTo, DivHead, DocAuthor, Designation, DateIssued, WorkerName)                                               |
| Worker Type & Category | 3 (ContractType, PermCategory, IsLocked)                                                                          |
| Section A — Perm/Temp  | 9 (SiteA, NoWorkersA, WorkstationA, JDA, WorkingHour, CurrentNoWorkers, EffDate, Justification, RequiredPeriodsA) |
| Section B — Shutdown   | 5 (SiteB, NoWorkersB, WorkstationB, JDB, RequiredPeriodsB)                                                        |
| HOD Endorsement        | 4 (HODApp, HODName, HODDate, HODRemark)                                                                           |
| Division Head Approval | 4 (DivApp, HODName3, HODDate3, HODRemark3)                                                                        |
| HR Acknowledgement     | 3 (HRName, HRPosition, HRDate)                                                                                    |
| Supporting             | 2 (Attachments, IssueNo)                                                                                          |
| **Total**              | **40**                                                                                                            |

## 5. Workflow

### 5a. Stage Map

| Stage | Name                   | Trigger          | Actor                         | Actions                 | Next Stage   | Notification Target      |
| ----- | ---------------------- | ---------------- | ----------------------------- | ----------------------- | ------------ | ------------------------ |
| 1     | Drafting               | New form         | DocAuthor                     | Fill details, submit    | 2            | DivHead (HOD) via SendTo |
| 2     | HOD Endorsement        | Stage 1 Submit   | DivHead (HOD)                 | Approve/Reject + Remark | 3 / Rejected | DocAuthor if rejected    |
| 3     | Division Head Approval | HOD Endorsed     | Division Head (HODName3 role) | Approve/Reject          | 4 / Rejected | DocAuthor, HOD           |
| 4     | HR Acknowledgement     | DivHead Approved | HR Officer                    | Acknowledge + sign      | Closed       | DocAuthor, DivHead       |
| R     | Rejected               | Any stage        | —                             | Record reason           | —            | DocAuthor                |

### 5b. Power Automate Flows

| Flow Name            | Trigger                | Key Actions                                                              |
| -------------------- | ---------------------- | ------------------------------------------------------------------------ |
| `CWR_OnSubmit`       | Stage 1 → Submit       | Generate INO, set CurrentStatus=Submitted, notify HOD                    |
| `CWR_OnHODEndorse`   | HOD Approves           | Set HODApp=Approved, set CurrentStatus=HODEndorsed, notify Division Head |
| `CWR_OnHODReject`    | HOD Rejects            | Set HODApp=Rejected, CurrentStatus=Rejected, notify DocAuthor            |
| `CWR_OnDivApprove`   | Division Head Approves | Set DivApp=Approved, CurrentStatus=DivApproved, notify HR                |
| `CWR_OnDivReject`    | Division Head Rejects  | Set DivApp=Rejected, CurrentStatus=Rejected, notify DocAuthor            |
| `CWR_OnHRAck`        | HR Acknowledges        | Set HRDate, CurrentStatus=HRAcknowledged, IsLocked=Yes, notify DocAuthor |
| `CWR_2MonthReminder` | DateIssued approaching | Remind DocAuthor to submit 2 months before effective date                |

## 6. Screen Inventory

| Screen          | Purpose                                                | Key Controls                                             |
| --------------- | ------------------------------------------------------ | -------------------------------------------------------- |
| `CWR_List`      | Gallery of all requisitions, filterable by site/status | Gallery, search, status chips                            |
| `CWR_New`       | New requisition form — both sections                   | Tabbed container (Section A / Section B), person pickers |
| `CWR_View`      | Read-only detail with full approval timeline           | Display form, approval timeline component                |
| `CWR_Edit`      | Edit by DocAuthor while in Draft                       | Edit form, section toggle                                |
| `CWR_HODReview` | HOD endorsement screen                                 | Read-only summary + Approve/Reject radios + Remark field |
| `CWR_DivReview` | Division Head approval screen                          | Read-only summary + Approve/Reject radios + Remark field |
| `CWR_HRAck`     | HR acknowledgement screen                              | Summary + HRName/Position/Date fields                    |

## 7. Navigation Map

```
CWR_List
  ├── [New Request] → CWR_New → OnSubmit → CWR_View
  ├── [Gallery Row] → CWR_View
  │     ├── [Edit] (Draft only) → CWR_Edit → CWR_View
  │     ├── [Endorse] (HOD role) → CWR_HODReview
  │     ├── [Approve/Reject] (DivHead role) → CWR_DivReview
  │     └── [Acknowledge] (HR role) → CWR_HRAck
  └── [Back] → Home
```

## 8. Role Matrix

| Role                  | SP Group          | Screen Access                 | Actions            |
| --------------------- | ----------------- | ----------------------------- | ------------------ |
| Requestor (DocAuthor) | D05-HR-Initiators | List, New, View, Edit (Draft) | Create, Edit Draft |
| HOD                   | D05-HR-HOD        | List, View, HODReview         | Endorse            |
| Division Head         | D05-HR-DivHead    | List, View, DivReview         | Approve/Reject     |
| HR Officer            | D05-HR-Officers   | List, View, HRAck             | Acknowledge        |
| HR Admin              | D05-HR-Admin      | All                           | Full + override    |
| Reader                | D05-HR-Readers    | List, View                    | Read only          |

## 9. Related Lists

| List                   | Relationship      | Purpose                                          |
| ---------------------- | ----------------- | ------------------------------------------------ |
| `MainDB_HR`            | Parent (shared)   | All HR forms via FormType discriminator          |
| `HR_Department_Master` | Lookup            | Site and department codes                        |
| `HR_JD_List`           | Lookup (optional) | Pre-approved job descriptions for JDA/JDB fields |
| `HR_CWR_List`          | Staging           | Historical Domino records                        |

## 10. Migration Notes

- **Period fields (RequiredPeriodsA / RequiredPeriodsB):** Domino stored up to 3 date-range periods
  per section as separate fields (`tPeriod_1_1`, `fPeriod_1_1`, `TotalDays_1_1`… ×3). M365 strategy:
  store as JSON array in a multi-line text column. Power Apps renders via a gallery control.
  Migration script transforms the legacy period columns to JSON during staging import.
- **2-month advance notice:** Encode as a PA reminder flow. Check `EffDate - 60 days` and alert
  DocAuthor if form not yet at HRAcknowledged status.
- **Legacy `IssueNo`:** Preserved as a searchable field for historical reference cross-referencing.
- **Section B (Shutdown):** All Section B fields are optional. In the canvas screen, Section B is
  shown/hidden based on a `varShowSectionB` toggle control.
- **INO generation:** NEVER computed in canvas. Power Automate `CWR_OnSubmit` generates
  `HR-CWR-YYMM-NNNN` and patches the SP item.
