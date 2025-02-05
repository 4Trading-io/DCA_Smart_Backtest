from cache_manager import fetch_cached_data

gold_rows = fetch_cached_data("gold_ohlc", "2024-03-17", "2024-03-22")
usd_rows  = fetch_cached_data("usd_ohlc", "2024-03-17", "2024-03-22")

print("GOLD:")
for g in gold_rows:
    print(g)
print("USD:")
for u in usd_rows:
    print(u)
