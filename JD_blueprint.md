# Technical Blueprint: JD — Job Description Documentation Control

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
| Form Code                  | JD                                                    |
| Official Name              | Job Description Documentation Control                 |
| Department                 | HR                                                    |
| Module                     | HR Administration — Document Control                  |
| Site(s)                    | PRAI, JOHOR                                           |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/JD.pdf  |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline) |
| Official Name Claim Status | Claimed from source PDF title                         |
| Blueprint Version          | 1.0                                                   |
| Blueprint Date             | 2026-04-19                                            |
| Architect                  | GitHub Copilot (Architect)                            |

---

## Purpose

JD manages the controlled authoring, versioning, and approval of Job Descriptions within IOI
Acidchem. HR creates a JD record capturing position details, reporting structure, job summary, and
up to 26 individual duty statements. The form is approved by the HOD and becomes the controlled
document for the position. The migrated solution must normalize the duty statements into a child
table, preserve revision numbering, and maintain a locked final state after HOD approval.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "JD"

### Parent List: MainDB_HR (JD header)

| #   | SP Internal Name | Display Label      | Column Type         | Required | Classification   | Source Mapping / Notes                                   |
| --- | ---------------- | ------------------ | ------------------- | -------- | ---------------- | -------------------------------------------------------- |
| 1   | Title            | Title              | Single line text    | Yes      | SYSTEM-COMPUTED  | JD prefix + JobNo                                        |
| 2   | FormCode         | Form Code          | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value JD                                           |
| 3   | JDCategory       | Category           | Choice              | Yes      | USER-ENTERED     | `category` — Executive, Manager, Supervisor, Staff, etc. |
| 4   | HoldingStatus    | Holding Status     | Choice              | No       | USER-ENTERED     | `HStatus` — Active, Superseded, Draft                    |
| 5   | Division         | Division           | Single line text    | Yes      | USER-ENTERED     | `div1`                                                   |
| 6   | Department       | Department         | Single line text    | Yes      | USER-ENTERED     | `department1`                                            |
| 7   | Section          | Section            | Single line text    | No       | USER-ENTERED     | `section`                                                |
| 8   | Company          | Company            | Choice              | Yes      | USER-ENTERED     | `Company` — IOI Oleochemical, IOI Acidchem               |
| 9   | JobNo            | Job No             | Single line text    | Yes      | USER-ENTERED     | `jobno`                                                  |
| 10  | EffectiveDate    | Effective Date     | Date and Time       | Yes      | USER-ENTERED     | `effectdate`                                             |
| 11  | RevisionNo       | Revision Number    | Single line text    | No       | USER-ENTERED     | `revnum` — e.g. Rev.01, Rev.02                           |
| 12  | JobTitle         | Job Title          | Single line text    | Yes      | USER-ENTERED     | `jobtitle`                                               |
| 13  | ReportsTo        | Reports To         | Single line text    | No       | USER-ENTERED     | `repno` — reporting position code                        |
| 14  | JobSummary       | Job Summary        | Multiple lines text | Yes      | USER-ENTERED     | `jobsum`                                                 |
| 15  | HOD              | Head of Department | Person or Group     | Yes      | USER-ENTERED     | HOD approver                                             |
| 16  | CurrentStatus    | Current Status     | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HOD_Approved, Superseded               |
| 17  | WorkflowStage    | Workflow Stage     | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=HOD_Review 4=Approved              |
| 18  | CurrentAction    | Current Action     | Choice              | Yes      | WORKFLOW-MANAGED | Hidden routing field                                     |
| 19  | EnvironmentTag   | Environment        | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                          |
| 20  | IsLocked         | Is Locked          | Yes/No              | No       | WORKFLOW-MANAGED | True after HOD approval                                  |

### Child List: HR_JD_Duties

Normalizes duties_1 through duties_26 from Domino into individual rows.

| #   | SP Internal Name | Display Label    | Column Type         | Required | Notes                                            |
| --- | ---------------- | ---------------- | ------------------- | -------- | ------------------------------------------------ |
| 1   | JDRef            | JD Reference     | Lookup (MainDB_HR)  | Yes      | Links to parent JD record                        |
| 2   | DutySeq          | Duty No          | Number              | Yes      | Sequence 1–26; display order                     |
| 3   | DutyDescription  | Duty Description | Multiple lines text | Yes      | `duties_N` — the duty statement text             |
| 4   | DutyCategory     | Duty Category    | Choice              | No       | Core Duty, Secondary Duty, Administrative, Other |

---

## Workflow Stage Map

```
[HR] → STAGE 1: Draft (create JD with duties)
      ↓ Submit
[HOD] → STAGE 2: HOD Review (Approve / Reject)
      ↓ Approve
STAGE 3: Approved (IsLocked = Yes, HoldingStatus = Active)
```

| Stage | Action          | Actor Role | SP Group     | Power Automate Trigger                                 |
| ----- | --------------- | ---------- | ------------ | ------------------------------------------------------ |
| 1     | Create & Submit | HR Staff   | D05-HR-Staff | When Status='Draft' and item created                   |
| 2     | HOD Review      | HOD        | D05-HR-HOD   | When Status='Submitted' — notify HOD for approval      |
| 3     | Approve / Lock  | System     | —            | When HOD approves → IsLocked=Yes, HoldingStatus=Active |

---

## Role Matrix

| Domino Group | SharePoint Group | SP Group Name  | Permissions    |
| ------------ | ---------------- | -------------- | -------------- |
| HR Admins    | HR Staff         | D05-HR-Staff   | Contribute     |
| HOD group    | HR HOD           | D05-HR-HOD     | Read + Approve |
| HR Manager   | HR Manager       | D05-HR-Manager | Full Control   |

---

## Power Automate Actions

| Flow Name         | Trigger                                  | Action                                                                     |
| ----------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| HR_JD_OnSubmit    | When Status='Draft' → item submitted     | Stamp effective date, set Stage=2, notify HOD                              |
| HR_JD_HODDecision | When Status='Submitted' and HOD responds | If Approve: IsLocked=Yes, HoldingStatus=Active; if Reject: return to Draft |

---

## Screen Inventory

| Screen Name    | Type      | Purpose                                               | Visible To                   |
| -------------- | --------- | ----------------------------------------------------- | ---------------------------- |
| JD_List        | Gallery   | List all JD records with department and status filter | D05-HR-Staff, D05-HR-Manager |
| JD_New         | Form      | Create new JD: header + duties child gallery          | D05-HR-Staff                 |
| JD_View        | Read-only | View full JD with all duty statements                 | All roles (own dept or HR)   |
| JD_Edit        | Form      | Edit draft JD (header + duties)                       | D05-HR-Staff (creator)       |
| JD_HODApproval | Approval  | HOD approval screen                                   | D05-HR-HOD                   |

---

## Navigation Map

```
JD_List → [New] → JD_New
JD_List → [View] → JD_View
JD_List → [Edit] → JD_Edit (Draft only)
JD_View → [HOD Action] → JD_HODApproval (HOD at Stage 2)
```

---

## Migration Risks & Notes

1. **26 duty fields to child table:** Domino stores duties_1 through duties_26 as flat columns.
   These must be migrated to `HR_JD_Duties` child table rows. The Craftsman must implement a gallery
   in JD_New/JD_Edit that allows adding/editing duty rows (up to 26) with drag-reorder or sequence
   number edit.

2. **Revision control:** JD revisions must not overwrite the previous version — each revision
   creates a new JD record with incremented `RevisionNo`, and the previous record's `HoldingStatus`
   is set to `Superseded`. Implement as a "New Revision" action in JD_View that pre-populates a new
   form.

3. **HoldingStatus = Superseded automation:** When a new revision is approved, Power Automate must
   automatically set the previous version's `HoldingStatus = Superseded` and `IsLocked = Yes`. Query
   by `JobNo` to find the prior version.

4. **ReportsTo as position code vs person:** The Domino `repno` field stores a position code (not a
   person). In M365, keep as free-text — do not link to a Person column, as the reporting structure
   is positional, not person-bound.

5. **Up to 26 duties performance:** Gallery rendering of 26+ child records may be slow on mobile.
   Implement `Concurrent()` loading and consider limiting gallery to top 15 with a "Show all" toggle
   for performance.

---

## v3 Impossibilities

| Domino Feature                            | v3 Status  | Workaround                                                             |
| ----------------------------------------- | ---------- | ---------------------------------------------------------------------- |
| Flat duties_1 to duties_26 columns        | NOT NATIVE | Child table HR_JD_Duties with sequence column                          |
| Auto-supersede prior revision on approval | NOT NATIVE | Power Automate queries by JobNo and updates prior record HoldingStatus |
| Drag-and-drop duty row reordering         | NOT NATIVE | Manual sequence number entry; no native drag-reorder in canvas v3      |

---

## Reference PDF

| Field          | Value                                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/JD.pdf                                                                                                          |
| Page Count     | 6                                                                                                                                                             |
| Field Evidence | category, HStatus, div1, department1, section, Company, jobno, effectdate, revnum, jobtitle, repno, jobsum, duties_1 through duties_26 — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (20 columns) + child table HR_JD_Duties (4 columns)
- [x] Child table: HR_JD_Duties normalizes duties_1–26 flat columns
- [x] Workflow Stage Map: ASCII diagram + formal trigger-condition table present
- [x] Role Matrix: all roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 2 flows named with HR*JD*[EventName] convention
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
**Blueprint:** JD (HR)  
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
