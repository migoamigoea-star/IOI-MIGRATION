<!-- Architect: FTCR form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

---

form_code: FTCR dept: HR official_name: "Fixed Term Contract Requisition Form" owner: "HR
Department, D05" complexity: Medium DQ_REQUIRED: NO gxp_class: "—" status: BLUEPRINT_DRAFT date:
2026-04-14 ino_pattern: "HR-FTC-YYMM-NNNN" sp_list_primary: "MainDB_HR" sp_form_type_discriminator:
"FTCR" sp_list_staging: "HR_FTCR_List"

---

# FTCR — Fixed Term Contract Requisition Form

## 1. Form Identity

| Attribute       | Value                                              |
| --------------- | -------------------------------------------------- |
| Form Code       | FTCR                                               |
| Full Name       | Fixed Term Contract Requisition Form               |
| Department      | Human Resources (D05)                              |
| Module          | M2 — Recruitment & Hiring                          |
| Site(s)         | PRAI, Johor                                        |
| Complexity      | Medium                                             |
| DQ Required     | NO                                                 |
| INO Pattern     | `HR-FTC-YYMM-NNNN` (Power Automate — NEVER canvas) |
| SP Primary List | `MainDB_HR` (FormType = "FTCR")                    |
| SP Staging List | `HR_FTCR_List` (historical import)                 |

## 2. Business Purpose

The FTCR form is the formal internal process for departments to request an extension or renewal of a
fixed-term contract for an existing employee whose contract is nearing its end (i.e., approaching
retirement date). The HOD/Division Head initiates the requisition, documents the business
justification, identifies whether a successor exists, and routes it through HR for approval by the
COO and/or Executive Director.

A key feature of this form is the **Employee Background History** — a 6-year rolling table of
performance (appraisal rating, disciplinary records, medical/hospitalisation leave, absent/late
records, and medical expenses) which informs the approval decision.

## 3. SharePoint Schema

### 3a. Primary List — `MainDB_HR` (FormType discriminator: "FTCR")

| #   | SP Internal Name  | Display Label               | Column Type    | Required | Classification   | Notes                                                                         |
| --- | ----------------- | --------------------------- | -------------- | -------- | ---------------- | ----------------------------------------------------------------------------- |
| 1   | FormType          | Form Type                   | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "FTCR"                                                                 |
| 2   | INO               | Reference No.               | Single line    | Yes      | SYSTEM-COMPUTED  | HR-FTC-YYMM-NNNN via PA                                                       |
| 3   | CurrentStatus     | Current Status              | Choice         | Yes      | WORKFLOW-MANAGED | Draft/Submitted/EndorsedHOD/ApprovedHR/ApprovedCOO/ApprovedED/Rejected/Closed |
| 4   | EnvironmentTag    | Environment                 | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                                                 |
| 5   | EmpName           | Employee Name               | Single line    | Yes      | USER-ENTERED     | Subject employee                                                              |
| 6   | EmpNo             | Employee No.                | Single line    | Yes      | USER-ENTERED     | Staff ID                                                                      |
| 7   | DOB               | Date of Birth               | Date           | Yes      | USER-ENTERED     | For age calculation                                                           |
| 8   | EmpAge            | Age                         | Number         | No       | SYSTEM-COMPUTED  | PA-calculated from DOB                                                        |
| 9   | EmpPost           | Position                    | Single line    | Yes      | USER-ENTERED     | Current title                                                                 |
| 10  | Dept              | Department/Section          | Single line    | Yes      | USER-ENTERED     | Employee's dept                                                               |
| 11  | JoinDate          | Date Joined                 | Date           | Yes      | USER-ENTERED     | Original join date                                                            |
| 12  | RetDate           | Retirement Date             | Date           | Yes      | USER-ENTERED     | Scheduled retirement                                                          |
| 13  | DivHead           | HOD/Division Head           | Person         | Yes      | USER-ENTERED     | Form initiator                                                                |
| 14  | Attachment        | Supporting Documents        | Attachment     | No       | USER-ENTERED     | Contract docs, CV                                                             |
| 15  | CPeriod           | Contract Period (Months)    | Number         | Yes      | USER-ENTERED     | No. of months for extension                                                   |
| 16  | Others            | Period Notes                | Single line    | No       | USER-ENTERED     | Specify if "Others" selected                                                  |
| 17  | DivHeadJust       | Division Head Justification | Multiple lines | Yes      | USER-ENTERED     | Business case                                                                 |
| 18  | InSuccess         | Identified Successor        | Choice         | Yes      | USER-ENTERED     | Yes/No                                                                        |
| 19  | Ext               | For External Advertisement  | Choice         | No       | USER-ENTERED     | Yes/No                                                                        |
| 20  | SucName           | Successor Name              | Single line    | No       | USER-ENTERED     | Required if InSuccess=Yes                                                     |
| 21  | SucEmpNo          | Successor Emp. No.          | Single line    | No       | USER-ENTERED     | Required if InSuccess=Yes                                                     |
| 22  | SucPost           | Successor Position          | Single line    | No       | USER-ENTERED     |                                                                               |
| 23  | SucAge            | Successor Age               | Number         | No       | SYSTEM-COMPUTED  |                                                                               |
| 24  | SucDept           | Successor Dept/Section      | Single line    | No       | USER-ENTERED     |                                                                               |
| 25  | SucDate           | Successor Start Date        | Date           | No       | USER-ENTERED     | When successor takes over                                                     |
| 26  | TrReq             | Training Required           | Choice         | No       | USER-ENTERED     | Yes/No                                                                        |
| 27  | TrList            | Training List               | Multiple lines | No       | USER-ENTERED     | List if TrReq=Yes                                                             |
| 28  | Remarks           | Remarks/Attachment Notes    | Multiple lines | No       | USER-ENTERED     | General comments                                                              |
| 29  | SubBy             | Submitted By (Dept Head)    | Single line    | No       | USER-ENTERED     | Department/Section Head name                                                  |
| 30  | SubDesg           | Submission Designation      | Single line    | No       | USER-ENTERED     | Submitter's title                                                             |
| 31  | SubDate           | Submission Date             | Date           | No       | USER-ENTERED     | Date submitted by Dept Head                                                   |
| 32  | EndBy             | Endorsed By (Div Head)      | Single line    | No       | WORKFLOW-MANAGED | Division/Dept Head name                                                       |
| 33  | EndDesg           | Endorser Designation        | Single line    | No       | WORKFLOW-MANAGED |                                                                               |
| 34  | EndDate           | Endorsement Date            | Date           | No       | WORKFLOW-MANAGED |                                                                               |
| 35  | AppHR             | Approved By HR              | Person         | No       | WORKFLOW-MANAGED | HR approver                                                                   |
| 36  | AppCOO            | Approved By COO             | Person         | No       | WORKFLOW-MANAGED | COO approver                                                                  |
| 37  | AppED             | Approved By ED              | Person         | No       | WORKFLOW-MANAGED | Exec Director (if required)                                                   |
| 38  | Fixed             | Contract Renewed            | Choice         | No       | WORKFLOW-MANAGED | Yes/No — final outcome                                                        |
| 39  | CaseStatus        | Case Status                 | Choice         | No       | WORKFLOW-MANAGED | Open/Approved/Rejected                                                        |
| 40  | AppFor            | Approved For (Period)       | Single line    | No       | WORKFLOW-MANAGED | Final approved period                                                         |
| 41  | NotHOD            | Notify HOD                  | Yes/No         | No       | WORKFLOW-MANAGED | Flag to send HOD notification                                                 |
| 42  | Remarks2          | HR Remarks                  | Multiple lines | No       | WORKFLOW-MANAGED | HR additional comments                                                        |
| 43  | CA                | Current Action              | Choice         | No       | WORKFLOW-MANAGED | Stage tracking                                                                |
| 44  | BackgroundHistory | Employee Background History | Multiple lines | No       | USER-ENTERED     | JSON: 6-year rolling table                                                    |

> **BackgroundHistory JSON schema:**
> `[{year, appraisalRating, disciplinaryCount, mcDays, hoDays, absentDays, lateDays, nplDays, medExpRM}]`
> (6 rows max)

### 3b. Staging List — `HR_FTCR_List`

Historical import from Lotus Domino. Mirrors `MainDB_HR` filtered to FormType=FTCR. Last 12 months
migrated (contract renewal records older than 12 months are archived only).

## 4. Field Inventory Summary

| Category               | Count                                                                        |
| ---------------------- | ---------------------------------------------------------------------------- |
| Identity / System      | 4 (FormType, INO, CurrentStatus, EnvironmentTag)                             |
| Employee Details       | 9 (EmpName, EmpNo, DOB, EmpAge, EmpPost, Dept, JoinDate, RetDate, DivHead)   |
| Contract Justification | 7 (CPeriod, Others, DivHeadJust, InSuccess, Ext, TrReq, TrList)              |
| Successor Details      | 7 (SucName, SucEmpNo, SucPost, SucAge, SucDept, SucDate, Remarks)            |
| Submission Block       | 4 (SubBy, SubDesg, SubDate, Attachment)                                      |
| Endorsement/Approval   | 9 (EndBy, EndDesg, EndDate, AppHR, AppCOO, AppED, Fixed, CaseStatus, AppFor) |
| Workflow / Admin       | 4 (NotHOD, Remarks2, CA, BackgroundHistory)                                  |
| **Total**              | **44**                                                                       |

## 5. Workflow

### 5a. Stage Map

| Stage | Name                           | Trigger             | Actor                     | Actions                                 | Next Stage         | Notification Target   |
| ----- | ------------------------------ | ------------------- | ------------------------- | --------------------------------------- | ------------------ | --------------------- |
| 1     | Drafting                       | New form            | DivHead                   | Fill employee and justification details | 2                  | HOD notification      |
| 2     | Dept Head Submission           | Submit by Dept Head | SubBy (Dept/Section Head) | Review + submit                         | 3                  | Division Head (EndBy) |
| 3     | Division/Dept Head Endorsement | Stage 2 Submit      | EndBy                     | Endorse                                 | 4                  | HR                    |
| 4     | HR Approval                    | Endorsed            | HR Officer (AppHR)        | Approve/Reject                          | 5 / Rejected       | COO                   |
| 5     | COO Approval                   | HR Approved         | COO (AppCOO)              | Approve/Reject                          | 6 (if ED) / Closed | ED or DocAuthor       |
| 6     | ED Approval (if needed)        | COO Approved        | ED (AppED)                | Approve/Reject                          | Closed             | DocAuthor             |
| R     | Rejected                       | Any stage           | —                         | Record reason                           | —                  | DivHead, DocAuthor    |

> **Note:** ED approval is only triggered for "New Headcount" or cases where CPeriod > 12 months.

### 5b. Power Automate Flows

| Flow Name              | Trigger             | Key Actions                                                                           |
| ---------------------- | ------------------- | ------------------------------------------------------------------------------------- |
| `FTCR_OnSubmit`        | Stage 1 Submit      | Generate INO, set CurrentStatus=Submitted, notify Dept Head (SubBy)                   |
| `FTCR_OnDeptSubmit`    | Dept Head submits   | Set CurrentStatus=EndorsedDept, notify DivHead                                        |
| `FTCR_OnEndorse`       | DivHead endorses    | Populate EndBy/EndDate/EndDesg, notify HR                                             |
| `FTCR_OnHRApprove`     | HR approves         | Set AppHR, notify COO                                                                 |
| `FTCR_OnCOOApprove`    | COO approves        | Set AppCOO; if CPeriod > 12 months → notify ED; else → close with Fixed=Yes           |
| `FTCR_OnEDApprove`     | ED approves         | Set AppED, Fixed=Yes, CaseStatus=Approved, notify DivHead/DocAuthor                   |
| `FTCR_OnReject`        | Any stage rejection | Set CaseStatus=Rejected, notify DivHead and DocAuthor                                 |
| `FTCR_AgeCalculation`  | DOB field populated | Compute EmpAge = DateDifference from DOB to today in years (triggered on item update) |
| `FTCR_RetirementAlert` | Scheduled daily     | 3 months before RetDate, alert HR and DivHead to initiate FTCR if not yet submitted   |

## 6. Screen Inventory

| Screen               | Purpose                                                | Key Controls                                                             |
| -------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------ |
| `FTCR_List`          | Gallery of all FTCR records, filterable by dept/status | Gallery, date range filter, status chips                                 |
| `FTCR_New`           | New FTCR form entry                                    | Employee picker, date pickers, JD fields, Background History table entry |
| `FTCR_View`          | Read-only view with full approval chain                | Display form, 6-year history table, approval timeline                    |
| `FTCR_Edit`          | Edit while in Draft/pending submission                 | Editable form, history table grid                                        |
| `FTCR_EndorseReview` | Division Head endorsement                              | Summary + Endorse button + date auto-fill                                |
| `FTCR_HRReview`      | HR approval screen                                     | Summary + history table + Approve/Reject                                 |
| `FTCR_COOReview`     | COO approval screen                                    | Executive summary + Approve/Reject                                       |
| `FTCR_EDReview`      | ED approval (conditional)                              | Executive summary + Approve/Reject                                       |

## 7. Navigation Map

```
FTCR_List
  ├── [New FTCR] → FTCR_New → submit → FTCR_View
  ├── [Gallery Row] → FTCR_View
  │     ├── [Edit] (Draft only) → FTCR_Edit → FTCR_View
  │     ├── [Endorse] (DivHead role) → FTCR_EndorseReview
  │     ├── [HR Approve] → FTCR_HRReview
  │     ├── [COO Approve] → FTCR_COOReview
  │     └── [ED Approve] (conditional) → FTCR_EDReview
  └── [Back] → Home
```

## 8. Role Matrix

| Role                | SP Group          | Screen Access             | Actions                      |
| ------------------- | ----------------- | ------------------------- | ---------------------------- |
| Initiator (DivHead) | D05-HR-Initiators | List, New, View, Edit     | Create, Edit Draft           |
| Dept/Section Head   | D05-HR-Editors-L1 | List, View, EndorseReview | Submit Dept stage            |
| Division Head       | D05-HR-DivHead    | List, View, EndorseReview | Endorse                      |
| HR Officer          | D05-HR-Officers   | List, View, HRReview      | Approve/Reject               |
| COO                 | D01-COO           | List, View, COOReview     | Approve/Reject               |
| Executive Director  | D01-Board-Members | List, View, EDReview      | Approve/Reject (conditional) |
| HR Admin            | D05-HR-Admin      | All                       | Full admin                   |
| Reader              | D05-HR-Readers    | List, View                | Read only                    |

## 9. Related Lists

| List                   | Relationship    | Purpose                                                         |
| ---------------------- | --------------- | --------------------------------------------------------------- |
| `MainDB_HR`            | Parent (shared) | All HR forms via FormType discriminator                         |
| `HR_Department_Master` | Lookup          | Department/section codes                                        |
| `HR_FTCR_List`         | Staging         | Historical Domino records                                       |
| `HR_Employee_Master`   | Lookup (future) | Employee demographic lookup (EmpNo → auto-fill DOB, post, dept) |

## 10. Migration Notes

- **Employee Background History:** Domino stored this as 8 separate fields × 6 years = 48 columns
  (AprRate_1 to AprRate_6, etc.). M365 strategy: consolidate into a single JSON multi-line field
  `BackgroundHistory`. Power Apps renders as a read-only gallery table (6 rows × 9 columns).
  Migration script transforms legacy columns to JSON array during staging import.
- **Successor details (SucName, SucEmpNo, etc.):** Shown/hidden in canvas based on `varInSuccess`
  toggle linked to `InSuccess` field value.
- **Age computation:** `EmpAge` is never entered manually — PA flow computes from `DOB`. Canvas
  displays but does not allow editing of this field.
- **ED approval gate:** Only triggered if `CPeriod > 12` or `DivHeadJust` contains keyword "New
  Headcount". This logic is enforced in `FTCR_OnCOOApprove` PA flow.
- **RetirementAlert:** Scheduled PA runs daily. If employee `RetDate` is within 90 days and no open
  FTCR exists, it creates a notification to HR suggesting a new FTCR be initiated.
- **INO generation:** NEVER in canvas. `FTCR_OnSubmit` generates `HR-FTC-YYMM-NNNN` and patches the
  SP item.
