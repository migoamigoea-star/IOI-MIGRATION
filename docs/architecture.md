# Technical Architecture

## Overview

This document describes the technical architecture for the IOI Migration Project, covering the Microsoft Dynamics 365 Business Central environment, custom AL extension design, data migration approach, and integration patterns.

---

## Environment Strategy

| Environment | Purpose |
|---|---|
| **Development** | AL extension development and unit testing |
| **Sandbox** | Integration testing, data migration dry runs, UAT |
| **Production** | Live business operations after go-live |

All environments run on Microsoft Dynamics 365 Business Central (cloud/SaaS or on-premises as determined during design phase).

---

## AL Extension Architecture

Custom extensions are developed using Microsoft's **AL (Application Language)** for Business Central. The extension architecture follows these principles:

- **Single Responsibility:** Each extension object (table, page, codeunit, etc.) has a clear, focused purpose.
- **Minimal Footprint:** Only necessary customizations are made; standard BC functionality is preserved wherever possible.
- **Event-Driven Patterns:** Business Central standard events and subscribers are used to hook into base application logic without modifying it.
- **Dependency Management:** Extension dependencies are declared in `app.json` and managed via `.alpackages`.

### Key Extension Objects

| Object Type | Usage |
|---|---|
| Table Extension | Extend standard BC tables with custom fields |
| Page Extension | Extend standard BC pages with custom UI |
| Codeunit | Encapsulate business logic |
| Report Extension | Custom reporting based on standard reports |
| XMLport | Data import/export interfaces |
| Enum Extension | Extend standard enumerations |

---

## Data Migration Architecture

Data migration follows a standard **Extract, Transform, Load (ETL)** approach:

```
Source System
     │
     ▼
[Extract]  ─── Export data from legacy system to flat files (CSV/XML)
     │
     ▼
[Transform] ── Map and cleanse data according to mapping rules
     │
     ▼
[Load]      ── Import into Business Central via XMLports, APIs, or RapidStart
     │
     ▼
[Validate]  ── Reconcile record counts, totals, and spot-check data
```

### Migration Objects

| Data Entity | Migration Method | Validation Method |
|---|---|---|
| Chart of Accounts | RapidStart / XMLport | Count + Balance check |
| Customers | RapidStart / XMLport | Count + Balance check |
| Vendors | RapidStart / XMLport | Count + Balance check |
| Items | RapidStart / XMLport | Count + Inventory value check |
| Open Transactions | Journal import via XMLport | Balance reconciliation |
| Historical Data | XMLport / Custom import | Sample-based spot-check |

---

## Integration Architecture

Where integrations with third-party systems are required, the following patterns are used:

- **REST API:** Business Central exposes OData and custom API pages for inbound/outbound data exchange.
- **Web Services:** SOAP-based web services may be used for legacy system compatibility.
- **Azure Integration Services:** For complex orchestration scenarios, Azure Logic Apps or Azure Service Bus may be used.

---

## Security Design

- User roles and permissions are configured using standard Business Central **Permission Sets**.
- Sensitive data is handled according to the organization's data governance policy.
- All AL extensions undergo code review to ensure no security vulnerabilities are introduced.

---

## Technology Stack

| Component | Technology |
|---|---|
| ERP Platform | Microsoft Dynamics 365 Business Central |
| Extension Language | AL (Application Language) |
| Development IDE | Visual Studio Code with AL Language extension |
| Version Control | Git (this repository) |
| CI/CD | GitHub Actions (as applicable) |
| Data Migration Tooling | RapidStart, XMLport, custom AL codeunits |

---

## References

- [Microsoft Dynamics 365 Business Central Documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/)
- [AL Language Documentation](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-programming-in-al)
- [Migration Plan](migration-plan.md)
- [Setup Guide](setup.md)
