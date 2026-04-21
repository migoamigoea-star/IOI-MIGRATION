# SII User Stories

## Workflow Stories
- As a Requestor, I want to Submit stock item inclusion request, so that the workflow progresses to HOD.
- As a HOD, I want to Approve/reject business need, so that the workflow progresses to Materials.
- As a Materials, I want to Approve/reject materials suitability, so that the workflow progresses to Finance.
- As a Finance, I want to Approve/reject cost and control, so that the workflow progresses to ED.
- As a ED, I want to Final executive decision, so that the workflow progresses to Master Data Completion.
- As a Master Data Team, I want to Complete warehouse/MRP/accounting and assign material code, so that the workflow progresses to Closed.
- As a Requestor/Approver, I want to Discard route, so that the workflow progresses to Discarded.

## Screen Stories
- As a STR users and reviewers, I want to use SII_List, so that Search and filter SII requests.
- As a Requestor, I want to use SII_New, so that New inclusion request.
- As a Authorized users, I want to use SII_View, so that Read-only request details and approvals.
- As a Requestor, I want to use SII_Edit, so that Draft/returned edits.
- As a HOD, Materials, Finance, ED, I want to use SII_Approval, so that Multi-stage review actions.
- As a Master Data Team, I want to use SII_Completion, so that Master data completion and code issuance.

## Role Stories
- As a Requestor, I want Contribute access via D13-STR-Users, so that I can complete my responsibilities.
- As a HOD Reviewer, I want Contribute access via D13-STR-HOD-Reviewers, so that I can complete my responsibilities.
- As a Materials Reviewer, I want Contribute access via D13-STR-Materials, so that I can complete my responsibilities.
- As a Finance Reviewer, I want Contribute access via D13-STR-Finance, so that I can complete my responsibilities.
- As a Executive Approver, I want Contribute access via D13-STR-Executive-Approvers, so that I can complete my responsibilities.
- As a Master Data Team, I want Contribute access via D13-STR-MasterData, so that I can complete my responsibilities.
- As a Admin, I want Full Control access via D13-STR-Admins, so that I can complete my responsibilities.
- As a Reader, I want Read access via D13-STR-Readers, so that I can complete my responsibilities.

## Acceptance Criteria
- Form Code is required.
- Inclusion Ref No is required.
- Workflow Status is required.
- Current Action is required.
- Request Date is required.
- Requestor is required.
- Requesting Department is required.
- Item Description is required.
- Item Category is required.
- Submitted By is required.
- Submitted Date is required.
- Environment is required.
