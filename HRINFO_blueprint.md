# Technical Blueprint: HR Notice / Information (HRINFO)

<!-- Architect: HRINFO form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

## Form Identity

| Field                      | Value                                                                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------- |
| Form Code                  | `HRINFO`                                                                                              |
| Official Name              | HR Notice / Information                                                                               |
| Department                 | HR (Department_05)                                                                                    |
| Module                     | M1 — General Administration & Facilities                                                              |
| Site(s)                    | PRAI                                                                                                  |
| Source PDF                 | `Latest_Client_provided_file/PRAI_DB_Design_Original_File/HR/HRINFO.pdf`                              |
| Domino Database            | HR.nsf                                                                                                |
| Official Name Claim Status | Claimed — "HR Notice/Information" (source: `Department_05_HR/HRINFO_analysis.md` extraction evidence) |
| Blueprint Version          | 1.0                                                                                                   |
| Blueprint Date             | 2026-04-14                                                                                            |
| Architect                  | GitHub Copilot (Architect Agent)                                                                      |
| DQ_REQUIRED                | NO                                                                                                    |
| GxP Class                  | Non-GxP                                                                                               |
| Complexity                 | Simple                                                                                                |

---

## Business Purpose

The HR department uses this form to broadcast internal notices, announcements, policy updates,
holiday advisories, and benefits changes to targeted staff groups. An HR Author composes the notice
(subject, body, optional attachment) and selects recipient distribution lists. On posting, Power
Automate sends a personalised email notification to all recipients. Staff can register their
engagement via interactive response actions (Read / Beneficial / Disseminate). After 30 days the
record is automatically locked to read-only. No approval workflow is required — the HR author posts
directly after drafting. A unique reference number (INO in format `HR-INF-YYMM-NNNN`) is generated
per notice.

---

## SharePoint Schema

### Primary Table: `MainDB_HR`

**URL:** `https://ioioi.sharepoint.com/sites/HR/Lists/MainDB_HR`

**Architecture Method:** DEC-001 (Live Submission Architecture)  
All HRINFO submissions → `MainDB_HR`. A `FormType` column = `"HRINFO"` distinguishes records within
the shared list.

| #   | Column Name      | SP Type                 | Required | Choices / Source         | Notes                                                                                                |
| --- | ---------------- | ----------------------- | -------- | ------------------------ | ---------------------------------------------------------------------------------------------------- |
| 1   | Title            | Single line of text     | Yes      | —                        | Auto-populated: `"HRINFO-" & INO`; display name in gallery                                           |
| 2   | INO              | Single line of text     | Yes      | —                        | System-computed via Power Automate (format: `HR-INF-YYMM-NNNN`); **PATTERN-E** — never set in canvas |
| 3   | FormType         | Single line of text     | Yes      | HRINFO                   | Fixed value to distinguish HRINFO records in shared MainDB_HR                                        |
| 4   | Subject          | Single line of text     | Yes      | —                        | Notice headline / subject (Domino: Subject)                                                          |
| 5   | Recipients       | Person or Group (multi) | Yes      | —                        | Primary target staff/departments (Domino: Send)                                                      |
| 6   | CC               | Person or Group (multi) | No       | —                        | Secondary notification recipients (Domino: CC)                                                       |
| 7   | Body             | Multiple lines of text  | Yes      | —                        | Announcement message body with rich text (Domino: Body/Announcement)                                 |
| 8   | ContactExt       | Single line of text     | No       | —                        | HR contact extension number (Domino: Ext)                                                            |
| 9   | Attachment       | Attachment              | No       | —                        | Supporting image or PDF notice (Domino: Att)                                                         |
| 10  | ReadCount        | Number                  | No       | —                        | Running count of staff who clicked "Read" (Domino: CtrLst; PA-incremented)                           |
| 11  | BeneficialUsers  | Person or Group (multi) | No       | —                        | Staff who clicked "Beneficial" engagement action (Domino: LkLst)                                     |
| 12  | DisseminateUsers | Person or Group (multi) | No       | —                        | Staff who clicked "Disseminate" engagement action (Domino: DslkLst)                                  |
| 13  | TotalViews       | Number                  | No       | —                        | Persistence view counter (Domino: Viewed; PA-incremented on each view)                               |
| 14  | HRHOD            | Person or Group         | Yes      | —                        | HR Manager / final admin sign-off (Domino: HRHOD)                                                    |
| 15  | HRAuthor         | Person or Group         | Yes      | —                        | HR Author who published the notice (Domino: HR/DocAuthor; auto-populated from logged-in user)        |
| 16  | PublishedDate    | Date and Time           | No       | —                        | Date notice was posted/broadcast (PA-set on post action)                                             |
| 17  | LockDate         | Date and Time           | No       | —                        | Auto-lock date = PublishedDate + 30 days (PA-set on post)                                            |
| 18  | IsLocked         | Yes/No                  | No       | —                        | Record locked flag (Domino: Lock; PA-set on auto-lock trigger)                                       |
| 19  | CurrentStatus    | Choice                  | Yes      | Draft; Published; Locked | Master workflow status (PA-managed)                                                                  |
| 20  | CurrentAction    | Choice                  | Yes      | Draft; Publish; Lock     | Active workflow action (PA-managed; sourced from Domino CurrentAction)                               |
| 21  | EnvironmentTag   | Choice                  | No       | DEV; TEST; PROD          | Three-tier environment strategy (DEC-004)                                                            |

---

### Staging Table (Historical Import Only): `HR_HRINFO_List`

Historical Domino HRINFO records imported for read-only reference, capped at last 12 months (see
Migration Notes). Older records archived to static PDF library.

---

## Field Inventory Summary

| Category       | Domino Fields                        | Disposition                 |
| -------------- | ------------------------------------ | --------------------------- |
| Reference      | INO                                  | Mapped → columns 1, 2       |
| Content        | Subject, Body/Announcement, Att, Ext | Mapped → columns 4, 7, 9, 8 |
| Distribution   | Send (Recipients), CC                | Mapped → columns 5, 6       |
| Engagement     | CtrLst, LkLst, DslkLst, Viewed       | Mapped → columns 10–13      |
| Governance     | HRHOD, HR/DocAuthor                  | Mapped → columns 14, 15     |
| Lifecycle      | PublishedDate, LockDate, Lock        | Mapped → columns 16–18      |
| Workflow state | CurrentAction                        | Mapped → columns 19–20      |

---

## Workflow

### Summary

Simple 2-stage broadcast lifecycle: **Draft → Published → Auto-Locked**. No approval chain required.

### Stage Map

| Stage | Name      | Trigger                      | Actor        | Actions                                                                            | Next Stage | Notifications                                                |
| ----- | --------- | ---------------------------- | ------------ | ---------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------ |
| 1     | Draft     | Record created               | HR Author    | Compose notice, set recipients, attach media                                       | 2          | None                                                         |
| 2     | Published | HR Author clicks "Post"      | PA (auto)    | Set INO, set PublishedDate, set LockDate = +30 days, set CurrentStatus = Published | End        | All Recipients (send) + CC personalised email with deep-link |
| Auto  | Locked    | Scheduled — LockDate reached | PA scheduled | Set IsLocked = true, set CurrentStatus = Locked                                    | —          | None (silent lockdown)                                       |

### Power Automate Flows Required

| Flow                        | Trigger                                                  | Actions                                                                                                                                                                             |
| --------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HRINFO_OnPublish            | Item created/updated with CurrentAction = Publish        | Generate INO (HR-INF-YYMM-NNNN), set PublishedDate, set LockDate (+30d), set CurrentStatus = Published, send personalised email to each recipient in Recipients + CC with deep-link |
| HRINFO_OnEngage_Read        | HTTP trigger from Power App (staff clicks "Read")        | Increment ReadCount on MainDB_HR record                                                                                                                                             |
| HRINFO_OnEngage_Beneficial  | HTTP trigger from Power App (staff clicks "Beneficial")  | Append current user to BeneficialUsers                                                                                                                                              |
| HRINFO_OnEngage_Disseminate | HTTP trigger from Power App (staff clicks "Disseminate") | Append current user to DisseminateUsers                                                                                                                                             |
| HRINFO_OnView               | HTTP trigger from Power App (record opened)              | Increment TotalViews                                                                                                                                                                |
| HRINFO_AutoLock             | Scheduled daily — check LockDate                         | If LockDate ≤ Today and IsLocked = false, set IsLocked = true, set CurrentStatus = Locked                                                                                           |

---

## Screen Inventory

| Screen Name      | Purpose                                    | Key Controls                                                                                                         | Visible To          |
| ---------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | ------------------- |
| HRINFO_Feed      | Social-style newsfeed of published notices | Gallery/Carousel, filter by date, search by subject, engagement badges                                               | All staff           |
| HRINFO_Detail    | Immersive notice reading view              | Display form with Body, Attachment viewer, Engagement action buttons (Read / Beneficial / Disseminate), view counter | All staff           |
| HRINFO_New       | New notice composer                        | Edit form: Subject, Recipients, CC, Body (rich text editor), Attachment, ContactExt                                  | HR Authors only     |
| HRINFO_Analytics | Engagement analytics for HR management     | View count, Beneficial list, Disseminate list, Read count per notice                                                 | HR Managers / HRHOD |

---

## Navigation Map

```
HRINFO_Feed  ──[Open]──►  HRINFO_Detail
HRINFO_Feed  ──[New Notice]──►  HRINFO_New  ──[Post]──►  HRINFO_Feed
HRINFO_Feed  ──[Analytics]──►  HRINFO_Analytics
HRINFO_Detail  ──[Back]──►  HRINFO_Feed
```

---

## Role & Permission Matrix

| Role               | Description                                    | SharePoint Group    | PA Access               |
| ------------------ | ---------------------------------------------- | ------------------- | ----------------------- |
| HR Author          | Creates and posts notices; HR dept staff       | D05-HR-Editors      | Create / Edit (Stage 1) |
| HR Manager / HRHOD | Administrative governance owner                | D05-HR-Managers     | Edit / Admin oversight  |
| Staff Reader       | General workforce — receives and reads notices | All-staff AAD group | Read only (Stage 2)     |
| IT Admin           | System administrator                           | D02-IT-Admins       | Full control            |

---

## Related Lists / Dependencies

- Shared people lookup: Org Chart (ORGCHART form) provides group/team structure for `Recipients`
  (Send field) population — HR can select department or team groups from ORGCHART-derived lists.
- User Social Profile linkage: `BeneficialUsers` and `DisseminateUsers` store AAD identities for
  engagement analytics.
- No parent-child relationships.
- INO pattern: `HR-INF-[YY][MM]-[NNNN sequential]`.

---

## Migration Notes

- **Historical migration:** Migrate last 12 months of HRINFO records to `HR_HRINFO_List` staging
  only. Older records archived to static PDF library to maintain gallery performance.
- **Rich text:** Domino Body field is rich text. Power Apps does not natively render rich text input
  — implement as a `Multiple lines of text` (enhanced rich text) SharePoint column and use
  SharePoint's rich text editor via Power Apps HTML control or a formatted text control. Canvas YAML
  will use a `HtmlText` control for display.
- **Engagement actions** (Read / Beneficial / Disseminate) are triggered via HTTP Power Automate
  flows, not canvas-side collections, to ensure accurate multi-user concurrency.
- **Terminology:** Use "Beneficial" (not "Like") and "Disseminate" (not "Dislike") in the canvas
  labels — HR compliance neutrality requirement per HRINFO_analysis.md.
- **Lock behaviour:** `IsLocked = true` makes all edit controls in HRINFO_New/Detail hidden/disabled
  and removes the notice from the Active Feed carousel (filter: `CurrentStatus = "Published"`).
