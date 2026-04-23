# AI Agent Tester — Power Apps Canvas Apps

This directory contains the complete AI-powered testing framework for the IOI-MIGRATION Power Apps canvas apps. It combines the **Power Apps Test Engine** (functional test runner) with an **Azure OpenAI GPT-4o** agent layer for intelligent bug detection, visual regression analysis, and automatic test-case generation.

---

## Directory Layout

```
testing/
├── README.md                          ← this file
├── agent/
│   ├── ai_test_agent.py               ← main AI agent (Python)
│   ├── requirements.txt               ← Python dependencies
│   ├── config.yaml                    ← agent settings (env-specific values via env vars)
│   └── prompts/
│       ├── test_generator_prompt.txt  ← LLM prompt: auto-generate YAML test cases
│       └── bug_analyzer_prompt.txt    ← LLM prompt: analyse screenshots & logs for bugs
└── test-engine/
    ├── testconfig.json                ← Power Apps Test Engine global config
    └── tests/
        ├── common/
        │   └── baseline_tests.yaml    ← baseline navigation & load-time checks
        └── IOIP/
            └── testplan.yaml          ← full IOIP app test plan
```

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| .NET SDK | 8.0+ | Required to run Power Apps Test Engine |
| Power Apps Test Engine | latest | `dotnet tool install …` (see below) |
| Python | 3.11+ | For the AI agent script |
| Azure OpenAI resource | GPT-4o deployment | Set `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_KEY` |
| Power Platform CLI (`pac`) | latest | For environment / app auth |

---

## Quick Start

### 1. Install Power Apps Test Engine

```bash
dotnet tool install --global Microsoft.PowerApps.TestEngine \
  --add-source https://pkgs.dev.azure.com/PowerAppsTestEngine/PowerAppsTestEngine/_packaging/PowerAppsTestEngine/nuget/v3/index.json
```

### 2. Configure environment variables

Create a `.env` file (never commit it — it is in `.gitignore`):

```bash
# Power Platform / Entra ID
POWERAPPS_TENANT_ID=<your-tenant-id>
POWERAPPS_CLIENT_ID=<service-principal-client-id>
POWERAPPS_CLIENT_SECRET=<service-principal-secret>
POWERAPPS_ENVIRONMENT_URL=https://<your-env>.crm.dynamics.com

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Optional: Teams webhook for notifications
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
```

### 3. Install Python dependencies

```bash
cd testing/agent
pip install -r requirements.txt
```

### 4. Run tests against a specific app

```bash
# Run Power Apps Test Engine for the IOIP app
pac test run \
  --provider "Canvas" \
  --tenant "$POWERAPPS_TENANT_ID" \
  --environment-id "$POWERAPPS_ENVIRONMENT_ID" \
  --app-logical-name "ioip_app" \
  --test-plan-file testing/test-engine/tests/IOIP/testplan.yaml \
  --output-directory testing/results/IOIP

# Run the AI agent to analyse results
python testing/agent/ai_test_agent.py \
  --results-dir testing/results/IOIP \
  --blueprint IOIP_blueprint.md \
  --user-story user_stories/IOIP_user_story.md
```

### 5. Auto-generate additional test cases with the AI agent

```bash
python testing/agent/ai_test_agent.py \
  --mode generate \
  --blueprint IOIP_blueprint.md \
  --user-story user_stories/IOIP_user_story.md \
  --output testing/test-engine/tests/IOIP/generated_tests.yaml
```

---

## CI/CD Integration

The GitHub Actions workflow at `.github/workflows/powerapps-ai-tester.yml` runs automatically:

- **On every push / pull request** to `main` or any `feature/*` branch
- **On a nightly schedule** (00:00 UTC) against the TEST environment
- **On manual trigger** (`workflow_dispatch`) with configurable target environment and app

The workflow:
1. Runs Power Apps Test Engine for all apps that have a `testplan.yaml`
2. Uploads screenshots and assertion results as job artifacts
3. Invokes the AI agent to analyse results and screenshots
4. Posts a structured bug report as a PR comment (if run on a PR)
5. Sends a Teams notification on failure

---

## What the AI Agent Detects

| Category | Examples |
|----------|---------|
| Formula errors | `#Error`, division by zero, null reference in labels |
| Broken navigation | Screen fails to load, `Navigate()` targets missing screen |
| Required-field bypass | Submit succeeds with blank required fields |
| Field-lock violations | Approved/Archived record still editable |
| Delegation warnings | Gallery shows partial data due to delegation limit |
| Connector failures | API timeouts, 401/403 from SharePoint connector |
| Visual regressions | Overlapping controls, invisible buttons, empty galleries |
| Accessibility issues | Missing `AccessibleLabel`, low contrast detected in screenshot |
| Performance regressions | Screen load > 3 s baseline |

---

## Adding Tests for a New App

1. Copy `testing/test-engine/tests/IOIP/testplan.yaml` to `testing/test-engine/tests/<FORMCODE>/testplan.yaml`
2. Update `testSuiteName`, `appLogicalName`, and `testCases` to match the new app's user story
3. Run the AI generator to expand coverage:
   ```bash
   python testing/agent/ai_test_agent.py \
     --mode generate \
     --blueprint <FORMCODE>_blueprint.md \
     --user-story user_stories/<FORMCODE>_user_story.md \
     --output testing/test-engine/tests/<FORMCODE>/generated_tests.yaml
   ```
4. Commit both files; CI will pick them up automatically

---

## Secrets Required in GitHub Repository Settings

| Secret Name | Description |
|-------------|-------------|
| `POWERAPPS_TENANT_ID` | Entra ID tenant GUID |
| `POWERAPPS_CLIENT_ID` | Service principal / app registration client ID |
| `POWERAPPS_CLIENT_SECRET` | Service principal secret |
| `POWERAPPS_ENVIRONMENT_ID` | Power Platform environment ID |
| `POWERAPPS_ENVIRONMENT_URL` | Environment URL (e.g., `https://org.crm.dynamics.com`) |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI resource endpoint |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | GPT-4o deployment name (default: `gpt-4o`) |
| `TEAMS_WEBHOOK_URL` | (Optional) Incoming webhook for Teams notifications |
