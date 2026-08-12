#!/usr/bin/env python3
"""
Compute lead-journey SLA numbers (time from form submission to CRM entry,
by topic) from the "Website form submissions" sheet's "All leads" tab.

Auth reuses the event-leads OAuth pair (see read_sheet_counts.py).
"""
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import statistics
import gspread

CREDS_DIR = Path(__file__).parent.parent / "event-leads"
SHEET_ID = "1QQVGbIGwzPdAZFjs3EcPdMEwsQ0o9plWXOYtmhgMChQ"

gc = gspread.oauth(
    credentials_filename=str(CREDS_DIR / "client_secret.json"),
    authorized_user_filename=str(CREDS_DIR / "google_token.json"),
)
sh = gc.open_by_key(SHEET_ID)
ws = sh.worksheet("All leads")
rows = ws.get_all_values()
header, data = rows[0], rows[1:]

idx = {name: i for i, name in enumerate(header)}


def parse_conv(s):
    s = s.strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%d/%m/%Y %H:%M")
    except ValueError:
        return None


def parse_sfid_date(s):
    s = s.strip()
    if not s:
        return None
    try:
        # e.g. 2026-02-26T15:19:55.000+0000
        return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


by_topic = defaultdict(lambda: {"total": 0, "reached_crm": 0, "lags_days": []})
overall_lags = []

for row in data:
    topic = row[idx["select_a_topic"]].strip() or "(blank)"
    by_topic[topic]["total"] += 1
    sfid = row[idx["SFID"]].strip()
    sfid_created = row[idx["SFID Created Date"]].strip()
    conv = parse_conv(row[idx["Conversion Date"]])
    if sfid:
        by_topic[topic]["reached_crm"] += 1
    if sfid_created and conv:
        crm_date = parse_sfid_date(sfid_created)
        if crm_date:
            lag = (crm_date - conv).days
            if lag >= 0:  # guard against bad data
                by_topic[topic]["lags_days"].append(lag)
                overall_lags.append(lag)

print(f"{'Topic':32s} {'Total':>6s} {'ReachedCRM':>11s} {'MedianLagDays':>14s} {'N(lag)':>7s}")
for topic, d in sorted(by_topic.items(), key=lambda kv: -kv[1]["total"]):
    med = statistics.median(d["lags_days"]) if d["lags_days"] else None
    print(f"{topic:32s} {d['total']:6d} {d['reached_crm']:11d} {str(med):>14s} {len(d['lags_days']):7d}")

print(f"\nOverall median lag (days), n={len(overall_lags)}: {statistics.median(overall_lags) if overall_lags else 'n/a'}")
print(f"Overall mean lag (days): {round(statistics.mean(overall_lags),1) if overall_lags else 'n/a'}")
