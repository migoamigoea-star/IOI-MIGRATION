# Technical Blueprint: FWWPE — Foreign Worker Work Period Extension

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
| Form Code                  | FWWPE                                                   |
| Official Name              | Foreign Worker Work Period Extension                    |
| Department                 | HR                                                      |
| Module                     | Employee Lifecycle — Foreign Worker Management          |
| Site(s)                    | PRAI, JOHOR                                             |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/FWWPE.pdf |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline)   |
| Official Name Claim Status | Claimed from source PDF title                           |
| Blueprint Version          | 1.0                                                     |
| Blueprint Date             | 2026-04-19                                              |
| Architect                  | GitHub Copilot (Architect)                              |

---

## Purpose

FWWPE manages the process of extending a foreign worker's work permit period within IOI Acidchem. HR
or the immediate supervisor submits the extension request with passport and work permit details,
which is reviewed and signed off by the Head of Section (HOS) and Head of Department (HOD). The
migrated solution must preserve dual-approver attribution, work permit expiry date tracking, and a
final contractor status flag for compliance and permit renewal records.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "FWWPE"

### Parent List: MainDB_HR

| #   | SP Internal Name  | Display Label           | Column Type         | Required | Classification   | Source Mapping / Notes                                            |
| --- | ----------------- | ----------------------- | ------------------- | -------- | ---------------- | ----------------------------------------------------------------- |
| 1   | Title             | Title                   | Single line text    | Yes      | SYSTEM-COMPUTED  | FWWPE prefix + EmpNo                                              |
| 2   | FormCode          | Form Code               | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value FWWPE                                                 |
| 3   | IssueNo           | Issue No                | Single line text    | No       | SYSTEM-COMPUTED  | `IssueNo` — auto-generated on submit                              |
| 4   | SendTo            | Send To                 | Person or Group     | No       | USER-ENTERED     | `SendTo` — notification recipient                                 |
| 5   | HOS               | Head of Section         | Person or Group     | Yes      | USER-ENTERED     | `HOS`                                                             |
| 6   | HOD               | Head of Department      | Person or Group     | Yes      | USER-ENTERED     | `HOD`                                                             |
| 7   | CC                | CC Recipients           | Multiple lines text | No       | USER-ENTERED     | `CC` — additional email addresses                                 |
| 8   | Company           | Company                 | Choice              | Yes      | USER-ENTERED     | `Company` — IOI Oleochemical, IOI Acidchem                        |
| 9   | EmpName           | Employee Name           | Single line text    | Yes      | USER-ENTERED     | `Name`                                                            |
| 10  | EmpNo             | Employee No             | Single line text    | Yes      | USER-ENTERED     | `EmpNo`                                                           |
| 11  | PassportNo        | Passport Number         | Single line text    | Yes      | USER-ENTERED     | `PassportNo`                                                      |
| 12  | Department        | Department              | Single line text    | Yes      | USER-ENTERED     | `Department`                                                      |
| 13  | Section           | Section                 | Single line text    | No       | USER-ENTERED     | `Section`                                                         |
| 14  | WPExpiryDate      | Work Permit Expiry Date | Date and Time       | Yes      | USER-ENTERED     | `WPExpDate`                                                       |
| 15  | ExtensionDateFrom | Extension From Date     | Date and Time       | Yes      | USER-ENTERED     | `DateF`                                                           |
| 16  | ExtensionDateTo   | Extension To Date       | Date and Time       | Yes      | USER-ENTERED     | `DateT`                                                           |
| 17  | ReplyRemark       | Reply Remarks           | Multiple lines text | No       | USER-ENTERED     | `ReplyRemark` — remarks on approval                               |
| 18  | HOSStatus         | HOS Status              | Choice              | No       | WORKFLOW-MANAGED | `HOSStatus` — Pending, Approved, Rejected                         |
| 19  | ContStatus        | Contractor Status       | Choice              | No       | WORKFLOW-MANAGED | `ContStatus` — Active, Expired, Extended                          |
| 20  | HODStatus         | HOD Status              | Choice              | No       | WORKFLOW-MANAGED | `HODStatus` — Pending, Approved, Rejected                         |
| 21  | CurrentStatus     | Current Status          | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HOS_Review, HOD_Review, Approved, Rejected      |
| 22  | WorkflowStage     | Workflow Stage          | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=HOS_Review 4=HOD_Review 5=Approved/Rejected |
| 23  | CurrentAction     | Current Action          | Choice              | Yes      | WORKFLOW-MANAGED | Hidden routing field                                              |
| 24  | EnvironmentTag    | Environment             | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                   |
| 25  | IsLocked          | Is Locked               | Yes/No              | No       | WORKFLOW-MANAGED | True after HOD decision                                           |

---

## Workflow Stage Map

```
[HR / Supervisor] → STAGE 1: Draft
      ↓ Submit
[HOS] → STAGE 2: HOS Review (Approve / Reject)
      ↓ Approve
[HOD] → STAGE 3: HOD Review (Approve / Reject)
      ↓ Approve
STAGE 4: Approved (ContStatus updated, IsLocked = Yes)
```

| Stage | Action               | Actor Role         | SP Group     | Power Automate Trigger                                    |
| ----- | -------------------- | ------------------ | ------------ | --------------------------------------------------------- |
| 1     | Create & Submit      | HR or Supervisor   | D05-HR-Staff | When Status='Draft' and item created                      |
| 2     | HOS Approve / Reject | Head of Section    | D05-HR-HOS   | When Status='Submitted' — notify HOS via adaptive card    |
| 3     | HOD Approve / Reject | Head of Department | D05-HR-HOD   | When Status='HOS_Review' and HOS approves — notify HOD    |
| 4     | Close                | System             | —            | When HOD approves → set ContStatus=Extended, IsLocked=Yes |

---

## Role Matrix

| Domino Group | SharePoint Group | SP Group Name  | Permissions    |
| ------------ | ---------------- | -------------- | -------------- |
| HR Admins    | HR Staff         | D05-HR-Staff   | Contribute     |
| HOS group    | HR HOS           | D05-HR-HOS     | Read + Approve |
| HOD group    | HR HOD           | D05-HR-HOD     | Read + Approve |
| HR Manager   | HR Manager       | D05-HR-Manager | Full Control   |

---

## Power Automate Actions

| Flow Name            | Trigger                                   | Action                                                                          |
| -------------------- | ----------------------------------------- | ------------------------------------------------------------------------------- |
| HR_FWWPE_OnSubmit    | When Status='Draft' → item submitted      | Generate IssueNo, stamp date, set Stage=2, notify HOS                           |
| HR_FWWPE_HOSDecision | When Status='Submitted' and HOS responds  | If Approve: set HOSStatus=Approved, Stage=3, notify HOD; if Reject: lock+notify |
| HR_FWWPE_HODDecision | When Status='HOS_Review' and HOD responds | If Approve: set ContStatus=Extended, IsLocked=Yes; if Reject: notify submitter  |

---

## Screen Inventory

| Screen Name       | Type      | Purpose                                   | Visible To                   |
| ----------------- | --------- | ----------------------------------------- | ---------------------------- |
| FWWPE_List        | Gallery   | List all FWWPE records with status filter | D05-HR-Staff, D05-HR-Manager |
| FWWPE_New         | Form      | New extension request                     | D05-HR-Staff                 |
| FWWPE_View        | Read-only | View extension record details             | All roles (own record)       |
| FWWPE_Edit        | Form      | Edit draft before submission              | D05-HR-Staff (creator)       |
| FWWPE_HOSApproval | Approval  | HOS decision: Approve / Reject            | D05-HR-HOS                   |
| FWWPE_HODApproval | Approval  | HOD final decision                        | D05-HR-HOD                   |

---

## Navigation Map

```
FWWPE_List → [New] → FWWPE_New
FWWPE_List → [View] → FWWPE_View
FWWPE_List → [Edit] → FWWPE_Edit (Draft only)
FWWPE_View → [HOS Action] → FWWPE_HOSApproval (HOS at Stage 2)
FWWPE_View → [HOD Action] → FWWPE_HODApproval (HOD at Stage 3)
```

---

## Migration Risks & Notes

1. **Work permit expiry date tracking:** WPExpiryDate is a compliance-critical field. A Power
   Automate scheduled flow should alert HR 60/30/14 days before expiry for any record with
   `ContStatus=Active`. Implement as a separate monitoring flow.

2. **Dual approver chain (HOS then HOD):** Both HOS and HOD must approve sequentially. If HOS
   rejects, the request is closed and does not advance to HOD. Implement strict stage gating in
   Power Automate — no bypass.

3. **CC field as email string:** The Domino CC field stores raw email addresses. In M365, convert to
   a multi-select Person field if possible, or keep as free-text and parse in Power Automate for
   notification delivery.

4. **IssueNo uniqueness:** Must be globally unique across PRAI and JOHOR sites. Use Power Automate
   to generate: `FWWPE-{Site}-{Year}-{Seq}` format.

5. **Contractor status synchronization:** `ContStatus` changes must be reflected in any outsourced
   worker registry (OWP form). This cross-form dependency requires a PA flow or a manual HR process
   documented in user training materials.

---

## v3 Impossibilities

| Domino Feature                        | v3 Status  | Workaround                                                            |
| ------------------------------------- | ---------- | --------------------------------------------------------------------- |
| Auto-email on permit expiry approach  | NOT NATIVE | Power Automate scheduled flow checks WPExpiryDate and alerts HR       |
| CC email list with multiple addresses | LIMITED    | Store as text; parse in Power Automate; use Person multi-select in v3 |
| Cross-form status sync (OWP linkage)  | NOT NATIVE | Separate PA flow or manual coordination; document in handoff notes    |

---

## Reference PDF

| Field          | Value                                                                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/FWWPE.pdf                                                                                                                                     |
| Page Count     | 4                                                                                                                                                                                           |
| Field Evidence | IssueNo, SendTo, HOS, HOD, CC, Company, Name, EmpNo, PassportNo, Department, Section, WPExpDate, DateF, DateT, Status, ReplyRemark, HOSStatus, ContStatus, HODStatus — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (25 columns) numbered, typed, classified, Domino-mapped
- [x] No child tables required (all fields fit in parent list)
- [x] Workflow Stage Map: ASCII diagram + formal trigger-condition table present
- [x] Role Matrix: all roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 3 flows named with HR*FWWPE*[EventName] convention
- [x] Screen Inventory: 6 screens listed with visibility rules
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
**Blueprint:** FWWPE (HR)  
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

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:59:08Z
