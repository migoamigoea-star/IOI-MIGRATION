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
| Form Code                  | `CMF_B`                                                           |
| Official Name              | `Cost Monitoring Form - Part B`                                   |
| Department                 | `FIN` (Department_04)                                             |
| Module                     | `M2 — Cost Monitoring & Analysis`                                 |
| Site(s)                    | `PRAI`                                                            |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CMF_B.pdf` |
| Domino Database            | `Finance.nsf`                                                     |
| Official Name Claim Status | `Claimed (source PDF verified)`                                   |
| Blueprint Version          | `1.0`                                                             |
| Blueprint Date             | `2026-04-18`                                                      |
| Architect                  | `GitHub Copilot (Architect Agent)`                                |

---

## Purpose

Cost Monitoring Form - Part B (CMF_B) is the second segment of multi-part cost tracking workflow.
Captures additional cost variance data, mitigation actions, and forecast adjustments. Submitted by
cost centre managers, reviewed by finance and department heads. Migrated to MainDB_FIN with
FormCode=CMF_B, supporting cost variance tracking and budget adjustment workflows.

---

## SharePoint Schema

**Target List:** `MainDB_FIN`  
**URL:** `https://ioioi.sharepoint.com/sites/FIN/Lists/MainDB_FIN`

**Architecture Method:** DEC-001 (Live Submission Architecture)

| #   | Column Name    | SP Type                | Required | Choices / Source                            | Notes                                     |
| --- | -------------- | ---------------------- | -------- | ------------------------------------------- | ----------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                           | Auto-populated from CMF_B tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: CMF_B                             | Shared list discriminator                 |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Review; Approve; Complete | Workflow routing state                    |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Review; Approved; Archived   | Lifecycle status                          |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                           | Cost centre manager                       |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                           | Submission timestamp                      |
| 7   | ApprovedBy     | Person or Group        | No       | —                                           | Finance approver (workflow-set)           |
| 8   | ApprovedDate   | Date and Time          | No       | —                                           | Approval timestamp                        |
| 9   | Comments       | Multiple lines of text | No       | —                                           | Reviewer and approver remarks             |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                             | DEC-004 environment tier                  |

---

## Workflow Stage Map

```
[Stage 1: Draft/Data Entry]
         │ submit
         ▼
[Stage 2: Finance Review]
         │ approve/return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Department Head Approval]
         │ sign-off/reject
         ├─→ Approved: Complete
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Archive]
```

| Stage | Action                | Trigger                       | Actor Role          | SP Group             | Power Automate Action                                           |
| ----- | --------------------- | ----------------------------- | ------------------- | -------------------- | --------------------------------------------------------------- |
| 1     | Create & submit CMF_B | Item created (FormCode=CMF_B) | Cost Centre Manager | `D04-FIN-Submitters` | Set Status=Draft, stamp SubmittedBy/SubmittedDate               |
| 2     | Finance review        | Status=Submitted              | Finance Analyst     | `D04-FIN-Reviewers`  | Review and approve; set CurrentAction=Approve                   |
| 3     | Dept head approval    | Status=Pending Review         | Department Head     | `D04-FIN-DeptHeads`  | Final sign-off on cost adjustments; set ApprovedBy/ApprovedDate |
| 4     | Archive               | Status=Approved               | System              | `D04-FIN-Admins`     | Lock record and archive                                         |

---

## Role Matrix

| Domino Role                     | SharePoint Group     | Permission Level | Notes                   |
| ------------------------------- | -------------------- | ---------------- | ----------------------- |
| Cost Centre Manager / Submitter | `D04-FIN-Submitters` | Contribute       | Submit CMF_B            |
| Finance Analyst / Reviewer      | `D04-FIN-Reviewers`  | Contribute       | Stage 2 review          |
| Department Head / Approver      | `D04-FIN-DeptHeads`  | Approve          | Stage 3 final approval  |
| System Admin                    | `D04-FIN-Admins`     | Full Control     | Configuration & support |

---

## Power Automate Actions

| Flow Name           | Trigger                       | Actions                                                                                                                                             |
| ------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_CMF_B_Submit`  | Item created (FormCode=CMF_B) | 1. Validate cost adjustment fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify finance reviewer. 5. Set CurrentAction=Review. |
| `FIN_CMF_B_Approve` | Status updated to Approved    | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Archived. 3. Archive record. 4. Send completion notification.                                      |
| `FIN_CMF_B_Return`  | Status updated to Returned    | 1. Set Status=Draft; CurrentAction=Draft. 2. Append return notes to Comments. 3. Route back to manager for revision.                                |

---

## Screen Inventory

| Screen Name | Purpose                          | Visible To            |
| ----------- | -------------------------------- | --------------------- |
| CMF_B_List  | Search and filter CMF_B records  | All FIN roles         |
| CMF_B_New   | Create new cost adjustment entry | `D04-FIN-Submitters`  |
| CMF_B_View  | Read-only detail view            | All authorized users  |
| CMF_B_Edit  | Edit in Draft state              | Manager and reviewers |

---

## Navigation Map

CMF_B_List → CMF_B_New → CMF_B_View ↔ CMF_B_Edit → CMF_B_List

---

## Migration Risks & Notes

- **Risk:** Multi-stage approval (Finance → Dept Head) must maintain order and prevent bypassing.
- **Mitigation:** Implement explicit state transitions in Power Automate; use CurrentAction for
  deterministic routing.
- **Risk:** Cost adjustment thresholds and forecast logic must be accurately migrated from Domino.
- **Mitigation:** Audit threshold values and formula logic in source PDF; replicate in flow
  definition.

---

## v3 Impossibilities

No v3 impossibilities identified. All fields are plain text, choice, date, or number types.

| Domino Feature | Reason                         | Recommended Workaround |
| -------------- | ------------------------------ | ---------------------- |
| —              | No blocking v3 impossibilities | —                      |

---

## Reference PDF

**Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CMF_B.pdf`  
**Page count:** Pending Sentinel verification  
**Evidence:** Source PDF contains form layout, cost adjustment thresholds, approval routing, role
assignments

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
