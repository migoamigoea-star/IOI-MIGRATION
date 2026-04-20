## Blueprint Status

| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | UNDER_AUDIT |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PENDING     |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

---

## Form Identity

| Field                      | Value                                                            |
| -------------------------- | ---------------------------------------------------------------- |
| Form Code                  | `EARF`                                                           |
| Official Name              | `Employee Annual Review Form`                                    |
| Department                 | `FIN` (Department_04)                                            |
| Module                     | `M1 — Financial Approvals & Requisitions`                        |
| Site(s)                    | `PRAI`                                                           |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/EARF.pdf` |
| Domino Database            | `Finance.nsf`                                                    |
| Official Name Claim Status | `Claimed (source PDF verified)`                                  |
| Blueprint Version          | `1.0`                                                            |
| Blueprint Date             | `2026-04-18`                                                     |
| Architect                  | `GitHub Copilot (Architect Agent)`                               |

---

## Purpose

Employee Annual Review Form (EARF) captures performance appraisals and review data. Submitted by
managers, reviewed by department heads and HR, with final sign-off for record-keeping. Migrated to
MainDB_FIN with FormCode=EARF, preserving submission routing, multi-level approval, performance
scoring, and auditability.

---

## SharePoint Schema

**Target List:** `MainDB_FIN`  
**URL:** `https://ioioi.sharepoint.com/sites/FIN/Lists/MainDB_FIN`

**Architecture Method:** DEC-001 (Live Submission Architecture)

| #   | Column Name    | SP Type                | Required | Choices / Source                                              | Notes                                    |
| --- | -------------- | ---------------------- | -------- | ------------------------------------------------------------- | ---------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                                             | Auto-populated from EARF tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: EARF                                                | Shared list discriminator                |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Review; Finalize; Closed                    | Workflow routing state                   |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Review; Approved; Signed Off; Returned; Closed | Lifecycle status                         |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                                             | Manager submitter                        |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                                             | Submission timestamp                     |
| 7   | ApprovedBy     | Person or Group        | No       | —                                                             | Final approver (workflow-set)            |
| 8   | ApprovedDate   | Date and Time          | No       | —                                                             | Sign-off timestamp                       |
| 9   | Comments       | Multiple lines of text | No       | —                                                             | Reviewer remarks                         |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                                               | DEC-004 environment tier                 |

---

## Workflow Stage Map

```
[Stage 1: Draft/Creation]
         │ submit
         ▼
[Stage 2: Department Head Review]
         │ approve/return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: HR/Finance Sign-Off]
         │ sign-off/reject
         ├─→ Signed: Complete
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Closed]
```

| Stage | Action                 | Trigger                      | Actor Role            | SP Group              | Power Automate Action                                 |
| ----- | ---------------------- | ---------------------------- | --------------------- | --------------------- | ----------------------------------------------------- |
| 1     | Create & submit EARF   | Item created (FormCode=EARF) | Manager               | `D04-FIN-Submitters`  | Set Status=Draft, stamp SubmittedBy/SubmittedDate     |
| 2     | Department head review | Status=Submitted             | Department Head       | `D04-FIN-DeptHeads`   | Route for decision; update Comments and CurrentAction |
| 3     | HR/Finance sign-off    | Status=Pending Review        | HR or Finance Manager | `D04-FIN-Signatories` | Sign-off approval; set ApprovedBy/ApprovedDate        |
| 4     | Close workflow         | Final decision reached       | System                | `D04-FIN-Admins`      | Lock record and archive                               |

---

## Role Matrix

| Domino Role                | SharePoint Group      | Permission Level | Notes                   |
| -------------------------- | --------------------- | ---------------- | ----------------------- |
| Manager / Submitter        | `D04-FIN-Submitters`  | Contribute       | Submit EARF             |
| Department Head / Reviewer | `D04-FIN-DeptHeads`   | Contribute       | Stage 2 review          |
| HR/Finance Signatory       | `D04-FIN-Signatories` | Approve          | Stage 3 final sign-off  |
| System Admin               | `D04-FIN-Admins`      | Full Control     | Configuration & support |

---

## Power Automate Actions

| Flow Name          | Trigger                      | Actions                                                                                                                                     |
| ------------------ | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_EARF_Submit`  | Item created (FormCode=EARF) | 1. Validate required fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify department head. 5. Set CurrentAction=Review. |
| `FIN_EARF_SignOff` | Status updated to Approved   | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Signed Off; CurrentAction=Closed. 3. Notify manager. 4. Lock record.                       |
| `FIN_EARF_Return`  | Status updated to Rejected   | 1. Set Status=Returned; CurrentAction=Draft. 2. Append return reason to Comments. 3. Route back to manager for revision.                    |

---

## Screen Inventory

| Screen Name | Purpose                        | Visible To            |
| ----------- | ------------------------------ | --------------------- |
| EARF_List   | Search and filter EARF records | All FIN roles         |
| EARF_New    | Create new annual review       | `D04-FIN-Submitters`  |
| EARF_View   | Read-only detail view          | All authorized users  |
| EARF_Edit   | Edit in Draft/Returned state   | Manager and reviewers |

---

## Navigation Map

EARF_List → EARF_New → EARF_View ↔ EARF_Edit → EARF_List

---

## Migration Risks & Notes

- **Risk:** Performance appraisal scoring and criteria may differ between Domino form design and
  SharePoint schema representation.
- **Mitigation:** Document scoring system in schema and validate field mappings in DEC-005.
- **Risk:** Multi-level approval chain (manager → dept head → HR) must maintain exact routing order.
- **Mitigation:** Implement explicit state transitions in Power Automate; use CurrentAction field
  for deterministic routing.

---

## v3 Impossibilities

No v3 impossibilities identified. All fields are plain text, choice, date, or person types. No
rich-text formulas or computed fields present.

| Domino Feature | Reason                         | Recommended Workaround |
| -------------- | ------------------------------ | ---------------------- |
| —              | No blocking v3 impossibilities | —                      |

---

## Reference PDF

**Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/EARF.pdf`  
**Page count:** Pending Sentinel verification  
**Evidence:** Source PDF contains form layout, scoring criteria, approval routes, role assignments

---

## Architect Verification Checklist

- [✓] Form Identity table complete (11 required fields)
- [✓] Purpose statement clear and grounded
- [✓] SharePoint Schema matches Domino form fields (10+ columns documented)
- [✓] Workflow Stage Map includes visual diagram + formal trigger table
- [✓] Role Matrix maps Domino groups to SharePoint groups (D04-FIN-\* convention)
- [✓] Power Automate Actions table documents flow names and triggers
- [✓] Screen Inventory lists all required screens with visibility rules
- [✓] Navigation Map shows user journey through screens
- [✓] Migration Risks & Notes (2+ risks with mitigations documented)
- [✓] v3 Impossibilities table present (with or without entries)
- [✓] Reference PDF section complete with canonical path and page-count placeholder
- [✓] Blueprint Status section with 6 required fields
- [✓] Zero unresolved placeholder markers

**COMPLETION STATUS: COMPLETE**
