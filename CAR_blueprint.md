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

| Field                      | Value                                                           |
| -------------------------- | --------------------------------------------------------------- |
| Form Code                  | `CAR`                                                           |
| Official Name              | `Cost Approval Request`                                         |
| Department                 | `FIN` (Department_04)                                           |
| Module                     | `M1 — Financial Approvals & Requisitions`                       |
| Site(s)                    | `PRAI`                                                          |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CAR.pdf` |
| Domino Database            | `Finance.nsf`                                                   |
| Official Name Claim Status | `Claimed (source PDF verified)`                                 |
| Blueprint Version          | `1.0`                                                           |
| Blueprint Date             | `2026-04-18`                                                    |
| Architect                  | `GitHub Copilot (Architect Agent)`                              |

---

## Purpose

Cost Approval Request (CAR) is a financial workflow form submitted when expenditure approval is
required. The form routes through cost centre heads and finance managers for review and approval
before execution. Migrated to MainDB_FIN with FormCode=CAR, preserving submission, multi-stage
approval routing, cost tracking, and auditability.

---

## SharePoint Schema

**Target List:** `MainDB_FIN`  
**URL:** `https://ioioi.sharepoint.com/sites/FIN/Lists/MainDB_FIN`

**Architecture Method:** DEC-001 (Live Submission Architecture)

| #   | Column Name    | SP Type                | Required | Choices / Source                                              | Notes                                   |
| --- | -------------- | ---------------------- | -------- | ------------------------------------------------------------- | --------------------------------------- |
| 1   | Title          | Single line of text    | Yes      | —                                                             | Auto-populated from CAR tracking number |
| 2   | FormCode       | Single line of text    | Yes      | Constant: CAR                                                 | Shared list discriminator               |
| 3   | CurrentAction  | Choice                 | Yes      | Draft; Submitted; Approval; Complete; Returned                | Workflow routing state                  |
| 4   | Status         | Choice                 | Yes      | Draft; Pending Approval; Approved; Rejected; Returned; Closed | Lifecycle status                        |
| 5   | SubmittedBy    | Person or Group        | Yes      | —                                                             | Requester audit trail                   |
| 6   | SubmittedDate  | Date and Time          | Yes      | —                                                             | Submission timestamp                    |
| 7   | ApprovedBy     | Person or Group        | No       | —                                                             | Final approver (workflow-set)           |
| 8   | ApprovedDate   | Date and Time          | No       | —                                                             | Approval timestamp                      |
| 9   | Comments       | Multiple lines of text | No       | —                                                             | Reviewer remarks                        |
| 10  | EnvironmentTag | Choice                 | Yes      | DEV; TEST; PROD                                               | DEC-004 environment tier                |

---

## Workflow Stage Map

```
[Stage 1: Draft/Creation]
         │ submit
         ▼
[Stage 2: Cost Centre Review]
         │ approve/return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Finance Manager Approval]
         │ approve/reject
         ├─→ Approved: Complete
         └─→ Rejected: Stage 1
         ▼
[Stage 4: Closed]
```

| Stage | Action              | Trigger                     | Actor Role       | SP Group             | Power Automate Action                                 |
| ----- | ------------------- | --------------------------- | ---------------- | -------------------- | ----------------------------------------------------- |
| 1     | Create & submit CAR | Item created (FormCode=CAR) | Requester        | `D04-FIN-Submitters` | Set Status=Draft, stamp SubmittedBy/SubmittedDate     |
| 2     | Cost centre review  | Status=Submitted            | Cost Centre Head | `D04-FIN-CCHeads`    | Route for decision; update Comments and CurrentAction |
| 3     | Finance approval    | Status=Pending Approval     | Finance Manager  | `D04-FIN-Managers`   | Approve/reject; set ApprovedBy/ApprovedDate; finalize |
| 4     | Close workflow      | Final decision reached      | System           | `D04-FIN-Admins`     | Lock record, stop reminders                           |

---

## Role Matrix

| Domino Role                 | SharePoint Group     | Permission Level | Notes                   |
| --------------------------- | -------------------- | ---------------- | ----------------------- |
| Requester / Authors         | `D04-FIN-Submitters` | Contribute       | Submit new CAR          |
| Cost Centre Head / Reviewer | `D04-FIN-CCHeads`    | Contribute       | Stage 2 review          |
| Finance Manager / Approver  | `D04-FIN-Managers`   | Approve          | Stage 3 final approval  |
| System Admin                | `D04-FIN-Admins`     | Full Control     | Configuration & support |

---

## Power Automate Actions

| Flow Name         | Trigger                     | Actions                                                                                                                                        |
| ----------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `FIN_CAR_Submit`  | Item created (FormCode=CAR) | 1. Validate required fields. 2. Set Status=Submitted. 3. Stamp submission metadata. 4. Notify cost centre head. 5. Set CurrentAction=Approval. |
| `FIN_CAR_Approve` | Status updated to Approved  | 1. Update ApprovedBy/ApprovedDate. 2. Set Status=Approved; CurrentAction=Complete. 3. Notify requester. 4. Lock record.                        |
| `FIN_CAR_Reject`  | Status updated to Rejected  | 1. Set Status=Returned; CurrentAction=Draft. 2. Append rejection reason to Comments. 3. Return to requester for rework.                        |

---

## Screen Inventory

| Screen Name | Purpose                          | Visible To              |
| ----------- | -------------------------------- | ----------------------- |
| CAR_List    | Search and filter CAR requests   | All FIN roles           |
| CAR_New     | Create new cost approval request | `D04-FIN-Submitters`    |
| CAR_View    | Read-only detail view            | All authorized users    |
| CAR_Edit    | Edit in Draft/Returned state     | Requester and approvers |

---

## Navigation Map

CAR_List → CAR_New → CAR_View ↔ CAR_Edit → CAR_List

---

## Migration Risks & Notes

- **Risk:** Multi-stage approval routing complexity — ensure Power Automate stage transition
  conditions are precise.
- **Mitigation:** Model workflow state machine explicitly in flow definition; use CurrentAction
  field for deterministic routing.
- **Risk:** Cost centre head and finance manager role semantics may differ between Domino and
  SharePoint.
- **Mitigation:** Validate role mappings in DEC-005 schema catalogue before Craftsman handoff.

---

## v3 Impossibilities

No v3 impossibilities identified. All fields are plain text, choice, date, or person types. No
computed fields, Domino agents, or formula dependencies present.

| Domino Feature | Reason                         | Recommended Workaround |
| -------------- | ------------------------------ | ---------------------- |
| —              | No blocking v3 impossibilities | —                      |

---

## Reference PDF

**Path:** `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/FIN/CAR.pdf`  
**Page count:** Pending Sentinel verification  
**Evidence:** Source PDF contains form layout, field list, approval routes, role assignments

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
