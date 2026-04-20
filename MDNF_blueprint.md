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
| Form Code                  | `MDNF`                                                           |
| Official Name              | `Material Disposal Notification Form`                            |
| Department                 | `STR (Department_13_STR)`                                        |
| Module                     | `M2 - Material Disposal`                                         |
| Site(s)                    | `PRAI`                                                           |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/MDNF.pdf` |
| Domino Database            | `PRAI_DB_Design_Original_File/STR`                               |
| Official Name Claim Status | `Claimed`                                                        |
| Blueprint Version          | `1.1`                                                            |
| Blueprint Date             | `2026-04-18`                                                     |
| Architect                  | `GitHub Copilot (Architect mode)`                                |

---

## Purpose

MDNF governs end-to-end material disposal from request initiation through procurement, collection,
finance completion, and controlled withdrawal closure. The migration preserves attributable
approvals, evidence capture, and auditable state transitions for disposal actions that affect
inventory and financial traceability.

## SharePoint Schema

**Target List:** `MainDB_STR`  
**Form Discriminator:** `FormCode = "MDNF"`

### Parent List: MainDB_STR

| #   | SP Internal Name     | Display Label          | Column Type     | Required | Classification   | Notes                                                                 |
| --- | -------------------- | ---------------------- | --------------- | -------- | ---------------- | --------------------------------------------------------------------- |
| 1   | FormCode             | Form Code              | Single line     | Yes      | SYSTEM-COMPUTED  | Fixed `MDNF`                                                          |
| 2   | INO                  | Disposal Ref No        | Single line     | Yes      | SYSTEM-COMPUTED  | Format `STR-MDNF-YYMM-NNNN` via flow                                  |
| 3   | CurrentStatus        | Workflow Status        | Choice          | Yes      | WORKFLOW-MANAGED | Draft, Submitted, Procurement, Collection, Finance, Closed, Withdrawn |
| 4   | CurrentAction        | Current Action         | Choice          | Yes      | WORKFLOW-MANAGED | Submit, Review, Approve, Complete, Withdraw                           |
| 5   | RequestDate          | Request Date           | Date and Time   | Yes      | USER-ENTERED     | Disposal request date                                                 |
| 6   | Requestor            | Requestor              | Person or Group | Yes      | USER-ENTERED     | Disposal initiator                                                    |
| 7   | RequestDept          | Requesting Department  | Single line     | Yes      | USER-ENTERED     | Origin department                                                     |
| 8   | ItemDescription      | Item Description       | Multiple lines  | Yes      | USER-ENTERED     | Material/item being disposed                                          |
| 9   | QtyToDispose         | Quantity to Dispose    | Number          | Yes      | USER-ENTERED     | Disposal quantity                                                     |
| 10  | DisposalReason       | Disposal Reason        | Multiple lines  | Yes      | USER-ENTERED     | Reason/justification                                                  |
| 11  | ProcurementAction    | Procurement Action     | Multiple lines  | No       | WORKFLOW-MANAGED | Buyer/procurement details                                             |
| 12  | CollectionDate       | Collection Date        | Date and Time   | No       | WORKFLOW-MANAGED | Disposal collection evidence                                          |
| 13  | FinanceStatus        | Finance Status         | Choice          | No       | WORKFLOW-MANAGED | Pending, Completed                                                    |
| 14  | FinanceCompletedDate | Finance Completed Date | Date and Time   | No       | WORKFLOW-MANAGED | Finance closure timestamp                                             |
| 15  | WithdrawalFlag       | Withdrawal Flag        | Yes/No          | No       | WORKFLOW-MANAGED | Indicates withdrawn request                                           |
| 16  | WithdrawalReason     | Withdrawal Reason      | Multiple lines  | No       | USER-ENTERED     | Mandatory when withdrawn                                              |
| 17  | SubmittedBy          | Submitted By           | Person or Group | Yes      | SYSTEM-COMPUTED  | Captured on submit                                                    |
| 18  | SubmittedDate        | Submitted Date         | Date and Time   | Yes      | SYSTEM-COMPUTED  | Captured on submit                                                    |
| 19  | ApprovedBy           | Approved By            | Person or Group | No       | WORKFLOW-MANAGED | Final approver actor                                                  |
| 20  | ApprovedDate         | Approved Date          | Date and Time   | No       | WORKFLOW-MANAGED | Final approval timestamp                                              |
| 21  | EnvironmentTag       | Environment            | Choice          | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                       |
| 22  | IsLocked             | Is Locked              | Yes/No          | No       | WORKFLOW-MANAGED | Set Yes at closure                                                    |

## Workflow Stage Map

`Draft -> Review/Approval -> Procurement -> Collection -> Finance Close`

| Stage | Action                                  | Actor Role            | SP Group                          | Power Automate Trigger            |
| ----- | --------------------------------------- | --------------------- | --------------------------------- | --------------------------------- |
| 1     | Create and submit disposal request      | Requestor             | D13-STR-Users                     | Item created with `FormCode=MDNF` |
| 2     | Review and approve/reject request       | HOD/Division Reviewer | D13-STR-Reviewers                 | `CurrentAction=Review`            |
| 3     | Record procurement and buyer processing | Procurement           | D13-STR-Procurement               | `CurrentStatus=Procurement`       |
| 4     | Confirm disposal collection evidence    | Store/Collection      | D13-STR-StoreOps                  | `CollectionDate` updated          |
| 5     | Complete finance closure                | Finance               | D13-STR-Finance                   | `FinanceStatus=Completed`         |
| R     | Withdraw request                        | Requestor/Approver    | D13-STR-Users / D13-STR-Reviewers | `WithdrawalFlag=true`             |

## Role Matrix

| Domino Role / Field     | SharePoint Group    | Permission Level |
| ----------------------- | ------------------- | ---------------- |
| Requestor               | D13-STR-Users       | Contribute       |
| Reviewer (HOD/Division) | D13-STR-Reviewers   | Contribute       |
| Procurement Processor   | D13-STR-Procurement | Contribute       |
| Finance Completer       | D13-STR-Finance     | Contribute       |
| Admin                   | D13-STR-Admins      | Full Control     |
| Reader                  | D13-STR-Readers     | Read             |

## Power Automate Actions

| Stage       | Flow Name                    | Trigger                           | Actions                                                                                    |
| ----------- | ---------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------ |
| Submit      | STR_MDNF_OnSubmit            | Item created with `FormCode=MDNF` | Generate INO, set SubmittedBy/SubmittedDate, set CurrentStatus=Submitted, notify reviewers |
| Approve     | STR_MDNF_OnReviewDecision    | Reviewer action recorded          | Set approval decision, route to Procurement or Rejected state, persist remarks             |
| Procurement | STR_MDNF_OnProcurementUpdate | `CurrentStatus=Procurement`       | Persist procurement details, notify collection owner                                       |
| Collection  | STR_MDNF_OnCollection        | `CollectionDate` populated        | Capture collection completion and notify Finance                                           |
| Close       | STR_MDNF_OnFinanceComplete   | `FinanceStatus=Completed`         | Set CurrentStatus=Closed, stamp closure, set IsLocked=Yes                                  |
| Withdraw    | STR_MDNF_OnWithdraw          | `WithdrawalFlag=true`             | Require reason, set CurrentStatus=Withdrawn, notify stakeholders                           |

## Screen Inventory

| Screen Name  | Purpose                          | Visible To                    |
| ------------ | -------------------------------- | ----------------------------- |
| MDNF_List    | Filter/search disposal requests  | STR users, reviewers, finance |
| MDNF_New     | New disposal request entry       | STR users                     |
| MDNF_View    | Read-only record and audit trail | All authorized users          |
| MDNF_Edit    | Draft/returned edit screen       | Requestor                     |
| MDNF_Review  | Review and decision screen       | Reviewers                     |
| MDNF_Closure | Finance closure and finalization | Finance                       |

## Navigation Map

`MDNF_List -> MDNF_New -> MDNF_View -> (MDNF_Edit or MDNF_Review or MDNF_Closure) -> MDNF_List`

## Migration Risks & Notes

- Disposal completion can be non-attributable if collection/finance evidence is optional; enforce
  mandatory stage fields before closure.
- Multi-role routing (requestor, reviewer, procurement, finance) can drift from Domino behavior if
  status transitions are user-editable; keep transitions flow-managed.
- Withdrawal path must preserve audit context; never delete records on withdrawal.
- DQ evidence identifies open item on final list naming; validate naming and column contracts before
  build.

## v3 Impossibilities

| Domino Feature                                               | Reason Impossible in v3                         | Recommended Workaround                                                                |
| ------------------------------------------------------------ | ----------------------------------------------- | ------------------------------------------------------------------------------------- |
| Domino section-level edit locks with formula authors/readers | Not natively portable to Canvas screen formulas | Enforce stage editability through role checks plus flow-managed status gates          |
| Domino-style server-side action buttons in NSF               | Canvas actions are client-driven                | Centralize critical transitions in Power Automate and patch only flow-approved fields |

## Reference PDF

- Path: `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/MDNF.pdf`
- Supporting DQ Evidence:
  `domino-tracker/data/uploads/docs/migration-analysis/DQ/STR/GxP_DQ_MDNF_2026-04-17.md`
- Form Technology: Printed source form (Domino-derived)
- Page Count: To be confirmed during Sentinel validation

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - MDNF (Material Disposal Notification Form)

[✓] All required sections present in canonical order
[✓] Blueprint status fields populated with architect gate values
[✓] Zero unresolved CLARIFY markers
[✓] Zero unresolved TODO markers
[✓] Zero unresolved UNCLEAR markers
[✓] Zero unresolved MISSING markers
[✓] Workflow stages mapped with actor and trigger
[✓] Roles mapped to concrete SharePoint groups
[✓] Power Automate actions defined by stage
[✓] SharePoint schema captures disposal, collection, finance, and withdrawal controls

COMPLETION STATUS: COMPLETE
```

**Handoff Status:** NOT READY FOR CRAFTSMAN (Sentinel validation pending)
