# Technical Blueprint: ORGCHART — Organisation Charts Documentation Control

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

| Field                      | Value                                                      |
| -------------------------- | ---------------------------------------------------------- |
| Form Code                  | ORGCHART                                                   |
| Official Name              | Organisation Charts Documentation Control                  |
| Department                 | HR                                                         |
| Module                     | HR Administration — Document Control                       |
| Site(s)                    | PRAI, JOHOR                                                |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/ORGCHART.pdf |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline)      |
| Official Name Claim Status | Claimed from source PDF title                              |
| Blueprint Version          | 1.0                                                        |
| Blueprint Date             | 2026-04-19                                                 |
| Architect                  | GitHub Copilot (Architect)                                 |

---

## Purpose

ORGCHART governs the controlled submission, review, and approval of organisation chart documents
within IOI Acidchem. A department submits a new or revised org chart with attached document file,
which is then reviewed by a Verifier, endorsed by an Endorser, and approved by a final Approver.
Each authority level is identified by name, designation, and date. The migrated solution must
preserve the 4-level approval chain, attachment handling, chart numbering, and the final
locked/archived state.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "ORGCHART"

### Parent List: MainDB_HR

| #   | SP Internal Name | Display Label             | Column Type         | Required | Classification   | Source Mapping / Notes                                                 |
| --- | ---------------- | ------------------------- | ------------------- | -------- | ---------------- | ---------------------------------------------------------------------- |
| 1   | Title            | Title                     | Single line text    | Yes      | SYSTEM-COMPUTED  | ORGCHART prefix + OrgChartNum                                          |
| 2   | FormCode         | Form Code                 | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value ORGCHART                                                   |
| 3   | OrgChartNum      | Org Chart Number          | Single line text    | Yes      | USER-ENTERED     | `OrgChartNum` — document control number                                |
| 4   | Division         | Division                  | Single line text    | Yes      | USER-ENTERED     | `div`                                                                  |
| 5   | Department       | Department                | Single line text    | Yes      | USER-ENTERED     | `dept`                                                                 |
| 6   | Section          | Section                   | Single line text    | No       | USER-ENTERED     | `sect`                                                                 |
| 7   | PIC              | Person in Charge          | Single line text    | Yes      | USER-ENTERED     | `pic`                                                                  |
| 8   | Retention        | Retention Period          | Single line text    | No       | USER-ENTERED     | `ret`                                                                  |
| 9   | Attachment       | Org Chart Attachment      | Hyperlink           | Yes      | USER-ENTERED     | `attach` — primary org chart file                                      |
| 10  | Attachment2      | Supporting Attachment     | Hyperlink           | No       | USER-ENTERED     | `attach_1` — supplementary file                                        |
| 11  | PreparedByName   | Prepared By (Name)        | Single line text    | Yes      | USER-ENTERED     | Preparer name                                                          |
| 12  | PreparedByDesig  | Prepared By (Designation) | Single line text    | Yes      | USER-ENTERED     | Preparer designation                                                   |
| 13  | PreparedDate     | Prepared Date             | Date and Time       | Yes      | USER-ENTERED     | Prepared date                                                          |
| 14  | DraftSubBy       | Draft Submitted By        | Person or Group     | Yes      | USER-ENTERED     | `DraftSubBy`                                                           |
| 15  | dtSubmitted      | Date Submitted            | Date and Time       | Yes      | SYSTEM-COMPUTED  | `dtSubmitted`                                                          |
| 16  | ChangesRequired  | Changes Required?         | Yes/No              | No       | USER-ENTERED     | `rbChangesRequired`                                                    |
| 17  | DraftRemarks     | Draft Remarks             | Multiple lines text | No       | USER-ENTERED     | `DraftRemarks`                                                         |
| 18  | DraftRevBy       | Draft Reviewed By         | Person or Group     | No       | USER-ENTERED     | `DraftRevBy`                                                           |
| 19  | OrgSelection     | Org Selection             | Choice              | No       | USER-ENTERED     | `OrgSelection` — type of org chart                                     |
| 20  | Changes          | Changes Summary           | Multiple lines text | No       | USER-ENTERED     | `Changes` — description of changes from prior version                  |
| 21  | HRRemarks        | HR Remarks                | Multiple lines text | No       | WORKFLOW-MANAGED | `HRRem`                                                                |
| 22  | OrgNum           | Final Org Number          | Single line text    | No       | WORKFLOW-MANAGED | `OrgNum` — assigned on approval                                        |
| 23  | VerifiedByName   | Verified By (Name)        | Single line text    | No       | WORKFLOW-MANAGED | Verifier name — Stage 2                                                |
| 24  | VerifiedByDesig  | Verified By (Designation) | Single line text    | No       | WORKFLOW-MANAGED | Verifier designation                                                   |
| 25  | VerifiedDate     | Verified Date             | Date and Time       | No       | WORKFLOW-MANAGED | Verification stamp date                                                |
| 26  | EndorsedByName   | Endorsed By (Name)        | Single line text    | No       | WORKFLOW-MANAGED | Endorser name — Stage 3                                                |
| 27  | EndorsedByDesig  | Endorsed By (Designation) | Single line text    | No       | WORKFLOW-MANAGED | Endorser designation                                                   |
| 28  | EndorsedDate     | Endorsed Date             | Date and Time       | No       | WORKFLOW-MANAGED | Endorsement stamp date                                                 |
| 29  | ApprovedByName   | Approved By (Name)        | Single line text    | No       | WORKFLOW-MANAGED | Approver name — Stage 4                                                |
| 30  | ApprovedByDesig  | Approved By (Designation) | Single line text    | No       | WORKFLOW-MANAGED | Approver designation                                                   |
| 31  | ApprovedDate     | Approved Date             | Date and Time       | No       | WORKFLOW-MANAGED | Approval stamp date                                                    |
| 32  | CurrentStatus    | Current Status            | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Submitted, Verification, Endorsement, Approval, Approved        |
| 33  | WorkflowStage    | Workflow Stage            | Number              | Yes      | WORKFLOW-MANAGED | 1=Draft 2=Submitted 3=Verification 4=Endorsement 5=Approval 6=Approved |
| 34  | EnvironmentTag   | Environment               | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                        |
| 35  | IsLocked         | Is Locked                 | Yes/No              | No       | WORKFLOW-MANAGED | True after final approval                                              |

---

## Workflow Stage Map

```
[HR] → STAGE 1: Draft (create org chart record + attachment)
      ↓ Submit
STAGE 2: Submitted → Verifier reviews
      ↓ Verified
STAGE 3: Verification → Endorser reviews
      ↓ Endorsed
STAGE 4: Endorsement → Approver reviews
      ↓ Approved
STAGE 5: Approved (IsLocked = Yes, OrgNum assigned)
```

| Stage | Action            | Actor Role | SP Group         | Power Automate Trigger                                             |
| ----- | ----------------- | ---------- | ---------------- | ------------------------------------------------------------------ |
| 1     | Create & Submit   | HR Staff   | D05-HR-Staff     | When Status='Draft' and item submitted                             |
| 2     | Verify / Reject   | Verifier   | D05-HR-Verifiers | When Status='Submitted' — notify Verifier                          |
| 3     | Endorse / Reject  | Endorser   | D05-HR-Endorsers | When Status='Verification' and Verifier approves — notify Endorser |
| 4     | Final Approve/Rej | Approver   | D05-HR-Approvers | When Status='Endorsement' and Endorser approves — notify Approver  |
| 5     | Close             | System     | —                | When Approver approves → assign OrgNum, IsLocked=Yes, archive      |

---

## Role Matrix

| Domino Group    | SharePoint Group | SP Group Name    | Permissions    |
| --------------- | ---------------- | ---------------- | -------------- |
| HR Admins       | HR Staff         | D05-HR-Staff     | Contribute     |
| Verifiers group | HR Verifiers     | D05-HR-Verifiers | Read + Approve |
| Endorsers group | HR Endorsers     | D05-HR-Endorsers | Read + Approve |
| Approvers group | HR Approvers     | D05-HR-Approvers | Read + Approve |
| HR Manager      | HR Manager       | D05-HR-Manager   | Full Control   |

---

## Power Automate Actions

| Flow Name                    | Trigger                                          | Action                                                                           |
| ---------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------- |
| HR_ORGCHART_OnSubmit         | When Status='Draft' → item submitted             | Stamp dtSubmitted, set Stage=2, notify Verifier group                            |
| HR_ORGCHART_VerifierDecision | When Status='Submitted' and Verifier responds    | If Verify: set Stage=3, notify Endorser; if Reject: return to Draft + notify HR  |
| HR_ORGCHART_EndorserDecision | When Status='Verification' and Endorser responds | If Endorse: set Stage=4, notify Approver; if Reject: return to Draft + notify HR |
| HR_ORGCHART_ApproverDecision | When Status='Endorsement' and Approver responds  | If Approve: assign OrgNum, IsLocked=Yes, Status=Approved; if Reject: → Draft     |

---

## Screen Inventory

| Screen Name      | Type      | Purpose                                                     | Visible To                   |
| ---------------- | --------- | ----------------------------------------------------------- | ---------------------------- |
| ORGCHART_List    | Gallery   | List all ORGCHART records with department and status filter | D05-HR-Staff, D05-HR-Manager |
| ORGCHART_New     | Form      | Create new org chart submission with attachment upload      | D05-HR-Staff                 |
| ORGCHART_View    | Read-only | View full record with all approval stages and attachments   | All roles (own dept or HR)   |
| ORGCHART_Edit    | Form      | Edit draft before submission                                | D05-HR-Staff (creator)       |
| ORGCHART_Verify  | Approval  | Verifier review screen                                      | D05-HR-Verifiers             |
| ORGCHART_Endorse | Approval  | Endorser review screen                                      | D05-HR-Endorsers             |
| ORGCHART_Approve | Approval  | Final approver screen                                       | D05-HR-Approvers             |

---

## Navigation Map

```
ORGCHART_List → [New] → ORGCHART_New
ORGCHART_List → [View] → ORGCHART_View
ORGCHART_List → [Edit] → ORGCHART_Edit (Draft only)
ORGCHART_View → [Verify] → ORGCHART_Verify (Verifier at Stage 2)
ORGCHART_View → [Endorse] → ORGCHART_Endorse (Endorser at Stage 3)
ORGCHART_View → [Approve] → ORGCHART_Approve (Approver at Stage 4)
```

---

## Migration Risks & Notes

1. **4-level approval chain complexity:** This is the most complex approval chain in the HR module.
   Each stage must be strictly gated — Endorser cannot act before Verifier, Approver cannot act
   before Endorser. Power Automate conditions must check prior stage completion before advancing.

2. **Attachment handling (org chart files):** The org chart document is the primary deliverable.
   Attachment handling in SharePoint must support file upload (not link). Use SharePoint
   `Attachments` column or a separate document library linked via lookup. Risk: file size limits for
   large org chart PDFs/Visio files.

3. **Verifier/Endorser/Approver group provisioning:** Three distinct SP groups (D05-HR-Verifiers,
   D05-HR-Endorsers, D05-HR-Approvers) must be provisioned at the SharePoint site level. These may
   not exist today — HR to supply group membership lists during provisioning.

4. **OrgNum assignment:** OrgNum is assigned by system on final approval. Define the numbering
   format with HR before Craftsman build: suggested `ORGCHART-{Year}-{Seq}`.

5. **Rejection flow returns to Draft:** All 3 levels can reject. On rejection at any stage, the form
   returns to Draft status and notifies the original submitter with the approver's designation and
   remarks. Implement `DraftRemarks` field update at each rejection point.

---

## v3 Impossibilities

| Domino Feature                                | v3 Status  | Workaround                                                                   |
| --------------------------------------------- | ---------- | ---------------------------------------------------------------------------- |
| 4-level sequential approval with named stamps | LIMITED    | Power Automate 4-step sequential flows; name+designation captured in columns |
| Auto-number OrgNum on approval                | NOT NATIVE | PA flow generates OrgNum using counter pattern on approval                   |
| Attachment version control                    | NOT NATIVE | SharePoint library versioning on document library; or rename on resubmit     |

---

## Reference PDF

| Field          | Value                                                                                                                                                                                                                                                             |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/ORGCHART.pdf                                                                                                                                                                                                        |
| Page Count     | 5                                                                                                                                                                                                                                                                 |
| Field Evidence | Status, OrgChartNum, div, dept, sect, pic, ret, attach, attach_1, prepared/verified/endorsed/approved by name/designation/date, DraftSubBy, dtSubmitted, rbChangesRequired, DraftRemarks, DraftRevBy, OrgSelection, Changes, HRRem, OrgNum — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (35 columns) numbered, typed, classified, Domino-mapped
- [x] No child tables required (all approval stage fields captured in parent list)
- [x] Workflow Stage Map: ASCII diagram + formal trigger-condition table (4-level approval)
- [x] Role Matrix: all 5 roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 4 flows named with HR*ORGCHART*[EventName] convention
- [x] Screen Inventory: 7 screens listed with visibility rules
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
**Blueprint:** ORGCHART (HR)  
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
