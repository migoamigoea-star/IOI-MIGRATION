# Technical Blueprint: Ilc (ILC)

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

| Field                      | Value                                                          |
| -------------------------- | -------------------------------------------------------------- |
| Form Code                  | ILC                                                            |
| Official Name              | Ilc                                                            |
| Department                 | SA                                                             |
| Module                     | Johor Migration Wave                                           |
| Site(s)                    | JOHOR                                                          |
| Source PDF                 | Latest_Client_provided_file/JOHOR_SITE_FORM/SlsAdmin/3_ILC.pdf |
| Domino Database            | Johor site Domino source catalog (PDF-backed baseline)         |
| Official Name Claim Status | Claimed from Johor source filename                             |
| Blueprint Version          | 1.0                                                            |
| Blueprint Date             | 2026-04-19                                                     |
| Architect                  | GitHub Copilot (Architect)                                     |

---

## Purpose

This blueprint defines the migration baseline for Ilc from Johor site source forms into
Microsoft 365. The target implementation will use Power Apps canvas screens and SharePoint
list-backed storage with environment-safe automation flow controls.

---

## SharePoint Schema

Target list: MainDB_SA

| #   | Column Name    | Type                | Required | Domino Mapping      | Notes                                        |
| --- | -------------- | ------------------- | -------- | ------------------- | -------------------------------------------- |
| 1   | Title          | Single line of text | Yes      | Document identifier | Primary title key                            |
| 2   | FormCode       | Single line of text | Yes      | Form code           | Fixed value ILC                              |
| 3   | CurrentStatus  | Choice              | Yes      | Workflow status     | Draft, Submitted, Approved, Rejected, Closed |
| 4   | DocAuthor      | Person or Group     | Yes      | Creator             | Submission owner                             |
| 5   | CDate          | Date and Time       | Yes      | Created date        | Submission timestamp                         |
| 6   | Modified       | Date and Time       | No       | Modified date       | Last update timestamp                        |
| 7   | UpdatedBy      | Person or Group     | No       | Modified by         | Last editor                                  |
| 8   | EnvironmentTag | Choice              | Yes      | Environment marker  | DEV, TEST, PROD                              |

---

## Workflow Stage Map

| Stage | Action         | Actor Role          | SharePoint Group | Trigger Condition                    |
| ----- | -------------- | ------------------- | ---------------- | ------------------------------------ |
| 1     | Draft entry    | Initiator           | SA-Initiators    | Record created in app draft state    |
| 2     | Submit         | Initiator           | SA-Initiators    | CurrentStatus set to Submitted       |
| 3     | Review         | Department reviewer | SA-Reviewers     | CurrentStatus is Submitted           |
| 4     | Final decision | Department approver | SA-Approvers     | Decision action updates final status |

---

## Role Matrix

| Domino Role | Business Function             | SharePoint Group | Permission   |
| ----------- | ----------------------------- | ---------------- | ------------ |
| Initiator   | Create and update own records | SA-Initiators    | Contribute   |
| Reviewer    | Validate submission content   | SA-Reviewers     | Contribute   |
| Approver    | Final approval or rejection   | SA-Approvers     | Contribute   |
| Reader      | Read-only visibility          | SA-Readers       | Read         |
| Admin       | Configuration and support     | SA-Admins        | Full Control |

---

## Power Automate Actions

| Flow Name              | Trigger                  | Core Actions                                                 |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| SA_ILC_OnSubmit        | SharePoint item created  | Normalize fields, set FormCode, set CDate, notify reviewer   |
| SA_ILC_OnReview        | SharePoint item modified | Track review decision, append audit fields, notify approver  |
| SA_ILC_OnFinalDecision | SharePoint item modified | Apply final status and lock rules, send closure notification |

---

## Screen Inventory

| Screen   | Purpose                   | Visibility              |
| -------- | ------------------------- | ----------------------- |
| ILC_List | Record listing and search | All authenticated roles |
| ILC_New  | New submission form       | Initiators              |
| ILC_View | Read-only details         | All authenticated roles |
| ILC_Edit | Editable review form      | Reviewers and approvers |

---

## Navigation Map

ILC_List -> ILC_New -> ILC_View -> ILC_Edit -> ILC_View

---

## Migration Risks & Notes

- Source form structure may include fields that require normalization during SharePoint mapping.
- Final role naming convention must be aligned with Johor tenant security groups.
- Flow trigger conditions must be validated against final list schema before production promotion.

---

## v3 Impossibilities

| Domino Capability                  | Limitation in v3                | Workaround                                   |
| ---------------------------------- | ------------------------------- | -------------------------------------------- |
| Native Domino document event model | Not available in canvas runtime | Use Power Automate event flows               |
| Domino rich formula inheritance    | Not directly portable           | Re-implement logic in app formulas and flows |

---

## Reference PDF

- Path: Latest_Client_provided_file/JOHOR_SITE_FORM/SlsAdmin/3_ILC.pdf
- Site: JOHOR
- File Name: 3_ILC.pdf
- Evidence Basis: Source filename and Johor site folder classification

---

## Architect Verification Checklist

- Field inventory extracted from Johor source reference
- Workflow stage mapping defined
- Role-to-group matrix defined
- Screen inventory defined
- Architecture baseline prepared for Sentinel validation

COMPLETION STATUS: COMPLETE
