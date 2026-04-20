# Technical Blueprint: EPDU — Employee Personal Detail Update

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

| Field                      | Value                                                  |
| -------------------------- | ------------------------------------------------------ |
| Form Code                  | EPDU                                                   |
| Official Name              | Employee Personal Detail Update                        |
| Department                 | HR                                                     |
| Module                     | Employee Lifecycle — Personal Data Management          |
| Site(s)                    | PRAI, JOHOR                                            |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/EPDU.pdf |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline)  |
| Official Name Claim Status | Claimed from source PDF title                          |
| Blueprint Version          | 1.0                                                    |
| Blueprint Date             | 2026-04-19                                             |
| Architect                  | GitHub Copilot (Architect)                             |

---

## Purpose

EPDU allows employees to submit updates to their personal data stored in the HR system — including
address, emergency contacts, marital status, statutory numbers (EPF/SOCSO/income tax), education
history, children details, and family emergency contacts. HR reviews the submission and confirms the
update in the HR master record. The migrated solution must normalize the repeating education,
children, and family sections into child tables and preserve the 2-stage submit-and-review flow.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "EPDU"

### Parent List: MainDB_HR (EPDU header)

| #   | SP Internal Name | Display Label        | Column Type         | Required | Classification   | Source Mapping / Notes                             |
| --- | ---------------- | -------------------- | ------------------- | -------- | ---------------- | -------------------------------------------------- |
| 1   | Title            | Title                | Single line text    | Yes      | SYSTEM-COMPUTED  | EPDU prefix + EmpNo                                |
| 2   | FormCode         | Form Code            | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value EPDU                                   |
| 3   | EmpNo            | Employee No          | Single line text    | Yes      | USER-ENTERED     | `EmpNo`                                            |
| 4   | Company          | Company              | Choice              | Yes      | USER-ENTERED     | `Company` — IOI Oleochemical, IOI Acidchem         |
| 5   | EmpName          | Employee Name        | Single line text    | Yes      | USER-ENTERED     | `EmpName`                                          |
| 6   | NRIC_Old         | NRIC (Old)           | Single line text    | No       | USER-ENTERED     | `NRIC_O`                                           |
| 7   | NRIC_New         | NRIC (New/Current)   | Single line text    | Yes      | USER-ENTERED     | `NRIC_N`                                           |
| 8   | MaritalStatus    | Marital Status       | Choice              | Yes      | USER-ENTERED     | `Marital` — Single, Married, Divorced, Widowed     |
| 9   | Disabilities     | Disabilities         | Single line text    | No       | USER-ENTERED     | `Disabilities`                                     |
| 10  | Address1         | Address Line 1       | Single line text    | Yes      | USER-ENTERED     | `Address1`                                         |
| 11  | Address2         | Address Line 2       | Single line text    | No       | USER-ENTERED     | `Address2`                                         |
| 12  | Postcode1        | Postcode (Permanent) | Single line text    | No       | USER-ENTERED     | `Poscode1`                                         |
| 13  | Postcode2        | Postcode (Mailing)   | Single line text    | No       | USER-ENTERED     | `Poscode2`                                         |
| 14  | TelNo1           | Tel No 1             | Single line text    | No       | USER-ENTERED     | `TelNo1`                                           |
| 15  | TelNo2           | Tel No 2             | Single line text    | No       | USER-ENTERED     | `TelNo2`                                           |
| 16  | EPFNo            | EPF Number           | Single line text    | No       | USER-ENTERED     | `EPF`                                              |
| 17  | SOCSONo          | SOCSO Number         | Single line text    | No       | USER-ENTERED     | `SOCSO`                                            |
| 18  | IncomeTaxNo      | Income Tax Number    | Single line text    | No       | USER-ENTERED     | `ITAX`                                             |
| 19  | SpouseName       | Spouse Name          | Single line text    | No       | USER-ENTERED     | `SpName`                                           |
| 20  | SpouseNRIC       | Spouse NRIC          | Single line text    | No       | USER-ENTERED     | `SpNRIC_N`                                         |
| 21  | SpouseWork       | Spouse Workplace     | Single line text    | No       | USER-ENTERED     | `SpWork`                                           |
| 22  | SpouseOccupation | Spouse Occupation    | Single line text    | No       | USER-ENTERED     | `SpOccupation`                                     |
| 23  | HRRemarks        | HR Review Remarks    | Multiple lines text | No       | WORKFLOW-MANAGED | HR comments on update request                      |
| 24  | CurrentStatus    | Current Status       | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HR_Review, Updated, Rejected     |
| 25  | WorkflowStage    | Workflow Stage       | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=HR_Review 4=Updated/Rejected |
| 26  | EnvironmentTag   | Environment          | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                    |
| 27  | IsLocked         | Is Locked            | Yes/No              | No       | WORKFLOW-MANAGED | True after HR confirms update                      |

### Child List: HR_EPDU_Education

Normalizes up to 5 education entries from Domino.

| #   | SP Internal Name | Display Label    | Column Type        | Required | Notes                       |
| --- | ---------------- | ---------------- | ------------------ | -------- | --------------------------- |
| 1   | EPDURef          | EPDU Reference   | Lookup (MainDB_HR) | Yes      | Links to parent EPDU record |
| 2   | EduSeq           | Entry No         | Number             | Yes      | Sequence 1–5                |
| 3   | Institution      | Institution Name | Single line text   | Yes      | School/university name      |
| 4   | Qualification    | Qualification    | Single line text   | Yes      | Degree/cert obtained        |
| 5   | FieldOfStudy     | Field of Study   | Single line text   | No       | Major/specialisation        |
| 6   | YearCompleted    | Year Completed   | Number             | No       | 4-digit year                |
| 7   | Grade            | Grade / CGPA     | Single line text   | No       | Result/grade/CGPA           |

### Child List: HR_EPDU_Children

Normalizes up to 8 children entries.

| #   | SP Internal Name | Display Label  | Column Type        | Required | Notes                       |
| --- | ---------------- | -------------- | ------------------ | -------- | --------------------------- |
| 1   | EPDURef          | EPDU Reference | Lookup (MainDB_HR) | Yes      | Links to parent EPDU record |
| 2   | ChildSeq         | Child No       | Number             | Yes      | Sequence 1–8                |
| 3   | ChildName        | Child Name     | Single line text   | Yes      |                             |
| 4   | ChildNRIC        | Child NRIC     | Single line text   | No       |                             |
| 5   | ChildDOB         | Date of Birth  | Date and Time      | No       |                             |
| 6   | ChildGender      | Gender         | Choice             | No       | Male, Female                |

### Child List: HR_EPDU_Family

Normalizes up to 10 family/emergency contact entries.

| #   | SP Internal Name | Display Label  | Column Type        | Required | Notes                          |
| --- | ---------------- | -------------- | ------------------ | -------- | ------------------------------ |
| 1   | EPDURef          | EPDU Reference | Lookup (MainDB_HR) | Yes      | Links to parent EPDU record    |
| 2   | FamilySeq        | Entry No       | Number             | Yes      | Sequence 1–10                  |
| 3   | FamilyName       | Name           | Single line text   | Yes      |                                |
| 4   | FamilyNRIC       | NRIC           | Single line text   | No       |                                |
| 5   | Relationship     | Relationship   | Choice             | Yes      | Parent, Sibling, Spouse, Other |
| 6   | ContactNo        | Contact Number | Single line text   | No       |                                |

---

## Workflow Stage Map

```
[Employee] → STAGE 1: Draft (enter updated personal details)
      ↓ Submit
[HR] → STAGE 2: HR Review (verify + confirm update in HR system)
      ↓ Confirm Update
STAGE 3: Updated (IsLocked = Yes)
```

| Stage | Action           | Actor Role | SP Group       | Power Automate Trigger                                                     |
| ----- | ---------------- | ---------- | -------------- | -------------------------------------------------------------------------- |
| 1     | Create & Submit  | Employee   | D05-HR-Staff   | When Status='Draft' and employee submits                                   |
| 2     | HR Review        | HR Admin   | D05-HR-Manager | When Status='Submitted' — notify HR for review                             |
| 3     | Confirm / Reject | System     | —              | When HR confirms: IsLocked=Yes, Status=Updated; if Reject: notify employee |

---

## Role Matrix

| Domino Group  | SharePoint Group | SP Group Name  | Permissions              |
| ------------- | ---------------- | -------------- | ------------------------ |
| All Employees | HR Staff         | D05-HR-Staff   | Contribute (own records) |
| HR Admins     | HR Manager       | D05-HR-Manager | Full Control             |

---

## Power Automate Actions

| Flow Name        | Trigger                                 | Action                                                               |
| ---------------- | --------------------------------------- | -------------------------------------------------------------------- |
| HR_EPDU_OnSubmit | When Status='Draft' → employee submits  | Stamp date, set Stage=2, notify HR Admin                             |
| HR_EPDU_HRReview | When Status='Submitted' and HR responds | If Confirm: IsLocked=Yes, Status=Updated; if Reject: notify employee |

---

## Screen Inventory

| Screen Name   | Type      | Purpose                                                 | Visible To                         |
| ------------- | --------- | ------------------------------------------------------- | ---------------------------------- |
| EPDU_List     | Gallery   | List employee's own EPDU records with status filter     | D05-HR-Staff, D05-HR-Manager       |
| EPDU_New      | Form      | New personal detail update with child section galleries | D05-HR-Staff (own)                 |
| EPDU_View     | Read-only | View submitted/confirmed personal detail update         | D05-HR-Staff (own), D05-HR-Manager |
| EPDU_Edit     | Form      | Edit draft before submission                            | D05-HR-Staff (creator)             |
| EPDU_HRReview | Approval  | HR review and confirmation screen                       | D05-HR-Manager                     |

---

## Navigation Map

```
EPDU_List → [New] → EPDU_New
EPDU_List → [View] → EPDU_View
EPDU_List → [Edit] → EPDU_Edit (Draft only)
EPDU_View → [HR Review] → EPDU_HRReview (HR at Stage 2)
```

---

## Migration Risks & Notes

1. **3 child tables with variable row counts:** Education (×5), Children (×8), and Family (×10) must
   all be rendered in the same form. EPDU_New and EPDU_Edit must show three inline editable
   galleries simultaneously — test performance carefully and use `Concurrent()` for data loading.

2. **Sensitive PII (NRIC, EPF, SOCSO, tax):** EPDU contains statutory numbers and personal identity
   data. Restrict the `EPDU_HRReview` screen and `HR_EPDU_Family` / `HR_EPDU_Children` lists to
   D05-HR-Manager only. Employee should see own records only — enforce via
   `Filter(MainDB_HR, EmpNo = gblCurrentEmpNo)`.

3. **Employee self-service scope:** Employees submit EPDU for themselves only. The gallery must
   filter by the current user's employee number (`gblCurrentEmpNo`). Do not allow employees to view
   or edit other employees' EPDU records.

4. **Spouse NRIC vs old NRIC:** Two NRIC fields exist: `NRIC_O` (old IC format) and `NRIC_N`
   (current IC). Both must be captured. Add tooltip or help text in the form explaining when each
   applies.

5. **HR system update is offline:** The final "confirm update" step in EPDU means HR manually
   updates the HR master system (SAP/payroll). Power Automate can only update SharePoint — the
   actual HR system update is manual. Document this in user training: EPDU confirms the change
   request; HR applies it separately.

---

## v3 Impossibilities

| Domino Feature                                | v3 Status  | Workaround                                                                 |
| --------------------------------------------- | ---------- | -------------------------------------------------------------------------- |
| Simultaneous 3 repeating sections in one form | LIMITED    | Three separate child gallery panels in a scrollable container              |
| Direct integration with HR master (SAP)       | NOT NATIVE | EPDU confirms intent; HR applies to SAP manually or via separate connector |
| Per-employee access scope enforcement         | LIMITED    | Power Fx Filter by EmpNo = gblCurrentEmpNo; enforce in gallery filter      |

---

## Reference PDF

| Field          | Value                                                                                                                                                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/EPDU.pdf                                                                                                                                                                                 |
| Page Count     | 3                                                                                                                                                                                                                                      |
| Field Evidence | EmpNo, Company, EmpName, NRIC_O/N, Marital, Disabilities, Address1/2, Poscode1/2, TelNo1/2, EPF, SOCSO, ITAX; education table ×5; children table ×8; family details ×10; SpName, SpNRIC_N, SpWork, SpOccupation — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (27 columns) + 3 child tables (Education/Children/Family)
- [x] Child tables: HR_EPDU_Education, HR_EPDU_Children, HR_EPDU_Family — all normalized
- [x] Workflow Stage Map: ASCII diagram + formal trigger-condition table present
- [x] Role Matrix: all roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 2 flows named with HR*EPDU*[EventName] convention
- [x] Screen Inventory: 5 screens listed with visibility rules
- [x] Navigation Map: screen flow documented
- [x] Migration Risks & Notes: 5 risks with mitigations
- [x] v3 Impossibilities: 3 items documented with workarounds
- [x] Reference PDF: path, page count, field evidence confirmed
- [x] Zero unresolved markers present in document
- [x] Blueprint Status section present and correctly populated

**COMPLETION STATUS: COMPLETE**

---

## Sentinel Validation Report

**Validation Date:** 2026-04-19  
**Validator Agent:** Sentinel v1.1  
**Blueprint:** EPDU (HR)  
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
