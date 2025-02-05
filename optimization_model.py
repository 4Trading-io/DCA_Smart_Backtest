"""
optimization_model.py
Defines an ILP model for either 'crypto' or 'gold'.
"""

import logging
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpBinary, LpContinuous
from data_preprocessing import get_crypto_data, get_gold_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def define_ilp_model(df, total_investment, monthly_limit, weekly_limit,
                     min_invest, per_buy_max, fee_percent=0.1):
    df = df.copy()
    df.set_index('Date', inplace=True)
    periods = df.index.tolist()

    model = LpProblem(name="asset-buying-optimization", sense=LpMaximize)

    invest_vars = {}
    invest_binaries = {}

    for period in periods:
        var_name = period.strftime("%Y%m%d_%H%M")
        invest_vars[period] = LpVariable(f"invest_{var_name}", lowBound=0, upBound=per_buy_max, cat=LpContinuous)
        invest_binaries[period] = LpVariable(f"binary_{var_name}", cat=LpBinary)

    # Objective
    objective_terms = []
    for period in periods:
        open_price = float(df.loc[period, 'Open'])
        if open_price <= 0:
            open_price = 1e-9
        objective_terms.append(invest_vars[period] * (1.0 / open_price))
    model += lpSum(objective_terms), "TotalCoins"

    # Constraints
    model += (lpSum(invest_vars.values()) <= total_investment), "TotalInvestment"

    df['Month'] = df.index.to_period('M')
    for m in df['Month'].unique():
        subset_idx = df[df['Month'] == m].index
        model += (lpSum(invest_vars[i] for i in subset_idx) <= monthly_limit), f"MonthLimit_{m}"

    df['Week'] = df.index.to_period('W')
    for w in df['Week'].unique():
        subset_idx = df[df['Week'] == w].index
        model += (lpSum(invest_vars[i] for i in subset_idx) <= weekly_limit), f"WeekLimit_{w}"

    for period in periods:
        model += invest_vars[period] >= (min_invest * invest_binaries[period])
        model += invest_vars[period] <= (per_buy_max * invest_binaries[period])

    logger.debug("ILP model defined successfully.")
    return model, invest_vars, invest_binaries

def build_model_for_asset(asset_type, start_date, end_date,
                          total_investment, monthly_limit, weekly_limit,
                          min_invest, per_buy_max, fee_percent=0.1,
                          symbol=None):
    logger.info(f"Building ILP model for {asset_type}, symbol={symbol}, range [{start_date}, {end_date}]")
    if asset_type == "crypto":
        if not symbol:
            raise ValueError("Must specify 'symbol' for crypto optimization.")
        df = get_crypto_data(symbol, start_date, end_date)
    else:
        df = get_gold_data(start_date, end_date)

    if df.empty:
        raise Exception(f"No data for {asset_type} in that date range. Cannot build ILP model.")

    model, invest_vars, invest_binaries = define_ilp_model(
        df, total_investment, monthly_limit, weekly_limit,
        min_invest, per_buy_max, fee_percent
    )
    logger.info(f"Model built for {asset_type}, rows={len(df)}.")
    return model, invest_vars, invest_binaries, df
