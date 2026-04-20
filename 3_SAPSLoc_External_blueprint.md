---
form_code: 3_SAPSLoc_External
dept: IT
official_name: "External Tank & Storage Location Creation request form used to create SAP-related tank/storage location master records through controlled request and approval."
module: M4 - SAP Management
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/3_SAPSLoc_External_analysis.md
---

# Blueprint - 3_SAPSLoc_External

## 1. Purpose

This blueprint defines the migration target for 3_SAPSLoc_External from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 3_SAPSLoc_External
Staging list: IT_3_SAPSLoc_External_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/3_SAPSLoc_External_analysis.md

## 3. Workflow

Baseline workflow stages:
1. Draft submission by initiator
2. Department/role validation
3. Finalization and active record management

Power Automate flow set:
- 3_SAPSLoc_External_OnSubmit
- 3_SAPSLoc_External_OnReview
- 3_SAPSLoc_External_OnComplete

## 4. Screen Set

- 3_SAPSLoc_External_List
- 3_SAPSLoc_External_New
- 3_SAPSLoc_External_View
- 3_SAPSLoc_External_Edit
- 3_SAPSLoc_External_Approval

## 5. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 6. Navigation

3_SAPSLoc_External_List -> 3_SAPSLoc_External_New -> 3_SAPSLoc_External_Approval -> 3_SAPSLoc_External_View
