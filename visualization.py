"""
visualization.py
Create and save PNG charts using Matplotlib for each scenario.
"""

import logging
import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def plot_scenario(asset_name, scenario_name, plan_df, market_df, output_path):
    """
    Plots the asset's Close price vs. the scenario's buy points.
    Saves as a PNG file at output_path.
      - asset_name: e.g. "bitcoin" or "gold"
      - scenario_name: e.g. "Optimized" or "Blind DCA #1"
      - plan_df: DataFrame with 'Date', 'Buy Price (USDT)' columns
      - market_df: DataFrame with 'Date', 'Close' columns
    """
    try:
        if market_df.empty:
            raise ValueError("market_df is empty, cannot plot scenario.")
        plt.figure(figsize=(12, 6))
        
        # Plot the asset's close price
        plt.plot(market_df['Date'], market_df['Close'], label=f"{asset_name.title()} Price", color='blue')
        
        # Plot the scenario's buy points, if any
        if not plan_df.empty:
            plt.scatter(plan_df['Date'], plan_df['Buy Price (USDT)'], 
                        color='red', marker='^', s=60, label=f"Buys: {scenario_name}")
        
        plt.title(f"{asset_name.title()} - {scenario_name} Strategy")
        plt.xlabel("Date")
        plt.ylabel("Price (USDT)")
        plt.legend()
        plt.grid(True)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved chart => {output_path}")
    except Exception as e:
        logger.error(f"plot_scenario error for {asset_name}, {scenario_name}: {e}", exc_info=True)
