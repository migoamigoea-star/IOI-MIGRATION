---
form_code: 1_HWInv_MSPNetworkPrinter
dept: IT
official_name: "MPS Network Printer inventory form used to register and maintain network printer asset records (model, IP, serial number, department, location, and operational remarks)."
module: M3 - Infrastructure & Operations
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/1_HWInv_MSPNetworkPrinter_analysis.md
---

# Blueprint - 1_HWInv_MSPNetworkPrinter

## 1. Purpose

This blueprint defines the migration target for 1_HWInv_MSPNetworkPrinter from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 1_HWInv_MSPNetworkPrinter
Staging list: IT_1_HWInv_MSPNetworkPrinter_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/1_HWInv_MSPNetworkPrinter_analysis.md

## 3. Workflow

Baseline workflow stages:
1. Draft submission by initiator
2. Department/role validation
3. Finalization and active record management

Power Automate flow set:
- 1_HWInv_MSPNetworkPrinter_OnSubmit
- 1_HWInv_MSPNetworkPrinter_OnReview
- 1_HWInv_MSPNetworkPrinter_OnComplete

## 4. Screen Set

- 1_HWInv_MSPNetworkPrinter_List
- 1_HWInv_MSPNetworkPrinter_New
- 1_HWInv_MSPNetworkPrinter_View
- 1_HWInv_MSPNetworkPrinter_Edit
- 1_HWInv_MSPNetworkPrinter_Approval

## 5. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 6. Navigation

1_HWInv_MSPNetworkPrinter_List -> 1_HWInv_MSPNetworkPrinter_New -> 1_HWInv_MSPNetworkPrinter_Approval -> 1_HWInv_MSPNetworkPrinter_View
