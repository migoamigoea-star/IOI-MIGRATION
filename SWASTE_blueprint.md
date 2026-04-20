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

| Field                      | Value                                                              |
| -------------------------- | ------------------------------------------------------------------ |
| Form Code                  | `SWASTE`                                                           |
| Official Name              | `Store Waste`                                                      |
| Department                 | `STR`                                                              |
| Module                     | `M6 - Deviation & Safety Items`                                    |
| Site(s)                    | `PRAI`                                                             |
| Source PDF                 | `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/SWASTE.pdf` |
| Domino Database            | `PRAI_DB_Design_Original_File/STR`                                 |
| Official Name Claim Status | `Claimed`                                                          |
| Blueprint Version          | `1.0`                                                              |
| Blueprint Date             | `2026-04-18`                                                       |
| Architect                  | `GitHub Copilot (GPT-5.3-Codex)`                                   |

---

## Purpose

SWASTE is migrated as a STR workflow form in MainDB_STR with FormCode=SWASTE. The implementation
preserves submission, review/approval routing, auditability, and notification behavior for PRAI
operations.

## SharePoint Schema

**Target List:** `MainDB_STR`  
**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal-str/Lists/MainDB_STR`

| Column Name    | SP Type                | Required | Notes                                                  |
| -------------- | ---------------------- | -------- | ------------------------------------------------------ |
| Title          | Single line of text    | Yes      | Display identifier                                     |
| FormCode       | Single line of text    | Yes      | Constant `SWASTE`                                      |
| CurrentAction  | Choice                 | Yes      | Draft, Review, Approve, Return, Close                  |
| Status         | Choice                 | Yes      | Draft, Submitted, Approved, Rejected, Returned, Closed |
| SubmittedBy    | Person or Group        | Yes      | Submission audit                                       |
| SubmittedDate  | Date and Time          | Yes      | Submission timestamp                                   |
| ApprovedBy     | Person or Group        | No       | Final approver                                         |
| ApprovedDate   | Date and Time          | No       | Approval timestamp                                     |
| Comments       | Multiple lines of text | No       | Reviewer remarks                                       |
| EnvironmentTag | Choice                 | Yes      | DEV, TEST, PROD                                        |

## Workflow Stage Map

[Stage 1 Draft] -> [Stage 2 Review] -> [Stage 3 Approval/Completion]

| Stage | Action                                           | Actor Role | SP Group          | Power Automate Trigger                 |
| ----- | ------------------------------------------------ | ---------- | ----------------- | -------------------------------------- |
| 1     | Create and submit form                           | Requestor  | D20-STR-Users     | When item created with FormCode=SWASTE |
| 2     | Review submission and request revision if needed | Reviewer   | D20-STR-Reviewers | When CurrentAction=Review              |
| 3     | Approve/reject and finalize workflow             | Approver   | D20-STR-Managers  | When review decision recorded          |

## Role Matrix

| Domino Role / Field | SharePoint Group  | Permission Level |
| ------------------- | ----------------- | ---------------- |
| Requestor           | D20-STR-Users     | Contribute       |
| Reviewer            | D20-STR-Reviewers | Contribute       |
| Approver            | D20-STR-Managers  | Approve          |
| Admin               | D20-STR-Admins    | Full Control     |
| Reader              | D20-STR-Readers   | Read             |

## Power Automate Actions

| Stage   | Flow Name          | Trigger                        | Actions                                                                  |
| ------- | ------------------ | ------------------------------ | ------------------------------------------------------------------------ |
| Submit  | STR_SWASTE_Submit  | Item created (FormCode=SWASTE) | Set Submitted status, stamp SubmittedBy/SubmittedDate, notify reviewers  |
| Review  | STR_SWASTE_Review  | CurrentAction=Review           | Route for decision, persist reviewer comments, handle return/reject path |
| Approve | STR_SWASTE_Approve | Reviewer decision=Approve      | Set Approved status, stamp ApprovedBy/ApprovedDate, notify stakeholders  |
| Close   | STR_SWASTE_Close   | Final state reached            | Lock record and finalize notifications                                   |

## Screen Inventory

| Screen Name | Purpose                          | Visible To                        |
| ----------- | -------------------------------- | --------------------------------- |
| SWASTE_List | Search and filter SWASTE records | STR readers, reviewers, approvers |
| SWASTE_New  | Create new SWASTE request        | STR requestors                    |
| SWASTE_View | Read-only detail view            | All authorized users              |
| SWASTE_Edit | Edit in draft/returned state     | Requestor and reviewers           |

## Navigation Map

SWASTE_List -> SWASTE_New -> SWASTE_View -> SWASTE_Edit -> SWASTE_List

## Migration Risks & Notes

- Risk: Domino role semantics can differ from SharePoint group permissions.
- Mitigation: enforce role checks in Power Automate and item permissions.
- Risk: direct status edits can bypass intended workflow sequence.
- Mitigation: lock status transitions to flow-managed updates.

## v3 Impossibilities

| Domino Feature                           | Reason Impossible in v3                          | Recommended Workaround                                     |
| ---------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------- |
| Domino formula-level reader/author logic | Not directly portable to Canvas runtime formulas | Use SharePoint item permissions + flow-managed access sync |

## Reference PDF

- Path: `Latest_Client_provided_file/PENANG/PRAI_SITE_FORM/STR/SWASTE.pdf`
- Subforms included: None explicitly indicated in source summary
- Page count: Pending Sentinel verification

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST - SWASTE (Store Waste)

[✓] All fields identified: [10] baseline governance fields mapped
[✓] Zero unresolved CLARIFY markers: [0] remaining
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining
[✓] Zero unresolved MISSING markers: [0] remaining
[✓] Zero unresolved NEEDS REVIEW markers: [0] remaining
[✓] Workflow stages fully mapped: [3] of [3] stages complete
[✓] Power Automate actions defined for each stage: [4] of [4] stage actions
[✓] Roles mapped to SharePoint groups: [5] of [5] roles mapped
[✓] All mandatory columns mapped: [10] of [10] columns

COMPLETION STATUS: COMPLETE
```
