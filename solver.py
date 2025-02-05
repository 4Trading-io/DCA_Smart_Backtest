"""
solver.py
Build and solve the ILP model for either a chosen crypto or gold.
"""

import logging
import pandas as pd
from pulp import PULP_CBC_CMD, LpStatus
from optimization_model import build_model_for_asset

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def solve_asset_optimization(asset_type, start_date, end_date,
                             total_investment, monthly_limit, weekly_limit,
                             min_invest, per_buy_max, fee_percent=0.1,
                             symbol=None):
    """
    asset_type: "crypto" or "gold"
    If asset_type="crypto", pass e.g. symbol="BTCUSDT"
    Returns plan_df, total_invested, total_profit, portfolio_value
    """
    logger.info(f"Solve optimization for {asset_type} in [{start_date}..{end_date}] symbol={symbol}")
    model, invest_vars, invest_binary, df = build_model_for_asset(
        asset_type, start_date, end_date,
        total_investment, monthly_limit, weekly_limit,
        min_invest, per_buy_max, fee_percent,
        symbol
    )

    solver = PULP_CBC_CMD(msg=0)
    model.solve(solver)

    status_str = LpStatus[model.status]
    logger.info(f"{asset_type} solver status: {status_str}")
    if status_str != "Optimal":
        raise Exception(f"Solver not optimal for {asset_type}. Status={status_str}")

    df.set_index('Date', inplace=True)
    plan_list = []
    for period, var in invest_vars.items():
        val = var.varValue
        if val is not None and val > 0.0:
            open_price = float(df.loc[period, 'Open'])
            plan_list.append({
                'Date': period,
                'Investment (USDT)': val,
                'Buy Price (USDT)': open_price
            })
    plan_df = pd.DataFrame(plan_list)
    if plan_df.empty:
        logger.warning(f"No invests found by solver for {asset_type}.")
        total_invested  = 0.0
        total_profit    = 0.0
        portfolio_value = 0.0
    else:
        last_price = df['Close'].iloc[-1]
        plan_df['Profit (USDT)'] = (last_price - plan_df['Buy Price (USDT)']) / plan_df['Buy Price (USDT)'] * plan_df['Investment (USDT)']
        total_invested  = plan_df['Investment (USDT)'].sum()
        total_profit    = plan_df['Profit (USDT)'].sum()
        portfolio_value = total_invested + total_profit

    logger.info(f"{asset_type} Optimize => Invested={total_invested:.2f}, Profit={total_profit:.2f}, Value={portfolio_value:.2f}")
    return plan_df, total_invested, total_profit, portfolio_value
