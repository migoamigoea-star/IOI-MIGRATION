---
form_code: 2_SAPDR_PanCen
dept: IT
official_name: "Pan Century SAP/Procedure entry form for controlled document setup with title, category, effective date, revision, department, and team ownership."
module: M6 - Disaster Recovery
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/2_SAPDR_PanCen_analysis.md
---

# Blueprint - 2_SAPDR_PanCen

## 1. Purpose

This blueprint defines the migration target for 2_SAPDR_PanCen from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 2_SAPDR_PanCen
Staging list: IT_2_SAPDR_PanCen_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/2_SAPDR_PanCen_analysis.md

## 3. Workflow

Baseline workflow stages:
1. Draft submission by initiator
2. Department/role validation
3. Finalization and active record management

Power Automate flow set:
- 2_SAPDR_PanCen_OnSubmit
- 2_SAPDR_PanCen_OnReview
- 2_SAPDR_PanCen_OnComplete

## 4. Screen Set

- 2_SAPDR_PanCen_List
- 2_SAPDR_PanCen_New
- 2_SAPDR_PanCen_View
- 2_SAPDR_PanCen_Edit
- 2_SAPDR_PanCen_Approval

## 5. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 6. Navigation

2_SAPDR_PanCen_List -> 2_SAPDR_PanCen_New -> 2_SAPDR_PanCen_Approval -> 2_SAPDR_PanCen_View
