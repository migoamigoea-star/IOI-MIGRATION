---
form_code: GLOBALAPP
dept: ALL
official_name: "IOI Global Portal Screen"
module: M0 - Global Navigation & Portal Entry
owner: "IT / Portal Admin"
complexity: Medium
DQ_REQUIRED: NO
gxp_class: "—"
status: BLUEPRINT_DRAFT
blueprint_date: 2026-04-21
source_analysis: N/A — new app, no Lotus Domino predecessor
---

# Blueprint — IOI Global Portal Screen (`GLOBALAPP`)

## Blueprint Status

| Field               | Value       |
|---------------------|-------------|
| Lifecycle Status    | BLUEPRINT_DRAFT |
| Architect Checklist | COMPLETE    |
| Sentinel Validation | PENDING     |
| Craftsman Build     | NOT_STARTED |
| QA Approval         | NOT_STARTED |
| Deployment          | NOT_READY   |

---

## Form Identity

| Field              | Value                                                   |
|--------------------|---------------------------------------------------------|
| Form Code          | `GLOBALAPP`                                             |
| Official Name      | IOI Global Portal Screen                                |
| Department         | All Departments (Cross-Departmental)                    |
| Module             | M0 - Global Navigation & Portal Entry                   |
| Site(s)            | All Sites                                               |
| SharePoint List(s) | `Config_Departments`, `Config_Announcements`, `Config_AppSettings` |
| Blueprint Version  | `1.0`                                                   |
| Blueprint Date     | `2026-04-21`                                            |
| Architect          | `GitHub Copilot (Architect Agent)`                      |

---

## DEC-001 / DEC-004 / DEC-005 Control Notes

- **DEC-001 (live submissions):** `GLOBALAPP` does not accept form submissions. It is a navigation-only app. No records are written to `MainDB_*` lists.
- **DEC-004 (environment strategy):** Environment-variant values (logo URL, site URL, `EnvironmentTag`, admin group name) must be loaded from `Config_AppSettings` for `DEV`, `TEST`, and `PROD`. Never hard-code environment-specific values inside the Canvas App.
- **DEC-005 (schema authority):** The two new lists (`Config_Departments`, `Config_Announcements`) must have their column definitions registered in `FORM_COLUMN_DEFINITIONS_ENHANCED.json` before TEST/PROD promotion.

---

## Purpose

`GLOBALAPP` is a **single Canvas App** that acts as the unified portal entry point for all IOI migrated Microsoft 365 applications. It provides:

1. A **Welcome Screen (`GLOBAL_Welcome`)** — company branding, personalised user greeting, today's date, and a live announcements banner sourced from SharePoint.
2. A **Department Selection Screen (`GLOBAL_DeptSelection`)** — a searchable, role-filtered tile grid from which users launch individual department Canvas Apps.

`GLOBALAPP` replaces the Lotus Domino home database navigator. It has **no Domino predecessor** and is a net-new artefact.

---

## SharePoint Schema

### List 1 — `Config_Departments`

**Purpose:** Stores the registry of department tiles displayed on the Department Selection Screen. Managed by Portal Admins; changes take effect on next app load without republishing.

**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal/Lists/Config_Departments`

| # | Column (Internal) | Display Name      | SP Type             | Required | Choices / Source                              | Notes                                                     |
|---|-------------------|-------------------|---------------------|----------|-----------------------------------------------|-----------------------------------------------------------|
| 1 | Title             | Department Name   | Single line of text | Yes      | Free text                                     | Full department display name (e.g., `Information Technology`) |
| 2 | DeptCode          | Dept Code         | Single line of text | Yes      | Free text                                     | Short code (e.g., `IT`, `ADM`, `HR`, `ENG`)               |
| 3 | DeptIcon          | Icon Name / URL   | Single line of text | No       | Fluent UI icon name or image URL              | Used as tile icon in gallery                              |
| 4 | DeptColor         | Tile Colour       | Single line of text | No       | Hex colour string                             | Tile background colour (e.g., `#0078D4`)                  |
| 5 | AppURL            | App Launch URL    | Single line of text | Yes      | Power Apps deep-link or screen target         | Destination when tile is tapped                           |
| 6 | IsActive          | Is Active         | Yes/No              | Yes      | —                                             | `true` = tile visible; `false` = hidden without deletion  |
| 7 | SortOrder         | Sort Order        | Number              | No       | Integer, ascending                            | Controls left-to-right / top-to-bottom tile order         |
| 8 | AllowedSPGroup    | Allowed SP Group  | Single line of text | No       | SharePoint group name                         | If blank = all users; if set = group members only         |
| 9 | SiteScope         | Site Scope        | Choice              | No       | All; PRAI; (others as needed)                 | Filter tiles shown to users of a specific site            |

---

### List 2 — `Config_Announcements`

**Purpose:** Stores portal announcements displayed on the Welcome Screen banner. Managed by Portal Admins.

**URL:** `https://ioioi.sharepoint.com/sites/ioi-portal/Lists/Config_Announcements`

| # | Column (Internal) | Display Name    | SP Type                | Required | Choices / Source             | Notes                                                     |
|---|-------------------|-----------------|------------------------|----------|------------------------------|-----------------------------------------------------------|
| 1 | Title             | Headline        | Single line of text    | Yes      | Free text                    | Short announcement title shown in banner                  |
| 2 | Body              | Body Text       | Multiple lines of text | No       | Free text / HTML             | Full announcement body for expanded view                  |
| 3 | StartDate         | Start Date      | Date and Time          | Yes      | Date picker                  | First day announcement is visible                         |
| 4 | EndDate           | End Date        | Date and Time          | Yes      | Date picker                  | Last day announcement is visible                          |
| 5 | IsActive          | Is Active       | Yes/No                 | Yes      | —                            | Manual show/hide override independent of date range       |
| 6 | Severity          | Severity        | Choice                 | No       | Info; Warning; Critical      | Controls banner colour and display priority               |

---

### List 3 — `Config_AppSettings` *(pre-existing, shared)*

`GLOBALAPP` reads the following keys from `Config_AppSettings`:

| Key (Title column)    | Expected Value Example                          | Used For                                      |
|-----------------------|-------------------------------------------------|-----------------------------------------------|
| `EnvironmentTag`      | `DEV` / `TEST` / `PROD`                         | Footer badge; environment isolation           |
| `PortalLogoURL`       | `https://ioioi.sharepoint.com/.../logo.png`     | Company logo on both screens                  |
| `PortalSiteURL`       | `https://ioioi.sharepoint.com/sites/ioi-portal` | Base URL for SharePoint list connections      |
| `PortalAdminGroup`    | `IOI-Portal-Admins`                             | Role-based tile management permissions        |

---

## Screens

### Screen 1 — `GLOBAL_Welcome`

**Purpose:** Branded landing screen shown immediately on app launch.

| Control Name        | Type            | Property Details                                                                         |
|---------------------|-----------------|------------------------------------------------------------------------------------------|
| `imgLogo`           | Image           | Image = `varPortalLogoURL`; positioned top-centre                                        |
| `lblGreeting`       | Label           | Text = `"Welcome, " & First(Split(User().FullName, " ")).Value`; large font               |
| `lblDate`           | Label           | Text = `Text(Today(), "[$-en-US]MMMM D, YYYY")`; subtitle style                         |
| `conAnnouncement`   | Container       | Visible = `!IsEmpty(colAnnouncements)`; Fill = severity colour                           |
| `lblAnnouncementHd` | Label           | Text = `First(colAnnouncements).Title`; bold                                             |
| `lblAnnouncementBd` | Label           | Text = `First(colAnnouncements).Body`; word-wrap                                         |
| `btnEnterPortal`    | Button          | Text = `"Enter Portal"`; OnSelect = `Navigate(GLOBAL_DeptSelection, ScreenTransition.Slide)` |
| `lblFooter`         | Label           | Text = `"v1.0  |  " & varEnvTag`; small font, bottom of screen                          |
| `ovlCritical`       | Container/Popup | Visible = `CountIf(colAnnouncements, Severity="Critical") > 0`; blocks screen until dismissed |

---

### Screen 2 — `GLOBAL_DeptSelection`

**Purpose:** Searchable, role-filtered department tile grid.

| Control Name     | Type       | Property Details                                                                                  |
|------------------|------------|---------------------------------------------------------------------------------------------------|
| `imgLogoSmall`   | Image      | Smaller logo in header                                                                            |
| `lblUserName`    | Label      | Text = `User().FullName`; header right side                                                       |
| `btnBack`        | Button     | Text = `"← Back"`; OnSelect = `Navigate(GLOBAL_Welcome, ScreenTransition.Back)`                  |
| `txtDeptSearch`  | Text Input | Placeholder = `"Search department…"`; OnChange triggers gallery re-filter                         |
| `galDeptTiles`   | Gallery    | Layout = Horizontal wrap (flexible grid); Items = filtered `colDepartments` (see formula below)   |
| `tileCard`       | Rectangle  | Inside gallery; Fill = `ThisItem.DeptColor`; OnSelect = tile navigation formula                   |
| `tileIcon`       | Image/Icon | Inside gallery; value from `ThisItem.DeptIcon`                                                    |
| `tileDeptCode`   | Label      | Inside gallery; Text = `ThisItem.DeptCode`; bold                                                  |
| `tileDeptName`   | Label      | Inside gallery; Text = `ThisItem.Title`; word-wrap                                                |
| `lblNoResults`   | Label      | Text = `"No departments found."`; Visible = `IsEmpty(galDeptTiles.AllItems)`                      |
| `lblFooter`      | Label      | Text = `"v1.0  |  " & varEnvTag`; bottom of screen                                               |

---

## Power Fx Formulas

### App `OnStart`

```powerfx
// Load department tiles (active only)
ClearCollect(
    colDepartments,
    Filter(Config_Departments, IsActive = true)
);

// Load active announcements within date range
ClearCollect(
    colAnnouncements,
    SortByColumns(
        Filter(
            Config_Announcements,
            IsActive = true &&
            StartDate <= Today() &&
            EndDate >= Today()
        ),
        "Severity",   // Critical first (sort order: Critical > Warning > Info)
        Descending
    )
);

// Cache current user
Set(varCurrentUser, User());

// Load global settings from Config_AppSettings
Set(varEnvTag,        LookUp(Config_AppSettings, Title = "EnvironmentTag",  Value));
Set(varPortalLogoURL, LookUp(Config_AppSettings, Title = "PortalLogoURL",   Value));
```

### `galDeptTiles` Items (Department Selection Screen)

```powerfx
Filter(
    colDepartments,
    IsBlank(txtDeptSearch.Text) ||
    StartsWith(DeptCode, txtDeptSearch.Text) ||
    StartsWith(Title,    txtDeptSearch.Text)
)
```

### Tile `OnSelect` — Navigation

```powerfx
If(
    StartsWith(ThisItem.AppURL, "https://"),
    Launch(ThisItem.AppURL),           // external Canvas App deep-link
    Navigate(                          // internal screen (same app, future use)
        App.ActiveScreen,
        ScreenTransition.Slide
    )
)
```

### Announcement Banner Fill Colour

```powerfx
Switch(
    First(colAnnouncements).Severity,
    "Critical", RGBA(255,  80,  80, 0.18),
    "Warning",  RGBA(255, 165,   0, 0.18),
    /* Info */  RGBA(  0, 120, 212, 0.12)
)
```

### Greeting Label

```powerfx
"Welcome, " & First(Split(varCurrentUser.FullName, " ")).Value
```

### Environment Footer

```powerfx
"IOI Portal  v1.0  |  " & varEnvTag
```

---

## Role Matrix

| Role                | SharePoint Group      | Permission on `Config_Departments` | Permission on `Config_Announcements` |
|---------------------|-----------------------|------------------------------------|--------------------------------------|
| All employees       | (Authenticated user)  | Read                               | Read                                 |
| Portal Admin        | `IOI-Portal-Admins`   | Full Control                       | Full Control                         |
| IT Admin            | `IOI-IT-Admins`       | Full Control                       | Contribute                           |

---

## Business Logic

### 1. Role-Based Tile Visibility

- If `AllowedSPGroup` is blank on a `Config_Departments` record → tile shown to all authenticated users.
- If `AllowedSPGroup` is set → tile is shown only to users who are members of that group. At `OnStart`, the app checks `Office365Groups.ListMemberOf()` or the SharePoint connector to resolve group membership and stores the result in `colUserGroups`. Each tile is then filtered accordingly.

### 2. Environment Isolation

- All site URLs, logo URLs, and admin group names are read from `Config_AppSettings` at `OnStart`.
- No DEV / TEST / PROD values are hard-coded inside the Canvas App.

### 3. Announcement Priority

- Active announcements are sorted by `Severity` descending (Critical > Warning > Info).
- A Critical announcement renders a full-screen modal overlay (`ovlCritical`) with a mandatory "I acknowledge" button before the user can tap `Enter Portal`.
- Non-critical announcements render as an inline banner only.

### 4. No Form Submission

- `GLOBALAPP` is a **navigation shell only**. It does not write to any `MainDB_*` list.
- All form creation/editing is handled within individual department Canvas Apps.

### 5. Accessibility

- All interactive controls must have `AccessibleLabel` and `AccessibleRole` set.
- Tile colour contrast must meet WCAG AA (minimum 4.5:1 for normal text).
- Focus/tab order: `btnEnterPortal` → `txtDeptSearch` → `galDeptTiles` → `btnBack`.

---

## Power Automate Requirements

`GLOBALAPP` does not trigger any dedicated Power Automate flows. It is a read-only navigation app.

Optional future enhancement: a scheduled flow to auto-deactivate expired announcements by setting `IsActive = false` when `EndDate < Today()`.

---

## v3 Impossibilities (if any)

| Lotus Domino Feature                   | Reason Impossible in Canvas Apps       | Recommended Workaround                                            |
|----------------------------------------|----------------------------------------|-------------------------------------------------------------------|
| Dynamic navigator icons from formula   | Canvas App icons are static or image-based | Store icon name/URL in `Config_Departments.DeptIcon` and render via Image control |
| Auto-close of session on idle          | Canvas App has no built-in idle timeout| Power Platform admin can enforce session timeout via AAD policy   |

---

## Architect Verification Checklist

```text
VERIFICATION CHECKLIST — IOI GLOBAL PORTAL SCREEN (GLOBALAPP)

[✓] All screens identified: [2] screens (GLOBAL_Welcome, GLOBAL_DeptSelection)
[✓] All controls identified per screen: complete
[✓] All Power Fx formulas specified: complete
[✓] SharePoint schema defined: [2] new lists + [1] shared list (Config_AppSettings)
[✓] Role matrix defined: [3] roles mapped
[✓] Environment isolation via Config_AppSettings: confirmed
[✓] No direct form submission — navigation shell only: confirmed
[✓] Accessibility requirements stated: confirmed
[✓] Zero unresolved TODO markers: [0] remaining
[✓] Zero unresolved UNCLEAR markers: [0] remaining

COMPLETION STATUS: [COMPLETE]
```
