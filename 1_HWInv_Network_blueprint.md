---
form_code: 1_HWInv_Network
dept: IT
official_name: "Network Hardware Inventory Form used to capture core network asset attributes (MAC, model, name, IP, serial number, location, purchase date)."
module: M3 - Infrastructure & Operations
owner: "IT"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-14
source_analysis: docs/migration-analysis/Department_06_IT/1_HWInv_Network_analysis.md
---

# Blueprint - 1_HWInv_Network

## 1. Purpose

This blueprint defines the migration target for 1_HWInv_Network from Domino into Microsoft 365 architecture under IT.

## 2. Target Data Model

Primary list: MainDB_IT with FormType = 1_HWInv_Network
Staging list: IT_1_HWInv_Network_List

Detailed field inventory and mapping source:
- docs/migration-analysis/Department_06_IT/1_HWInv_Network_analysis.md

## 3. Workflow

### Stage Flow Diagram

```
[Stage 1: Asset Registration — Draft]
         │ submit
         ▼
[Stage 2: Validation — IT Network Admin Review]
         │ approve / return
         ├─→ Approved: Stage 3
         └─→ Returned: Stage 1
         ▼
[Stage 3: Active Inventory]
```

### Stage Matrix

| Stage # | Stage Name         | Trigger                      | Actor              | Actions                                                                    | Next Stage    | Notifications                     |
| ------- | ------------------ | ---------------------------- | ------------------ | -------------------------------------------------------------------------- | ------------- | --------------------------------- |
| 1       | Asset Registration | New registration started     | IT Technician      | Populate MAC address, model, IP, serial number, location, purchase date    | 2             | IT Network Admin                  |
| 2       | Validation         | Record submitted for review  | IT Network Admin   | Validate MAC/IP uniqueness, serial number, data quality; approve or return | 3 or 1        | Requestor/Initiator on return     |
| 3       | Active Inventory   | Record approved               | System (auto)     | Finalise active inventory state; expose for reporting                      | —             | Reporting channels only           |

### Trigger-Condition Matrix

| Stage      | Trigger Condition                       | Required Checks                                     | Advance Path               | Return/Reject Path                          |
| ---------- | --------------------------------------- | --------------------------------------------------- | -------------------------- | ------------------------------------------- |
| Capture    | Item created with FormType=1_HWInv_Network | MAC, IP, model, serial number populated          | Route to validation queue  | Missing-fields notice to initiator          |
| Validation | Item updated by IT Network Admin        | MAC uniqueness; IP conflict check; purchase date    | Mark approved; publish active record | Flag duplicate/inconsistent; return to initiator |
| Active     | Status changed to active                | Data-quality checks pass                            | Keep active baseline       | N/A                                         |

### Power Automate Flows

| Flow Name                      | Trigger                       | Key Actions                                                                            |
| ------------------------------ | ----------------------------- | -------------------------------------------------------------------------------------- |
| `1_HWInv_Network_OnSubmit`     | Item created                  | Validate required fields; set Status=Submitted; stamp SubmittedDate; notify Network Admin |
| `1_HWInv_Network_OnReview`     | Status updated to UnderReview | Route to IT Network Admin; stamp ReviewDate; notify reviewer                           |
| `1_HWInv_Network_OnComplete`   | Status updated to Approved    | Set Status=Active; stamp CompletedDate; lock record; update network inventory register |

## 4. Screen Set

- 1_HWInv_Network_List
- 1_HWInv_Network_New
- 1_HWInv_Network_View
- 1_HWInv_Network_Edit
- 1_HWInv_Network_Approval

## 5. Migration Notes

1. Keep Domino field IDs traceable in mapping sheet.
2. Preserve full stage/audit comments in the target list.
3. Apply EnvironmentTag isolation for DEV/TEST/PROD.
4. Enforce controlled choice/lookup mappings where legacy text values exist.

## 6. Navigation

1_HWInv_Network_List -> 1_HWInv_Network_New -> 1_HWInv_Network_Approval -> 1_HWInv_Network_View
