# Technical Blueprint: TNPRA — Typhoid/NPRA Medical Records Database

## Blueprint Status

| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | VALIDATED   |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PASS        |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

---

## Form Identity

| Field                      | Value                                                   |
| -------------------------- | ------------------------------------------------------- |
| Form Code                  | TNPRA                                                   |
| Official Name              | Typhoid & NPRA Medical Records Database                 |
| Department                 | HR                                                      |
| Module                     | HR Administration — Occupational Health & Compliance    |
| Site(s)                    | PRAI, JOHOR                                             |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/TNPRA.pdf |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline)   |
| Official Name Claim Status | Claimed from source PDF title                           |
| Blueprint Version          | 1.0                                                     |
| Blueprint Date             | 2026-04-19                                              |
| Architect                  | GitHub Copilot (Architect)                              |

---

## Purpose

TNPRA is a medical compliance registry for tracking employee typhoid vaccination records, food
handler examination results, and NPRA (National Pharmaceutical Regulatory Agency) medical
examination records. HR admins create and maintain records for each employee, tracking vaccination
dates, next-due dates, hospital, doctor, and test results. There is no approval workflow — this is a
CRUD registry with scheduled expiry alerts. The migrated solution must normalize the 3 repeating
medical record sections into child tables and preserve expiry-based alerting.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "TNPRA"

### Parent List: MainDB_HR (TNPRA header)

| #   | SP Internal Name | Display Label         | Column Type      | Required | Classification  | Source Mapping / Notes                                 |
| --- | ---------------- | --------------------- | ---------------- | -------- | --------------- | ------------------------------------------------------ |
| 1   | Title            | Title                 | Single line text | Yes      | SYSTEM-COMPUTED | TNPRA prefix + EmpNo                                   |
| 2   | FormCode         | Form Code             | Single line text | Yes      | SYSTEM-COMPUTED | Fixed value TNPRA                                      |
| 3   | Category         | Category              | Choice           | Yes      | USER-ENTERED    | `Category` — Food Handler, Non-Food Handler, NPRA-Only |
| 4   | Company          | Company               | Choice           | Yes      | USER-ENTERED    | `Company` — IOI Oleochemical, IOI Acidchem             |
| 5   | RecordStatus     | Record Status         | Choice           | Yes      | USER-ENTERED    | `Status` — Active, Inactive, Terminated                |
| 6   | ContractCompany  | Contract Company      | Single line text | No       | USER-ENTERED    | `ContractCompany` — if contractor                      |
| 7   | EmpName          | Employee Name         | Single line text | Yes      | USER-ENTERED    | `Name`                                                 |
| 8   | EmpNo            | Employee No           | Single line text | Yes      | USER-ENTERED    | `EmpNo`                                                |
| 9   | IdentityNo       | Identity No (NRIC/IC) | Single line text | Yes      | USER-ENTERED    | `IdentityNo`                                           |
| 10  | Gender           | Gender                | Choice           | Yes      | USER-ENTERED    | `Gender` — Male, Female                                |
| 11  | Designation      | Designation           | Single line text | No       | USER-ENTERED    | `Designation`                                          |
| 12  | Section          | Section               | Single line text | No       | USER-ENTERED    | `Section`                                              |
| 13  | Department       | Department            | Single line text | Yes      | USER-ENTERED    | `Department`                                           |
| 14  | Superior         | Immediate Superior    | Single line text | No       | USER-ENTERED    | `Superior`                                             |
| 15  | EnvironmentTag   | Environment           | Choice           | Yes      | SYSTEM-COMPUTED | DEV, TEST, PROD                                        |

### Child List: HR_TNPRA_TyphoidRecords

Normalizes up to 10 typhoid vaccination records per employee.

| #   | SP Internal Name | Display Label     | Column Type        | Required | Notes                        |
| --- | ---------------- | ----------------- | ------------------ | -------- | ---------------------------- |
| 1   | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Links to parent TNPRA record |
| 2   | TyphoidSeq       | Record No         | Number             | Yes      | Sequence 1–10                |
| 3   | DateGiven        | Date Given        | Date and Time      | Yes      | Vaccination date             |
| 4   | Hospital         | Hospital / Clinic | Single line text   | Yes      | Where vaccination was given  |
| 5   | DoctorName       | Doctor Name       | Single line text   | No       |                              |
| 6   | NextDueDate      | Next Due Date     | Date and Time      | Yes      | For alert scheduling         |
| 7   | BatchNo          | Batch Number      | Single line text   | No       | Vaccine batch identifier     |

### Child List: HR_TNPRA_FoodHandlerExam

Normalizes up to 10 food handler examination records.

| #   | SP Internal Name | Display Label     | Column Type        | Required | Notes                        |
| --- | ---------------- | ----------------- | ------------------ | -------- | ---------------------------- |
| 1   | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Links to parent TNPRA record |
| 2   | ExamSeq          | Record No         | Number             | Yes      | Sequence 1–10                |
| 3   | ExamDate         | Exam Date         | Date and Time      | Yes      | Date of examination          |
| 4   | Hospital         | Hospital / Clinic | Single line text   | Yes      |                              |
| 5   | DoctorName       | Doctor Name       | Single line text   | No       |                              |
| 6   | ExamResult       | Result            | Choice             | Yes      | Pass, Fail                   |
| 7   | NextExamDate     | Next Exam Date    | Date and Time      | Yes      | For alert scheduling         |

### Child List: HR_TNPRA_NPRARecords

NPRA examination records (typically one active record per employee).

| #   | SP Internal Name | Display Label     | Column Type        | Required | Notes                        |
| --- | ---------------- | ----------------- | ------------------ | -------- | ---------------------------- |
| 1   | TNPRARef         | TNPRA Reference   | Lookup (MainDB_HR) | Yes      | Links to parent TNPRA record |
| 2   | NPRASeq          | Record No         | Number             | Yes      | Sequence                     |
| 3   | DateExam         | Exam Date         | Date and Time      | Yes      |                              |
| 4   | Hospital         | Hospital / Clinic | Single line text   | Yes      |                              |
| 5   | DoctorName       | Doctor Name       | Single line text   | No       |                              |
| 6   | ExamResult       | Result            | Choice             | Yes      | Pass, Fail                   |
| 7   | NPRARefNo        | NPRA Reference No | Single line text   | No       | Regulatory reference number  |

---

## Workflow Stage Map

```
[HR Admin] → Create TNPRA record (CRUD — no approval)
[System] → Daily expiry alert scheduled flow
```

| Stage | Action               | Actor Role | SP Group       | Power Automate Trigger                                            |
| ----- | -------------------- | ---------- | -------------- | ----------------------------------------------------------------- |
| 1     | Create / Edit Record | HR Admin   | D05-HR-Manager | On item create or update                                          |
| 2     | Expiry Alert         | System     | —              | Daily scheduled — check NextDueDate < Today+30 → email HR Manager |

---

## Role Matrix

| Domino Group | SharePoint Group | SP Group Name  | Permissions                                  |
| ------------ | ---------------- | -------------- | -------------------------------------------- |
| HR Admins    | HR Manager       | D05-HR-Manager | Full Control (CRUD + view all employee data) |
| All Staff    | HR Staff         | D05-HR-Staff   | Read Only (view own record only)             |

---

## Power Automate Actions

| Flow Name            | Trigger                              | Action                                                                                                                                                     |
| -------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HR_TNPRA_ExpiryAlert | Scheduled daily (recurrence trigger) | Query HR_TNPRA_TyphoidRecords and HR_TNPRA_FoodHandlerExam for NextDueDate ≤ Today+30; send email to D05-HR-Manager with employee name, type, and due date |

---

## Screen Inventory

| Screen Name | Type      | Purpose                                                             | Visible To                                    |
| ----------- | --------- | ------------------------------------------------------------------- | --------------------------------------------- |
| TNPRA_List  | Gallery   | List all TNPRA records with category/department/status filter       | D05-HR-Manager (all); D05-HR-Staff (own only) |
| TNPRA_New   | Form      | Create new employee medical record with child table entry galleries | D05-HR-Manager only                           |
| TNPRA_View  | Read-only | View all sections: typhoid, food handler, NPRA records              | D05-HR-Manager, D05-HR-Staff (own)            |
| TNPRA_Edit  | Form      | Edit existing record and add new rows to child galleries            | D05-HR-Manager only                           |

---

## Navigation Map

```
TNPRA_List → [New] → TNPRA_New (Manager only)
TNPRA_List → [View] → TNPRA_View
TNPRA_List → [Edit] → TNPRA_Edit (Manager only)
TNPRA_View → [Edit] → TNPRA_Edit
```

---

## Migration Risks & Notes

1. **3 child tables with repeating medical entries:** TyphoidRecords (×10), FoodHandlerExam (×10),
   and NPRARecords must all appear in the TNPRA_View and TNPRA_Edit screens. Use three collapsible
   gallery panels within the screen to manage visual density. Load all three `Concurrent()` on
   screen load.

2. **Expiry alert logic for two date fields:** The scheduled flow must check two different
   `NextDueDate` fields — one from `HR_TNPRA_TyphoidRecords` and one from
   `HR_TNPRA_FoodHandlerExam`. Implement as a single scheduled flow with two parallel query
   branches. Alert threshold: 30 days before expiry.

3. **NPRA vs Food Handler vs Typhoid category split:** Not all employees require all 3 record types.
   The `Category` column (Food Handler, Non-Food Handler, NPRA-Only) determines which child table
   panels to show or hide in the canvas app. Use `If(gblCategory = "Food Handler", true, false)` to
   control visibility per panel.

4. **Sensitive medical data access:** Medical records are highly sensitive. Employees should only
   see their own TNPRA record (filter by EmpNo = gblCurrentEmpNo). HR Manager can see all. Do not
   allow cross-employee viewing by staff.

5. **Record-per-employee pattern:** One parent TNPRA record per employee (not one per visit).
   Multiple visit rows live in child tables. On TNPRA_List, HR should be able to search/filter by
   employee name, department, category, and status.

---

## v3 Impossibilities

| Domino Feature                           | v3 Status  | Workaround                                                     |
| ---------------------------------------- | ---------- | -------------------------------------------------------------- |
| 10-row repeating table for vaccinations  | NOT NATIVE | Normalize to HR_TNPRA_TyphoidRecords child table with gallery  |
| 10-row repeating table for food handler  | NOT NATIVE | Normalize to HR_TNPRA_FoodHandlerExam child table with gallery |
| Scheduled expiry alert from Domino agent | NOT NATIVE | Power Automate recurrence trigger + date comparison expression |
| Category-based field visibility          | LIMITED    | Power Fx `If(gblCategory="X", Visible:=true)` per panel        |

---

## Reference PDF

| Field          | Value                                                                                                                                                                                                                                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/TNPRA.pdf                                                                                                                                                                                                                                                                                                       |
| Page Count     | 5                                                                                                                                                                                                                                                                                                                                                             |
| Field Evidence | Category, Company, Status, ContractCompany, Name, EmpNo, IdentityNo, Gender, Designation, Section, Department, Superior; Typhoid table ×10 (DateGiven, Hospital, DoctorName, NextDue, BatchNo); FoodHandler table ×10 (ExamDate, Hospital, DoctorName, Result, NextExamDate); NPRA (DateExam, Hospital, DoctorName, Result, NPRARefNo) — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (15 columns) + 3 child tables
      (TyphoidRecords/FoodHandlerExam/NPRARecords)
- [x] Child tables: HR_TNPRA_TyphoidRecords, HR_TNPRA_FoodHandlerExam, HR_TNPRA_NPRARecords — all
      normalized
- [x] Workflow Stage Map: ASCII diagram + formal trigger-condition table present (CRUD + scheduled
      alert)
- [x] Role Matrix: all roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 1 scheduled flow named with HR*TNPRA*[EventName] convention
- [x] Screen Inventory: 4 screens listed with visibility rules
- [x] Navigation Map: screen flow documented
- [x] Migration Risks & Notes: 5 risks with mitigations
- [x] v3 Impossibilities: 4 items documented with workarounds
- [x] Reference PDF: path, page count, field evidence confirmed
- [x] Zero unresolved markers present in document
- [x] Blueprint Status section present and correctly populated

**COMPLETION STATUS: COMPLETE**

---

## Sentinel Validation Report

**Validation Date:** 2026-04-19  
**Validator Agent:** Sentinel v1.1  
**Blueprint:** TNPRA (HR)  
**Input Status:** COMPLETE

### Validation Results

| Check # | Validation Item                 | Status  | Evidence / Comment                           |
| ------- | ------------------------------- | ------- | -------------------------------------------- |
| 1       | Form Identity table present     | ✅ PASS | Required identity fields present             |
| 2       | Section order compliance        | ✅ PASS | Canonical blueprint section order maintained |
| 3       | Workflow Stage Map formal table | ✅ PASS | Stage/action table present                   |
| 4       | Role Matrix mapped to SP groups | ✅ PASS | D05-HR role mappings present                 |
| 5       | Domino field mappings           | ✅ PASS | Schema and field evidence documented         |
| 6       | Marker gate status              | ✅ PASS | check-markers.sh exit code 0                 |

### Validation Verdict

**GATE STATUS:** ✅ **PASS** — Blueprint meets all compliance requirements. Ready for Craftsman
dispatch.

---

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:59:10Z
