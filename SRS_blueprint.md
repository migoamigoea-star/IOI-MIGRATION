---
form_code: SRS
dept: ADM
official_name: "SRS"
module: ADM Module
owner: "ADM"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-20
source_analysis: docs/migration-analysis/Department_01_ADM/SRS_analysis.md
---

# Blueprint — SRS (SRS)

## Blueprint Status

| Field               | Value       |
|---------------------|-------------|
| Lifecycle Status    | UNDER_AUDIT |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PENDING     |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

## Form Identity

| Field           | Value                                                     |
|-----------------|-----------------------------------------------------------|
| Form Code       | SRS                                                       |
| Official Name   | SRS                                                       |
| Department      | ADM (Department_01)                                       |
| Module          | ADM Module                                                |
| Site(s)         | Prai                                                      |
| Source Analysis | docs/migration-analysis/Department_01_ADM/SRS_analysis.md |
| DQ Required     | NO                                                        |
| Complexity      | Medium                                                    |
| Owner           | ADM                                                       |
| Blueprint Date  | 2026-04-20                                                |
| GxP Class       | —                                                         |

## Purpose

SRS is an administration form migrated from Lotus Domino to Microsoft 365 (Power Apps + SharePoint Online).
The form supports standardized administrative submission, review, and approval at the Prai site.
Detailed field-level extraction remains anchored in the source analysis artifact.

## SharePoint Schema

**Primary List:** `MainDB_ADM`

| # | Column (Internal) | Display Name    | Type                   | Required | Notes                                |
|---|-------------------|-----------------|------------------------|----------|--------------------------------------|
| 1 | Title             | Title           | Single line of text    | Yes      | Record identifier                    |
| 2 | FormType          | Form Type       | Single line of text    | Yes      | Fixed value: SRS                     |
| 3 | CurrentStatus     | Current Status  | Choice                 | Yes      | Draft, Submitted, Approved, Rejected |
| 4 | Requestor         | Requestor       | Person                 | Yes      | Initiator                            |
| 5 | RequestDate       | Request Date    | Date                   | Yes      | Created/submitted date               |
| 6 | ReviewComments    | Review Comments | Multiple lines of text | No       | Review notes                         |
| 7 | AttachmentLink    | Attachment Link | Hyperlink              | No       | Supporting reference                 |
| 8 | EnvironmentTag    | Environment Tag | Choice                 | Yes      | DEV, TEST, PROD                      |

## Workflow Stage Map

```
[Draft] -> [Submitted] -> [Reviewed] -> [Approved/Rejected]
```

| Stage | Action     | Actor Role | SP Group          | Power Automate Trigger                        |
|-------|------------|------------|-------------------|-----------------------------------------------|
| 1     | Submit SRS | Initiator  | D01-ADM-Users     | When CurrentStatus = 'Submitted'              |
| 2     | Review SRS | Reviewer   | D01-ADM-Reviewers | When CurrentStatus = 'Reviewed'               |
| 3     | Decide SRS | Approver   | D01-ADM-Approvers | When CurrentStatus = 'Approved' OR 'Rejected' |

## Role Matrix

| Domino Role | SharePoint Group  | Permissions           |
|-------------|-------------------|-----------------------|
| Initiator   | D01-ADM-Users     | Create, Read own      |
| Reviewer    | D01-ADM-Reviewers | Read, Edit in review  |
| Approver    | D01-ADM-Approvers | Read, Approve, Reject |
| Admin       | D01-ADM-Admins    | Full control          |

## Power Automate Actions

| Flow Name         | Trigger                   | Action                                   |
|-------------------|---------------------------|------------------------------------------|
| ADM_SRS_OnSubmit  | CurrentStatus='Submitted' | Notify reviewer and stamp review stage   |
| ADM_SRS_OnReview  | CurrentStatus='Reviewed'  | Notify approver and stamp decision stage |
| ADM_SRS_OnApprove | CurrentStatus='Approved'  | Lock record and notify initiator         |
| ADM_SRS_OnReject  | CurrentStatus='Rejected'  | Return to initiator with reason          |

## Screen Inventory

| Screen       | Purpose               | Visibility            |
|--------------|-----------------------|-----------------------|
| SRS_List     | List all SRS records  | Authenticated users   |
| SRS_New      | Create SRS request    | D01-ADM-Users+        |
| SRS_View     | View SRS detail       | Authenticated users   |
| SRS_Edit     | Edit SRS draft/review | Initiator + reviewers |
| SRS_Approval | Approve/reject SRS    | D01-ADM-Approvers     |

## Navigation Map

```
SRS_List -> SRS_New -> SRS_View
SRS_List -> SRS_View -> SRS_Edit
SRS_View -> SRS_Approval
```

## Migration Risks & Notes

1. Domino field semantics must be fully reconciled during final schema lock.
2. Approval history must remain auditable and immutable post-decision.
3. Attachment links must preserve traceability to the migrated source.
4. EnvironmentTag filtering must isolate DEV/TEST/PROD records.

## v3 Impossibilities

| Domino Feature                          | Migration Constraint         | Workaround                             |
|-----------------------------------------|------------------------------|----------------------------------------|
| Agent-driven background updates         | Not native in canvas runtime | Move logic to Power Automate           |
| Rich document-level computed behavior   | Not directly portable        | Use Power Fx + flow-assisted updates   |
| Legacy UI formulas tied to Notes client | Unsupported                  | Rebuild interaction in canvas controls |

## Reference PDF

- Source PDF: docs/migration-analysis/Department_01_ADM/SRS.pdf
- Analysis file: docs/migration-analysis/Department_01_ADM/SRS_analysis.md
- Evidence mapping: to be validated during Sentinel review

## Architect Verification Checklist

- [x] Form Identity table present
- [x] Purpose section completed
- [x] SharePoint Schema section completed
- [x] Workflow Stage Map formal table present
- [x] Role Matrix mapped to SharePoint groups
- [x] Power Automate actions identified
- [x] Screen Inventory enumerated
- [x] Navigation Map documented
- [x] Migration Risks & Notes documented
- [x] v3 Impossibilities documented
- [x] Reference PDF section present
- [ ] Column-level mapping validated against source evidence
- [ ] Architect quality gate complete

COMPLETION STATUS: INCOMPLETE
