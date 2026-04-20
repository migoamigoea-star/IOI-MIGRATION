# Technical Blueprint: Cafeteria Inspection (CIR)

<!-- Architect: CIR form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

## Form Identity

| Field                      | Value                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------- |
| Form Code                  | `CIR`                                                                                             |
| Official Name              | Cafeteria Inspection Database                                                                     |
| Department                 | HR (Department_05)                                                                                |
| Module                     | M1 — General Administration & Facilities                                                          |
| Site(s)                    | PRAI                                                                                              |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/HR/CIR.pdf`                             |
| Domino Database            | HR.nsf                                                                                            |
| Official Name Claim Status | Claimed — "Cafeteria Inspection" (source: `Department_05_HR/CIR_analysis.md` extraction evidence) |
| Blueprint Version          | 1.0                                                                                               |
| Blueprint Date             | 2026-04-14                                                                                        |
| Architect                  | GitHub Copilot (Architect Agent)                                                                  |
| DQ_REQUIRED                | NO                                                                                                |
| GxP Class                  | Non-GxP                                                                                           |
| Complexity                 | Simple                                                                                            |

---

## Business Purpose

The HR department uses the Cafeteria Inspection form to record and track periodic hygiene and
compliance inspections of company cafeteria facilities at PRAI. An initiator (HR Admin or Hygiene
Officer) documents the inspection date, team, site, and findings. The record is then reviewed by a
designated reviewer who adds corrective action remarks. The form supports committee oversight via
ACM and ECM members fields. An INO (Internal Number) is system-generated via Power Automate as the
unique identifier.

---

## SharePoint Schema

### Primary Table: `MainDB_HR`

**URL:** `https://ioioi.sharepoint.com/sites/HR/Lists/MainDB_HR`

**Architecture Method:** DEC-001 (Live Submission Architecture)  
All new CIR form submissions → `MainDB_HR`. Historical Domino records are imported to the staging
table `HR_CIR_List` for read-only reference only.

| #   | Column Name    | SP Type                 | Required | Choices / Source                                | Notes                                                                                                |
| --- | -------------- | ----------------------- | -------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1   | Title          | Single line of text     | Yes      | —                                               | Auto-populated: `"CIR-" & INO`; used as record display name                                          |
| 2   | INO            | Single line of text     | Yes      | —                                               | System-computed via Power Automate (format: `HR-CIR-YYMM-NNNN`); **PATTERN-E** — never set in canvas |
| 3   | Site           | Choice                  | Yes      | PRAI; Johor                                     | Cafeteria site location (Domino: Site)                                                               |
| 4   | InspectionDate | Date and Time           | Yes      | —                                               | Date of cafeteria inspection (Domino: InsDate)                                                       |
| 5   | InspectionTime | Single line of text     | No       | —                                               | Time of inspection (Domino: InsTime; stored as text HH:MM)                                           |
| 6   | Inspector      | Person or Group         | Yes      | —                                               | Primary inspector (Domino: Inspector)                                                                |
| 7   | TeamMembers    | Person or Group (multi) | No       | —                                               | Additional inspection team members (Domino: TeamMembers)                                             |
| 8   | SubmittedBy    | Person or Group         | Yes      | —                                               | Record initiator (Domino: SubmittedBy; auto-populated from logged-in user)                           |
| 9   | SubmittedDate  | Date and Time           | Yes      | —                                               | Submission timestamp (Domino: SubmittedDate; PA-set on submit)                                       |
| 10  | ReviewedBy     | Person or Group         | No       | —                                               | Corrective action reviewer (Domino: ReviewedBy; set during review stage)                             |
| 11  | ReviewedDate   | Date and Time           | No       | —                                               | Date review was completed (Domino: ReviewedDate; PA-set on review submit)                            |
| 12  | Remarks        | Multiple lines of text  | No       | —                                               | Corrective action review remarks (Domino: Remarks)                                                   |
| 13  | ACMCommittee   | Person or Group (multi) | No       | —                                               | ACM committee members for this inspection (Domino: ACMComm)                                          |
| 14  | ECMCommittee   | Person or Group (multi) | No       | —                                               | ECM committee members for this inspection (Domino: ECMComm)                                          |
| 15  | ITNotify       | Person or Group         | No       | —                                               | IT notification recipient (Domino: IT; for system-related issues flagged during inspection)          |
| 16  | CurrentStatus  | Choice                  | Yes      | Draft; Submitted; UnderReview; Reviewed; Closed | Master workflow status (PA-managed; sourced from Domino CurrentAction)                               |
| 17  | CurrentAction  | Choice                  | Yes      | Create; Submit; Review; Close                   | Active workflow action (PA-managed; sourced from Domino CurrentAction hidden field)                  |
| 18  | Editors        | Person or Group (multi) | No       | —                                               | Access control — editors group (Domino: Editors; Editor1; Editor2)                                   |
| 19  | EnvironmentTag | Choice                  | No       | DEV; TEST; PROD                                 | Three-tier environment strategy (DEC-004)                                                            |
| 20  | InitiatorEmail | Person or Group         | No       | —                                               | Requestor identity for audit trail (PA-set from Office 365 login)                                    |

---

### Staging Table (Historical Import Only): `HR_CIR_List`

Historical Domino CIR records imported for read-only reference. No live form submissions target this
list.

---

## Field Inventory Summary

| Category                 | Domino Fields                            | Disposition                     |
| ------------------------ | ---------------------------------------- | ------------------------------- |
| Reference                | Num, INO                                 | Mapped → MainDB_HR columns 1, 2 |
| Location                 | Site                                     | Mapped → column 3               |
| Inspection details       | InsDate, InsTime, Inspector, TeamMembers | Mapped → columns 4–7            |
| Submission               | SubmittedBy, SubmittedDate               | Mapped → columns 8–9            |
| Review/Corrective action | ReviewedBy, ReviewedDate, Remarks        | Mapped → columns 10–12          |
| Committee                | ACMComm, ECMComm                         | Mapped → columns 13–14          |
| IT notification          | IT                                       | Mapped → column 15              |
| Workflow state           | CurrentAction                            | Mapped → columns 16–17          |
| Access control           | Editors, Editor1, Editor2                | Mapped → column 18              |

---

## Workflow

### Summary

Simple 2-stage inspection lifecycle: **Submission → Review → Closed**.

### Stage Map

| Stage | Name                     | Trigger           | Actor                              | Actions                         | Next Stage | Notifications                |
| ----- | ------------------------ | ----------------- | ---------------------------------- | ------------------------------- | ---------- | ---------------------------- |
| 1     | Draft / Submission       | Record created    | Initiator (SubmittedBy)            | Fill inspection details, Submit | 2          | None                         |
| 2     | Corrective Action Review | Stage 1 submitted | ReviewedBy (HR/Facilities Manager) | Add remarks, complete review    | End        | Initiator email confirmation |
| End   | Closed                   | Review submitted  | PA (auto)                          | Set status = Closed             | —          | CC: ACMComm, ECMComm         |

### Power Automate Flows Required

| Flow          | Trigger                                                    | Actions                                                                                         |
| ------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| CIR_OnSubmit  | Item created in MainDB_HR with CurrentAction = Submit      | Set INO (HR-CIR-YYMM-NNNN), set SubmittedDate, set CurrentStatus = Submitted, notify ReviewedBy |
| CIR_OnReview  | Item updated with CurrentAction = Review                   | Set ReviewedDate, set CurrentStatus = Reviewed, notify Initiator, notify ACMComm/ECMComm        |
| CIR_AutoClose | Scheduled — 7 days after ReviewedDate if no further action | Set CurrentStatus = Closed                                                                      |

---

## Screen Inventory

| Screen Name | Purpose                                          | Key Controls                                                                              | Visible To        |
| ----------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------- | ----------------- |
| CIR_List    | Gallery list of all cafeteria inspection records | Gallery, search by site/date, filter by status                                            | All HR staff      |
| CIR_New     | New inspection data entry                        | Edit form: Site, InspectionDate, InspectionTime, Inspector, TeamMembers, ACMComm, ECMComm | Initiators        |
| CIR_View    | Read-only record detail                          | Display form with all fields, status banner, timeline                                     | Readers/Reviewers |
| CIR_Edit    | Edit/review stage                                | Conditional fields: Remarks, ReviewedBy (only visible in Review stage)                    | Reviewer          |

---

## Navigation Map

```
CIR_List  ──[New]──►  CIR_New  ──[Submit]──►  CIR_View
CIR_List  ──[Open]──►  CIR_View
CIR_View  ──[Edit / Review]──►  CIR_Edit  ──[Save]──►  CIR_View
```

---

## Role & Permission Matrix

| Role             | Description                                             | SharePoint Group  | PA Access         |
| ---------------- | ------------------------------------------------------- | ----------------- | ----------------- |
| Initiator        | HR Admin / Hygiene Officer creating inspection record   | D05-HR-Initiators | Create / Edit own |
| Reviewer         | HR Manager / Facilities Lead handling corrective review | D05-HR-Managers   | Edit (Stage 2)    |
| Committee Member | ACM / ECM members notified at close                     | D05-HR-Readers    | Read only         |
| IT Admin         | System administrator                                    | D02-IT-Admins     | Full control      |

---

## Related Lists / Dependencies

- Shared lookup: `Config_HR_Sites` (PRAI / Johor site list)
- Shared people lookup: `HR_EmployeeDirectory` for Inspector / TeamMembers choices (optional — can
  fall back to AAD People Picker)
- No parent-child relationships for this form; INO is standalone

---

## Migration Notes

- No complex computed fields; field names are straightforward (Domino labels map 1:1 to display
  names).
- InsTime stored as plain text — no date-picker required, single text field is sufficient.
- ACMComm / ECMComm are committee notification fields; stored as Person (multi) and used by PA
  notification flows only.
- Historical migration: import last 3 years of inspection records to `HR_CIR_List` staging table.
- INO pattern: `HR-CIR-[YY][MM]-[NNNN sequential]`.
