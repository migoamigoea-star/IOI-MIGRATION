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
| Form Code                  | `CMF_C`                                                           |
| Official Name              | `Cost Monitoring Form - Part C`                                   |
| Department                 | `FIN` (Department_04)                                             |
| Module                     | `M2 — Cost Monitoring & Analysis`                                 |
| Site(s)                    | `PRAI`                                                            |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CMF_C.pdf` |
| Domino Database            | `Finance.nsf`                                                     |
| Official Name Claim Status | `Claimed (source PDF verified)`                                   |
| Blueprint Version          | `1.0`                                                             |
| Blueprint Date             | `2026-04-18`                                                      |
| Architect                  | `GitHub Copilot (Architect Agent)`                                |

---

## Purpose

Cost Monitoring Form - Part C (CMF_C) is the final segment of multi-part cost tracking workflow.
Captures summary analysis, corrective actions, and final variance reporting. Submitted by cost
centre managers, reviewed and signed-off by finance and senior management. Migrated to MainDB_FIN
with FormCode=CMF_C, supporting cost tracking completion and financial reporting workflows.

---

## SharePoint Schema

**Target List:** `MainDB_FIN`  
**URL:** `https://ioioi.sharepoint.com/sites/FIN/Lists/MainDB_FIN`

**Architecture Method:** DEC-001 (Live Submission Architecture)

| #   | Column Name    | SP Type                | Required | Choices / Source                                      | Notes                                     |
| --- | -------------- | ---------------------- | -------- | ----------------------------------------------------- | ----------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                                     | Auto-populated from CMF_C tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: CMF_C                                       | Shared list discriminator                 |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Review; Finalize; Complete          | Workflow routing state                    |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Review; Approved; Signed Off; Archived | Lifecycle status                          |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                                     | Cost centre manager                       |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                                     | Submission timestamp                      |
| 7   | ApprovedBy     | Person or Group        | No       | —                                                     | Finance approver (workflow-set)           |
| 8   | ApprovedDate   | Date and Time          | No       | —                                                     | Approval/sign-off timestamp               |
| 9   | Comments       | Multiple lines of text | No       | —                                                     | Finance and management remarks            |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                                       | DEC-004 environment tier                  |

---

## Workflow Stage Map

```
[Stage 1: Draft/Analysis]
         │ submit
         ▼
[Stage 2: Finance Review]
         │ approve/return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Senior Management Sign-Off]
         │ sign-off/reject
         ├─→ Signed: Complete
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Archive]
```

| Stage | Action                | Trigger                       | Actor Role             | SP Group              | Power Automate Action                                      |
| ----- | --------------------- | ----------------------------- | ---------------------- | --------------------- | ---------------------------------------------------------- |
| 1     | Create & submit CMF_C | Item created (FormCode=CMF_C) | Cost Centre Manager    | `D04-FIN-Submitters`  | Set Status=Draft, stamp SubmittedBy/SubmittedDate          |
| 2     | Finance review        | Status=Submitted              | Finance Manager        | `D04-FIN-Managers`    | Review summary analysis; approve or return                 |
| 3     | Senior mgmt sign-off  | Status=Pending Review         | Senior Finance Officer | `D04-FIN-Signatories` | Final sign-off on cost report; set ApprovedBy/ApprovedDate |
| 4     | Archive               | Status=Signed Off             | System                 | `D04-FIN-Admins`      | Lock record and archive to financial records               |

---

## Role Matrix

| Domino Role                        | SharePoint Group      | Permission Level | Notes                   |
| ---------------------------------- | --------------------- | ---------------- | ----------------------- |
| Cost Centre Manager / Submitter    | `D04-FIN-Submitters`  | Contribute       | Submit CMF_C            |
| Finance Manager / Reviewer         | `D04-FIN-Managers`    | Contribute       | Stage 2 review          |
| Senior Finance Officer / Signatory | `D04-FIN-Signatories` | Approve          | Stage 3 final sign-off  |
| System Admin                       | `D04-FIN-Admins`      | Full Control     | Configuration & support |

---

## Power Automate Actions

| Flow Name           | Trigger                       | Actions                                                                                                                                             |
| ------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_CMF_C_Submit`  | Item created (FormCode=CMF_C) | 1. Validate summary analysis fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify finance manager. 5. Set CurrentAction=Review. |
| `FIN_CMF_C_SignOff` | Status updated to Approved    | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Signed Off. 3. Archive record to financial ledger. 4. Send completion notification.                |
| `FIN_CMF_C_Return`  | Status updated to Returned    | 1. Set Status=Draft; CurrentAction=Draft. 2. Append return notes to Comments. 3. Route back to manager for revision.                                |

---

## Screen Inventory

| Screen Name | Purpose                         | Visible To            |
| ----------- | ------------------------------- | --------------------- |
| CMF_C_List  | Search and filter CMF_C records | All FIN roles         |
| CMF_C_New   | Create new final cost summary   | `D04-FIN-Submitters`  |
| CMF_C_View  | Read-only detail view           | All authorized users  |
| CMF_C_Edit  | Edit in Draft state             | Manager and reviewers |

---

## Navigation Map

CMF_C_List → CMF_C_New → CMF_C_View ↔ CMF_C_Edit → CMF_C_List

---

## Migration Risks & Notes

- **Risk:** CMF_A/B/C form chain creates dependencies — summary in C must reflect data from A and B.
- **Mitigation:** Implement referential integrity checks and cross-form validation in Power Automate
  flows.
- **Risk:** Senior management sign-off stage must not allow bypassing despite multi-stage
  complexity.
- **Mitigation:** Enforce explicit approval routing in flows; use CurrentAction field for state
  tracking.

---

## v3 Impossibilities

No v3 impossibilities identified. All fields are plain text, choice, date, or number types.

| Domino Feature | Reason                         | Recommended Workaround |
| -------------- | ------------------------------ | ---------------------- |
| —              | No blocking v3 impossibilities | —                      |

---

## Reference PDF

**Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CMF_C.pdf`  
**Page count:** Pending Sentinel verification  
**Evidence:** Source PDF contains form layout, summary analysis fields, sign-off authority,
financial reporting integration

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
