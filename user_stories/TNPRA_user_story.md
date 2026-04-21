# Product Requirements Document & User Story
# TNPRA — Typhoid & NPRA Medical Records Database

> **Form Code:** `TNPRA`
> **Department:** HR — Human Resources
> **Module:** HR Administration — Occupational Health & Compliance
> **Site(s):** PRAI, JOHOR
> **SharePoint Target List:** `MainDB_HR` (discriminated by `FormCode = "TNPRA"`)
> **Blueprint Version:** 1.0 — 2026-04-19
> **PRD Status:** READY FOR BUILD

---

## Part 1 — Product Requirements Document (PRD)

### 1.1 Executive Summary

TNPRA is the digital migration of the paper-based Typhoid & NPRA Medical Records register
previously managed in Lotus Domino at the PRAI and JOHOR manufacturing sites of IOI
Oleochemical and IOI Acidchem. The system tracks three distinct categories of occupational
health compliance records for each employee: (1) typhoid vaccination history, (2) food handler
medical examination results, and (3) NPRA (National Pharmaceutical Regulatory Agency)
examination records.

The migrated solution is built on Microsoft Power Apps (Canvas App) backed by SharePoint Online
and automated by Power Automate. The system has no approval workflow — it is a CRUD-only
registry. Its primary operational value lies in expiry-date alerting: HR Managers must be
notified automatically when an employee's typhoid vaccination or food handler examination is
approaching its next-due date, ensuring continuous compliance with occupational health
regulations.

### 1.2 Business Objectives

| #    | Objective                                                                                                                                                                          |
|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BO-1 | Eliminate paper-based tracking of typhoid vaccination and food handler examination records at PRAI and JOHOR sites.                                                                |
| BO-2 | Enforce a one-record-per-employee model with up to 10 historical entries per medical record type (typhoid, food handler, NPRA).                                                   |
| BO-3 | Automate proactive expiry alerts — notify HR Managers 30 days before any employee's next vaccination or exam due date, removing reliance on manual diary checks.                  |
| BO-4 | Enforce role-based data access: HR Managers see all employee records; employees see only their own record.                                                                         |
| BO-5 | Support two operating companies (IOI Oleochemical, IOI Acidchem) and two sites (PRAI, JOHOR) within a single unified database.                                                   |
| BO-6 | Maintain an EnvironmentTag (DEV / TEST / PROD) on every record to allow safe parallel operation of non-production environments without data contamination.                         |

### 1.3 Scope

**In Scope:**

- Creation and maintenance of employee medical compliance records (parent record + three child
  record types) via a Canvas App.
- Role-differentiated views: HR Manager sees all records; HR Staff sees their own record only.
- Category-driven panel visibility: the three medical sub-sections (Typhoid, Food Handler, NPRA)
  are shown or hidden based on the employee's `Category` value (Food Handler / Non-Food Handler /
  NPRA-Only).
- Automated daily scheduled Power Automate flow (`HR_TNPRA_ExpiryAlert`) that queries both
  `HR_TNPRA_TyphoidRecords` and `HR_TNPRA_FoodHandlerExam` for records where
  `NextDueDate <= Today + 30 days` and emails the D05-HR-Manager group.
- SharePoint Online lists: one parent list (`MainDB_HR`) and three normalised child lists
  (`HR_TNPRA_TyphoidRecords`, `HR_TNPRA_FoodHandlerExam`, `HR_TNPRA_NPRARecords`).

**Out of Scope:**

- Approval or endorsement workflow (there is no approval chain for this form).
- Integration with external HR systems, payroll systems, or SAP.
- Medical diagnosis or clinical data beyond what is recorded on the source PDF form.
- Any fields or logic not documented in the TNPRA blueprint v1.0.

### 1.4 User Personas

**Persona 1 — HR Manager (D05-HR-Manager)**

- Role: HR Administrator at PRAI or JOHOR site.
- Responsibilities: Creates new employee medical records, edits existing records, adds new
  vaccination or examination rows to child tables, monitors compliance status across all
  employees.
- Access level: Full Control — can read, create, and edit all TNPRA records for all employees.
- Primary pain point in the legacy system: Manual tracking of expiry dates across paper forms;
  no automated reminder when a vaccination or exam is about to expire.

**Persona 2 — HR Staff / Employee (D05-HR-Staff)**

- Role: Any employee whose medical compliance record exists in the system.
- Responsibilities: Views their own typhoid, food handler, and NPRA records to confirm
  compliance status or verify details recorded by HR.
- Access level: Read Only — can view only the record linked to their own employee number
  (`EmpNo` = their login identity).
- Primary pain point in the legacy system: No self-service visibility into their own vaccination
  or exam history without requesting a paper copy from HR.

**Persona 3 — System (Power Automate)**

- Role: Automated scheduler responsible for proactive compliance alerting.
- Responsibilities: Runs daily, queries child tables for upcoming expiry dates, sends email
  notifications to the D05-HR-Manager group listing all employees with vaccinations or exams
  due within 30 days.
- Access level: Service account / flow connection with read access to child lists and
  send-email permission.

### 1.5 Constraints and Migration Risks

| Constraint / Risk | Detail | Mitigation |
|-------------------|--------|------------|
| Domino repeating tables (x10 rows) are not native in SharePoint | Both the typhoid and food handler sections in the original PDF store up to 10 time-ordered records per employee. SharePoint does not support in-row repeating tables. | Normalise each repeating section into a dedicated child list. Use a gallery in the Canvas App to render and manage rows. |
| Two independent NextDueDate fields require a single expiry-alert flow | `HR_TNPRA_TyphoidRecords.NextDueDate` and `HR_TNPRA_FoodHandlerExam.NextExamDate` both trigger the same HR Manager notification. | Implement `HR_TNPRA_ExpiryAlert` as a single scheduled flow with two parallel query branches — one per child list — merging results before sending the notification email. |
| Category-based panel visibility | Not all employees require all three medical record types. Showing irrelevant sections causes confusion and data entry errors. | Use Power Fx `If(gblCategory = "Food Handler", true, false)` (and equivalent expressions per category) to control the `Visible` property of each of the three gallery panels. |
| Sensitive medical data — cross-employee access must be blocked | Medical records are legally sensitive. Staff must not be able to view each other's records. | In `TNPRA_List`, the gallery items formula must filter by `EmpNo = gblCurrentEmpNo` when the signed-in user is a member of D05-HR-Staff. D05-HR-Manager bypasses this filter. |
| One parent record per employee — not one per visit | The Domino source used one master record per employee with repeating sections for each visit. This pattern must be preserved. | Parent `MainDB_HR` record: one row per employee. Visit rows live exclusively in child lists. |
| Scheduled Domino agent replaced by Power Automate recurrence | The legacy Domino agent fired expiry alerts automatically. Power Automate does not replicate Domino scheduling natively. | Use a Power Automate recurrence trigger (daily) as a direct functional replacement for the Domino agent. |

### 1.6 SharePoint Architecture

**Parent List: `MainDB_HR`** (shared list, discriminated by `FormCode = "TNPRA"`)

One parent row per employee. Contains demographic and employment attributes. All three child
lists reference this parent via a Lookup column `TNPRARef`.

**Child List: `HR_TNPRA_TyphoidRecords`**
Normalises up to 10 typhoid vaccination records per employee.

**Child List: `HR_TNPRA_FoodHandlerExam`**
Normalises up to 10 food handler examination records per employee.

**Child List: `HR_TNPRA_NPRARecords`**
Stores NPRA examination records (typically one active record per employee, sequenced).

---

## Part 2 — User Stories

### US-01 — Create a New Employee Medical Record

> **As an** HR Manager (member of `D05-HR-Manager`),
> **I want to** create a new TNPRA parent record for an employee by entering their personal
> details, employment details, category, and company,
> **So that** the employee has a master compliance record in the system to which typhoid,
> food handler, and NPRA visit rows can be added.

**Pre-conditions:**
- The HR Manager is signed in with a Microsoft 365 account that belongs to the
  `D05-HR-Manager` SharePoint group.
- No existing TNPRA parent record exists for the employee's `EmpNo` in `MainDB_HR`.

**Main Flow:**
1. HR Manager opens the TNPRA Canvas App and lands on `TNPRA_List`.
2. HR Manager taps `+ New` to navigate to `TNPRA_New`.
3. HR Manager selects `Category` (Food Handler / Non-Food Handler / NPRA-Only). The app
   immediately shows or hides the three child gallery panels based on this selection.
4. HR Manager selects `Company` (IOI Oleochemical or IOI Acidchem).
5. HR Manager enters `EmpName`, `EmpNo`, `IdentityNo` (NRIC/IC), and `Gender`.
6. HR Manager optionally enters `Designation`, `Section`, `Department`, `Superior`, and
   `ContractCompany` (if the employee is a contractor).
7. HR Manager sets `RecordStatus` to Active, Inactive, or Terminated.
8. The app system-computes `Title` as `"TNPRA-" & EmpNo` and sets `FormCode = "TNPRA"`.
9. The app system-sets `EnvironmentTag` from `Config_AppSettings` (DEV / TEST / PROD).
10. HR Manager taps `Save`. The parent record is patched to `MainDB_HR`.
11. The app navigates to `TNPRA_View` for the newly created record.

**Alternate Flow — Missing required field:**
- If HR Manager attempts to save without filling all required fields, the required fields
  are highlighted in red and the `Save` button remains disabled until all required fields
  are populated.

**Post-conditions:**
- One new row exists in `MainDB_HR` with `FormCode = "TNPRA"` and
  `Title = "TNPRA-" & EmpNo`.
- The record is immediately visible in `TNPRA_List` for all D05-HR-Manager members.
- The record is visible in `TNPRA_List` for D05-HR-Staff only if the logged-in employee's
  EmpNo matches the record's EmpNo.

**Acceptance Criteria:**
- [ ] `Title` is auto-computed as `TNPRA-` concatenated with `EmpNo`. HR Manager cannot
      manually edit `Title`.
- [ ] `FormCode` is fixed to `"TNPRA"` and is never editable by any user.
- [ ] `Category` selection drives panel visibility for Typhoid, Food Handler, and NPRA
      sections.
- [ ] All required fields (`Title`, `FormCode`, `Category`, `Company`, `RecordStatus`,
      `EmpName`, `EmpNo`, `IdentityNo`, `Gender`, `Department`, `EnvironmentTag`) are
      enforced; the `Save` button is disabled until all are populated.
- [ ] `EnvironmentTag` is set from `Config_AppSettings` — the HR Manager does not
      manually enter this value.
- [ ] Saving a record with a duplicate `EmpNo` is blocked (one parent record per employee).

---

### US-02 — Add a Typhoid Vaccination Record

> **As an** HR Manager (member of `D05-HR-Manager`),
> **I want to** add a new typhoid vaccination row to an existing employee's TNPRA record
> by entering the date of vaccination, hospital/clinic, optional doctor name, next due date,
> and optional batch number,
> **So that** the employee's full vaccination history is captured and the expiry alert flow
> has an up-to-date `NextDueDate` value to monitor.

**Pre-conditions:**
- A parent TNPRA record already exists for the employee.
- The employee's `Category` is `Food Handler` or `Non-Food Handler` (Typhoid panel is
  visible for both).
- The HR Manager is a member of `D05-HR-Manager`.

**Main Flow:**
1. HR Manager opens the employee's record in `TNPRA_Edit`.
2. In the Typhoid Records gallery panel, HR Manager taps `+ Add Row`.
3. HR Manager enters `DateGiven` (vaccination date), `Hospital` (hospital or clinic name),
   and `NextDueDate` (required — used by the expiry alert flow).
4. HR Manager optionally enters `DoctorName` and `BatchNo`.
5. `TyphoidSeq` is auto-assigned as the next sequential integer (1–10) for this employee.
6. `TNPRARef` lookup is system-set to the parent TNPRA record's SharePoint ID.
7. HR Manager taps `Save Row`. The new row is patched to `HR_TNPRA_TyphoidRecords`.

**Post-conditions:**
- A new row exists in `HR_TNPRA_TyphoidRecords` linked to the parent TNPRA record.
- The row's `NextDueDate` is available for daily evaluation by `HR_TNPRA_ExpiryAlert`.
- The Typhoid gallery in `TNPRA_View` displays the new row in sequence order.

**Acceptance Criteria:**
- [ ] `DateGiven`, `Hospital`, and `NextDueDate` are required. Saving fails if any are blank.
- [ ] `TyphoidSeq` is auto-assigned sequentially; the HR Manager cannot manually set the
      sequence number.
- [ ] `TNPRARef` is always populated with the parent record's lookup ID — not a free-text
      entry.
- [ ] Up to 10 vaccination rows may exist per employee. The `+ Add Row` button is disabled
      when 10 rows already exist.
- [ ] The new row appears immediately in the Typhoid gallery on `TNPRA_View` after saving.

---

### US-03 — Add a Food Handler Examination Record

> **As an** HR Manager (member of `D05-HR-Manager`),
> **I want to** add a food handler examination record to an employee's TNPRA record by
> recording the exam date, hospital/clinic, result (Pass/Fail), next exam date, and optional
> doctor name,
> **So that** the employee's food handler certification history is traceable and the expiry
> alert flow can monitor the `NextExamDate` for proactive renewal reminders.

**Pre-conditions:**
- A parent TNPRA record exists for the employee.
- The employee's `Category` is `Food Handler`.
- The HR Manager is a member of `D05-HR-Manager`.

**Main Flow:**
1. HR Manager opens the employee's record in `TNPRA_Edit`.
2. The Food Handler Exam gallery panel is visible because `Category = Food Handler`.
3. HR Manager taps `+ Add Row` in the Food Handler Exam panel.
4. HR Manager enters `ExamDate`, `Hospital`, `ExamResult` (Pass or Fail), and
   `NextExamDate`.
5. HR Manager optionally enters `DoctorName`.
6. `ExamSeq` is auto-assigned sequentially. `TNPRARef` is system-set to the parent record
   ID.
7. HR Manager taps `Save Row`. The new row is patched to `HR_TNPRA_FoodHandlerExam`.

**Post-conditions:**
- A new row exists in `HR_TNPRA_FoodHandlerExam` linked to the parent TNPRA record.
- The row's `NextExamDate` is available for daily evaluation by `HR_TNPRA_ExpiryAlert`.

**Acceptance Criteria:**
- [ ] The Food Handler Exam panel is visible only when `Category = Food Handler`. For
      `Non-Food Handler` or `NPRA-Only`, the panel is hidden and no rows can be added.
- [ ] `ExamDate`, `Hospital`, `ExamResult`, and `NextExamDate` are required fields.
- [ ] `ExamResult` is a two-option Choice column: `Pass` or `Fail`. Free-text entry is not
      permitted.
- [ ] Up to 10 examination rows may exist per employee. The `+ Add Row` button is disabled
      at 10 rows.

---

### US-04 — Add an NPRA Examination Record

> **As an** HR Manager (member of `D05-HR-Manager`),
> **I want to** add an NPRA examination record for an employee by entering the exam date,
> hospital/clinic, result (Pass/Fail), and optional NPRA reference number and doctor name,
> **So that** the employee's NPRA regulatory compliance examination is documented and
> traceable.

**Pre-conditions:**
- A parent TNPRA record exists for the employee.
- The HR Manager is a member of `D05-HR-Manager`.

**Main Flow:**
1. HR Manager opens the employee's record in `TNPRA_Edit`.
2. The NPRA Records gallery panel is visible (shown for `NPRA-Only` and `Food Handler`
   categories; hidden for `Non-Food Handler`).
3. HR Manager taps `+ Add Row` in the NPRA panel.
4. HR Manager enters `DateExam`, `Hospital`, and `ExamResult` (Pass or Fail).
5. HR Manager optionally enters `DoctorName` and `NPRARefNo` (the regulatory reference
   number issued by NPRA).
6. `NPRASeq` is auto-assigned. `TNPRARef` is system-set to the parent record ID.
7. HR Manager taps `Save Row`. The new row is patched to `HR_TNPRA_NPRARecords`.

**Acceptance Criteria:**
- [ ] `DateExam`, `Hospital`, and `ExamResult` are required fields.
- [ ] `ExamResult` is a two-option Choice column: `Pass` or `Fail`.
- [ ] `NPRARefNo`, though optional, must accept alphanumeric input within the single-line-
      text column limit.
- [ ] The NPRA panel is hidden when `Category = Non-Food Handler`. It is visible for
      `Food Handler` and `NPRA-Only`.

---

### US-05 — View Own Medical Record (Employee Self-Service)

> **As an** employee (member of `D05-HR-Staff`),
> **I want to** view my own TNPRA medical compliance record including all vaccination and
> examination entries relevant to my category,
> **So that** I can verify the accuracy of my vaccination dates, exam results, and next due
> dates without having to request a paper copy from HR.

**Pre-conditions:**
- The signed-in user's Microsoft 365 account belongs to `D05-HR-Staff`.
- A TNPRA parent record exists for the user's employee number.

**Main Flow:**
1. Employee opens the TNPRA Canvas App and lands on `TNPRA_List`.
2. The gallery is filtered to show only the record where `EmpNo` matches the signed-in
   employee's employee number (`gblCurrentEmpNo`). The employee cannot see any other
   employee's record.
3. The employee taps their record to navigate to `TNPRA_View`.
4. `TNPRA_View` displays the parent demographic fields in read-only mode.
5. Depending on `Category`, the applicable child gallery panels (Typhoid, Food Handler,
   NPRA) are displayed in read-only mode showing all historical rows in sequence order.
6. No `Edit`, `+ New`, or `+ Add Row` buttons are visible to D05-HR-Staff members.

**Post-conditions:**
- The employee has read-only visibility into their own record. No data is modified.

**Acceptance Criteria:**
- [ ] The gallery in `TNPRA_List` for a D05-HR-Staff member returns at most one record —
      the employee's own record. If no TNPRA record exists for the signed-in employee,
      the gallery shows an empty state with an appropriate message.
- [ ] `TNPRA_View` displays all fields from the parent record and all rows from the
      applicable child lists.
- [ ] No create, edit, or delete controls are visible or accessible to D05-HR-Staff members
      anywhere in the app.
- [ ] Cross-employee access is prevented at the data source level (gallery Items formula),
      not only through UI hiding.

---

### US-06 — Search and Filter All Records (HR Manager)

> **As an** HR Manager (member of `D05-HR-Manager`),
> **I want to** search and filter the full list of TNPRA records by employee name,
> department, category, and record status,
> **So that** I can quickly locate a specific employee's compliance record across two
> companies and two sites without scrolling through the entire registry.

**Pre-conditions:**
- The signed-in user is a member of `D05-HR-Manager`.

**Main Flow:**
1. HR Manager opens `TNPRA_List`. The gallery loads all TNPRA records from `MainDB_HR`
   where `FormCode = "TNPRA"`.
2. HR Manager types in the search box. The gallery filters rows where `EmpName` or `EmpNo`
   starts with the entered text.
3. HR Manager uses the `Category` filter chip to narrow results to `Food Handler`,
   `Non-Food Handler`, or `NPRA-Only`.
4. HR Manager uses the `Department` filter to narrow results by department text.
5. HR Manager uses the `RecordStatus` filter to show only Active, Inactive, or Terminated
   employees.
6. The HR Manager taps any row to navigate to `TNPRA_View` for that employee, or taps the
   `Edit` icon to go directly to `TNPRA_Edit`.

**Acceptance Criteria:**
- [ ] The gallery loads all `MainDB_HR` records discriminated by `FormCode = "TNPRA"`.
- [ ] Search filters on `EmpName` and `EmpNo` using a starts-with match. An empty search
      text shows all records.
- [ ] Category, Department, and RecordStatus filter controls are functional and combinable.
- [ ] Each gallery row displays at minimum: `EmpName`, `EmpNo`, `Category`, `Department`,
      and `RecordStatus`.

---

### US-07 — Receive Automated Expiry Alert (HR Manager)

> **As an** HR Manager (member of `D05-HR-Manager`),
> **I want to** receive a daily email notification listing all employees whose typhoid
> vaccination `NextDueDate` or food handler examination `NextExamDate` is within 30 days
> of today's date,
> **So that** I can arrange for employees to renew their vaccinations or examinations before
> they lapse, maintaining uninterrupted occupational health compliance.

**Pre-conditions:**
- The `HR_TNPRA_ExpiryAlert` Power Automate flow is active and configured with the
  production schedule.
- At least one row in `HR_TNPRA_TyphoidRecords` or `HR_TNPRA_FoodHandlerExam` has a
  `NextDueDate` / `NextExamDate` value <= Today + 30.

**Main Flow (automated — no user action required to trigger):**
1. The `HR_TNPRA_ExpiryAlert` flow fires on its daily recurrence schedule.
2. Branch A: The flow queries `HR_TNPRA_TyphoidRecords` and retrieves all rows where
   `NextDueDate` is not blank and `NextDueDate <= Today + 30 days`. For each matching row,
   it resolves the parent employee's `EmpName`, `EmpNo`, and `Department` via `TNPRARef`.
3. Branch B: The flow queries `HR_TNPRA_FoodHandlerExam` and retrieves all rows where
   `NextExamDate` is not blank and `NextExamDate <= Today + 30 days`. For each matching
   row, it resolves the parent employee's `EmpName`, `EmpNo`, and `Department`.
4. The two result sets are merged into a single notification payload.
5. If the merged list is non-empty, the flow sends one email to the `D05-HR-Manager` group
   listing each employee's name, employee number, record type (Typhoid Vaccination or Food
   Handler Exam), and the due date.
6. If no records are approaching expiry, the flow completes without sending an email.

**Post-conditions:**
- D05-HR-Manager members have received an email with all upcoming expirations.
- No SharePoint data is modified by this flow.

**Acceptance Criteria:**
- [ ] The flow fires once per calendar day using a Power Automate Recurrence trigger.
      The schedule is not hard-coded to a specific environment; time zone is sourced from
      `Config_AppSettings`.
- [ ] The query threshold is exactly 30 days: `NextDueDate <= addDays(utcNow(), 30)`.
      Records with `NextDueDate` beyond 30 days from today are excluded.
- [ ] Both `HR_TNPRA_TyphoidRecords.NextDueDate` and
      `HR_TNPRA_FoodHandlerExam.NextExamDate` are evaluated in the same flow run —
      not in two separate flows.
- [ ] The notification email body includes, for each expiring record: employee full name,
      employee number, record type (Typhoid / Food Handler Exam), and exact due date.
- [ ] The email recipient list is resolved from `Config_AppSettings` — the email address
      is not hard-coded in the flow.
- [ ] If there are zero expiring records, no email is sent.
- [ ] The flow includes error-handling scope: if the SharePoint query fails, a failure
      notification is sent to the admin group.

---

## Part 3 — SharePoint List Requirements

### 3.1 Parent List: `MainDB_HR` (TNPRA records)

**Form Discriminator:** `FormCode = "TNPRA"`

| #   | SP Internal Name | Display Label         | Column Type      | Required | Classification  | Source Mapping / Notes                                            |
|-----|------------------|-----------------------|------------------|----------|-----------------|-------------------------------------------------------------------|
| 1   | Title            | Title                 | Single line text | Yes      | SYSTEM-COMPUTED | Auto-set to `"TNPRA-" & EmpNo`. Not user-editable.               |
| 2   | FormCode         | Form Code             | Single line text | Yes      | SYSTEM-COMPUTED | Fixed constant `"TNPRA"`. Not user-editable.                     |
| 3   | Category         | Category              | Choice           | Yes      | USER-ENTERED    | Options: Food Handler, Non-Food Handler, NPRA-Only               |
| 4   | Company          | Company               | Choice           | Yes      | USER-ENTERED    | Options: IOI Oleochemical, IOI Acidchem                          |
| 5   | RecordStatus     | Record Status         | Choice           | Yes      | USER-ENTERED    | Options: Active, Inactive, Terminated                            |
| 6   | ContractCompany  | Contract Company      | Single line text | No       | USER-ENTERED    | Populated only if employee is a contractor.                      |
| 7   | EmpName          | Employee Name         | Single line text | Yes      | USER-ENTERED    | Full employee name.                                              |
| 8   | EmpNo            | Employee No           | Single line text | Yes      | USER-ENTERED    | Unique employee number. Used as the unique key per employee.     |
| 9   | IdentityNo       | Identity No (NRIC/IC) | Single line text | Yes      | USER-ENTERED    | National ID or NRIC number.                                      |
| 10  | Gender           | Gender                | Choice           | Yes      | USER-ENTERED    | Options: Male, Female.                                           |
| 11  | Designation      | Designation           | Single line text | No       | USER-ENTERED    | Job title or designation.                                        |
| 12  | Section          | Section               | Single line text | No       | USER-ENTERED    | Organisational section.                                          |
| 13  | Department       | Department            | Single line text | Yes      | USER-ENTERED    | Department name.                                                 |
| 14  | Superior         | Immediate Superior    | Single line text | No       | USER-ENTERED    | Name of reporting manager.                                       |
| 15  | EnvironmentTag   | Environment           | Choice           | Yes      | SYSTEM-COMPUTED | Options: DEV, TEST, PROD. Set from `Config_AppSettings`.         |

### 3.2 Child List: `HR_TNPRA_TyphoidRecords`

Normalises typhoid vaccination history. Maximum 10 rows per parent TNPRA record.

| #  | SP Internal Name | Display Label     | Column Type        | Required | Notes                                                            |
|----|------------------|-------------------|--------------------|----------|------------------------------------------------------------------|
| 1  | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Lookup to parent TNPRA record. System-set by app.               |
| 2  | TyphoidSeq       | Record No         | Number             | Yes      | Sequential integer 1–10. System-assigned by app.                |
| 3  | DateGiven        | Date Given        | Date and Time      | Yes      | Date the typhoid vaccination was administered.                  |
| 4  | Hospital         | Hospital / Clinic | Single line text   | Yes      | Name of hospital or clinic where vaccination was given.         |
| 5  | DoctorName       | Doctor Name       | Single line text   | No       | Name of administering doctor.                                   |
| 6  | NextDueDate      | Next Due Date     | Date and Time      | Yes      | Date the next vaccination is due. Used by expiry alert flow.    |
| 7  | BatchNo          | Batch Number      | Single line text   | No       | Vaccine batch identifier for traceability.                      |

### 3.3 Child List: `HR_TNPRA_FoodHandlerExam`

Normalises food handler examination history. Maximum 10 rows per parent TNPRA record.

| #  | SP Internal Name | Display Label     | Column Type        | Required | Notes                                                            |
|----|------------------|-------------------|--------------------|----------|------------------------------------------------------------------|
| 1  | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Lookup to parent TNPRA record. System-set by app.               |
| 2  | ExamSeq          | Record No         | Number             | Yes      | Sequential integer 1–10. System-assigned by app.                |
| 3  | ExamDate         | Exam Date         | Date and Time      | Yes      | Date the food handler examination was conducted.                |
| 4  | Hospital         | Hospital / Clinic | Single line text   | Yes      | Name of hospital or clinic.                                     |
| 5  | DoctorName       | Doctor Name       | Single line text   | No       | Name of examining doctor.                                       |
| 6  | ExamResult       | Result            | Choice             | Yes      | Options: Pass, Fail. No other values permitted.                 |
| 7  | NextExamDate     | Next Exam Date    | Date and Time      | Yes      | Date the next food handler exam is due. Used by alert flow.     |

### 3.4 Child List: `HR_TNPRA_NPRARecords`

Stores NPRA examination records. Sequenced for history; typically one active record per employee.

| #  | SP Internal Name | Display Label     | Column Type        | Required | Notes                                                            |
|----|------------------|-------------------|--------------------|----------|------------------------------------------------------------------|
| 1  | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Lookup to parent TNPRA record. System-set by app.               |
| 2  | NPRASeq          | Record No         | Number             | Yes      | Sequence number. System-assigned by app.                        |
| 3  | DateExam         | Exam Date         | Date and Time      | Yes      | Date the NPRA examination was conducted.                        |
| 4  | Hospital         | Hospital / Clinic | Single line text   | Yes      | Name of hospital or clinic.                                     |
| 5  | DoctorName       | Doctor Name       | Single line text   | No       | Name of examining doctor.                                       |
| 6  | ExamResult       | Result            | Choice             | Yes      | Options: Pass, Fail.                                            |
| 7  | NPRARefNo        | NPRA Reference No | Single line text   | No       | Regulatory reference number issued by NPRA.                     |

---

## Part 4 — Screen Requirements

### 4.1 Screen Inventory

| Screen Name | Type      | Purpose                                                                          | Visible To                                                          |
|-------------|-----------|----------------------------------------------------------------------------------|---------------------------------------------------------------------|
| TNPRA_List  | Gallery   | Lists all TNPRA records. Supports search and filter by employee, department, category, and status. | D05-HR-Manager: all records. D05-HR-Staff: own record only.        |
| TNPRA_New   | Form      | Creates a new parent TNPRA record with galleries for adding initial child rows for Typhoid, Food Handler, and NPRA sections based on Category. | D05-HR-Manager only.                                                |
| TNPRA_View  | Read-only | Displays all parent fields and all child gallery rows for Typhoid, Food Handler, and NPRA sections in read-only mode. | D05-HR-Manager (all records). D05-HR-Staff (own record only).      |
| TNPRA_Edit  | Form      | Edits existing parent record fields. Allows adding new rows to child galleries.  | D05-HR-Manager only.                                                |

### 4.2 Navigation Map

```
TNPRA_List
  +-- [+ New]  --> TNPRA_New       (D05-HR-Manager only)
  +-- [View]   --> TNPRA_View      (both roles)
  +-- [Edit]   --> TNPRA_Edit      (D05-HR-Manager only)

TNPRA_View
  +-- [Edit]   --> TNPRA_Edit      (D05-HR-Manager only)

TNPRA_New / TNPRA_Edit
  +-- [Save]   --> TNPRA_View
  +-- [Cancel] --> TNPRA_List
```

### 4.3 Screen Interaction Details

**TNPRA_List**
- Gallery data source: `Filter(MainDB_HR, FormCode = "TNPRA")` for D05-HR-Manager.
- For D05-HR-Staff: `Filter(MainDB_HR, FormCode = "TNPRA" && EmpNo = gblCurrentEmpNo)`.
- Each gallery row displays: `EmpName`, `EmpNo`, `Category`, `Department`, `RecordStatus`.
- A search text box filters by `EmpName` and `EmpNo` (StartsWith match).
- Filter controls: `Category` (choice chip set), `Department` (text input), `RecordStatus`
  (choice chip set). Multiple active filters combine to narrow the result set.
- The `+ New` button is visible only to D05-HR-Manager members.
- Tapping a row navigates to `TNPRA_View` passing the selected record as `varRecord`.

**TNPRA_New**
- Data entry form bound to `MainDB_HR`.
- `Category` is selected first. Changing `Category` immediately toggles the `Visible`
  property of the three child-gallery panels using Power Fx conditional expressions.
- Required fields display a red asterisk label. The `Save` button is disabled until all
  required fields in the parent form are populated.
- Three collapsible gallery panels below the parent form header: Typhoid Records, Food
  Handler Exam, NPRA Records. Each panel is visible or hidden based on `gblCategory`.
- Each gallery panel has a `+ Add Row` button that opens an inline form for entering a
  new child row. On saving a child row, it is immediately visible in the gallery.
- `Cancel` button discards all unsaved changes and navigates to `TNPRA_List`.

**TNPRA_View**
- All parent fields are displayed in a read-only display form layout.
- Three gallery panels (Typhoid, Food Handler, NPRA) display all rows from the respective
  child lists linked to this parent record via `TNPRARef`. Only the panels relevant to
  the employee's `Category` are shown.
- All three child galleries are loaded concurrently using `Concurrent()` on screen load.
- The `Edit` button is visible only to D05-HR-Manager members.

**TNPRA_Edit**
- Same layout as `TNPRA_New` but pre-populated with existing parent field values and
  existing child gallery rows.
- HR Manager can modify all parent fields except `Title`, `FormCode`, and `EnvironmentTag`.
- HR Manager can add new rows to any of the three child gallery panels. The `+ Add Row`
  button is disabled when the child list already has 10 rows for this employee.
- `Save` button patches all modified parent fields and all new child rows.

---

## Part 5 — Power Fx Formula Requirements

### 5.1 Title Auto-Computation (TNPRA_New — OnSave)

```powerfx
// System-sets Title as TNPRA prefix + EmpNo. HR Manager does not type the Title.
Patch(
    MainDB_HR,
    Defaults(MainDB_HR),
    {
        Title:           "TNPRA-" & txtEmpNo.Text,
        FormCode:        "TNPRA",
        Category:        drpCategory.Selected.Value,
        Company:         drpCompany.Selected.Value,
        RecordStatus:    drpRecordStatus.Selected.Value,
        EmpName:         txtEmpName.Text,
        EmpNo:           txtEmpNo.Text,
        IdentityNo:      txtIdentityNo.Text,
        Gender:          drpGender.Selected.Value,
        Designation:     txtDesignation.Text,
        Section:         txtSection.Text,
        Department:      txtDepartment.Text,
        Superior:        txtSuperior.Text,
        ContractCompany: txtContractCompany.Text,
        EnvironmentTag:  gblEnvironmentTag
    }
);
Navigate(
    TNPRA_View,
    ScreenTransition.None,
    {varRecord: Last(Filter(MainDB_HR, EmpNo = txtEmpNo.Text))}
)
```

### 5.2 Category-Driven Panel Visibility

```powerfx
// Typhoid Records panel Visible property
drpCategory.Selected.Value = "Food Handler" ||
drpCategory.Selected.Value = "Non-Food Handler"

// Food Handler Exam panel Visible property
drpCategory.Selected.Value = "Food Handler"

// NPRA Records panel Visible property
drpCategory.Selected.Value = "NPRA-Only" ||
drpCategory.Selected.Value = "Food Handler"
```

### 5.3 Gallery Filter — TNPRA_List (HR Manager view)

```powerfx
Filter(
    MainDB_HR,
    FormCode = "TNPRA" &&
    (IsBlank(txtSearch.Text) ||
        StartsWith(EmpName, txtSearch.Text) ||
        StartsWith(EmpNo, txtSearch.Text)) &&
    (IsBlank(drpCategoryFilter.Selected.Value) ||
        Category = drpCategoryFilter.Selected.Value) &&
    (IsBlank(drpStatusFilter.Selected.Value) ||
        RecordStatus = drpStatusFilter.Selected.Value) &&
    (IsBlank(txtDeptFilter.Text) ||
        StartsWith(Department, txtDeptFilter.Text))
)
```

### 5.4 Gallery Filter — TNPRA_List (HR Staff view — own record only)

```powerfx
Filter(
    MainDB_HR,
    FormCode = "TNPRA" &&
    EmpNo = gblCurrentEmpNo
)
```

### 5.5 Load All Three Child Galleries Concurrently (TNPRA_View — OnVisible)

```powerfx
Concurrent(
    ClearCollect(
        colTyphoidRecords,
        Filter(HR_TNPRA_TyphoidRecords, TNPRARef.Id = varRecord.ID)
    ),
    ClearCollect(
        colFoodHandlerExam,
        Filter(HR_TNPRA_FoodHandlerExam, TNPRARef.Id = varRecord.ID)
    ),
    ClearCollect(
        colNPRARecords,
        Filter(HR_TNPRA_NPRARecords, TNPRARef.Id = varRecord.ID)
    )
)
```

### 5.6 Field Lock — All Fields Read-Only for D05-HR-Staff

```powerfx
// DisplayMode property for all editable controls
If(
    gblUserRole = "D05-HR-Staff",
    DisplayMode.View,
    DisplayMode.Edit
)
```

---

## Part 6 — Power Automate Requirements

### 6.1 Flow: `HR_TNPRA_ExpiryAlert`

| Attribute    | Value                                                                                                                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Flow Name    | HR_TNPRA_ExpiryAlert                                                                                                                                                                                   |
| Trigger      | Recurrence — daily schedule. Time and time zone sourced from `Config_AppSettings`. Not hard-coded.                                                                                                     |
| Branch A     | Get items from `HR_TNPRA_TyphoidRecords` where `NextDueDate` is not null and `NextDueDate <= addDays(utcNow(), 30)`. Expand `TNPRARef` to retrieve `EmpName`, `EmpNo`, `Department`.                   |
| Branch B     | Get items from `HR_TNPRA_FoodHandlerExam` where `NextExamDate` is not null and `NextExamDate <= addDays(utcNow(), 30)`. Expand `TNPRARef` to retrieve `EmpName`, `EmpNo`, `Department`.                |
| Merge        | Combine Branch A and Branch B results into a single array with a `RecordType` label: "Typhoid Vaccination" or "Food Handler Exam".                                                                     |
| Condition    | If merged array is empty — flow terminates without sending email.                                                                                                                                      |
| Email Action | Send one email to the email address(es) configured for `D05-HR-Manager` in `Config_AppSettings`. Subject: `[TNPRA] Medical Compliance Expiry Alert — {Today's Date}`. Body: tabular list of Employee Name, Employee No, Record Type, Due Date for each expiring record. |
| Error Scope  | All SharePoint Get items actions and the Send email action are wrapped in a Try/Catch scope (Scope + Run after = has failed). On failure, send an error notification to the admin email configured in `Config_AppSettings`. |

### 6.2 Flow Design Principles

1. **Environment isolation:** All email recipients, admin contacts, and site URLs are read
   from `Config_AppSettings` using `EnvironmentTag`. No DEV/TEST/PROD values are
   hard-coded in the flow.
2. **Idempotency:** The recurrence trigger is the sole trigger. Duplicate runs on the same
   day do not cause duplicate emails because the query threshold is date-based.
3. **Error handling:** All SharePoint query actions and email actions are enclosed in
   error-handling scopes with fail-path notifications.
4. **No status field modifications:** This flow does not update any SharePoint columns.
   It is read-only with respect to SharePoint data.
5. **Notification standard:** Email subject includes `[TNPRA]` prefix, form code, and
   current date. Email body includes: Employee Name, Employee No, Record Type, Due Date,
   and the TNPRA Canvas App deep-link URL.

---

## Part 7 — Role-Based Access Control

| Persona    | SharePoint Group | TNPRA_List                  | TNPRA_New | TNPRA_View                   | TNPRA_Edit |
|------------|------------------|-----------------------------|-----------|------------------------------|------------|
| HR Manager | D05-HR-Manager   | All records — full CRUD     | Yes       | All records — read           | Yes        |
| HR Staff   | D05-HR-Staff     | Own record only — read only | No        | Own record only — read only  | No         |
| System (PA)| Service account  | Read child lists only       | No        | No                           | No         |

**Data isolation rule:** The gallery items formula for D05-HR-Staff must filter at the data
source level — `Filter(MainDB_HR, FormCode = "TNPRA" && EmpNo = gblCurrentEmpNo)`. UI-only
hiding is insufficient and must not be used as the sole protection.

---

## Part 8 — Acceptance Criteria

All of the following criteria must be met before `TNPRA` is promoted from TEST to PROD.

**SharePoint Schema**
- [ ] `MainDB_HR` contains all 15 TNPRA parent columns with correct column types, required
      flags, and Choice option sets as defined in section 3.1.
- [ ] Child list `HR_TNPRA_TyphoidRecords` is created with all 7 columns. `TNPRARef` is a
      Lookup to `MainDB_HR`.
- [ ] Child list `HR_TNPRA_FoodHandlerExam` is created with all 7 columns. `TNPRARef` is a
      Lookup to `MainDB_HR`.
- [ ] Child list `HR_TNPRA_NPRARecords` is created with all 7 columns. `TNPRARef` is a
      Lookup to `MainDB_HR`.
- [ ] `FormCode` column has a column-level validation rule enforcing the fixed value
      `"TNPRA"`.
- [ ] `EnvironmentTag` column is populated by the app from `Config_AppSettings` and is not
      user-editable in the Canvas App or directly in SharePoint by non-admin users.

**Canvas App — Screens and Navigation**
- [ ] `TNPRA_List` gallery loads all TNPRA records for D05-HR-Manager.
- [ ] `TNPRA_List` gallery loads only the signed-in employee's own record for D05-HR-Staff.
- [ ] Search by `EmpName` and `EmpNo`, and filter by `Category`, `Department`, and
      `RecordStatus` all function correctly on `TNPRA_List`.
- [ ] `+ New` button on `TNPRA_List` is visible only to D05-HR-Manager members.
- [ ] `TNPRA_New` correctly shows/hides the Typhoid, Food Handler, and NPRA gallery panels
      based on the selected `Category`.
- [ ] All required parent fields are validated before the `Save` button is enabled.
- [ ] `Title` is auto-generated as `"TNPRA-" & EmpNo` and is not user-editable.
- [ ] `TNPRA_View` loads all three child galleries concurrently using `Concurrent()`.
- [ ] No create, edit, or delete controls are visible or accessible to D05-HR-Staff members.
- [ ] A D05-HR-Staff member cannot access another employee's record by any means (URL
      manipulation, direct gallery filter removal, etc.).

**Canvas App — Child Record Management**
- [ ] Adding a typhoid vaccination row to `HR_TNPRA_TyphoidRecords` succeeds and the row
      appears immediately in the Typhoid gallery on `TNPRA_View`.
- [ ] Adding a food handler exam row to `HR_TNPRA_FoodHandlerExam` is possible only when
      `Category = Food Handler`. The panel is hidden and the action is not available for
      other categories.
- [ ] Adding an NPRA record to `HR_TNPRA_NPRARecords` succeeds for `Food Handler` and
      `NPRA-Only` categories.
- [ ] The `+ Add Row` button in each child gallery is disabled when 10 rows already exist
      for that employee in that child list.

**Power Automate**
- [ ] `HR_TNPRA_ExpiryAlert` fires daily and queries both
      `HR_TNPRA_TyphoidRecords.NextDueDate` and
      `HR_TNPRA_FoodHandlerExam.NextExamDate` within a single flow run.
- [ ] Email is sent to D05-HR-Manager recipients when records with
      `NextDueDate` / `NextExamDate` <= Today + 30 days exist.
- [ ] No email is sent when zero records meet the 30-day threshold.
- [ ] Email body lists each expiring record with: Employee Name, Employee No, Record Type,
      and Due Date.
- [ ] All recipient email addresses are sourced from `Config_AppSettings`. No addresses are
      hard-coded in the flow definition.
- [ ] Flow error-handling scope is active: a failure notification is sent to the admin group
      if the flow encounters a runtime error.

**Environment and Deployment**
- [ ] `EnvironmentTag` on every TNPRA record correctly reflects the deployment environment
      (DEV / TEST / PROD).
- [ ] DEV and TEST records do not appear in the PROD environment gallery.
- [ ] The Canvas App has been tested end-to-end in the TEST environment by both an
      HR Manager persona and an HR Staff persona before promotion to PROD.
