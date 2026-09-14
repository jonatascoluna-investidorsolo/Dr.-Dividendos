from datetime import date
from dd_engine.market.providers import YahooChartProvider

if __name__ == "__main__":
    quotes = YahooChartProvider().fetch_daily_close("PETR4", date(2026, 9, 1), date(2026, 9, 12))
    for q in quotes:
        print(q)
