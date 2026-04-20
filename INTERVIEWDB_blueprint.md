<!-- Architect: INTERVIEWDB form analysis → M365 blueprint. Zero unresolved markers permitted before hand-off. -->

---

form_code: INTERVIEWDB dept: HR official_name: "Interview Evaluation Database" owner: "HR
Department, D05" complexity: Complex DQ_REQUIRED: NO gxp_class: "—" status: BLUEPRINT_DRAFT date:
2026-04-14 ino_pattern: "HR-INT-YYMM-NNNN" sp_list_primary: "MainDB_HR" sp_form_type_discriminator:
"INTERVIEWDB" sp_list_staging: "HR_INTERVIEWDB_List" sp_child_table: "HR_INTERVIEWDB_Candidates"

---

# INTERVIEWDB — Interview Evaluation Database

## 1. Form Identity

| Attribute       | Value                                                         |
| --------------- | ------------------------------------------------------------- |
| Form Code       | INTERVIEWDB                                                   |
| Full Name       | Interview Evaluation Database                                 |
| Department      | Human Resources (D05)                                         |
| Module          | M2 — Recruitment & Hiring                                     |
| Entity Scope    | PCO / PCEO / ECM                                              |
| Complexity      | Complex                                                       |
| DQ Required     | NO                                                            |
| INO Pattern     | `HR-INT-YYMM-NNNN` (Power Automate — NEVER canvas)            |
| SP Primary List | `MainDB_HR` (FormType = "INTERVIEWDB")                        |
| SP Child Table  | `HR_INTERVIEWDB_Candidates` (one row per candidate per batch) |
| SP Staging List | `HR_INTERVIEWDB_List` (historical import)                     |

## 2. Business Purpose

The INTERVIEWDB form is the core recruitment funnel tool. It manages high-volume interview batches
for specific vacancies — up to 30 candidates per batch. The form covers four sections:

- **Section A (Header):** Batch identity — vacancy title, interview date, batch ID, and HR PICs.
- **Section B (Scoring):** Up to 10 technical/soft-skill evaluation scores (A1–A10) per candidate.
- **Section C (Verification):** Candidate status verification (Selected, Rejected, Reserved) per
  slot (S1–S10).
- **Section D (HR Use):** Email notification status (Offer/Regret sent) and final archiving
  (E1–E10).

> **Key M365 design decision:** Domino stored all 30 candidates as flat column arrays (CName_1 to
> CName_30, A1_1 to A10_30 etc.) — a total of ~300 columns. M365 architecture normalises this into a
> **parent + child table** model: the parent record (`MainDB_HR`) holds the batch header; each
> candidate is a row in `HR_INTERVIEWDB_Candidates`.

## 3. SharePoint Schema

### 3a. Primary List — `MainDB_HR` (FormType: "INTERVIEWDB") — Batch Header

| #   | SP Internal Name | Display Label             | Column Type    | Required | Classification   | Notes                                                |
| --- | ---------------- | ------------------------- | -------------- | -------- | ---------------- | ---------------------------------------------------- |
| 1   | FormType         | Form Type                 | Choice         | Yes      | SYSTEM-COMPUTED  | Fixed: "INTERVIEWDB"                                 |
| 2   | INO              | Batch Reference           | Single line    | Yes      | SYSTEM-COMPUTED  | HR-INT-YYMM-NNNN via PA                              |
| 3   | CurrentStatus    | Current Status            | Choice         | Yes      | WORKFLOW-MANAGED | Sourcing/Interviewing/Verifying/Communicating/Closed |
| 4   | EnvironmentTag   | Environment               | Choice         | Yes      | SYSTEM-COMPUTED  | DEV/TEST/PROD                                        |
| 5   | VacancyTitle     | Vacancy Title             | Single line    | Yes      | USER-ENTERED     | Job position being filled                            |
| 6   | LinkedSRRef      | Linked SR Reference       | Lookup         | No       | USER-ENTERED     | Link to approving SR record                          |
| 7   | LinkedJDRef      | Linked JD Reference       | Lookup         | No       | USER-ENTERED     | Pull required competencies from JD                   |
| 8   | InDate           | Interview Date            | Date           | Yes      | USER-ENTERED     | Date of interview                                    |
| 9   | InName           | Interviewer / Evaluator   | Person         | Yes      | USER-ENTERED     | Lead interviewer                                     |
| 10  | VrName           | Verifier                  | Person         | No       | WORKFLOW-MANAGED | HR Manager verifying results                         |
| 11  | HRE              | HR PIC (Executive)        | Person         | Yes      | WORKFLOW-MANAGED | HR Exec lead for communication                       |
| 12  | HRN              | HR PIC (Non-Executive)    | Person         | No       | WORKFLOW-MANAGED | HR support staff                                     |
| 13  | InRemarks        | Interview Remarks         | Multiple lines | No       | USER-ENTERED     | General batch-level notes                            |
| 14  | VrRemarks        | Verification Notes        | Multiple lines | No       | USER-ENTERED     | Auditor observations                                 |
| 15  | DocAuthor        | Created By                | Person         | Yes      | SYSTEM-COMPUTED  | HR Recruiter                                         |
| 16  | CA               | Current Action            | Choice         | No       | WORKFLOW-MANAGED | Stage control                                        |
| 17  | TotalCandidates  | Total Candidates in Batch | Number         | No       | SYSTEM-COMPUTED  | Count of child rows                                  |
| 18  | EmailDate        | HR Notification Date      | Date           | No       | SYSTEM-COMPUTED  | When communications sent                             |
| 19  | Attachment       | CV Batch (PDF)            | Attachment     | No       | USER-ENTERED     | Consolidated candidate CV file                       |
| 20  | IsLocked         | Is Locked                 | Yes/No         | No       | WORKFLOW-MANAGED | Lock after Closed                                    |

### 3b. Child Table — `HR_INTERVIEWDB_Candidates`

One row per candidate per batch. Linked to parent via `BatchINO` (lookup to MainDB_HR.INO).

| #   | SP Internal Name | Display Label              | Column Type        | Required | Notes                               |
| --- | ---------------- | -------------------------- | ------------------ | -------- | ----------------------------------- |
| 1   | BatchINO         | Batch Reference            | Lookup (MainDB_HR) | Yes      | Parent record link                  |
| 2   | SlotNo           | Candidate Slot #           | Number             | Yes      | 1–30                                |
| 3   | CandidateName    | Candidate Name             | Single line        | Yes      | USER-ENTERED                        |
| 4   | EvalScore        | Evaluation Score (A-score) | Number             | No       | Average of A1–A10 scores            |
| 5   | EvalBreakdown    | Score Breakdown            | Multiple lines     | No       | JSON: {a1..a10} per quality         |
| 6   | CandidateStatus  | Status                     | Choice             | Yes      | Selected/Rejected/Reserved/Pending  |
| 7   | EmailStatus      | Email Status               | Choice             | No       | Pending/SentOffer/SentRegret        |
| 8   | EmailSentDate    | Email Sent Date            | Date               | No       | WORKFLOW-MANAGED                    |
| 9   | Remarks          | Candidate Remarks          | Multiple lines     | No       | Interviewer notes on this candidate |

### 3c. Staging List — `HR_INTERVIEWDB_List`

Historical flat-column records from Domino. Migration script normalises CName_1–30 arrays into
individual child rows in `HR_INTERVIEWDB_Candidates`. Batch header in `HR_INTERVIEWDB_List`.

## 4. Field Inventory Summary

| Category                        | Count                                    |
| ------------------------------- | ---------------------------------------- |
| Batch Header (MainDB_HR)        | 20                                       |
| Candidate Child (per candidate) | 9                                        |
| **Total distinct fields**       | **29** (vs ~300+ flat columns in Domino) |

## 5. Workflow

### 5a. Stage Map

| Stage  | Name          | Trigger          | Actor                    | Actions                                | Next Stage | Notification Target  |
| ------ | ------------- | ---------------- | ------------------------ | -------------------------------------- | ---------- | -------------------- |
| 1      | Sourcing      | New batch        | DocAuthor (HR Recruiter) | Add candidates, set InDate             | 2          | InName (Interviewer) |
| 2      | Interviewing  | Batch submitted  | InName                   | Score candidates (A1–A10)              | 3          | VrName (HR Manager)  |
| 3      | Verifying     | Scoring complete | VrName                   | Audit results, set S1–S10 status       | 4          | HRE / HRN            |
| 4      | Communicating | Verified         | HRE Group                | Send offer/regret emails to candidates | Closed     | Candidates           |
| Closed | Archived      | All comms sent   | PA                       | Lock record, set IsLocked=Yes          | —          | —                    |

### 5b. Power Automate Flows

| Flow Name                   | Trigger         | Key Actions                                                                                                                                  |
| --------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `INTERVIEWDB_OnCreate`      | Batch created   | Generate INO, set Status=Sourcing, notify InName                                                                                             |
| `INTERVIEWDB_OnScoreSubmit` | Stage 2 submit  | Compute average EvalScore per candidate, set Status=Verifying, notify VrName                                                                 |
| `INTERVIEWDB_OnVerify`      | Stage 3 submit  | Set Status=Communicating, notify HRE/HRN                                                                                                     |
| `INTERVIEWDB_OnCommunicate` | Stage 4 action  | For each child row: if CandidateStatus=Selected → create "Offer Letter" task; if Rejected → send regret email and set EmailStatus=SentRegret |
| `INTERVIEWDB_JDCorrelation` | LinkedJDRef set | Pull "Required Skills" from linked JD record and populate EvalBreakdown quality labels                                                       |
| `INTERVIEWDB_OnClose`       | All comms sent  | Set IsLocked=Yes, CurrentStatus=Closed                                                                                                       |

## 6. Screen Inventory

| Screen                    | Purpose                                     | Key Controls                                                                            |
| ------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------- |
| `INTERVIEWDB_List`        | Gallery of all interview batches            | Search by vacancy/date/status; RAG status indicator                                     |
| `INTERVIEWDB_New`         | New batch header + candidate entry          | Header fields + editable candidate gallery (up to 30 rows)                              |
| `INTERVIEWDB_View`        | Read-only batch detail with candidate table | Batch header, sortable candidate gallery with scores and status                         |
| `INTERVIEWDB_Edit`        | Edit batch header while in Sourcing stage   | Header + candidate add/edit                                                             |
| `INTERVIEWDB_Score`       | Interviewer scoring portal                  | Per-candidate score sliders (A1–A10); read-only candidate list; submit for verification |
| `INTERVIEWDB_Verify`      | HR Manager verification portal              | Candidate list + status choice per row (Selected/Rejected/Reserved)                     |
| `INTERVIEWDB_Communicate` | HR Specialist communication hub             | Batch summary; "Send All Regrets" toggle; individual override per candidate             |

## 7. Navigation Map

```
INTERVIEWDB_List
  ├── [New Batch] → INTERVIEWDB_New → OnCreate → INTERVIEWDB_View
  ├── [Gallery Row] → INTERVIEWDB_View
  │     ├── [Edit] (Sourcing stage) → INTERVIEWDB_Edit
  │     ├── [Score Candidates] (InName role) → INTERVIEWDB_Score
  │     ├── [Verify] (VrName role) → INTERVIEWDB_Verify
  │     └── [Communicate] (HRE role) → INTERVIEWDB_Communicate
  └── [Back] → Home
```

## 8. Role Matrix

| Role                     | SP Group          | Screen Access           | Actions                |
| ------------------------ | ----------------- | ----------------------- | ---------------------- |
| HR Recruiter (DocAuthor) | D05-HR-Recruiters | List, New, View, Edit   | Create, add candidates |
| Interviewer (InName)     | D[Dept]-Managers  | List, View, Score       | Score candidates       |
| HR Manager (VrName)      | D05-HR-Managers   | List, View, Verify      | Audit and set status   |
| HR Specialist (HRE)      | D05-HR-Staff      | List, View, Communicate | Trigger emails         |
| HR Admin                 | D05-HR-Admin      | All                     | Full admin             |
| Reader                   | D05-HR-Readers    | List, View              | Read only              |

> **Privacy note:** Interviewers can only see candidates from their own assigned batch (item-level
> permissions via PA-managed SP group assignment).

## 9. Related Lists

| List                        | Relationship    | Purpose                                  |
| --------------------------- | --------------- | ---------------------------------------- |
| `MainDB_HR`                 | Parent (shared) | Batch header via FormType=INTERVIEWDB    |
| `HR_INTERVIEWDB_Candidates` | Child           | Normalised candidate rows                |
| `MainDB_HR` (FormType = SR) | Linked parent   | SR that authorised the recruitment drive |
| `MainDB_HR` (FormType = JD) | Linked lookup   | Competency framework for scoring         |
| `HR_INTERVIEWDB_List`       | Staging         | Historical Domino flat-column records    |

## 10. Migration Notes

- **Normalisation from flat to child table:** The most critical migration transformation. Domino
  CName_1–30, A_1–10, S_1–10, E_1–10 arrays become individual rows in `HR_INTERVIEWDB_Candidates`.
  Migration script groups by batch INO and creates one child row per non-blank CName slot.
- **EvalBreakdown (A1–A10):** The 10 evaluation dimensions are stored as JSON in `EvalBreakdown`
  rather than 10 separate SP columns. Power Apps renders these as a scrollable rating matrix within
  `INTERVIEWDB_Score`.
- **30-candidate UI:** `INTERVIEWDB_New` and `INTERVIEWDB_Score` use a gallery with `AddColumns` and
  inline editing. Maximum gallery rows = 30 via `CountRows` validation.
- **Email automation:** Candidate communications are handled 100% by Power Automate. Canvas buttons
  call HTTP PA flows — no direct email from canvas.
- **JD Correlation:** When `LinkedJDRef` is set, PA flow pulls "Required Skills" from the JD record
  and patches `EvalBreakdown` quality labels. This is informational only — scores remain with the
  interviewer.
- **INO generation:** NEVER in canvas. `INTERVIEWDB_OnCreate` generates `HR-INT-YYMM-NNNN`.
