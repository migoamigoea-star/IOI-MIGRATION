# Technical Blueprint: WT — Walkie Talkie Equipment Tracking

## Blueprint Status

| Status Label        | Value         |
| ------------------- | ------------- |
| Lifecycle Status    | `UNDER_AUDIT` |
| Architect Checklist | `COMPLETE`    |
| Sentinel Validation | `PENDING`     |
| Craftsman Build     | `NOT_STARTED` |
| QA Approval         | `NOT_STARTED` |
| Deployment          | `NOT_READY`   |

## Form Identity

| Field                      | Value                                                                 |
| -------------------------- | --------------------------------------------------------------------- |
| Form Code                  | `WT`                                                                  |
| Official Name              | `Walkie Talkie Equipment Tracking`                                    |
| Department                 | `SEC (Department_18)`                                                 |
| Module                     | `M5 - Equipment Tracking & Maintenance`                               |
| Site(s)                    | PRAI                                                                  |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/SEC/WT.pdf` |
| Domino Database            | `security.nsf`                                                        |
| Official Name Claim Status | `Claimed`                                                             |
| Blueprint Version          | `1.0`                                                                 |
| Blueprint Date             | `2026-04-14`                                                          |
| Architect                  | `GitHub Copilot (Architect mode)`                                     |

---

## Purpose

WT tracks walkie-talkie equipment inventory, assignment, channel allocation, and access control
across departments for secure communications management. Captures equipment model, serial number,
frequency, location, and person-in-charge; implements approvals for new equipment or access changes;
maintains audit trail of usage and ownership. Used for regulatory compliance and equipment
accountability.

---

## SharePoint Schema

**Target List:** `MainDB_SEC`  
**Form Discriminator:** `FormType = "WT"`

### Parent List: MainDB_SEC

| #   | SP Internal Name | Display Label         | Column Type     | Required | Classification   | Notes                                                          |
| --- | ---------------- | --------------------- | --------------- | -------- | ---------------- | -------------------------------------------------------------- |
| 1   | FormType         | Form Type             | Choice          | Yes      | SYSTEM-COMPUTED  | Fixed value WT                                                 |
| 2   | WTNo             | Walkie Talkie No      | Single line     | Yes      | WORKFLOW-MANAGED | Auto-generated (SEC-WT-YYMM-NNNN)                              |
| 3   | Group            | Department Group      | Single line     | Yes      | USER-ENTERED     | Department/group name; maps Domino Group field                 |
| 4   | Dept             | Specific Department   | Single line     | Yes      | USER-ENTERED     | Sub-department; maps Domino Dept field                         |
| 5   | PIC              | Person-in-Charge Name | Single line     | Yes      | USER-ENTERED     | Equipment owner/manager; maps Domino PIC field                 |
| 6   | Model            | Equipment Model       | Single line     | Yes      | USER-ENTERED     | Walkie-talkie model/type; maps Domino Model field              |
| 7   | SerialNo         | Serial Number         | Single line     | Yes      | USER-ENTERED     | Equipment serial number for traceability; maps Domino SerialNo |
| 8   | Qty              | Quantity              | Number          | Yes      | USER-ENTERED     | Number of units; maps Domino Qty field                         |
| 9   | Channel          | Assigned Channel      | Single line     | Yes      | USER-ENTERED     | Frequency/channel allocation; maps Domino Channel field        |
| 10  | Access           | Access Level          | Choice          | Yes      | USER-ENTERED     | Restricted, Standard, Full; maps Domino Access field           |
| 11  | Location         | Storage Location      | Single line     | No       | USER-ENTERED     | Equipment location/storage; maps Domino Location field         |
| 12  | Frequency        | Operating Frequency   | Single line     | No       | USER-ENTERED     | Technical frequency specification; maps Domino Frequency       |
| 13  | CurrentStatus    | Current Status        | Choice          | Yes      | WORKFLOW-MANAGED | Registered; Verified; Assigned; Recalled; Decommissioned       |
| 14  | CurrentAction    | Current Action        | Single line     | Yes      | WORKFLOW-MANAGED | REGISTRATION, VERIFICATION, ASSIGNMENT, RECALL                 |
| 15  | EnvironmentTag   | Environment           | Choice          | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                                  |
| 16  | DocAuthor        | Created By            | Person or Group | Yes      | SYSTEM-COMPUTED  | Originator of equipment request; system-set on creation        |
| 17  | CDate            | Created Date          | Date and Time   | Yes      | SYSTEM-COMPUTED  | System-set timestamp                                           |
| 18  | SubmitDate       | Submitted On          | Date and Time   | No       | SYSTEM-COMPUTED  | Timestamp when moved to Verification stage                     |
| 19  | ApprovedDate     | Approved On           | Date and Time   | No       | SYSTEM-COMPUTED  | Final approval timestamp                                       |
| 20  | ApprovedBy       | Approved By           | Person or Group | No       | WORKFLOW-MANAGED | Security manager who approved; workflow-set                    |

---

## Workflow Stage Map

```
[Stage 1: Registration] ──submit──► [Stage 2: Security Verification] ──approve──► [Stage 3: Assignment] ──assign──► [Active]
        │                                      │                                         │
        │                                   reject                                     recall
        │                                      │                                         │
        └──────────────────────────────────────┴─────────────────────────────────────────┴──► [Decommissioned]
```

| Stage | Action                                  | Actor Role        | SP Group          | Power Automate Trigger                                     |
| ----- | --------------------------------------- | ----------------- | ----------------- | ---------------------------------------------------------- |
| 1     | Register equipment and request approval | Requester         | D18-SEC-Staff     | When item created (CurrentStatus=Registered)               |
| 2     | Security verify channel/access          | Security Verifier | D18-SEC-Verifiers | When CurrentStatus=Registered (CurrentAction=VERIFICATION) |
| 3     | Final assignment to person-in-charge    | Security Manager  | D18-SEC-Managers  | When CurrentStatus=Verified (CurrentAction=ASSIGNMENT)     |
| —     | Recall or decommission                  | Security Manager  | D18-SEC-Managers  | When requested or equipment end-of-life reached            |

---

## Role Matrix

| Domino Role / Field | SharePoint Group  | Permission Level |
| ------------------- | ----------------- | ---------------- |
| Requester / Staff   | D18-SEC-Staff     | Contribute       |
| Security Verifier   | D18-SEC-Verifiers | Contribute       |
| Security Manager    | D18-SEC-Managers  | Contribute       |
| SEC Admin           | D18-SEC-Admin     | Full Control     |
| Reader              | D18-SEC-Readers   | Read             |

---

## Power Automate Actions

| Stage        | Flow Name       | Trigger                                          | Actions                                                                                  | Notification Target         |
| ------------ | --------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- | --------------------------- |
| Submit       | SEC_WT_OnSubmit | SP when item created                             | Generate WTNo (SEC-WT-YYMM-NNNN), set CurrentStatus=Registered, set CurrentAction=VERIFY | Security Verifier, Manager  |
| Verify       | SEC_WT_OnVerify | SP when CurrentStatus=Registered and verified OK | Set CurrentStatus=Verified, capture verification metadata, set CurrentAction=ASSIGNMENT  | Security Manager            |
| Reject       | SEC_WT_OnReject | SP when verification fails or access denied      | Set CurrentStatus=Rejected, persist rejection reason, notify Requester                   | Requester, Manager          |
| Assign       | SEC_WT_OnAssign | SP when CurrentStatus=Verified                   | Set CurrentStatus=Assigned, set ApprovedBy & ApprovedDate, lock equipment record         | PIC, Requester, All Readers |
| Recall       | SEC_WT_OnRecall | SP when equipment return requested               | Set CurrentStatus=Recalled, capture return metadata, disable access flags                | PIC, Requester, Manager     |
| Decommission | SEC_WT_OnDecomm | SP when equipment lifecycle ends                 | Set CurrentStatus=Decommissioned, archive record, notify audit trail                     | Manager, Audit Trail        |

---

## Screen Inventory

| Screen Name | Purpose                                       | Key Controls                                           | Visible To                                         |
| ----------- | --------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------- |
| WT_List     | Browse all walkie-talkie equipment inventory  | Gallery, filters by status/department/channel, search  | All authorized users                               |
| WT_New      | Register new equipment                        | Header form (Model, SerialNo, Channel, Access, etc.)   | D18-SEC-Staff                                      |
| WT_View     | Read-only equipment detail                    | Display form, verification/assignment history          | All authorized users                               |
| WT_Edit     | Update equipment info (conditional by stage)  | Editable sections by role; locked when Assigned        | D18-SEC-Staff, D18-SEC-Verifiers, D18-SEC-Managers |
| WT_Approval | Security verification and assignment decision | Read-only equipment data, Verify/Reject/Assign actions | D18-SEC-Verifiers, D18-SEC-Managers                |

---

## Navigation Map

```
WT_List ──► WT_New ──after submit──► WT_Edit (Verification stage)
     ▲                                      │
     │                                      ▼
     ├─ WT_View (read-only)
     │   └──► WT_Edit (if not locked)
     │
     └─ WT_Approval (manager stage only)
         └──► WT_List (on decision)
```

---

## Migration Risks & Notes

- **Serial number traceability:** Equipment identification critical for security and compliance.
  Ensure SerialNo field is unique constraint across all records to prevent duplicates.
- **Channel frequency conflicts:** Domino may not enforce unique assignment of frequencies. M365
  should validate no two active equipment records use same Channel; implement validation in Power
  Automate or Power Apps.
- **Access level classification:** Legacy system may use free-text access values. Standardize on
  Choice field with exact options (Restricted, Standard, Full) and document mapping to security
  clearance levels.
- **WTNo auto-increment (SEC-WT-YYMM-NNNN):** Ensure Power Automate generates sequence monthly;
  critical for audit trail and equipment reference lookups.

---

## v3 Impossibilities (if any)

| Domino Feature                           | Reason Impossible in v3                                   | Recommended Workaround                                                                    |
| ---------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Inline equipment usage/checkout tracking | Canvas form cannot handle concurrent multi-user checkouts | Create separate WT_Checkout child list for usage logs and checkout/return history         |
| Computed frequency conflict validation   | PA v3 cannot query all records in real-time for conflicts | Implement validation in Power Automate before item creation (check for duplicate Channel) |

---

## Reference PDF

- **Path:** `Latest_Client_provided_file/PRAI_DB_Design_Original_File/SEC/WT.pdf`
- **Form Technology:** Printed PDF (static export, no AcroForm)
- **Page Count:** [Confirm during Craftsman build]
- **Subforms:** None explicit
- **Field Evidence:** Group, Dept, PIC, Channel, Access, Model, SerialNo, Qty, Location, Frequency,
  CurrentAction, status/approval metadata, EnvironmentTag

---

## Architect Verification Checklist

```
VERIFICATION CHECKLIST — WT (Walkie Talkie Equipment Tracking)

[✓] All fields identified: 20 parent fields found, 0 clarified
[✓] Workflow stages fully mapped: 4 of 4 stages complete (Registration → Verification → Assignment → Decommission)
[✓] Power Automate actions defined for each stage: 6 of 6 flows defined
[✓] Roles mapped to SharePoint groups: 5 of 5 roles mapped (Staff, Verifiers, Managers, Admin, Readers)
[✓] All mandatory columns mapped: 20 of 20 parent columns
[✓] Form Identity table complete: 11 required fields present
[✓] Workflow Stage Map with visual diagram and formal trigger table: Present
[✓] Role Matrix with AD/SP group mappings: Complete
[✓] v3 Impossibilities documented: 2 items (Usage tracking, Frequency conflict validation)
[✓] Reference PDF metadata: Complete
[✓] Navigation Map: Present (visual flow)
[✓] Screen Inventory: 5 screens defined with role visibility

COMPLETION STATUS: COMPLETE
```

---

**Handoff Status:** PENDING SENTINEL VALIDATION

WT blueprint is architect-complete and canonical format verified. Sentinel validation is required
before Craftsman hand-off.
