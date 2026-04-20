# Technical Blueprint: OWP — Outsource Worker Database

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

| Field                      | Value                                                 |
| -------------------------- | ----------------------------------------------------- |
| Form Code                  | OWP                                                   |
| Official Name              | Outsource Worker Database                             |
| Department                 | HR                                                    |
| Module                     | Employee Lifecycle — Contractor & Outsource Tracking  |
| Site(s)                    | PRAI, JOHOR                                           |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/OWP.pdf |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline) |
| Official Name Claim Status | Claimed from source PDF title                         |
| Blueprint Version          | 1.0                                                   |
| Blueprint Date             | 2026-04-19                                            |
| Architect                  | GitHub Copilot (Architect)                            |

---

## Purpose

OWP is a registry database form for tracking outsourced and contract workers engaged by IOI
Acidchem. It stores personal details, immigration documents (passport, work permit), employment
status, and separation date. There is no approval workflow — HR staff perform direct CRUD operations
to maintain accurate headcount records for compliance, permit renewal monitoring, and workforce
reporting.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "OWP"

### Parent List: MainDB_HR

| #   | SP Internal Name | Display Label           | Column Type         | Required | Classification  | Source Mapping / Notes                           |
| --- | ---------------- | ----------------------- | ------------------- | -------- | --------------- | ------------------------------------------------ |
| 1   | Title            | Title                   | Single line text    | Yes      | SYSTEM-COMPUTED | OWP prefix + EmpNo                               |
| 2   | FormCode         | Form Code               | Single line text    | Yes      | SYSTEM-COMPUTED | Fixed value OWP                                  |
| 3   | Company          | Company                 | Choice              | Yes      | USER-ENTERED    | `Company` — IOI Oleochemical, IOI Acidchem       |
| 4   | WorkerStatus     | Status                  | Choice              | Yes      | USER-ENTERED    | `Status` — Active, Resigned, Expired, Terminated |
| 5   | EmpName          | Worker Name             | Single line text    | Yes      | USER-ENTERED    | `Name`                                           |
| 6   | EmpNo            | Employee No             | Single line text    | Yes      | USER-ENTERED    | `EmpNo`                                          |
| 7   | Section          | Section                 | Single line text    | No       | USER-ENTERED    | `Section`                                        |
| 8   | DateOfBirth      | Date of Birth           | Date and Time       | Yes      | USER-ENTERED    | `DOB`                                            |
| 9   | DateOfJoining    | Date of Joining         | Date and Time       | Yes      | USER-ENTERED    | `DOJ`                                            |
| 10  | PassportNo       | Passport Number         | Single line text    | Yes      | USER-ENTERED    | `PassportNo`                                     |
| 11  | PassportExpiry   | Passport Expiry Date    | Date and Time       | Yes      | USER-ENTERED    | `PassportExpiryDate`                             |
| 12  | Nationality      | Nationality             | Single line text    | Yes      | USER-ENTERED    | `Nationality`                                    |
| 13  | WPExpiryDate     | Work Permit Expiry Date | Date and Time       | Yes      | USER-ENTERED    | `WorkPermitExpiryDate`                           |
| 14  | WorkPermitNo     | Work Permit Number      | Single line text    | Yes      | USER-ENTERED    | `WorkPermitNo`                                   |
| 15  | WPEmployed       | Work Permit Employed By | Choice              | No       | USER-ENTERED    | `WPEmployed` — IOI Acidchem, Contractor company  |
| 16  | WPEmployer       | Employer Name           | Single line text    | No       | USER-ENTERED    | `WPEmployer`                                     |
| 17  | ResignDate       | Resignation / Exit Date | Date and Time       | No       | USER-ENTERED    | `ResignDate`                                     |
| 18  | ExitReason       | Exit Reason             | Multiple lines text | No       | USER-ENTERED    | `Reason`                                         |
| 19  | EnvironmentTag   | Environment             | Choice              | Yes      | SYSTEM-COMPUTED | DEV, TEST, PROD                                  |
| 20  | IsLocked         | Is Locked               | Yes/No              | No       | USER-MANAGED    | Lock on resignation/termination                  |

---

## Workflow Stage Map

OWP is a CRUD registry with no approval workflow. All records are maintained directly by HR.

```
[HR Staff] → CREATE → Registry Entry (Active)
[HR Staff] → EDIT   → Update permit/document details
[HR Staff] → UPDATE Status → Active / Resigned / Expired / Terminated
```

| Stage | Action          | Actor Role | SP Group     | Trigger                                   |
| ----- | --------------- | ---------- | ------------ | ----------------------------------------- |
| 1     | Create record   | HR Staff   | D05-HR-Staff | HR creates new outsource worker entry     |
| 2     | Update record   | HR Staff   | D05-HR-Staff | HR edits permit/document details          |
| 3     | Set exit status | HR Staff   | D05-HR-Staff | HR sets Status=Resigned/Terminated + date |

---

## Role Matrix

| Domino Group | SharePoint Group | SP Group Name  | Permissions       |
| ------------ | ---------------- | -------------- | ----------------- |
| HR Admins    | HR Staff         | D05-HR-Staff   | Contribute (CRUD) |
| HR Manager   | HR Manager       | D05-HR-Manager | Full Control      |

---

## Power Automate Actions

| Flow Name                  | Trigger         | Action                                                          |
| -------------------------- | --------------- | --------------------------------------------------------------- |
| HR_OWP_ExpiryAlertPassport | Scheduled daily | Alert HR 60/30/14 days before PassportExpiry for Active workers |
| HR_OWP_ExpiryAlertWP       | Scheduled daily | Alert HR 60/30/14 days before WPExpiryDate for Active workers   |

---

## Screen Inventory

| Screen Name | Type      | Purpose                                               | Visible To                   |
| ----------- | --------- | ----------------------------------------------------- | ---------------------------- |
| OWP_List    | Gallery   | List all outsource workers with status/company filter | D05-HR-Staff, D05-HR-Manager |
| OWP_New     | Form      | Register new outsource worker                         | D05-HR-Staff                 |
| OWP_View    | Read-only | View worker record (documents + status)               | D05-HR-Staff, D05-HR-Manager |
| OWP_Edit    | Form      | Edit worker details                                   | D05-HR-Staff                 |

---

## Navigation Map

```
OWP_List → [New] → OWP_New
OWP_List → [View] → OWP_View
OWP_List → [Edit] → OWP_Edit
```

---

## Migration Risks & Notes

1. **Passport and permit expiry monitoring:** The primary value of this registry is expiry tracking.
   Scheduled Power Automate flows must fire daily alerts — failure to implement these renders the
   migrated system non-compliant with immigration monitoring requirements.

2. **Sensitive personal data (IC/passport/DOB):** OWP stores PII and immigration data. Ensure the
   SharePoint site permissions restrict access to `D05-HR-Staff` and `D05-HR-Manager` only. No
   IOI-AllStaff-Read permissions on this list.

3. **Dual employer tracking (WPEmployed / WPEmployer):** Some foreign workers are on contractor
   company permits, not directly held by IOI. The `WPEmployed` and `WPEmployer` fields must be
   accurately populated to distinguish direct-hire vs contractor-permit workers.

4. **EmpNo alignment with FWWPE:** OWP EmpNo must match the EmpNo used in FWWPE extension requests.
   If a FWWPE extension is approved, HR should update the corresponding OWP record's WPExpiryDate
   manually (or via a linked PA flow).

5. **Exit record preservation:** Resigned/Terminated OWP records must be retained per regulatory and
   audit requirements (7-year minimum for immigration-related records). Do not physically delete —
   set `WorkerStatus = Resigned/Terminated` and archive filtering in gallery.

---

## v3 Impossibilities

| Domino Feature                         | v3 Status  | Workaround                                                              |
| -------------------------------------- | ---------- | ----------------------------------------------------------------------- |
| Automatic permit expiry calendar alert | NOT NATIVE | Power Automate scheduled flow with date comparison                      |
| Cross-form EmpNo lookup to FWWPE       | LIMITED    | Display FWWPE link via filtered gallery; no native cross-list FK        |
| Bulk import of worker records from CSV | NOT NATIVE | Use SharePoint list import or PA data import flow for initial migration |

---

## Reference PDF

| Field          | Value                                                                                                                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/OWP.pdf                                                                                                                                               |
| Page Count     | 2                                                                                                                                                                                                   |
| Field Evidence | Company, Status, Name, EmpNo, Section, DOB, DOJ, PassportNo, PassportExpiryDate, Nationality, WorkPermitExpiryDate, WorkPermitNo, WPEmployed, WPEmployer, ResignDate, Reason — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (20 columns) numbered, typed, classified, Domino-mapped
- [x] No child tables required (all fields fit in parent list)
- [x] Workflow Stage Map: CRUD registry (no approval workflow) — documented
- [x] Role Matrix: all roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 2 scheduled expiry alert flows documented
- [x] Screen Inventory: 4 screens listed with visibility rules
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
**Blueprint:** OWP (HR)  
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

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:59:09Z
