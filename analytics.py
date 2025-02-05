"""
analytics.py
Compute MDD, volatility, Sharpe ratio, etc. for either 4h or daily data.
"""

import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def compute_analytics(df, frequency='4h'):
    """
    df should have columns ['Date','Close','Return'].
    frequency='4h' => annual_factor ~ sqrt(2190)
    frequency='1d' => annual_factor ~ sqrt(365)
    """
    try:
        if df.empty:
            raise ValueError("DataFrame is empty in compute_analytics.")

        df = df.copy()
        df.sort_values('Date', inplace=True)
        if 'Return' not in df.columns:
            df['Return'] = df['Close'].pct_change()

        # Cumulative & drawdown
        df['Cumulative'] = (1 + df['Return']).cumprod()
        df['CumulativeMax'] = df['Cumulative'].cummax()
        df['Drawdown'] = df['Cumulative'] / df['CumulativeMax'] - 1
        max_drawdown = df['Drawdown'].min()

        if frequency == '4h':
            annual_factor = np.sqrt(2190)
        elif frequency == '1d':
            annual_factor = np.sqrt(365)
        else:
            annual_factor = 1.0

        vol = df['Return'].std() * annual_factor
        sharpe = (df['Return'].mean() * annual_factor) / (df['Return'].std() + 1e-9)

        return {
            'max_drawdown': max_drawdown,
            'volatility': vol,
            'sharpe_ratio': sharpe
        }
    except Exception as e:
        logger.error(f"Error in compute_analytics: {e}", exc_info=True)
        return {
            'max_drawdown': None,
            'volatility': None,
            'sharpe_ratio': None
        }
