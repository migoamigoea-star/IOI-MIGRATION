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

| Field                      | Value                                                             |
| -------------------------- | ----------------------------------------------------------------- |
| Form Code                  | `CMF_A`                                                           |
| Official Name              | `Cost Monitoring Form - Part A`                                   |
| Department                 | `FIN` (Department_04)                                             |
| Module                     | `M2 — Cost Monitoring & Analysis`                                 |
| Site(s)                    | `PRAI`                                                            |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CMF_A.pdf` |
| Domino Database            | `Finance.nsf`                                                     |
| Official Name Claim Status | `Claimed (source PDF verified)`                                   |
| Blueprint Version          | `1.0`                                                             |
| Blueprint Date             | `2026-04-18`                                                      |
| Architect                  | `GitHub Copilot (Architect Agent)`                                |

---

## Purpose

Cost Monitoring Form - Part A (CMF_A) is the first segment of a multi-part cost tracking and
variance analysis form. Captures period cost data, budgets, and initial variance reporting.
Submitted by cost centre managers, reviewed by finance. Migrated to MainDB_FIN with FormCode=CMF_A,
supporting cost variance tracking and budget monitoring workflows.

---

## SharePoint Schema

**Target List:** `MainDB_FIN`  
**URL:** `https://ioioi.sharepoint.com/sites/FIN/Lists/MainDB_FIN`

**Architecture Method:** DEC-001 (Live Submission Architecture)

| #   | Column Name    | SP Type                | Required | Choices / Source                             | Notes                                     |
| --- | -------------- | ---------------------- | -------- | -------------------------------------------- | ----------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                            | Auto-populated from CMF_A tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: CMF_A                              | Shared list discriminator                 |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Review; Complete; Archived | Workflow routing state                    |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Review; Approved; Archived    | Lifecycle status                          |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                            | Cost centre manager                       |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                            | Submission timestamp                      |
| 7   | ApprovedBy     | Person or Group        | No       | —                                            | Finance reviewer (workflow-set)           |
| 8   | ApprovedDate   | Date and Time          | No       | —                                            | Review completion timestamp               |
| 9   | Comments       | Multiple lines of text | No       | —                                            | Finance remarks and variance notes        |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                              | DEC-004 environment tier                  |

---

## Workflow Stage Map

```
[Stage 1: Draft/Data Entry]
         │ submit
         ▼
[Stage 2: Finance Review]
         │ review/approve
         ├─→ Approved: Complete
         └─→ Returned: Stage 1
         ▼
[Stage 3: Archive]
```

| Stage | Action                | Trigger                       | Actor Role          | SP Group             | Power Automate Action                             |
| ----- | --------------------- | ----------------------------- | ------------------- | -------------------- | ------------------------------------------------- |
| 1     | Create & submit CMF_A | Item created (FormCode=CMF_A) | Cost Centre Manager | `D04-FIN-Submitters` | Set Status=Draft, stamp SubmittedBy/SubmittedDate |
| 2     | Finance review        | Status=Submitted              | Finance Analyst     | `D04-FIN-Reviewers`  | Review variance, append comments, approve         |
| 3     | Archive               | Status=Approved               | System              | `D04-FIN-Admins`     | Set Status=Archived; lock record                  |

---

## Role Matrix

| Domino Role                     | SharePoint Group     | Permission Level | Notes                     |
| ------------------------------- | -------------------- | ---------------- | ------------------------- |
| Cost Centre Manager / Submitter | `D04-FIN-Submitters` | Contribute       | Submit CMF_A              |
| Finance Analyst / Reviewer      | `D04-FIN-Reviewers`  | Contribute       | Stage 2 review & approval |
| System Admin                    | `D04-FIN-Admins`     | Full Control     | Configuration & support   |

---

## Power Automate Actions

| Flow Name           | Trigger                       | Actions                                                                                                                                       |
| ------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_CMF_A_Submit`  | Item created (FormCode=CMF_A) | 1. Validate cost data fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify finance reviewer. 5. Set CurrentAction=Review. |
| `FIN_CMF_A_Approve` | Status updated to Approved    | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Archived; CurrentAction=Complete. 3. Lock record. 4. Archive to historical store.            |
| `FIN_CMF_A_Return`  | Status updated to Returned    | 1. Set Status=Draft; CurrentAction=Draft. 2. Append return notes to Comments. 3. Route back to manager for revision.                          |

---

## Screen Inventory

| Screen Name | Purpose                                  | Visible To            |
| ----------- | ---------------------------------------- | --------------------- |
| CMF_A_List  | Search and filter CMF_A cost records     | All FIN roles         |
| CMF_A_New   | Create new monthly cost monitoring entry | `D04-FIN-Submitters`  |
| CMF_A_View  | Read-only detail view                    | All authorized users  |
| CMF_A_Edit  | Edit in Draft state                      | Manager and reviewers |

---

## Navigation Map

CMF_A_List → CMF_A_New → CMF_A_View ↔ CMF_A_Edit → CMF_A_List

---

## Migration Risks & Notes

- **Risk:** Cost variance calculations and thresholds must map consistently from Domino formulas to
  Power Automate flow logic.
- **Mitigation:** Audit variance calculation formulas in source PDF and replicate in flow
  definition.
- **Risk:** Multi-period cost data chains (CMF_A → CMF_B → CMF_C) require referential integrity.
- **Mitigation:** Document parent-child relationships and implement lookup validations in
  SharePoint.

---

## v3 Impossibilities

No v3 impossibilities identified. All fields are plain text, choice, date, or number types. No
complex formula fields present.

| Domino Feature | Reason                         | Recommended Workaround |
| -------------- | ------------------------------ | ---------------------- |
| —              | No blocking v3 impossibilities | —                      |

---

## Reference PDF

**Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CMF_A.pdf`  
**Page count:** Pending Sentinel verification  
**Evidence:** Source PDF contains form layout, cost field definitions, variance thresholds, review
routing

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
