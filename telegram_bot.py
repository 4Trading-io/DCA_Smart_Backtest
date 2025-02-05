"""
telegram_bot.py
Main Telegram Bot that:
 - Lets user pick a Binance pair (BTCUSDT, ETHUSDT, etc.)
 - Downloads 4h data for that pair
 - Compares with Gold (daily)
 - Does blind DCA & ILP optimization for both
 - Produces multi-scenario final report, charts, Excel.

Now includes a big welcome message in English/Farsi that explains functionalities.
"""

import os
import threading
import time
import logging
from datetime import datetime
import telebot
from telebot import types
import pandas as pd

import user_sessions
from database_manager import init_db
from binance_data import download_binance_data
from navasan_data import main_download_and_convert_gold
from solver import solve_asset_optimization
from blind_dca import simulate_blind_dca
from data_preprocessing import get_crypto_data, get_gold_data
from analytics import compute_analytics
from visualization import plot_scenario
import reporting
from credentials import telegram_bot_token

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/telegram_bot.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BOT_TOKEN = telegram_bot_token
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set.")

bot = telebot.TeleBot(BOT_TOKEN)
last_message_time = {}
RATE_LIMIT_SECONDS = 0.5

MESSAGES = {
    'en': {
        'welcome_intro': 
            "👋 *Hello!* Welcome to the **Crypto & Gold DCA Bot**. We're here to help you make smart, data-driven investment decisions.\n\n"
            "Here's what this bot does for you:\n"
            "1️⃣ *Choose a crypto pair* (e.g., `BTCUSDT`, `ETHUSDT`, `SOLUSDT`) from Binance.\n"
            "2️⃣ The bot fetches *4-hour interval price data* from Binance for the pair you've selected.\n"
            "3️⃣ We also download historical *gold prices* in Iran, including:\n"
            "    - The price of **1 gram of gold** in Iranian *Tomans*.\n"
            "    - The **historical Dollar (USD)** price in the Iranian market.\n"
            "    - We automatically convert the price of gold to **USD** to provide an accurate international comparison.\n"
            "4️⃣ We simulate *two powerful DCA strategies* for both crypto and gold:\n"
            "    - A **Blind DCA Strategy** (two custom frequencies).\n"
            "    - An **Optimized DCA Strategy** (using advanced mathematical models).\n"
            "5️⃣ The bot generates **detailed reports**, including:\n"
            "    - 📊 *Charts* showing your strategy's performance.\n"
            "    - 💼 *Profit summaries* and **portfolio value** analysis.\n"
            "    - 📄 *Excel files* for each scenario.\n\n"
            "🌐 *Ready to start?* Let's begin by choosing your language!\n\n",
        
        'choose_language': "🌍 Please choose your language:",
        'language_set': "✅ Language set to English.",
        'ask_crypto_pair': "🔹 Enter the *Binance pair* you want to analyze (e.g., `BTCUSDT`, `ETHUSDT`):",
        'ask_total_investment': "🔹 Enter your *Total Investment Budget* (e.g., `10000` USDT):",
        'ask_start_date': "🔹 Enter the *Backtest Start Date* in `YYYY-MM-DD` format (e.g., `2021-01-01`):",
        'ask_end_date': "🔹 Enter the *Backtest End Date* in `YYYY-MM-DD` format (e.g., `2025-02-01`):",
        'ask_monthly_limit': "🔹 Enter the *Maximum Monthly Investment* (e.g., `1000` USDT):",
        'ask_weekly_limit': "🔹 Enter the *Maximum Weekly Investment* (e.g., `250` USDT):",
        'ask_min_invest': "🔹 Enter the *Minimum Investment per Buy* (e.g., `50` USDT):",
        'ask_max_invest': "🔹 Enter the *Maximum Investment per Buy* (e.g., `250` USDT):",
        'ask_blind_freq1': "🔹 Enter the *Blind DCA frequency (days)* for Strategy 1:",
        'ask_blind_freq2': "🔹 Enter the *Blind DCA frequency (days)* for Strategy 2:",
        'processing': "⏳ All inputs received! We are processing your request. This may take a few moments...",
        'pipeline_complete': "✅ *Pipeline complete!* Your **Crypto & Gold comparison** is ready.",
        'error': "⚠️ An error occurred: *{error}*",
        'help': "💡 *Available commands:*\n/start - Restart\n/help - Show help",
    },

    'fa': {
        'welcome_intro': 
            "👋 *سلام!* به **ربات سرمایه‌گذاری کریپتو و طلا** خوش آمدید. ما به شما کمک می‌کنیم که تصمیمات هوشمندانه و مبتنی بر داده در سرمایه‌گذاری بگیرید.\n\n"
            "در اینجا خلاصه‌ای از عملکرد این ربات را می‌بینید:\n"
            "1️⃣ *یک جفت ارز دیجیتال* در بایننس انتخاب کنید (مثلاً `BTCUSDT`، `ETHUSDT`).\n"
            "2️⃣ ربات *داده‌های قیمتی ۴ ساعته* این جفت ارز را از بایننس دانلود می‌کند.\n"
            "3️⃣ همچنین داده‌های تاریخی *قیمت طلا* در ایران دریافت می‌شود، شامل:\n"
            "    - **قیمت یک گرم طلا** به تومان.\n"
            "    - **قیمت دلار (USD)** در بازار ایران.\n"
            "    - ما به طور خودکار قیمت طلا را به **دلار** تبدیل می‌کنیم تا مقایسه بین‌المللی دقیقی ارائه شود.\n"
            "4️⃣ ما *دو استراتژی قدرتمند DCA* را برای کریپتو و طلا شبیه‌سازی می‌کنیم:\n"
            "    - **استراتژی کور DCA** (با دو فاصله زمانی دلخواه).\n"
            "    - **استراتژی بهینه DCA** (با استفاده از مدل‌های ریاضی پیشرفته).\n"
            "5️⃣ این ربات **گزارش‌های جامع** تولید می‌کند، شامل:\n"
            "    - 📊 *نمودارهایی* که عملکرد استراتژی شما را نشان می‌دهند.\n"
            "    - 💼 *خلاصه سود و ارزش سبد سرمایه‌گذاری*.\n"
            "    - 📄 *فایل‌های اکسل* برای هر سناریو.\n\n"
            "🌐 *آماده‌ای؟* بیایید زبان موردنظر خود را انتخاب کنیم. لطفا تمامی اعداد را به انگلیسی وارد کنید!",
        
        'choose_language': "🌍 لطفاً زبان خود را انتخاب کنید:",
        'language_set': "✅ زبان به فارسی تنظیم شد.",
        'ask_crypto_pair': "🔹 جفت ارز بایننس موردنظر خود را وارد کنید (مثلاً `BTCUSDT`, `ETHUSDT`):",
        'ask_total_investment': "🔹 *بودجه کل سرمایه‌گذاری* خود را وارد کنید (مثلاً `10000` USDT):",
        'ask_start_date': "🔹 *تاریخ شروع تحلیل* را با فرمت `YYYY-MM-DD` وارد کنید (مثلاً `01-01-2024`):",
        'ask_end_date': "🔹 *تاریخ پایان تحلیل* را با فرمت `YYYY-MM-DD` وارد کنید (مثلاً `01-02-2025`):",
        'ask_monthly_limit': "🔹 *حداکثر سرمایه‌گذاری ماهانه* را وارد کنید (مثلاً `1000` USDT):",
        'ask_weekly_limit': "🔹 *حداکثر سرمایه‌گذاری هفتگی* را وارد کنید (مثلاً `250` USDT):",
        'ask_min_invest': "🔹 *حداقل سرمایه‌گذاری در هر خرید* را وارد کنید (مثلاً `50` USDT):",
        'ask_max_invest': "🔹 *حداکثر سرمایه‌گذاری در هر خرید* را وارد کنید (مثلاً `250` USDT):",
        'ask_blind_freq1': "🔹 فاصله زمانی (روز) برای *استراتژی کور DCA اول* را وارد کنید:",
        'ask_blind_freq2': "🔹 فاصله زمانی (روز) برای *استراتژی کور DCA دوم* را وارد کنید:",
        'processing': "⏳ همه ورودی‌ها دریافت شد! در حال پردازش درخواست شما هستیم. این کار ممکن است چند لحظه طول بکشد...",
        'pipeline_complete': "✅ *فرآیند کامل شد!* **مقایسه طلا و کریپتو** شما آماده است.",
        'error': "⚠️ خطایی رخ داد: *{error}*",
        'help': "💡 *دستورات موجود:*\n/start - شروع مجدد\n/help - راهنما",
    }
}

def get_language(chat_id):
    session = user_sessions.get_session(chat_id)
    if session and 'language' in session['inputs']:
        return session['inputs']['language']
    return 'en'

def get_message(chat_id, key, **kwargs):
    lang = get_language(chat_id)
    return MESSAGES[lang][key].format(**kwargs)

def rate_limited(func):
    def wrapper(message, *args, **kwargs):
        chat_id = message.chat.id
        now = time.time()
        if chat_id in last_message_time and (now - last_message_time[chat_id] < RATE_LIMIT_SECONDS):
            return
        last_message_time[chat_id] = now
        return func(message, *args, **kwargs)
    return wrapper

@bot.message_handler(commands=['start'])
@rate_limited
def handle_start(message):
    chat_id = message.chat.id
    # Start conversation with a welcome intro
    user_sessions.update_session(chat_id, "choose_language", {"language": None})
    lang_buttons = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    lang_buttons.add("English", "فارسی")

    # We'll send the bilingual intro text, then ask to choose language
    bot.send_message(chat_id, 
        MESSAGES['en']['welcome_intro'] + "\n" + MESSAGES['fa']['welcome_intro'],
        parse_mode="Markdown"
    )
    bot.send_message(chat_id,
        MESSAGES['en']['choose_language'] + "\n" + MESSAGES['fa']['choose_language'],
        reply_markup=lang_buttons
    )

@bot.message_handler(commands=['help'])
@rate_limited
def handle_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, get_message(chat_id, 'help'), parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
@rate_limited
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    session = user_sessions.get_session(chat_id)

    if not session:
        bot.send_message(chat_id, "Please type /start to begin.")
        return

    state = session['state']
    inputs = session['inputs']
    try:
        if state == "choose_language":
            if text in ["English", "فارسی"]:
                language = "en" if text == "English" else "fa"
                inputs['language'] = language
                user_sessions.update_session(chat_id, "ask_crypto_pair", inputs)
                bot.send_message(chat_id, MESSAGES[language]['language_set'], parse_mode="Markdown")
                bot.send_message(chat_id, get_message(chat_id, 'ask_crypto_pair'), parse_mode="Markdown")
            else:
                bot.send_message(chat_id, "Please choose either 'English' or 'فارسی'.")

        elif state == "ask_crypto_pair":
            # The user typed something like "BTCUSDT" or "ETHUSDT"
            inputs['crypto_pair'] = text.upper()  # standardize to uppercase
            user_sessions.update_session(chat_id, "ask_total_investment", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_total_investment'), parse_mode="Markdown")

        elif state == "ask_total_investment":
            inputs['total_investment'] = float(text)
            user_sessions.update_session(chat_id, "ask_start_date", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_start_date'), parse_mode="Markdown")

        elif state == "ask_start_date":
            inputs['start_date'] = text
            user_sessions.update_session(chat_id, "ask_end_date", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_end_date'), parse_mode="Markdown")

        elif state == "ask_end_date":
            inputs['end_date'] = text
            user_sessions.update_session(chat_id, "ask_monthly_limit", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_monthly_limit'), parse_mode="Markdown")

        elif state == "ask_monthly_limit":
            inputs['monthly_limit'] = float(text)
            user_sessions.update_session(chat_id, "ask_weekly_limit", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_weekly_limit'), parse_mode="Markdown")

        elif state == "ask_weekly_limit":
            inputs['weekly_limit'] = float(text)
            user_sessions.update_session(chat_id, "ask_min_invest", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_min_invest'), parse_mode="Markdown")

        elif state == "ask_min_invest":
            inputs['min_invest'] = float(text)
            user_sessions.update_session(chat_id, "ask_max_invest", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_max_invest'), parse_mode="Markdown")

        elif state == "ask_max_invest":
            inputs['max_invest'] = float(text)
            user_sessions.update_session(chat_id, "ask_blind_freq1", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_blind_freq1'), parse_mode="Markdown")

        elif state == "ask_blind_freq1":
            inputs['blind_freq1'] = int(text)
            user_sessions.update_session(chat_id, "ask_blind_freq2", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'ask_blind_freq2'), parse_mode="Markdown")

        elif state == "ask_blind_freq2":
            inputs['blind_freq2'] = int(text)
            user_sessions.update_session(chat_id, "processing", inputs)
            bot.send_message(chat_id, get_message(chat_id, 'processing'), parse_mode="Markdown")

            # Start pipeline in background
            thread = threading.Thread(target=run_pipeline, args=(chat_id, inputs))
            thread.start()

        elif state == "processing":
            bot.send_message(chat_id, "Processing in progress, please wait...")

        else:
            bot.send_message(chat_id, "Unexpected state. Type /start to restart.")

    except Exception as e:
        logger.error(f"Error processing input from {chat_id}: {e}", exc_info=True)
        bot.send_message(chat_id, get_message(chat_id, 'error', error=str(e)), parse_mode="Markdown")


def run_pipeline(chat_id, inputs):
    """
    The main pipeline producing multiple scenario results,
    for chosen 'crypto_pair' and gold, sending charts, Excel, final multi-scenario report.
    """
    lang = inputs.get('language', 'en')
    try:
        init_db()

        symbol_pair = inputs['crypto_pair']
        start_date  = inputs['start_date']
        end_date    = inputs['end_date']

        # 1) Download user-chosen crypto pair (4h)
        download_binance_data(symbol_pair, start_date, end_date)

        # 2) Download & Convert Gold (daily)
        # Shamsi placeholders
        start_shamsi = "1399-10-12"
        end_shamsi   = "1403-11-16"
        main_download_and_convert_gold(start_shamsi, end_shamsi)

        # ============= SCENARIOS: CRYPTO =============
        # A) Crypto Optimized
        from solver import solve_asset_optimization
        crypto_opt_df, crypto_opt_invested, crypto_opt_profit, crypto_opt_value = solve_asset_optimization(
            asset_type='crypto',
            start_date=start_date,
            end_date=end_date,
            total_investment=inputs['total_investment'],
            monthly_limit=inputs['monthly_limit'],
            weekly_limit=inputs['weekly_limit'],
            min_invest=inputs['min_invest'],
            per_buy_max=inputs['max_invest'],
            fee_percent=0.1,
            symbol=symbol_pair
        )
        # B) Crypto Blind DCA #1
        from blind_dca import simulate_blind_dca
        crypto_blind1_df, crypto_blind1_sum = simulate_blind_dca(
            "crypto",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq1'],
            symbol=symbol_pair
        )
        # C) Crypto Blind DCA #2
        crypto_blind2_df, crypto_blind2_sum = simulate_blind_dca(
            "crypto",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq2'],
            symbol=symbol_pair
        )

        # ============= SCENARIOS: GOLD =============
        # D) Gold Optimized
        gold_opt_df, gold_opt_invested, gold_opt_profit, gold_opt_value = solve_asset_optimization(
            asset_type='gold',
            start_date=start_date,
            end_date=end_date,
            total_investment=inputs['total_investment'],
            monthly_limit=inputs['monthly_limit'],
            weekly_limit=inputs['weekly_limit'],
            min_invest=inputs['min_invest'],
            per_buy_max=inputs['max_invest'],
            fee_percent=0.1
        )
        # E) Gold Blind DCA #1
        gold_blind1_df, gold_blind1_sum = simulate_blind_dca(
            "gold",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq1']
        )
        # F) Gold Blind DCA #2
        gold_blind2_df, gold_blind2_sum = simulate_blind_dca(
            "gold",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq2']
        )

        # 3) Analytics
        from data_preprocessing import get_crypto_data, get_gold_data
        crypto_df = get_crypto_data(symbol_pair, start_date, end_date)
        gold_df   = get_gold_data(start_date, end_date)
        from analytics import compute_analytics
        analytics_crypto = compute_analytics(crypto_df, frequency='4h')  # chosen pair at 4h
        analytics_gold   = compute_analytics(gold_df, frequency='1d')

        # 4) Save each plan to Excel
        os.makedirs("data/excels", exist_ok=True)
        crypto_opt_excel    = f"data/excels/{symbol_pair}_optimized.xlsx"
        crypto_blind1_excel = f"data/excels/{symbol_pair}_blind1.xlsx"
        crypto_blind2_excel = f"data/excels/{symbol_pair}_blind2.xlsx"
        gold_opt_excel      = "data/excels/gold_optimized.xlsx"
        gold_blind1_excel   = "data/excels/gold_blind1.xlsx"
        gold_blind2_excel   = "data/excels/gold_blind2.xlsx"

        if not crypto_opt_df.empty:      crypto_opt_df.to_excel(crypto_opt_excel, index=False)
        if not crypto_blind1_df.empty:   crypto_blind1_df.to_excel(crypto_blind1_excel, index=False)
        if not crypto_blind2_df.empty:   crypto_blind2_df.to_excel(crypto_blind2_excel, index=False)
        if not gold_opt_df.empty:        gold_opt_df.to_excel(gold_opt_excel, index=False)
        if not gold_blind1_df.empty:     gold_blind1_df.to_excel(gold_blind1_excel, index=False)
        if not gold_blind2_df.empty:     gold_blind2_df.to_excel(gold_blind2_excel, index=False)

        # 5) Create 6 PNG charts
        os.makedirs("data/charts", exist_ok=True)
        from visualization import plot_scenario

        crypto_opt_png    = f"data/charts/{symbol_pair}_optimized.png"
        crypto_blind1_png = f"data/charts/{symbol_pair}_blind1.png"
        crypto_blind2_png = f"data/charts/{symbol_pair}_blind2.png"
        gold_opt_png      = "data/charts/gold_optimized.png"
        gold_blind1_png   = "data/charts/gold_blind1.png"
        gold_blind2_png   = "data/charts/gold_blind2.png"

        plot_scenario(symbol_pair, "Optimized", crypto_opt_df, crypto_df, crypto_opt_png)
        plot_scenario(symbol_pair, f"Blind DCA (freq={inputs['blind_freq1']})", crypto_blind1_df, crypto_df, crypto_blind1_png)
        plot_scenario(symbol_pair, f"Blind DCA (freq={inputs['blind_freq2']})", crypto_blind2_df, crypto_df, crypto_blind2_png)

        plot_scenario("gold", "Optimized", gold_opt_df, gold_df, gold_opt_png)
        plot_scenario("gold", f"Blind DCA (freq={inputs['blind_freq1']})", gold_blind1_df, gold_df, gold_blind1_png)
        plot_scenario("gold", f"Blind DCA (freq={inputs['blind_freq2']})", gold_blind2_df, gold_df, gold_blind2_png)

        # 6) Build scenario dicts for final reporting
        crypto_opt_info = {
            'label': f"{symbol_pair} Optimized",
            'invested': crypto_opt_invested,
            'profit':   crypto_opt_profit,
            'value':    crypto_opt_value,
            'freq':     None
        }
        crypto_blind1_info = {
            'label': f"{symbol_pair} Blind DCA #1",
            'invested': crypto_blind1_sum['total_invested'],
            'profit':   crypto_blind1_sum['profit'],
            'value':    crypto_blind1_sum['portfolio_value'],
            'freq':     crypto_blind1_sum['frequency_days']
        }
        crypto_blind2_info = {
            'label': f"{symbol_pair} Blind DCA #2",
            'invested': crypto_blind2_sum['total_invested'],
            'profit':   crypto_blind2_sum['profit'],
            'value':    crypto_blind2_sum['portfolio_value'],
            'freq':     crypto_blind2_sum['frequency_days']
        }
        gold_opt_info = {
            'label': "Gold Optimized",
            'invested': gold_opt_invested,
            'profit':   gold_opt_profit,
            'value':    gold_opt_value,
            'freq':     None
        }
        gold_blind1_info = {
            'label': "Gold Blind DCA #1",
            'invested': gold_blind1_sum['total_invested'],
            'profit':   gold_blind1_sum['profit'],
            'value':    gold_blind1_sum['portfolio_value'],
            'freq':     gold_blind1_sum['frequency_days']
        }
        gold_blind2_info = {
            'label': "Gold Blind DCA #2",
            'invested': gold_blind2_sum['total_invested'],
            'profit':   gold_blind2_sum['profit'],
            'value':    gold_blind2_sum['portfolio_value'],
            'freq':     gold_blind2_sum['frequency_days']
        }

        # 7) Send final text + images + Excel
        bot.send_message(chat_id, get_message(chat_id, 'pipeline_complete'), parse_mode="Markdown")

        import reporting
        if lang == 'en':
            final_msg = reporting.generate_final_report_en(
                crypto_opt_info, crypto_blind1_info, crypto_blind2_info,
                gold_opt_info, gold_blind1_info, gold_blind2_info
            )
        else:
            final_msg = reporting.generate_final_report_fa(
                crypto_opt_info, crypto_blind1_info, crypto_blind2_info,
                gold_opt_info, gold_blind1_info, gold_blind2_info
            )
        bot.send_message(chat_id, final_msg, parse_mode="Markdown")

        # Send charts
        scenario_pngs = [
            crypto_opt_png, crypto_blind1_png, crypto_blind2_png,
            gold_opt_png, gold_blind1_png, gold_blind2_png
        ]
        for png in scenario_pngs:
            if os.path.isfile(png):
                with open(png, 'rb') as f:
                    bot.send_photo(chat_id, f, caption=os.path.basename(png))

        # Send Excel
        scenario_excels = [
            crypto_opt_excel, crypto_blind1_excel, crypto_blind2_excel,
            gold_opt_excel, gold_blind1_excel, gold_blind2_excel
        ]
        for xls in scenario_excels:
            if os.path.isfile(xls):
                with open(xls, 'rb') as f:
                    bot.send_document(chat_id, f, caption=os.path.basename(xls))

        user_sessions.delete_session(chat_id)

    except Exception as e:
        logger.error(f"Pipeline error for chat_id={chat_id}: {e}", exc_info=True)
        bot.send_message(chat_id, get_message(chat_id, 'error', error=str(e)), parse_mode="Markdown")

if __name__ == "__main__":
    logger.info("Starting bot polling...")
    bot.infinity_polling()
