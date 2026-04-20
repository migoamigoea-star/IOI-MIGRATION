# Technical Blueprint: ESF — ESF Form

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
| Form Code                  | `ESF`                                                                 |
| Official Name              | `ESF Form`                                                            |
| Department                 | `HR (Department_05)`                                                  |
| Module                     | `M3 - Employee Records & Information`                                 |
| Site(s)                    | `PRAI (Penang)`                                                       |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/HR/ESF.pdf` |
| Domino Database            | `hr.nsf`                                                              |
| Official Name Claim Status | `Working`                                                             |
| Blueprint Version          | `1.0`                                                                 |
| Blueprint Date             | `2026-04-19`                                                          |
| Architect                  | `GitHub Copilot (Architect mode)`                                     |

## Purpose

ESF enables HR record submission and approval routing with standardized status control and
auditability.

## SharePoint Schema

**Target List:** `MainDB_HR`

| #   | SP Internal Name | Display Label  | Column Type     | Required | Notes             |
| --- | ---------------- | -------------- | --------------- | -------- | ----------------- |
| 1   | FormType         | Form Type      | Choice          | Yes      | Fixed value `ESF` |
| 2   | INO              | Reference No.  | Single line     | Yes      | Flow-generated    |
| 3   | CurrentStatus    | Current Status | Choice          | Yes      | Workflow-managed  |
| 4   | Requester        | Requester      | Person or Group | Yes      | Initiator         |
| 5   | Department       | Department     | Single line     | Yes      | HR department     |
| 6   | Remarks          | Remarks        | Multiple lines  | No       | Optional notes    |

## Workflow Stage Map

```text
Draft -> HR Review -> Final Decision
```

| Stage | Action         | Actor Role  | SP Group          | Power Automate Trigger        |
| ----- | -------------- | ----------- | ----------------- | ----------------------------- |
| 1     | Create draft   | Initiator   | D05-HR-Initiators | On create                     |
| 2     | Review         | HR Reviewer | D05-HR-Editors-L1 | When CurrentStatus=Submitted  |
| 3     | Final decision | HR Manager  | D05-HR-Manager    | When review outcome submitted |

## Role Matrix

| Domino Role | SharePoint Group  | Permission   |
| ----------- | ----------------- | ------------ |
| Initiator   | D05-HR-Initiators | Contribute   |
| Reviewer    | D05-HR-Editors-L1 | Contribute   |
| Manager     | D05-HR-Manager    | Contribute   |
| Admin       | D05-HR-Admin      | Full Control |
| Reader      | D05-HR-Readers    | Read         |

## Power Automate Actions

| Stage  | Flow Name         | Trigger        | Action Summary                   |
| ------ | ----------------- | -------------- | -------------------------------- |
| Submit | HR_ESF_OnSubmit   | Item created   | Set status and notify reviewer   |
| Review | HR_ESF_OnReview   | Status updated | Route to manager                 |
| Final  | HR_ESF_OnDecision | Manager action | Lock record and notify requester |

## Screen Inventory

| Screen Name  | Purpose        | Visible To             |
| ------------ | -------------- | ---------------------- |
| ESF_List     | List records   | All authorized users   |
| ESF_New      | Create request | Initiator              |
| ESF_Edit     | Update request | Initiator and reviewer |
| ESF_View     | Read-only view | All authorized users   |
| ESF_Approval | Final decision | Manager                |

## Navigation Map

```text
ESF_List -> ESF_New -> ESF_Edit -> ESF_Approval -> ESF_View -> ESF_List
```

## Migration Risks & Notes

- Field-level validation rules require final confirmation against source PDF.
- Approval SLA timers must be finalized in flow design.
- Existing Domino attachments require migration mapping confirmation.

## v3 Impossibilities

| Domino Feature                       | Limitation                                | Workaround                     |
| ------------------------------------ | ----------------------------------------- | ------------------------------ |
| Atomic sequence generation in client | Canvas cannot guarantee atomic increments | Generate INO in Power Automate |

## Reference PDF

- Path: `Latest_Client_provided_file/PRAI_DB_Design_Original_File/HR/ESF.pdf`
- Evidence Source: HR Domino export package

## Architect Verification Checklist

- [x] Form identity table completed
- [x] Canonical section order applied
- [x] SharePoint schema section present
- [x] Workflow stage map table present
- [x] Role matrix mapped to SP groups
- [x] Power Automate actions mapped by stage
- [x] Screen inventory included
- [x] Navigation map included
- [x] Risks and impossibilities documented

COMPLETION STATUS: COMPLETE
