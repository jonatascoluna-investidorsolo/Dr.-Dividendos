from datetime import date
from dd_engine.b3.proventos import DividendEvent, aggregate_dpa, calculate_payout


events = [
    DividendEvent("ABEV3", "DIVIDEND", 0.20, ex_date=date(2026, 3, 10), source_event_id="sample-1"),
    DividendEvent("ABEV3", "JCP", 0.15, ex_date=date(2026, 9, 10), source_event_id="sample-2"),
]

dpa = aggregate_dpa(events, date(2026, 1, 1), date(2026, 12, 31))
print({"ticker": "ABEV3", "dpa_realized": dpa, "payout": calculate_payout(dpa, 1_000_000_000, 1_000_000_000)})
