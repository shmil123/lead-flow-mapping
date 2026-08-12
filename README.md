# Lead Flow Mapping

LIVE at https://shmil123.github.io/lead-flow-mapping/ — one-page HTML brief: maps the three lead flows — website form, webinar, event — as a flowchart with volume counts at each stage, showing what's automated today, what's manual, and what needs a decision. Content is `docs/index.html`; deploy = git push.

- **Open:** `docs/index.html` in a browser, or just visit the live URL above.
- **Data sources:**
  - Topic + monthly volume for the "Contact Us" form → the manager-built HubSpot dashboard (screenshot only, not live-fetched).
  - CRM-status breakdown (In CRM / Disqualified / Maybe / Qualified-not-in-CRM / Other) → live Google Sheet **"Website form submissions"** (`1QQVGbIGwzPdAZFjs3EcPdMEwsQ0o9plWXOYtmhgMChQ`).
  - Webinar registered (176) / attended (127) counts → HubSpot lists 2229/2228 (portal 19920509), pulled live via `query_crm_data`.
- **Refresh before sending an update:** run `python3 read_sheet_counts.py` (reuses the `event-leads/` OAuth credentials — same Google identity as `Events/`, `linkedin-engagers/`) for current row counts per tab, then update the numbers in `docs/index.html` by hand and `git push`. `compute_sla.py` also exists in this folder (submission-to-CRM lag by lane) but isn't used in the current doc — Matan wants pure volume mapping, not a speed/SLA narrative.
- Framing is deliberately just "how many leads flow through each step" — no time/speed/SLA claims, no implying anyone is slow or unresponsive. Copy uses "CRM" generically rather than naming Salesforce.
- Scope is deliberately narrow to the "Contact Us" form only (confirmed with Matan — no other website forms feed leads) and treats webinar/event leads as fully manual today, independent of the separate `event-leads-push` skill (badge-scanner → HubSpot), which is not part of this mapping.
