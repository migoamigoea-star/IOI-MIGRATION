<!-- Architect: INTERN form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

---

form_code: INTERN dept: HR official_name: "Industrial Trainees Registry (IOI Scholars)" owner: "HR
Department, D05" complexity: Simple DQ_REQUIRED: NO gxp_class: "—" status: BLUEPRINT_DRAFT date:
2026-04-14 ino_pattern: "HR-TRA-YYMM-NNNN" sp_list_primary: "MainDB_HR" sp_form_type_discriminator:
"INTERN" sp_list_staging: "HR_INTERN_List"

---

# INTERN — Industrial Trainees Registry (IOI Scholars)

## 1. Form Identity

| Attribute       | Value                                              |
| --------------- | -------------------------------------------------- |
| Form Code       | INTERN                                             |
| Full Name       | Industrial Trainees Registry (IOI Scholars)        |
| Department      | Human Resources (D05)                              |
| Module          | M2 — Recruitment & Hiring                          |
| Entity Scope    | PCO / PCEO / ECM                                   |
| Complexity      | Simple                                             |
| DQ Required     | NO                                                 |
| INO Pattern     | `HR-TRA-YYMM-NNNN` (Power Automate — NEVER canvas) |
| SP Primary List | `MainDB_HR` (FormType = "INTERN")                  |
| SP Staging List | `HR_INTERN_List` (historical import)               |

## 2. Business Purpose

The INTERN form manages the end-to-end lifecycle of IOI Scholarship holders and industrial training
placements. It tracks academic background (name, university, course), training duration (start/end
dates), scholarship bonding commitment, placement context (HOD assigned, department), and employment
conversion status.

Three key lifecycle stages:

- **Enrolment:** HR Coordinator logs trainee profile at intake.
- **Monitoring:** HOD oversees placement and mentorship during training period.
- **Conversion:** If the trainee joins as full-time staff after graduation, this form triggers a
  `PAF` (Personnel Action Form) for formal onboarding. If not continuing, it triggers an offboarding
  checklist.

## 3. SharePoint Schema

### 3a. Primary List — `MainDB_HR` (FormType discriminator: "INTERN")

| #   | SP Internal Name    | Display Label               | Column Type    | Required | Classification   | Notes                                             |
| --- | ------------------- | --------------------------- | -------------- | -------- | ---------------- | ------------------------------------------------- |
| 1   | FormType            | Form Type                   | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "INTERN"                                   |
| 2   | INO                 | Reference No.               | Single line    | Yes      | SYSTEM-COMPUTED  | HR-TRA-YYMM-NNNN via PA                           |
| 3   | CurrentStatus       | Current Status              | Choice         | Yes      | WORKFLOW-MANAGED | Enrolled/Monitoring/Converted/Completed/Withdrawn |
| 4   | EnvironmentTag      | Environment                 | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                     |
| 5   | TraineeName         | Scholar Name                | Single line    | Yes      | USER-ENTERED     | Full name of trainee                              |
| 6   | University          | University / College        | Single line    | Yes      | USER-ENTERED     | Academic institution                              |
| 7   | CourseTitle         | Course Title                | Single line    | No       | USER-ENTERED     | Field of study                                    |
| 8   | TrainingStart       | Training Start              | Date           | Yes      | USER-ENTERED     | Placement start date                              |
| 9   | TrainingEnd         | Training End                | Date           | Yes      | USER-ENTERED     | Placement end date                                |
| 10  | Bond                | Bond Period (Years)         | Number         | Yes      | USER-ENTERED     | 1–5 years typical                                 |
| 11  | HOD                 | Supervisor / HOD            | Person         | Yes      | USER-ENTERED     | Assigned department supervisor                    |
| 12  | Department          | Placement Department        | Single line    | No       | USER-ENTERED     | Department hosting the trainee                    |
| 13  | Company             | Company Entity              | Choice         | Yes      | USER-ENTERED     | PCO/PCEO/ECM                                      |
| 14  | EmpStatus           | Employment Status           | Choice         | Yes      | WORKFLOW-MANAGED | Trainee/Staff/CompletedBonded/Resigned/Offboarded |
| 15  | DateJoin            | Actual Join Date            | Date           | No       | USER-ENTERED     | Only set when EmpStatus → Staff                   |
| 16  | ExpDateJoin         | Expected Joining Date       | Date           | No       | USER-ENTERED     | Projected join date for funnel                    |
| 17  | LastDay             | Last Day of Service         | Date           | No       | WORKFLOW-MANAGED | Set when trainee exits without joining            |
| 18  | JobPosting          | Job Posting Notes           | Multiple lines | No       | USER-ENTERED     | Ad-hoc placement notes                            |
| 19  | DocAuthor           | Created By (HR Coordinator) | Person         | Yes      | SYSTEM-COMPUTED  | Auto-filled from login                            |
| 20  | Attachment          | CV / Certificates           | Attachment     | No       | USER-ENTERED     | Supporting docs                                   |
| 21  | BondExpiryDate      | Bond Expiry Date            | Date           | No       | SYSTEM-COMPUTED  | PA-calculated: DateJoin + Bond years              |
| 22  | RetentionReviewDone | Retention Review Done       | Yes/No         | No       | WORKFLOW-MANAGED | Set by PA when review triggered                   |
| 23  | IsLocked            | Is Locked                   | Yes/No         | No       | WORKFLOW-MANAGED | Lock after Completed/Offboarded                   |

### 3b. Staging List — `HR_INTERN_List`

Historical import from Lotus Domino. Mirrors `MainDB_HR` filtered to FormType=INTERN. Records with
missing `TrainingStart` or `Bond` will receive default values (TrainingStart=1900-01-01, Bond=0) to
prevent PA flow failures.

## 4. Field Inventory Summary

| Category          | Count                                                                   |
| ----------------- | ----------------------------------------------------------------------- |
| Identity / System | 4 (FormType, INO, CurrentStatus, EnvironmentTag)                        |
| Trainee Profile   | 5 (TraineeName, University, CourseTitle, Company, DocAuthor)            |
| Training Dates    | 4 (TrainingStart, TrainingEnd, TrainingDuration auto-calc, ExpDateJoin) |
| Bond & Employment | 5 (Bond, EmpStatus, DateJoin, LastDay, BondExpiryDate)                  |
| Placement Context | 4 (HOD, Department, JobPosting, Attachment)                             |
| Workflow Flags    | 2 (RetentionReviewDone, IsLocked)                                       |
| **Total**         | **23**                                                                  |

## 5. Workflow

### 5a. Stage Map

| Stage | Name                  | Trigger                        | Actor                      | Actions                                       | Next Stage | Notification Target   |
| ----- | --------------------- | ------------------------------ | -------------------------- | --------------------------------------------- | ---------- | --------------------- |
| 1     | Enrolled              | New record                     | DocAuthor (HR Coordinator) | Log trainee profile                           | 2          | HOD                   |
| 2     | Monitoring            | Placement confirmed            | HOD                        | Update placement notes and mentorship log     | 3          | DocAuthor             |
| 3     | Converting            | Graduation / programme end     | DocAuthor (HR Manager)     | Set EmpStatus = Staff/Completed/Withdrawn     | End        | Payroll/IT (if Staff) |
| —     | Bond Retention Review | 6 months before BondExpiryDate | PA Trigger                 | Alert HOD and DocAuthor                       | —          | HOD, DocAuthor        |
| —     | Offboarding           | LastDay populated              | PA Trigger                 | Send offboarding checklist to IT + Facilities | —          | IT, Facilities        |

### 5b. Power Automate Flows

| Flow Name                   | Trigger                                   | Key Actions                                                                             |
| --------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------- |
| `INTERN_OnEnrol`            | New item created                          | Generate INO, set CurrentStatus=Enrolled, notify HOD                                    |
| `INTERN_OnConvert`          | EmpStatus → Staff                         | Set DateJoin, compute BondExpiryDate, trigger PAF creation                              |
| `INTERN_OnOffboard`         | LastDay populated                         | Send offboarding checklist to IT (revoke access) and Facilities (collect ID)            |
| `INTERN_BondRetentionAlert` | Scheduled: 6 months before BondExpiryDate | Send "Retention Review Required" alert to HOD and DocAuthor, set RetentionReviewDone=No |
| `INTERN_BondExpiry`         | Scheduled: On BondExpiryDate              | If EmpStatus=Staff, set EmpStatus=CompletedBonded, notify HR Manager                    |

## 6. Screen Inventory

| Screen           | Purpose                                                                    | Key Controls                                             |
| ---------------- | -------------------------------------------------------------------------- | -------------------------------------------------------- |
| `INTERN_List`    | Searchable trainee gallery, filterable by EmpStatus / University / Company | Gallery, status chips, university filter                 |
| `INTERN_New`     | New trainee entry                                                          | Person picker (HOD), date pickers, company/entity choice |
| `INTERN_View`    | Read-only detail with bond status indicator                                | Display form, bond countdown gauge, employment timeline  |
| `INTERN_Edit`    | Edit whilst in Enrolled/Monitoring stage                                   | Edit form                                                |
| `INTERN_Convert` | Employment conversion action                                               | EmpStatus choice, DateJoin picker, "Generate PAF" button |

## 7. Navigation Map

```
INTERN_List
  ├── [New Trainee] → INTERN_New → OnEnrol → INTERN_View
  ├── [Gallery Row] → INTERN_View
  │     ├── [Edit] (Enrolled/Monitoring) → INTERN_Edit → INTERN_View
  │     └── [Convert/Offboard] (HR Manager) → INTERN_Convert
  └── [Back] → Home
```

## 8. Role Matrix

| Role                          | SP Group          | Screen Access                  | Actions                            |
| ----------------------------- | ----------------- | ------------------------------ | ---------------------------------- |
| HR Coordinator (DocAuthor)    | D05-HR-InternTeam | List, New, View, Edit, Convert | Create, Edit, Convert              |
| HOD (Supervisor)              | D[Dept]-Managers  | List, View                     | Read, update notes (Stage 2)       |
| HR Manager                    | D05-HR-Managers   | All                            | Full control — Stage 3, conversion |
| IT / Facilities (offboarding) | D05-HR-Readers    | View only (triggered by PA)    | Read notification                  |
| Reader                        | D05-HR-Readers    | List, View                     | Read only                          |

## 9. Related Lists

| List                         | Relationship    | Purpose                                           |
| ---------------------------- | --------------- | ------------------------------------------------- |
| `MainDB_HR`                  | Parent (shared) | All HR forms via FormType discriminator           |
| `MainDB_HR` (FormType = PAF) | Linked child    | When EmpStatus → Staff, PAF is created and linked |
| `HR_Department_Master`       | Lookup          | Valid company/department codes                    |
| `HR_INTERN_List`             | Staging         | Historical Domino records                         |

## 10. Migration Notes

- **Missing legacy dates:** Records with blank `TrainingStart` or `Bond` receive placeholder
  defaults (TrainingStart=1900-01-01, Bond=0) during staging import. HR is responsible for
  correcting these before going live.
- **Bond expiry calculation:** `BondExpiryDate` is computed by `INTERN_OnConvert` as
  `DateJoin + Bond × 365 days`. Never computed in canvas.
- **PAF integration:** The "Convert to Staff" action triggers `INTERN_OnConvert` which creates a new
  PAF item in `MainDB_HR` (FormType=PAF) with pre-filled employee details from the INTERN record.
  Canvas "Generate PAF" button is a PA HTTP trigger — NOT a direct SP write in canvas.
- **`TRA` abbreviation for INO:** `HR-TRA-YYMM-NNNN` chosen to avoid ambiguity with `INTERN` as a
  keyword in some systems.
- **INO generation:** NEVER in canvas. PA flow generates and patches.
