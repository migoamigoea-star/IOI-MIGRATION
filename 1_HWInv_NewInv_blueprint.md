---
form_code: 1_HWInv_NewInv
dept: IT
official_name: "PC Hardware List entry form for registering new or existing endpoint/server inventory details including machine identity, model, ownership, network profile, and lifecycle status."
module: M3 - Infrastructure & Operations
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_READY
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/1_HWInv_NewInv_analysis.md
---

# Blueprint - 1_HWInv_NewInv

## 1. Purpose

This blueprint defines the migration target for 1_HWInv_NewInv from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 1_HWInv_NewInv
Staging list: IT_1_HWInv_NewInv_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/1_HWInv_NewInv_analysis.md

### SharePoint column mapping

| Column name (Domino) | Display name | SharePoint column type | Required | Notes |
|---|---|---|---|---|
| machineid | Machine ID | Single line of text | Yes | Primary asset key; enforce uniqueness. |
| TagNo | Tag No | Single line of text | No | Asset tag identifier. |
| status | Status | Choice | Yes | Controlled lifecycle state values only. |
| type | Type | Choice | Yes | Controlled device class values only. |
| DeskType | Access Type | Choice | No | Desk/access classification. |
| compname | Computer Name | Single line of text | Yes | Hostname/device name. |
| compmodel | Computer Model | Single line of text | No | Endpoint model details. |
| srvrmodel | Server Model | Single line of text | No | Server model details for server assets. |
| comp | Company | Choice | No | Owning company/entity lookup or controlled choice. |
| usedby | Used by | Person or Group | No | Assigned user/owner identity. |

### Derived/system columns

| Column name | Purpose |
|---|---|
| FormType | List discriminator fixed to 1_HWInv_NewInv. |
| EnvironmentTag | DEV/TEST/PROD isolation and filtering. |
| SubmittedOn | Record creation timestamp from app/flow. |
| LastUpdatedOn | Last workflow/app mutation timestamp. |

## 3. Workflow

Baseline workflow stages:
1. Draft submission by initiator
2. Department/role validation
3. Finalization and active record management

Power Automate flow set:
- 1_HWInv_NewInv_OnSubmit
- 1_HWInv_NewInv_OnReview
- 1_HWInv_NewInv_OnComplete

### Stage matrix

| Stage # | Stage name | Trigger | Actor | Actions | Next stage | Notifications |
|---|---|---|---|---|---|---|
| 1 | Asset Capture | New registration started | IT Technician | Populate machine identity and device metadata | 2 | IT Asset Admin |
| 2 | Validation | Record submitted for review | IT Asset Admin | Validate ownership/model/data quality; approve or return | 3 or 1 | Requestor/Initiator |
| 3 | Inventory Active | Record approved | System | Finalize active inventory state and expose for reporting | - | Reporting channels only |

### Trigger-condition matrix

| Workflow stage | Trigger condition | Required checks | Advance path | Return/reject path | Time-based trigger |
|---|---|---|---|---|---|
| Capture | Item created | machineid, status, type, compname populated | Route to validation queue | Return to draft with missing-fields notice | Incomplete-item reminder |
| Validation | Item updated by reviewer | Uniqueness check for machineid/TagNo and consistency checks | Mark approved and publish active inventory | Flag duplicate/inconsistent record and return to initiator | Weekly reconciliation |
| Active | Status changed to active | Data-quality checks pass | Keep active baseline inventory | N/A | Quarterly recertification |

## 4. Screen Set

- 1_HWInv_NewInv_List
- 1_HWInv_NewInv_New
- 1_HWInv_NewInv_View
- 1_HWInv_NewInv_Edit
- 1_HWInv_NewInv_Approval

### Screen-to-purpose mapping

| Screen name | Purpose | Primary controls | Visible to |
|---|---|---|---|
| 1_HWInv_NewInv_List | Inventory list, filter, and search | Gallery, filter chips, search box | Authorized users |
| 1_HWInv_NewInv_New | Create inventory record | Edit form, validation labels, submit/cancel actions | Initiators/IT technicians |
| 1_HWInv_NewInv_View | Read-only record inspection | Display form, activity summary | Readers/Admin |
| 1_HWInv_NewInv_Edit | Record maintenance and correction | Edit form, save action, data checks | IT Asset Admin |
| 1_HWInv_NewInv_Approval | Validation decision stage | Approval component, comments, approve/return actions | IT Asset Admin |

Naming note: source analysis uses `HWInv_NewInv_*`; implementation in this module standardizes to `1_HWInv_NewInv_*` to align with form code.

## 5. Roles and Permissions

| Role | SharePoint group | Access level |
|---|---|---|
| IT Technician | D06-IT-Initiators | Create/Edit own records |
| IT Asset Admin | D06-IT-IT-Admin | Edit all/Admin approval actions |
| Department/User Reader | D06-IT-Readers | Read-only |

## 6. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 7. Navigation

1_HWInv_NewInv_List -> 1_HWInv_NewInv_New -> 1_HWInv_NewInv_Approval -> 1_HWInv_NewInv_View
1_HWInv_NewInv_List -> 1_HWInv_NewInv_Edit -> 1_HWInv_NewInv_View

## 8. Exit Criteria To Dispatch Craftsman

1. Blueprint has zero unresolved markers (PASS).
2. Data model includes explicit SharePoint column mapping and required flags.
3. Workflow stage and trigger-condition matrices are complete.
4. Screen inventory and navigation are implementation-ready.
