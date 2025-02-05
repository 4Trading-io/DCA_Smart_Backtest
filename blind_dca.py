"""
blind_dca.py
Perform blind DCA for either the chosen crypto or gold.
We pass something like blind_dca.simulate_blind_dca("crypto", "BTCUSDT", ...)
or "gold" if we want to do gold.
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
from data_preprocessing import get_crypto_data, get_gold_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def simulate_blind_dca(asset_type, total_investment, start_date, end_date, frequency_days, symbol=None):
    """
    asset_type: "crypto" or "gold"
    symbol: if asset_type="crypto", specify e.g. "BTCUSDT"
    We fetch the relevant data, do blind DCA, return plan_df, summary.
    """
    logger.info(f"simulate_blind_dca({asset_type}), freq={frequency_days} days, symbol={symbol}")
    if asset_type == "crypto":
        if not symbol:
            raise ValueError("Must provide 'symbol' for crypto DCA.")
        df = get_crypto_data(symbol, start_date, end_date)
    else:
        df = get_gold_data(start_date, end_date)

    if df.empty:
        raise Exception(f"No data for {asset_type} in range. Cannot do DCA.")
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt   = datetime.strptime(end_date,   "%Y-%m-%d")
    schedule_dates = []
    current_date = start_dt
    while current_date <= end_dt:
        schedule_dates.append(current_date)
        current_date += timedelta(days=frequency_days)

    n_investments = len(schedule_dates)
    if n_investments == 0:
        raise Exception("No DCA investment dates generated. Check date range/frequency.")

    amount_per_invest = total_investment / n_investments
    plan = []
    for sch_date in schedule_dates:
        row_candidate = df[df['Date'] >= sch_date]
        if row_candidate.empty:
            row = df.iloc[-1]
        else:
            row = row_candidate.iloc[0]
        buy_date = row['Date']
        buy_price = row['Open']
        coins = 0.0
        if buy_price > 0:
            coins = amount_per_invest / buy_price

        plan.append({
            "Date": buy_date,
            "Investment (USDT)": amount_per_invest,
            "Buy Price (USDT)": buy_price,
            "Coins Purchased": coins,
            "Frequency": frequency_days
        })

    plan_df = pd.DataFrame(plan)
    total_coins = plan_df['Coins Purchased'].sum()
    final_price = df['Close'].iloc[-1]
    portfolio_value = total_coins * final_price
    profit = portfolio_value - total_investment

    summary = {
        "asset": asset_type,
        "symbol": symbol,
        "total_invested": total_investment,
        "total_coins": total_coins,
        "final_price": final_price,
        "portfolio_value": portfolio_value,
        "profit": profit,
        "n_investments": n_investments,
        "frequency_days": frequency_days
    }
    logger.info(f"Blind DCA {asset_type} => profit={profit:.2f}, port_value={portfolio_value:.2f}")
    return plan_df, summary
