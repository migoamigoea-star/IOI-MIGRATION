# Technical Blueprint: HEALTHINFO — Health & Title Information Broadcast

## Blueprint Status

| Status Label        | Value       |
| ------------------- | ----------- |
| Lifecycle Status    | VALIDATED   |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PASS        |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

---

## Form Identity

| Field                      | Value                                                        |
| -------------------------- | ------------------------------------------------------------ |
| Form Code                  | HEALTHINFO                                                   |
| Official Name              | Health & Title Information Broadcast                         |
| Department                 | HR                                                           |
| Module                     | HR Administration — Internal Communications                  |
| Site(s)                    | PRAI, JOHOR                                                  |
| Source PDF                 | Latest_Client_provided_file/PRAI_SITE_FORM/HR/HEALTHINFO.pdf |
| Domino Database            | PRAI site Domino source catalog (PDF-backed baseline)        |
| Official Name Claim Status | Claimed from source PDF title                                |
| Blueprint Version          | 1.0                                                          |
| Blueprint Date             | 2026-04-19                                                   |
| Architect                  | GitHub Copilot (Architect)                                   |

---

## Purpose

HEALTHINFO is an internal broadcast form allowing HR administrators to publish health-related
notices, policy title updates, and informational announcements to staff. There is no approval
workflow — only an admin-publish action that creates the record and notifies designated recipients.
The migrated solution must preserve the category-based routing, the send target selection,
attachment support, and the read-only broadcast experience for recipients.

---

## SharePoint Schema

**Target List:** MainDB_HR **Form Discriminator:** FormCode = "HEALTHINFO"

### Parent List: MainDB_HR (HEALTHINFO)

| #   | SP Internal Name | Display Label         | Column Type         | Required | Classification   | Source Mapping / Notes                               |
| --- | ---------------- | --------------------- | ------------------- | -------- | ---------------- | ---------------------------------------------------- |
| 1   | Title            | Title                 | Single line text    | Yes      | SYSTEM-COMPUTED  | HEALTHINFO prefix + Subject                          |
| 2   | FormCode         | Form Code             | Single line text    | Yes      | SYSTEM-COMPUTED  | Fixed value HEALTHINFO                               |
| 3   | Category         | Category              | Choice              | Yes      | USER-ENTERED     | `Category` — Health, Title, General, Policy          |
| 4   | SendTo           | Send To               | Person or Group     | Yes      | USER-ENTERED     | `Send` — recipients or group to notify               |
| 5   | Subject          | Subject               | Single line text    | Yes      | USER-ENTERED     | `Subject`                                            |
| 6   | Body             | Message Body          | Multiple lines text | Yes      | USER-ENTERED     | `Body` — HTML-capable announcement body              |
| 7   | Attachment       | Attachment            | Hyperlink           | No       | USER-ENTERED     | `Att` — optional supporting document                 |
| 8   | ExtensionInfo    | Extension / Reference | Single line text    | No       | USER-ENTERED     | `Ext` — phone/ext number or reference code           |
| 9   | PublishStatus    | Status                | Choice              | Yes      | WORKFLOW-MANAGED | Draft, Published                                     |
| 10  | Author           | Published By          | Person or Group     | Yes      | SYSTEM-COMPUTED  | `Author` — HR admin who published                    |
| 11  | DateSent         | Date Published        | Date and Time       | Yes      | SYSTEM-COMPUTED  | `DateSent`                                           |
| 12  | IsLocked         | Is Locked             | Yes/No              | No       | WORKFLOW-MANAGED | `Lock` — true after publish                          |
| 13  | CurrentAction    | Current Action        | Single line text    | No       | WORKFLOW-MANAGED | `CurrentAction` — internal workflow state descriptor |
| 14  | IsAdmin          | Is Admin              | Yes/No              | No       | USER-ENTERED     | `ISADMIN` — flag for admin-only visibility features  |
| 15  | EnvironmentTag   | Environment           | Choice              | Yes      | SYSTEM-COMPUTED  | DEV, TEST, PROD                                      |

---

## Workflow Stage Map

```
[HR Admin] → Create broadcast record (Draft)
      ↓ Publish
[System] → Notify recipients → Record locked (Published)
```

| Stage | Action            | Actor Role | SP Group       | Power Automate Trigger                                          |
| ----- | ----------------- | ---------- | -------------- | --------------------------------------------------------------- |
| 1     | Create & Publish  | HR Admin   | D05-HR-Manager | When Status='Draft' → HR Admin publishes                        |
| 2     | Notify Recipients | System     | —              | When Status changes to 'Published' → send email to SendTo group |

---

## Role Matrix

| Domino Group | SharePoint Group | SP Group Name  | Permissions                           |
| ------------ | ---------------- | -------------- | ------------------------------------- |
| HR Admins    | HR Manager       | D05-HR-Manager | Full Control (create + publish)       |
| All Staff    | HR Staff         | D05-HR-Staff   | Read Only (view published broadcasts) |

---

## Power Automate Actions

| Flow Name               | Trigger                            | Action                                                                      |
| ----------------------- | ---------------------------------- | --------------------------------------------------------------------------- |
| HR_HEALTHINFO_OnPublish | When Status changes to 'Published' | Send email to SendTo recipients with Subject, Body, Attachment; lock record |

---

## Screen Inventory

| Screen Name     | Type      | Purpose                                                         | Visible To                   |
| --------------- | --------- | --------------------------------------------------------------- | ---------------------------- |
| HEALTHINFO_List | Gallery   | List all published health/title broadcasts with category filter | D05-HR-Staff, D05-HR-Manager |
| HEALTHINFO_New  | Form      | Create and publish new broadcast                                | D05-HR-Manager only          |
| HEALTHINFO_View | Read-only | View full broadcast details with attachment                     | D05-HR-Staff, D05-HR-Manager |

---

## Navigation Map

```
HEALTHINFO_List → [New] → HEALTHINFO_New (Manager only)
HEALTHINFO_List → [View] → HEALTHINFO_View
```

---

## Migration Risks & Notes

1. **No approval workflow — admin-publish model:** HEALTHINFO is a one-step publish form. There are
   no approval stages. The only "workflow" is the publish action which triggers the notification
   flow. Craftsman must not add unnecessary approval buttons or stages.

2. **SendTo group vs individual selection:** The `Send` field in Domino may reference department
   groups or named individuals. In SharePoint, `Person or Group` column supports both. Ensure the
   flow reads this column and sends email to each selected person/group correctly.

3. **IsAdmin flag logic:** The `ISADMIN` column gates some features visible only to HR Admin users.
   In Power Fx, this should be driven by `D05-HR-Manager` membership check
   (`gblIsHRManager = Office365Users.MyProfile().userPrincipalName in ...`) rather than a field
   value.

4. **Body field HTML content:** Domino may store HTML in the `Body` field. SharePoint Multi-line
   text (Enhanced rich text) can store HTML, but Power Apps canvas `HtmlText` control is needed to
   render it properly. Verify with HR whether plain text is sufficient.

5. **Lock-on-publish:** Once published, the record should be read-only to prevent retroactive edits
   to distributed communications. `IsLocked = Yes` + conditional `DisplayMode` enforcement in canvas
   app ensures this.

---

## v3 Impossibilities

| Domino Feature                          | v3 Status  | Workaround                                                             |
| --------------------------------------- | ---------- | ---------------------------------------------------------------------- |
| Rich HTML body in Domino form           | LIMITED    | Use SharePoint Enhanced Rich Text column; render with HtmlText control |
| Group-based send with Domino directory  | NOT NATIVE | Use SharePoint Person/Group column; PA flow enumerates group members   |
| Admin-only view logic via ISADMIN field | NOT NATIVE | Replace with group membership check in gblIsHRManager variable         |

---

## Reference PDF

| Field          | Value                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| PDF Path       | Latest_Client_provided_file/PRAI_SITE_FORM/HR/HEALTHINFO.pdf                                                           |
| Page Count     | 2                                                                                                                      |
| Field Evidence | Category, Send, Subject, Body, Att, Ext, Status, Author, DateSent, Lock, CurrentAction, ISADMIN — all confirmed in PDF |

---

## Architect Verification Checklist

- [x] Form Identity table: all 11 fields populated with non-placeholder values
- [x] Purpose: 1–3 sentence business narrative present
- [x] SharePoint Schema: parent list (15 columns) — no child tables required
- [x] Workflow Stage Map: ASCII diagram + formal trigger-condition table present (simple 2-step)
- [x] Role Matrix: all roles mapped to D05-HR-[Role] SharePoint groups
- [x] Power Automate Actions: 1 flow named with HR*HEALTHINFO*[EventName] convention
- [x] Screen Inventory: 3 screens listed with visibility rules
- [x] Navigation Map: screen flow documented
- [x] Migration Risks & Notes: 5 risks with mitigations
- [x] v3 Impossibilities: 3 items documented with workarounds
- [x] Reference PDF: path, page count, field evidence confirmed
- [x] Zero unresolved markers present in document
- [x] Blueprint Status section present and correctly populated

**COMPLETION STATUS: COMPLETE**

---

## Sentinel Validation Report

**Validation Date:** 2026-04-19  
**Validator Agent:** Sentinel v1.1  
**Blueprint:** HEALTHINFO (HR)  
**Input Status:** COMPLETE

### Validation Results

| Check # | Validation Item                 | Status  | Evidence / Comment                           |
| ------- | ------------------------------- | ------- | -------------------------------------------- |
| 1       | Form Identity table present     | ✅ PASS | Required identity fields present             |
| 2       | Section order compliance        | ✅ PASS | Canonical blueprint section order maintained |
| 3       | Workflow Stage Map formal table | ✅ PASS | Stage/action table present                   |
| 4       | Role Matrix mapped to SP groups | ✅ PASS | D05-HR role mappings present                 |
| 5       | Domino field mappings           | ✅ PASS | Schema and field evidence documented         |
| 6       | Marker gate status              | ✅ PASS | check-markers.sh exit code 0                 |

### Validation Verdict

**GATE STATUS:** ✅ **PASS** — Blueprint meets all compliance requirements. Ready for Craftsman
dispatch.

---

**Sentinel Signature:** Sentinel v1.1 — 2026-04-19T08:59:10Z
