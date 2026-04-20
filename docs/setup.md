# Developer Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Download |
|---|---|---|
| [Visual Studio Code](https://code.visualstudio.com/) | Latest | https://code.visualstudio.com/ |
| [AL Language Extension](https://marketplace.visualstudio.com/items?itemName=ms-dynamics-smb.al) | Latest | VS Code Marketplace |
| [Git](https://git-scm.com/) | 2.x+ | https://git-scm.com/ |
| Access to Business Central Sandbox | — | Provided by project admin |

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/migoamigoea-star/IOI-MIGRATION.git
cd IOI-MIGRATION
```

### 2. Open in Visual Studio Code

```bash
code .
```

### 3. Configure the AL Language Extension

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Run **AL: Go!** to create a new AL project, or open the existing workspace
3. Edit `.vscode/launch.json` to point to your Business Central sandbox:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Your own server",
      "type": "al",
      "request": "launch",
      "environmentType": "Sandbox",
      "environmentName": "<your-sandbox-environment-name>",
      "startupObjectId": 22,
      "startupObjectType": "Page",
      "breakOnError": "All",
      "launchBrowser": true,
      "tenant": "<your-tenant-id>"
    }
  ]
}
```

> **Note:** `launch.json` is excluded from version control via `.gitignore` since it contains environment-specific settings.

### 4. Download Symbols

1. Open the Command Palette
2. Run **AL: Download Symbols**

This will download the Business Central base application symbols into the `.alpackages` folder (also excluded from version control).

### 5. Build the Extension

Press `Ctrl+Shift+B` (or `Cmd+Shift+B`) to build the extension. The compiled `.app` file will be placed in the `.output` folder (excluded from version control).

### 6. Publish and Deploy

Press `F5` to publish and deploy the extension to your configured sandbox environment.

---

## Project Structure

```
IOI-MIGRATION/
├── docs/                    # Project documentation (this folder)
├── .gitignore               # Files excluded from version control
└── README.md                # Project overview
```

> AL source files (`.al`), `app.json`, and other extension source files will be added as development progresses.

---

## Coding Standards

- Follow [Microsoft AL coding guidelines](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-al-code-guidelines)
- Use **PascalCase** for object names and variable names
- All custom objects must use the assigned object ID range for this project
- Add XML documentation comments to all public procedures
- All changes must be reviewed via pull request before merging to `main`

---

## Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready code |
| `develop` | Integration branch for ongoing development |
| `feature/<name>` | Individual feature or task branches |
| `bugfix/<name>` | Bug fix branches |

---

## Troubleshooting

**Symbols not downloading?**
- Verify your `launch.json` is correctly configured with valid tenant and environment details
- Ensure you are authenticated to your Microsoft 365 tenant in VS Code

**Build errors?**
- Run **AL: Download Symbols** again to refresh
- Check that your object IDs are within the allocated range for this project

**Extension not publishing?**
- Confirm the sandbox environment is running and accessible
- Check the AL output panel in VS Code for detailed error messages

---

## References

- [AL Language Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-dynamics-smb.al)
- [Business Central Developer Docs](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/)
- [Architecture Overview](architecture.md)
