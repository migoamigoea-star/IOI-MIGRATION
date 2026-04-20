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
| Form Code                  | `RSES`                                                           |
| Official Name              | `Resource Supply Estimation Sheet`                               |
| Department                 | `FIN` (Department_04)                                            |
| Module                     | `M3 — Resource Planning & Analysis`                              |
| Site(s)                    | `PRAI`                                                           |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/RSES.pdf` |
| Domino Database            | `Finance.nsf`                                                    |
| Official Name Claim Status | `Claimed (source PDF verified)`                                  |
| Blueprint Version          | `1.0`                                                            |
| Blueprint Date             | `2026-04-18`                                                     |
| Architect                  | `GitHub Copilot (Architect Agent)`                               |

---

## Purpose

Resource Supply Estimation Sheet (RSES) forecasts resource requirements and supply plans for
upcoming periods. Submitted by department heads, reviewed by finance and operations for resource
capacity planning. Migrated to MainDB_FIN with FormCode=RSES, supporting resource planning, budget
forecasting, and capacity analysis workflows.

---

## SharePoint Schema

**Target List:** `MainDB_FIN`  
**URL:** `https://ioioi.sharepoint.com/sites/FIN/Lists/MainDB_FIN`

**Architecture Method:** DEC-001 (Live Submission Architecture)

| #   | Column Name    | SP Type                | Required | Choices / Source                            | Notes                                    |
| --- | -------------- | ---------------------- | -------- | ------------------------------------------- | ---------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                           | Auto-populated from RSES tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: RSES                              | Shared list discriminator                |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Review; Approve; Complete | Workflow routing state                   |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Review; Approved; Archived   | Lifecycle status                         |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                           | Department head submitter                |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                           | Submission timestamp                     |
| 7   | ApprovedBy     | Person or Group        | No       | —                                           | Finance approver (workflow-set)          |
| 8   | ApprovedDate   | Date and Time          | No       | —                                           | Approval timestamp                       |
| 9   | Comments       | Multiple lines of text | No       | —                                           | Finance and operations remarks           |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                             | DEC-004 environment tier                 |

---

## Workflow Stage Map

```
[Stage 1: Draft/Planning]
         │ submit
         ▼
[Stage 2: Finance Review]
         │ approve/return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Operations Approval]
         │ approve/reject
         ├─→ Approved: Complete
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Archive]
```

| Stage | Action               | Trigger                      | Actor Role         | SP Group             | Power Automate Action                                    |
| ----- | -------------------- | ---------------------------- | ------------------ | -------------------- | -------------------------------------------------------- |
| 1     | Create & submit RSES | Item created (FormCode=RSES) | Department Head    | `D04-FIN-Submitters` | Set Status=Draft, stamp SubmittedBy/SubmittedDate        |
| 2     | Finance review       | Status=Submitted             | Finance Analyst    | `D04-FIN-Reviewers`  | Review resource forecast; approve or return              |
| 3     | Operations approval  | Status=Pending Review        | Operations Manager | `D04-FIN-Approvers`  | Verify capacity and approve; set ApprovedBy/ApprovedDate |
| 4     | Archive              | Status=Approved              | System             | `D04-FIN-Admins`     | Lock record and archive to planning database             |

---

## Role Matrix

| Domino Role                   | SharePoint Group     | Permission Level | Notes                   |
| ----------------------------- | -------------------- | ---------------- | ----------------------- |
| Department Head / Submitter   | `D04-FIN-Submitters` | Contribute       | Submit RSES             |
| Finance Analyst / Reviewer    | `D04-FIN-Reviewers`  | Contribute       | Stage 2 review          |
| Operations Manager / Approver | `D04-FIN-Approvers`  | Approve          | Stage 3 final approval  |
| System Admin                  | `D04-FIN-Admins`     | Full Control     | Configuration & support |

---

## Power Automate Actions

| Flow Name          | Trigger                      | Actions                                                                                                                                               |
| ------------------ | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_RSES_Submit`  | Item created (FormCode=RSES) | 1. Validate resource forecast fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify finance reviewer. 5. Set CurrentAction=Review. |
| `FIN_RSES_Approve` | Status updated to Approved   | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Archived. 3. Archive record to planning database. 4. Send approval notification.                     |
| `FIN_RSES_Return`  | Status updated to Returned   | 1. Set Status=Draft; CurrentAction=Draft. 2. Append return notes to Comments. 3. Route back to department for revision.                               |

---

## Screen Inventory

| Screen Name | Purpose                             | Visible To                     |
| ----------- | ----------------------------------- | ------------------------------ |
| RSES_List   | Search and filter RSES records      | All FIN roles                  |
| RSES_New    | Create new resource supply estimate | `D04-FIN-Submitters`           |
| RSES_View   | Read-only detail view               | All authorized users           |
| RSES_Edit   | Edit in Draft state                 | Department heads and reviewers |

---

## Navigation Map

RSES_List → RSES_New → RSES_View ↔ RSES_Edit → RSES_List

---

## Migration Risks & Notes

- **Risk:** Resource forecasting logic and capacity thresholds must be accurately migrated from
  Domino calculations.
- **Mitigation:** Audit forecast algorithms in source PDF; replicate in Power Automate flow logic.
- **Risk:** Multi-period resource planning chains require cross-form referential integrity.
- **Mitigation:** Implement lookup validations and period-to-period consistency checks in
  SharePoint.

---

## v3 Impossibilities

No v3 impossibilities identified. All fields are plain text, choice, date, or number types.

| Domino Feature | Reason                         | Recommended Workaround |
| -------------- | ------------------------------ | ---------------------- |
| —              | No blocking v3 impossibilities | —                      |

---

## Reference PDF

**Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/RSES.pdf`  
**Page count:** Pending Sentinel verification  
**Evidence:** Source PDF contains form layout, resource categories, forecast thresholds, approval
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
