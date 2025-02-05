"""
reporting.py
Generates multi-scenario final messages in EN/FA with the chosen crypto symbol.
"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def generate_scenario_report_en(scenario_label, total_invested, profit, portfolio_value, freq_days=None):
    msg = f"🔹 *{scenario_label}*\n"
    msg += f"   - Total Invested: {total_invested:.2f} USDT\n"
    msg += f"   - Profit: {profit:.2f} USDT\n"
    msg += f"   - Portfolio Value: {portfolio_value:.2f} USDT\n"
    if freq_days is not None:
        msg += f"   - Frequency (days): {freq_days}\n"
    msg += "\n"
    return msg

def generate_scenario_report_fa(scenario_label, total_invested, profit, portfolio_value, freq_days=None):
    msg = f"🔹 *{scenario_label}*\n"
    msg += f"   - سرمایه‌گذاری کل: {total_invested:.2f} USDT\n"
    msg += f"   - سود: {profit:.2f} USDT\n"
    msg += f"   - ارزش سبد: {portfolio_value:.2f} USDT\n"
    if freq_days is not None:
        msg += f"   - فاصله: {freq_days} روز\n"
    msg += "\n"
    return msg

def generate_final_report_en(crypto_opt, crypto_dca1, crypto_dca2, gold_opt, gold_dca1, gold_dca2):
    msg = "✨ *Detailed Multi-Scenario Report* ✨\n\n"

    # Crypto
    msg += generate_scenario_report_en(crypto_opt['label'], crypto_opt['invested'], crypto_opt['profit'], crypto_opt['value'])
    msg += generate_scenario_report_en(crypto_dca1['label'], crypto_dca1['invested'], crypto_dca1['profit'], crypto_dca1['value'], crypto_dca1['freq'])
    msg += generate_scenario_report_en(crypto_dca2['label'], crypto_dca2['invested'], crypto_dca2['profit'], crypto_dca2['value'], crypto_dca2['freq'])

    # Gold
    msg += generate_scenario_report_en(gold_opt['label'], gold_opt['invested'], gold_opt['profit'], gold_opt['value'])
    msg += generate_scenario_report_en(gold_dca1['label'], gold_dca1['invested'], gold_dca1['profit'], gold_dca1['value'], gold_dca1['freq'])
    msg += generate_scenario_report_en(gold_dca2['label'], gold_dca2['invested'], gold_dca2['profit'], gold_dca2['value'], gold_dca2['freq'])

    msg += "🆚 *Comparison*\n"
    msg += "Above, we see how your chosen Crypto pair and Gold performed under both optimized and blind DCA strategies.\n"
    msg += "You can review the charts and Excel files for each scenario's detailed buy attempts.\n\n"
    msg += "💡 *Thank you for using our DCA Bot!* 💰🚀"
    return msg

def generate_final_report_fa(crypto_opt, crypto_dca1, crypto_dca2, gold_opt, gold_dca1, gold_dca2):
    msg = "✨ *گزارش چند سناریویی* ✨\n\n"

    # Crypto
    msg += generate_scenario_report_fa(crypto_opt['label'], crypto_opt['invested'], crypto_opt['profit'], crypto_opt['value'])
    msg += generate_scenario_report_fa(crypto_dca1['label'], crypto_dca1['invested'], crypto_dca1['profit'], crypto_dca1['value'], crypto_dca1['freq'])
    msg += generate_scenario_report_fa(crypto_dca2['label'], crypto_dca2['invested'], crypto_dca2['profit'], crypto_dca2['value'], crypto_dca2['freq'])

    # Gold
    msg += generate_scenario_report_fa(gold_opt['label'], gold_opt['invested'], gold_opt['profit'], gold_opt['value'])
    msg += generate_scenario_report_fa(gold_dca1['label'], gold_dca1['invested'], gold_dca1['profit'], gold_dca1['value'], gold_dca1['freq'])
    msg += generate_scenario_report_fa(gold_dca2['label'], gold_dca2['invested'], gold_dca2['profit'], gold_dca2['value'], gold_dca2['freq'])

    msg += "🆚 *مقایسه*\n"
    msg += "در بالا مشاهده می‌کنید که جفت رمز ارز انتخابی شما و طلا در روش‌های کور DCA و استراتژی بهینه چگونه عمل کرده‌اند.\n"
    msg += "می‌توانید نمودارها و فایل‌های اکسل هر سناریو را برای جزئیات بیشتر بررسی کنید.\n\n"
    msg += "💡 *سپاس از استفاده از ربات DCA!* 💰🚀"
    return msg
