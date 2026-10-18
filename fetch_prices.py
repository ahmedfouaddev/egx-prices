#!/usr/bin/env python3
"""Fetch delayed EGX quotes from TradingView's scanner and write prices.json."""
import json, sys, urllib.request, datetime

TICKERS = ["ORHD", "RAYA", "MPRC", "DSCW", "CIRA", "ISPH", "TMGH", "BONY"]
URL = "https://scanner.tradingview.com/egypt/scan"

body = json.dumps({
    "symbols": {"tickers": [f"EGX:{t}" for t in TICKERS]},
    "columns": ["close", "change", "time"],
}).encode()
req = urllib.request.Request(URL, data=body, headers={
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.load(r)["data"]

quotes = {}
for e in data:
    t = e["s"].split(":")[1]
    close, change, ts = e["d"]
    quotes[t] = {"price": close, "change_pct": change, "bar_time_utc": ts}

if len(quotes) != len(TICKERS):
    print("incomplete data", quotes, file=sys.stderr)
    sys.exit(1)

out = {
    "fetched_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "source": "scanner.tradingview.com (15 min delayed)",
    "quotes": quotes,
}
json.dump(out, open("prices.json", "w"), indent=2, sort_keys=True)
print(json.dumps(out))
