<!-- Architect: SR form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

---

form_code: SR dept: HR official_name: "Staff Requisition (SR) Form" owner: "Oleo Local HR"
complexity: Medium DQ_REQUIRED: YES gxp_class: "Indirect GxP" status: BLUEPRINT_DRAFT date:
2026-04-14 ino_pattern: "HR-SR-YYMM-NNNN" sp_list_primary: "MainDB_HR" sp_form_type_discriminator:
"SR" sp_list_staging: "HR_SR_List" sp_child_table: "HR_SR_InterviewLog"

---

# SR — Staff Requisition Form

## 1. Form Identity

| Attribute       | Value                                                                              |
| --------------- | ---------------------------------------------------------------------------------- |
| Form Code       | SR                                                                                 |
| Full Name       | Staff Requisition (SR) Form                                                        |
| Department      | Human Resources (D05)                                                              |
| Module          | M2 — Recruitment & Hiring                                                          |
| Entity Scope    | PCO / PCEO / ECM                                                                   |
| Complexity      | Medium                                                                             |
| DQ Required     | **YES — Indirect GxP**                                                             |
| GxP Class       | Indirect GxP (authorises personnel for roles that may interact with GxP processes) |
| DQ Owner        | Oleo Local HR                                                                      |
| INO Pattern     | `HR-SR-YYMM-NNNN` (Power Automate — NEVER canvas)                                  |
| SP Primary List | `MainDB_HR` (FormType = "SR")                                                      |
| SP Child Table  | `HR_SR_InterviewLog` (interview batch tracking rows)                               |
| SP Staging List | `HR_SR_List` (historical import)                                                   |

## 2. Business Purpose

The SR form is the **formal gateway to the recruitment process**. No job vacancy can be advertised —
internally or externally — without an approved SR. It authorises a functional department to fill a
vacancy (replacement headcount) or create a new headcount position.

The form routes through a 4-tier approval chain:

1. Requisitioner creates the SR and specifies the vacancy (job title, grade, reason).
2. HOD validates and budgets the request.
3. Executive team (Division Head / ED) provides strategic clearance.
4. HR/GHR verifies headcount budget and publishes the job.

The SR also captures an **interview tracking table** (up to 10 recruitment cycles) to audit the
recruitment pipeline for each approved vacancy — this creates the Indirect GxP nexus for filling
roles that may affect product quality.

> **Policy: Internal advertisement must be posted for 5 working days before external advertisement
> is permitted.** PA flow enforces this lockout.

## 3. SharePoint Schema

### 3a. Primary List — `MainDB_HR` (FormType: "SR") — Requisition Header

| #   | SP Internal Name | Display Label              | Column Type | Required | Classification   | Notes                                                       |
| --- | ---------------- | -------------------------- | ----------- | -------- | ---------------- | ----------------------------------------------------------- |
| 1   | FormType         | Form Type                  | Choice      | Yes      | SYSTEM-COMPUTED  | Fixed: "SR"                                                 |
| 2   | INO              | SR Ref No.                 | Single line | Yes      | SYSTEM-COMPUTED  | HR-SR-YYMM-NNNN via PA                                      |
| 3   | CurrentStatus    | Workflow Status            | Choice      | Yes      | WORKFLOW-MANAGED | Proposing/Authorizing/Finalizing/Commencing/Rejected/Closed |
| 4   | EnvironmentTag   | Environment                | Choice      | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                               |
| 5   | DocNo            | SR Reference No. (Legacy)  | Single line | No       | SYSTEM-COMPUTED  | Legacy DocNo from Domino                                    |
| 6   | DocAuthor        | Created By (Requisitioner) | Person      | Yes      | SYSTEM-COMPUTED  | Auto-filled from login                                      |
| 7   | ReqDept          | Requesting Department      | Single line | Yes      | USER-ENTERED     | Department with vacancy                                     |
| 8   | VacancyTitle     | Vacancy Title              | Single line | Yes      | USER-ENTERED     | Job title required                                          |
| 9   | Grade            | Grade / Band               | Single line | Yes      | USER-ENTERED     | Salary band                                                 |
| 10  | VacancyReason    | Reason for Vacancy         | Choice      | Yes      | USER-ENTERED     | New Headcount/Replacement/Promotion                         |
| 11  | ReplacingName    | Replacing (Name)           | Single line | No       | USER-ENTERED     | Only if Reason=Replacement                                  |
| 12  | LinkedJDRef      | Linked JD Reference        | Lookup      | No       | USER-ENTERED     | Link to approved JD record                                  |
| 13  | AdChannel        | Advertisement Channel      | Choice      | Yes      | USER-ENTERED     | Internal/External/JobsDB/LinkedIn/Multiple                  |
| 14  | InternalAdDate   | Internal Ad Posted Date    | Date        | No       | WORKFLOW-MANAGED | Set by PA on internal posting                               |
| 15  | ExternalAdDate   | External Ad Posted Date    | Date        | No       | WORKFLOW-MANAGED | Set by PA — only after 5-day lockout                        |
| 16  | hodName          | GHR Reviewer (HR Manager)  | Person      | Yes      | WORKFLOW-MANAGED | Final HR verifier                                           |
| 17  | hodStatus        | GHR Status                 | Choice      | Yes      | WORKFLOW-MANAGED | Pending/Acknowledged/Rejected                               |
| 18  | Editor1          | HOD Approver               | Person      | Yes      | WORKFLOW-MANAGED | Stage 2 actor                                               |
| 19  | Editor2          | Reserve Approver           | Person      | No       | WORKFLOW-MANAGED | Backup for Editor1                                          |
| 20  | Editor3          | Division Head              | Person      | No       | WORKFLOW-MANAGED | Stage 3 actor                                               |
| 21  | Editor4          | Executive Director         | Person      | No       | WORKFLOW-MANAGED | Stage 3 ED if needed                                        |
| 22  | Editor5          | CFO (New HC only)          | Person      | No       | WORKFLOW-MANAGED | Only triggered for new headcount                            |
| 23  | DateModified     | Last Revised               | Date        | No       | SYSTEM-COMPUTED  | Auto-updated by SP                                          |
| 24  | NextRemDate      | SLA Nudge Date             | Date        | No       | SYSTEM-COMPUTED  | Computed: Submitted + 5 working days                        |
| 25  | Attachment       | Supporting Documents       | Attachment  | No       | USER-ENTERED     | JD copies, org charts                                       |
| 26  | IsLocked         | Is Locked                  | Yes/No      | No       | WORKFLOW-MANAGED | Lock after Closed                                           |

### 3b. Child Table — `HR_SR_InterviewLog`

Tracks recruitment cycles linked to the SR. One row per advertisement cycle / interview batch.
Linked to parent via `SRRef` (lookup to MainDB_HR.INO).

| #   | SP Internal Name | Display Label          | Column Type        | Required | Notes                          |
| --- | ---------------- | ---------------------- | ------------------ | -------- | ------------------------------ |
| 1   | SRRef            | SR Reference           | Lookup (MainDB_HR) | Yes      | Parent SR record               |
| 2   | BatchNo          | Batch / Cycle No.      | Number             | Yes      | 1–10                           |
| 3   | InterviewDate    | Interview Date         | Date               | No       | USER-ENTERED                   |
| 4   | NoApplicants     | No. of Applicants      | Number             | No       | USER-ENTERED                   |
| 5   | NoShortlisted    | No. Shortlisted        | Number             | No       | USER-ENTERED                   |
| 6   | LinkedINTRef     | Linked INTERVIEWDB Ref | Lookup             | No       | Link to INTERVIEWDB batch      |
| 7   | Outcome          | Outcome                | Choice             | No       | OngoingSearch/Filled/Withdrawn |

### 3c. Staging List — `HR_SR_List`

Historical Domino records. Interview tracking rows `I_1-10`, `B_1-10`, `G_1-10` are normalised into
individual rows in `HR_SR_InterviewLog` during migration.

## 4. Field Inventory Summary

| Category                       | Count                                                                                  |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| Identity / System              | 5 (FormType, INO, CurrentStatus, EnvironmentTag, DocNo)                                |
| Requisition Details            | 7 (DocAuthor, ReqDept, VacancyTitle, Grade, VacancyReason, ReplacingName, LinkedJDRef) |
| Advertisement                  | 3 (AdChannel, InternalAdDate, ExternalAdDate)                                          |
| Approval Chain                 | 8 (hodName, hodStatus, Editor1–Editor5)                                                |
| SLA / Process                  | 3 (DateModified, NextRemDate, IsLocked)                                                |
| Supporting                     | 1 (Attachment)                                                                         |
| Interview Log (child, per row) | 7                                                                                      |
| **Total**                      | **34**                                                                                 |

## 5. Workflow

### 5a. Stage Map

| Stage | Name        | Trigger          | Actor                              | Actions                        | Next Stage | Notification Target       |
| ----- | ----------- | ---------------- | ---------------------------------- | ------------------------------ | ---------- | ------------------------- |
| 1     | Proposing   | New SR           | DocAuthor                          | Log vacancy details, link JD   | 2          | Editor1 (HOD)             |
| 2     | Authorizing | Stage 1 Submit   | Editor1 (HOD) + Editor3 (Div Head) | Budget sign-off                | 3          | ED List / CFO (if New HC) |
| 3     | Finalizing  | Stage 2 Approved | Editor4 (ED)                       | Executive clearance            | 4          | hodName (HR)              |
| 4     | Commencing  | Stage 3 OK       | hodName (HR Manager)               | Acknowledge headcount, post ad | Closed     | DocAuthor, Recruiter      |
| R     | Rejected    | Any stage        | —                                  | Record reason                  | —          | DocAuthor                 |

> **CFO gate:** If `VacancyReason = New Headcount`, `FTCR_OnCOOApprove` triggers an additional CFO
> (Editor5) approval node at Stage 3 before ED sign-off.

### 5b. Power Automate Flows

| Flow Name            | Trigger                         | Key Actions                                                                                                      |
| -------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `SR_OnSubmit`        | Stage 1 Submit                  | Generate INO, set CurrentStatus=Authorizing, compute NextRemDate (+5 wd), notify Editor1                         |
| `SR_OnHODApprove`    | Editor1 approves                | Notify Editor3 (Div Head)                                                                                        |
| `SR_OnDivApprove`    | Editor3 approves                | If VacancyReason=New Headcount → add CFO (Editor5) node, else notify Editor4 (ED)                                |
| `SR_OnCFOApprove`    | Editor5 approves                | Notify Editor4 (ED)                                                                                              |
| `SR_OnEDApprove`     | Editor4 approves                | Set CurrentStatus=Finalizing, notify hodName                                                                     |
| `SR_OnHRCommence`    | hodName acknowledges            | Set hodStatus=Acknowledged, post internal ad, set InternalAdDate, CurrentStatus=Commencing                       |
| `SR_InternalLockout` | InternalAdDate + 5 working days | Unlock ExternalAdDate write permission                                                                           |
| `SR_SLANudge`        | Scheduled daily                 | Check NextRemDate; if past and CurrentStatus not advanced → send "Stalled Recruitment" alert to pending approver |
| `SR_OnReject`        | Any stage rejection             | Set CurrentStatus=Rejected, notify DocAuthor and previous actors                                                 |
| `SR_JDSync`          | LinkedJDRef set                 | Pull approved JD skills profile and attach to SR view for HOD reference                                          |

## 6. Screen Inventory

| Screen          | Purpose                                  | Key Controls                                                                 |
| --------------- | ---------------------------------------- | ---------------------------------------------------------------------------- |
| `SR_List`       | Active recruitment funnel dashboard      | Gallery with funnel status chips, vacancy age indicator                      |
| `SR_New`        | New SR entry form                        | Vacancy fields, JD lookup, reason choice, approver chain auto-fill           |
| `SR_View`       | Full read-only detail with interview log | Display form + child gallery (interview batches) + approval timeline         |
| `SR_Edit`       | Edit while in Proposing stage            | Edit form                                                                    |
| `SR_HODReview`  | HOD approval screen                      | Vacancy summary + Approve/Reject                                             |
| `SR_DivReview`  | Division Head review                     | Business impact summary (org chart context) + Approve/Reject                 |
| `SR_EDReview`   | ED strategic clearance                   | Executive summary with budget context + Approve/Reject                       |
| `SR_HRCommence` | HR acknowledgement and ad posting        | Final checklist + Acknowledge + ad channel confirmation                      |
| `SR_AuditView`  | Interview tracking summary table         | Grid of interview batches, applicants/shortlisted counts + INTERVIEWDB links |

## 7. Navigation Map

```
SR_List
  ├── [New SR] → SR_New → OnSubmit → SR_View
  ├── [Gallery Row] → SR_View
  │     ├── [Edit] (Proposing) → SR_Edit → SR_View
  │     ├── [HOD Approve] (Editor1) → SR_HODReview
  │     ├── [Div Head Review] (Editor3) → SR_DivReview
  │     ├── [ED Clearance] (Editor4) → SR_EDReview
  │     ├── [HR Commence] (hodName) → SR_HRCommence
  │     └── [Audit Log] → SR_AuditView
  └── [Back] → Home
```

## 8. Role Matrix

| Role                      | SP Group          | Screen Access                     | Actions                  |
| ------------------------- | ----------------- | --------------------------------- | ------------------------ |
| Requisitioner (DocAuthor) | D[Dept]-Staff     | List, New, View, Edit             | Create, Edit Draft       |
| HOD (Editor1)             | D[Dept]-Managers  | List, View, HODReview             | Approve/Reject Stage 2   |
| Division Head (Editor3)   | D05-HR-DivHead    | List, View, DivReview             | Approve Stage 2          |
| CFO (Editor5)             | D01-Finance       | List, View, CFO panel             | Approve (New HC only)    |
| ED (Editor4)              | D01-Board-Members | List, View, EDReview              | Final strategic sign-off |
| HR Manager (hodName)      | D05-HR-Managers   | List, View, HRCommence, AuditView | Acknowledge, post ad     |
| HR Admin                  | D05-HR-Admin      | All                               | Full admin               |
| Reader                    | D05-HR-Readers    | List, View                        | Read only                |

## 9. Related Lists

| List                                 | Relationship      | Purpose                                      |
| ------------------------------------ | ----------------- | -------------------------------------------- |
| `MainDB_HR`                          | Parent (shared)   | All HR forms via FormType discriminator      |
| `HR_SR_InterviewLog`                 | Child             | Normalised interview batch tracking rows     |
| `MainDB_HR` (FormType = JD)          | Linked lookup     | Job description attached to vacancy          |
| `MainDB_HR` (FormType = INTERVIEWDB) | Linked downstream | Interview batch created after SR is approved |
| `HR_SR_List`                         | Staging           | Historical Domino records                    |

## 10. Migration Notes

- **Interview log normalisation (I_1-10, B_1-10, G_1-10):** Domino stored up to 10 recruitment
  cycles as flat arrays per SR record. M365 normalises these into individual rows in
  `HR_SR_InterviewLog`. Migration script creates one child row per non-blank `I_n` date.
- **Internal advertisement lockout policy:** `SR_InternalLockout` PA flow computes +5 working days
  from `InternalAdDate` (excluding weekends). The ExternalAdDate field is forced read-only in canvas
  until the lockout PA posts a permission grant signal.
- **Budget guardrail (New Headcount):** `VacancyReason = New Headcount` triggers the `Editor5` (CFO)
  approval node. This is the DQ-relevant path — new personnel in GxP-adjacent roles must have CFO
  financial sign-off before HR can commit to the headcount.
- **Dynamic approver chain:** `Editor1–Editor5` are populated by PA at submission time based on the
  requester's `ReqDept` and `OrgUnit`. Canvas does not hardcode approver names.
- **SLA nudge:** `NextRemDate` is computed at submission as `SubmittedDate + 5 working days`. PA
  daily scan alerts the pending stage actor if the SR has been stalled.
- **DQ designation — Indirect GxP rationale:** SR authorises personnel assignment into GxP-adjacent
  operational roles (QC, Production, Engineering). Incorrect or unapproved headcount changes could
  affect product quality system oversight. Therefore DQ documentation is required per ISO 9001:2015
  clause 7.1.2 (Competence) and internal audit requirements.
- **INO generation:** NEVER in canvas. `SR_OnSubmit` generates `HR-SR-YYMM-NNNN` and patches SP
  item.
- **DQ next step:** After blueprint marker gate PASS, route to DQ Engineer to produce
  `GxP_DQ_SR_[DATE].md` before Craftsman handoff.
