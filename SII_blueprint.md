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
| Form Code                  | `SII`                                                           |
| Official Name              | `Stock Item Inclusion`                                          |
| Department                 | `STR (Department_13_STR)`                                       |
| Module                     | `M1 - Stock Item Management`                                    |
| Site(s)                    | `PRAI`                                                          |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/SII.pdf` |
| Domino Database            | `PRAI_DB_Design_Original_File/STR`                              |
| Official Name Claim Status | `Claimed`                                                       |
| Blueprint Version          | `1.1`                                                           |
| Blueprint Date             | `2026-04-18`                                                    |
| Architect                  | `GitHub Copilot (Architect mode)`                               |

---

## Purpose

SII controls master-data onboarding for new stock items, including requestor details, sourcing and
cost review, HOD/materials/finance/executive approvals, warehouse-MRP-accounting completion, and
final material-code traceability. The workflow ensures that no stock item is activated without
controlled approvals and attributable completion records.

## SharePoint Schema

**Target List:** `MainDB_STR`  
**Form Discriminator:** `FormCode = "SII"`

### Parent List: MainDB_STR

| #   | SP Internal Name       | Display Label            | Column Type     | Required | Classification   | Notes                                                                                                         |
| --- | ---------------------- | ------------------------ | --------------- | -------- | ---------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | FormCode               | Form Code                | Single line     | Yes      | SYSTEM-COMPUTED  | Fixed `SII`                                                                                                   |
| 2   | INO                    | Inclusion Ref No         | Single line     | Yes      | SYSTEM-COMPUTED  | `STR-SII-YYMM-NNNN` via flow                                                                                  |
| 3   | CurrentStatus          | Workflow Status          | Choice          | Yes      | WORKFLOW-MANAGED | Draft, Submitted, HODApproved, MaterialsApproved, FinanceApproved, EDApproved, Completed, Rejected, Discarded |
| 4   | CurrentAction          | Current Action           | Choice          | Yes      | WORKFLOW-MANAGED | Submit, Review, Approve, Complete, Discard                                                                    |
| 5   | RequestDate            | Request Date             | Date and Time   | Yes      | USER-ENTERED     | Request initiation date                                                                                       |
| 6   | Requestor              | Requestor                | Person or Group | Yes      | USER-ENTERED     | Initiator                                                                                                     |
| 7   | RequestDept            | Requesting Department    | Single line     | Yes      | USER-ENTERED     | Requesting unit                                                                                               |
| 8   | ItemDescription        | Item Description         | Multiple lines  | Yes      | USER-ENTERED     | Technical item description                                                                                    |
| 9   | ItemCategory           | Item Category            | Choice          | Yes      | USER-ENTERED     | Raw Material, Packaging, Spare, Consumable, Other                                                             |
| 10  | BuyerAssessment        | Buyer Assessment         | Multiple lines  | No       | USER-ENTERED     | Sourcing suitability                                                                                          |
| 11  | EstimatedCost          | Estimated Cost           | Currency        | No       | USER-ENTERED     | Estimated item cost                                                                                           |
| 12  | TotalHoldingCost       | Total Holding Cost       | Currency        | No       | SYSTEM-COMPUTED  | Cost roll-up or entered summary                                                                               |
| 13  | HODDecision            | HOD Decision             | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 14  | MaterialsDecision      | Materials Decision       | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 15  | FinanceDecision        | Finance Decision         | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 16  | EDDecision             | ED Decision              | Choice          | No       | WORKFLOW-MANAGED | Approved, Rejected                                                                                            |
| 17  | WarehouseDataComplete  | Warehouse Data Complete  | Yes/No          | No       | USER-ENTERED     | Master data completion check                                                                                  |
| 18  | MRPDataComplete        | MRP Data Complete        | Yes/No          | No       | USER-ENTERED     | Master data completion check                                                                                  |
| 19  | AccountingDataComplete | Accounting Data Complete | Yes/No          | No       | USER-ENTERED     | Master data completion check                                                                                  |
| 20  | MaterialCode           | Material Code            | Single line     | No       | WORKFLOW-MANAGED | Final code at completion                                                                                      |
| 21  | PRCreated              | PR Created               | Yes/No          | No       | WORKFLOW-MANAGED | Purchase requisition generated                                                                                |
| 22  | DiscardFlag            | Discard Flag             | Yes/No          | No       | WORKFLOW-MANAGED | Discard workflow route                                                                                        |
| 23  | DiscardReason          | Discard Reason           | Multiple lines  | No       | USER-ENTERED     | Mandatory when discarded                                                                                      |
| 24  | SubmittedBy            | Submitted By             | Person or Group | Yes      | SYSTEM-COMPUTED  | Submission actor                                                                                              |
| 25  | SubmittedDate          | Submitted Date           | Date and Time   | Yes      | SYSTEM-COMPUTED  | Submission timestamp                                                                                          |
| 26  | EnvironmentTag         | Environment              | Choice          | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                                                                               |
| 27  | IsLocked               | Is Locked                | Yes/No          | No       | WORKFLOW-MANAGED | Set after completion/discard                                                                                  |

## Workflow Stage Map

`Draft -> HOD -> Materials -> Finance -> ED -> Master Data Completion -> Closed`

| Stage | Action                                                     | Actor Role         | SP Group                              | Power Automate Trigger            |
| ----- | ---------------------------------------------------------- | ------------------ | ------------------------------------- | --------------------------------- |
| 1     | Submit stock item inclusion request                        | Requestor          | D13-STR-Users                         | Item created with `FormCode=SII`  |
| 2     | Approve/reject business need                               | HOD                | D13-STR-HOD-Reviewers                 | `CurrentStatus=Submitted`         |
| 3     | Approve/reject materials suitability                       | Materials          | D13-STR-Materials                     | `CurrentStatus=HODApproved`       |
| 4     | Approve/reject cost and control                            | Finance            | D13-STR-Finance                       | `CurrentStatus=MaterialsApproved` |
| 5     | Final executive decision                                   | ED                 | D13-STR-Executive-Approvers           | `CurrentStatus=FinanceApproved`   |
| 6     | Complete warehouse/MRP/accounting and assign material code | Master Data Team   | D13-STR-MasterData                    | `CurrentStatus=EDApproved`        |
| D     | Discard route                                              | Requestor/Approver | D13-STR-Users / D13-STR-HOD-Reviewers | `DiscardFlag=true`                |

## Role Matrix

| Domino Role / Field | SharePoint Group            | Permission Level |
| ------------------- | --------------------------- | ---------------- |
| Requestor           | D13-STR-Users               | Contribute       |
| HOD Reviewer        | D13-STR-HOD-Reviewers       | Contribute       |
| Materials Reviewer  | D13-STR-Materials           | Contribute       |
| Finance Reviewer    | D13-STR-Finance             | Contribute       |
| Executive Approver  | D13-STR-Executive-Approvers | Contribute       |
| Master Data Team    | D13-STR-MasterData          | Contribute       |
| Admin               | D13-STR-Admins              | Full Control     |
| Reader              | D13-STR-Readers             | Read             |

## Power Automate Actions

| Stage            | Flow Name                    | Trigger                          | Actions                                                                    |
| ---------------- | ---------------------------- | -------------------------------- | -------------------------------------------------------------------------- |
| Submit           | STR_SII_OnSubmit             | Item created with `FormCode=SII` | Generate INO, set CurrentStatus=Submitted, stamp SubmittedBy/SubmittedDate |
| HOD Review       | STR_SII_OnHODDecision        | `HODDecision` updated            | Route to Materials or reject path                                          |
| Materials Review | STR_SII_OnMaterialsDecision  | `MaterialsDecision` updated      | Route to Finance or reject path                                            |
| Finance Review   | STR_SII_OnFinanceDecision    | `FinanceDecision` updated        | Route to ED or reject path                                                 |
| Executive Review | STR_SII_OnEDDecision         | `EDDecision` updated             | Route to Master Data completion                                            |
| Complete         | STR_SII_OnMasterDataComplete | All completion flags true        | Set MaterialCode, PRCreated, CurrentStatus=Completed, IsLocked=Yes         |
| Discard          | STR_SII_OnDiscard            | `DiscardFlag=true`               | Enforce reason, set CurrentStatus=Discarded, notify stakeholders           |

## Screen Inventory

| Screen Name    | Purpose                                  | Visible To                  |
| -------------- | ---------------------------------------- | --------------------------- |
| SII_List       | Search and filter SII requests           | STR users and reviewers     |
| SII_New        | New inclusion request                    | Requestor                   |
| SII_View       | Read-only request details and approvals  | Authorized users            |
| SII_Edit       | Draft/returned edits                     | Requestor                   |
| SII_Approval   | Multi-stage review actions               | HOD, Materials, Finance, ED |
| SII_Completion | Master data completion and code issuance | Master Data Team            |

## Navigation Map

`SII_List -> SII_New -> SII_View -> (SII_Edit or SII_Approval or SII_Completion) -> SII_List`

## Migration Risks & Notes

- High approval-depth workflow can be bypassed if status is editable directly; lock transition
  fields to flow-only updates.
- Master-data completion quality depends on all three completion flags (warehouse/MRP/accounting);
  enforce all-or-none closure rule.
- Cost-threshold and escalation behavior from Domino must be validated during Craftsman
  implementation for finance control parity.

## v3 Impossibilities

| Domino Feature                                                                      | Reason Impossible in v3                                 | Recommended Workaround                                                |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- |
| Domino routing logic with multiple AEditor/RemDate chains embedded in form formulas | Canvas does not natively execute Domino formula routing | Implement deterministic stage router flows with explicit owner fields |
| Embedded Domino reminders coupled to document events                                | No direct equivalent in canvas runtime                  | Scheduled/triggered Power Automate reminders keyed by pending stage   |

## Reference PDF

- Path: `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/SII.pdf`
- Supporting DQ Evidence:
  `domino-tracker/data/uploads/docs/migration-analysis/DQ/STR/GxP_DQ_SII_2026-04-17.md`
- Form Technology: Printed source form (Domino-derived)
- Page Count: To be confirmed during Sentinel validation

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - SII (Stock Item Inclusion)

[✓] All required sections present in canonical order
[✓] Blueprint status fields populated with architect gate values
[✓] Zero unresolved CLARIFY markers
[✓] Zero unresolved TODO markers
[✓] Zero unresolved UNCLEAR markers
[✓] Zero unresolved MISSING markers
[✓] Workflow stages mapped across request, approvals, and completion
[✓] Role matrix mapped to concrete SharePoint groups
[✓] Power Automate actions cover approval, completion, and discard paths
[✓] Schema includes master data completeness controls and final material code fields

COMPLETION STATUS: COMPLETE
```

**Handoff Status:** NOT READY FOR CRAFTSMAN (Sentinel validation pending)
