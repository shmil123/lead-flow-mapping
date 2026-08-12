#!/usr/bin/env python3
"""
Re-fetch row counts from the "Website form submissions" Google Sheet
(id set below) so the numbers in lead-flow-mapping.html can be refreshed
before the CRO/Duncan meeting if the tracker has moved on.

Auth reuses the same Google OAuth as event-leads/linkedin-engagers/Events
(gspread user-OAuth flow, not a service account).

Usage:
  python3 read_sheet_counts.py
"""
from pathlib import Path
import gspread

CREDS_DIR = Path(__file__).parent.parent / "event-leads"
SHEET_ID = "1QQVGbIGwzPdAZFjs3EcPdMEwsQ0o9plWXOYtmhgMChQ"

gc = gspread.oauth(
    credentials_filename=str(CREDS_DIR / "client_secret.json"),
    authorized_user_filename=str(CREDS_DIR / "google_token.json"),
)
sh = gc.open_by_key(SHEET_ID)

print(f"{sh.title}\n")
total_data_rows = None
for ws in sh.worksheets():
    values = ws.get_all_values()
    data_rows = max(len(values) - 1, 0)  # minus header
    print(f"{ws.title:28s} {data_rows:4d} rows")
    if ws.title == "All leads":
        total_data_rows = data_rows

if total_data_rows:
    print(f"\nAll leads (data rows): {total_data_rows}")
