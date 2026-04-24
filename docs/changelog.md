# Changelog

All notable changes to the IOI Migration Project documentation will be recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Initial project documentation structure
- `README.md` — project overview, table of contents, and documentation index
- `docs/overview.md` — project objectives, scope, stakeholders, and key milestones
- `docs/migration-plan.md` — phased migration approach with tasks and deliverables for each phase
- `docs/architecture.md` — technical architecture covering AL extensions, data migration ETL approach, integrations, and technology stack
- `docs/setup.md` — developer environment setup guide for AL development in VS Code
- `docs/changelog.md` — this file

---

## How to Update This Changelog

When making changes to the project documentation or codebase:

1. Add an entry under `[Unreleased]` describing your change
2. Use one of the following change categories:
   - **Added** — new documents, features, or content
   - **Changed** — updates to existing content
   - **Deprecated** — content that will be removed in the future
   - **Removed** — content that has been removed
   - **Fixed** — corrections to errors or inaccuracies
3. When a version is released, move the `[Unreleased]` entries under a new version heading with the date:

```markdown
## [1.0.0] — YYYY-MM-DD
```
