# User Story — IOI Global Screen App (`GLOBALAPP`)

> **Department:** All Departments (Cross-Departmental)
> **Module:** M0 - Global Navigation & Portal Entry
> **Site(s):** All Sites (PRAI, and others)
> **SharePoint List:** `Config_AppSettings`
> **Form Code:** `GLOBALAPP`

---

## 1. App Overview & Purpose

`GLOBALAPP` is a single Canvas App that serves as the **global portal entry point** for all IOI migrated applications hosted in Microsoft 365 (Power Apps + SharePoint Online). It replaces the Lotus Domino home database navigator by providing:

1. A **Welcome Screen** — branding, user greeting, announcements, and quick links.
2. A **Department Selection Screen** — a tile/card grid listing every department, allowing users to drill into the department's available forms and apps.

All other Canvas Apps (e.g., `SRS`, `IOIP`, `ITI`, etc.) are launched from this global app via deep links or `Launch()` / `Navigate()` calls.

---

## 2. User Stories

**US-01: View welcome screen on app launch**
> As an **authenticated IOI employee**,
> I want to see a branded welcome screen when I open the IOI portal,
> So that I know I am in the correct application and can see my name, today's date, and any active announcements.
>
> *Trigger:* On app start (`OnStart`)

**US-02: Select a department to view its apps**
> As an **authenticated IOI employee**,
> I want to browse a grid of department tiles on the Department Selection Screen,
> So that I can quickly navigate to the department whose forms I need to access.
>
> *Trigger:* User taps "Enter Portal" button on Welcome Screen or navigates directly to the Department Selection Screen.

**US-03: Search / filter departments**
> As a **power user with access to multiple departments**,
> I want to type a department name or code into a search box on the Department Selection Screen,
> So that I can find the right department tile without scrolling through all tiles.
>
> *Trigger:* User types in `txtDeptSearch` text input.

**US-04: Launch a department app from the portal**
> As an **authenticated IOI employee**,
> I want to tap a department tile and be taken to that department's app list or directly into the correct Canvas App,
> So that I do not need to remember individual app URLs or use the Power Apps home page.
>
> *Trigger:* User taps a department tile card.

**US-05: View only departments I am authorised to access**
> As an **employee with restricted department access**,
> I want to see only the department tiles I am a member of,
> So that I am not confused by tiles for departments I cannot use.
>
> *Trigger:* App start — tiles are filtered by current user's Azure AD group membership (read from `Config_AppSettings`).

**US-ADMIN: Manage department tile configuration**
> As a **Portal Administrator** (member of `IOI-Portal-Admins`),
> I want to add, edit, or hide department tiles via the `Config_Departments` SharePoint list,
> So that the portal stays up to date without requiring an app republish.
>
> *Trigger:* Admin updates `Config_Departments` list; changes reflect on next app load.

**US-ANNOUNCE: Display active announcements**
> As an **authenticated IOI employee**,
> I want to see active announcements on the Welcome Screen (e.g., system maintenance, new form releases),
> So that I am informed of important updates before diving into my work.
>
> *Trigger:* On Welcome Screen load — reads `Config_Announcements` list filtered by `IsActive = true`.

---

## 3. SharePoint List Requirements

### 3a. `Config_Departments` — Department Tile Registry

| Column Name      | SP Type             | Required | Notes                                                             |
| ---------------- | ------------------- | -------- | ----------------------------------------------------------------- |
| Title            | Single line of text | Yes      | Department display name (e.g., `Information Technology`)         |
| DeptCode         | Single line of text | Yes      | Short code (e.g., `IT`, `ADM`, `HR`)                              |
| DeptIcon         | Single line of text | No       | Fluent UI icon name or image URL for tile icon                    |
| DeptColor        | Single line of text | No       | Hex colour string for tile background (e.g., `#0078D4`)           |
| AppURL           | Single line of text | Yes      | Power Apps deep-link URL or navigate target screen name           |
| IsActive         | Yes/No              | Yes      | `true` = tile visible in portal                                   |
| SortOrder        | Number              | No       | Display order in tile grid (ascending)                            |
| AllowedSPGroup   | Single line of text | No       | SP group name; if set, tile only shown to members of this group   |
| SiteScope        | Choice              | No       | All; PRAI; etc. — used to filter tiles by site if multi-site app  |

### 3b. `Config_Announcements` — Portal Announcements

| Column Name  | SP Type                | Required | Notes                                           |
| ------------ | ---------------------- | -------- | ----------------------------------------------- |
| Title        | Single line of text    | Yes      | Announcement headline                           |
| Body         | Multiple lines of text | No       | Full announcement text (plain text or HTML)     |
| StartDate    | Date and Time          | Yes      | First date the announcement is shown            |
| EndDate      | Date and Time          | Yes      | Last date the announcement is shown             |
| IsActive     | Yes/No                 | Yes      | Manual override to show/hide                    |
| Severity     | Choice                 | No       | Info; Warning; Critical                         |

### 3c. `Config_AppSettings` — Environment & Global Settings

*(Shared cross-app settings list; pre-existing. `GLOBALAPP` reads `EnvironmentTag`, portal branding values, and group names from this list.)*

---

## 4. Screen Requirements

| Screen                  | Purpose                                                       | Visible To             |
| ----------------------- | ------------------------------------------------------------- | ---------------------- |
| `GLOBAL_Welcome`        | Landing screen with company branding, user greeting, and announcements | All authenticated users |
| `GLOBAL_DeptSelection`  | Department tile grid with search/filter and navigation actions | All authenticated users (filtered by group membership) |

### Screen Interaction Details

**GLOBAL_Welcome Screen**
- Company logo displayed prominently (loaded from `Config_AppSettings` or asset library).
- Personalised greeting: *"Welcome, [First Name]"* using `User().FullName`.
- Current date displayed.
- Announcement banner (if `Config_Announcements` has active records): shows latest active announcement with severity colour coding (Info = blue, Warning = amber, Critical = red).
- `Enter Portal` button navigates to `GLOBAL_DeptSelection` with slide transition.
- Footer shows app version and environment tag (DEV / TEST / PROD).

**GLOBAL_DeptSelection Screen**
- Header: company logo + logged-in user name + `Back` button to return to `GLOBAL_Welcome`.
- `txtDeptSearch` text input for live filtering of tiles by `DeptCode` or `Title`.
- Responsive tile gallery (`galDeptTiles`): each tile shows `DeptIcon`, `DeptCode`, and `Title`.
- Tile tap action: `Launch(AppURL)` or `Navigate()` to the selected department's app.
- Tiles filtered by `IsActive = true` and (if `AllowedSPGroup` is set) current user's group membership.
- Empty-state label shown when no tiles match the search text.

---

## 5. Formula Requirements (Power Fx)

### 1. On App Start — Load Configuration

```powerfx
// App OnStart: load departments and announcements into collections
ClearCollect(
    colDepartments,
    Filter(Config_Departments, IsActive = true)
);
ClearCollect(
    colAnnouncements,
    Filter(
        Config_Announcements,
        IsActive = true &&
        StartDate <= Today() &&
        EndDate >= Today()
    )
);
Set(varCurrentUser, User());
Set(varEnvTag, LookUp(Config_AppSettings, Key = "EnvironmentTag", Value));
```

### 2. Personalised Greeting

```powerfx
// Label Text on GLOBAL_Welcome
"Welcome, " & First(Split(varCurrentUser.FullName, " ")).Value
```

### 3. Announcement Banner Visibility & Colour

```powerfx
// Announcement container Visible
!IsEmpty(colAnnouncements)

// Announcement banner Fill colour
Switch(
    First(colAnnouncements).Severity,
    "Critical", RGBA(255, 0, 0, 0.15),
    "Warning",  RGBA(255, 165, 0, 0.15),
    /* Info */  RGBA(0, 120, 212, 0.10)
)
```

### 4. Department Gallery Filter (Search)

```powerfx
// galDeptTiles Items formula
Filter(
    colDepartments,
    IsBlank(txtDeptSearch.Text) ||
    StartsWith(DeptCode, txtDeptSearch.Text) ||
    StartsWith(Title,    txtDeptSearch.Text)
)
```

### 5. Department Tile Navigation

```powerfx
// Tile OnSelect
If(
    StartsWith(ThisItem.AppURL, "https://"),
    Launch(ThisItem.AppURL),
    Navigate(App.ActiveScreen, ScreenTransition.None)   // replaced per actual target
)
```

### 6. Environment Tag Badge

```powerfx
// Footer label
"v1.0  |  " & varEnvTag
```

---

## 6. Business Logic Requirements

### 1. Role-Based Tile Visibility

- If `Config_Departments.AllowedSPGroup` is blank, the tile is visible to **all** authenticated users.
- If `AllowedSPGroup` is set, the tile is only shown to users who are members of that SharePoint group. Group membership is resolved at `OnStart` by checking the user's groups via the SharePoint connector.

### 2. Environment Isolation

- The `EnvironmentTag` value from `Config_AppSettings` must be displayed in the app footer.
- All SharePoint list connections must point to environment-specific site URLs loaded from `Config_AppSettings` (never hard-coded).

### 3. Announcement Priority

- Only **active** announcements (`IsActive = true`, within `StartDate`–`EndDate`) are displayed.
- If multiple announcements are active, the highest-severity one is shown first.
- Critical announcements are shown with a dismissible modal overlay on the Welcome Screen before the user can proceed.

### 4. No Direct Form Launch from Welcome Screen

- The Welcome Screen does **not** link directly to individual forms. All form navigation must pass through `GLOBAL_DeptSelection` to ensure consistent access control and tile filtering.

### 5. Accessibility

- All tile colours must meet WCAG AA contrast ratios.
- Tab order must be logical: Search → Tiles (left-to-right, top-to-bottom) → Back button.
- Screen reader labels (`AccessibleLabel`) must be set on all interactive controls.

---

## 7. Acceptance Criteria

- [ ] `Config_Departments` SharePoint list is created with all required columns.
- [ ] `Config_Announcements` SharePoint list is created with all required columns.
- [ ] `GLOBAL_Welcome` screen shows company logo, personalised greeting, date, and announcements.
- [ ] `GLOBAL_DeptSelection` screen shows all active, authorised department tiles.
- [ ] Search/filter in `GLOBAL_DeptSelection` filters tiles in real time.
- [ ] Tapping a tile launches the correct department app or navigates to the correct screen.
- [ ] Users without access to a department's SP group do not see that department's tile.
- [ ] `EnvironmentTag` is displayed correctly in the app footer (DEV / TEST / PROD).
- [ ] Critical announcements display a modal overlay before the user can enter the portal.
- [ ] App loads within 3 seconds on a standard corporate network (collections pre-loaded at `OnStart`).
- [ ] All controls have `AccessibleLabel` values set for screen reader support.
