# telegram_bot.py

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
import ui_helpers
from messages import get_message

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

def get_language(chat_id):
    """Retrieve the language from the user's session; default is 'en'."""
    session = user_sessions.get_session(chat_id)
    if session and 'language' in session['inputs']:
        lang = session['inputs']['language']
        if lang:
            return lang
    return 'en'

def bot_message(chat_id, key, **kwargs):
    """Retrieve a message for the given chat and key using the correct language."""
    language = get_language(chat_id)
    return get_message(language, key, **kwargs)

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
    # Reset the session state for a new conversation
    user_sessions.update_session(chat_id, "choose_language", {"language": "fa"})  # default to en
    welcome_text = bot_message(chat_id, 'welcome_intro')
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown")
    bot.send_message(
        chat_id,
        bot_message(chat_id, 'choose_language'),
        reply_markup=ui_helpers.get_language_keyboard(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['help'])
@rate_limited
def handle_help(message):
    chat_id = message.chat.id
    help_text = bot_message(chat_id, 'help')
    bot.send_message(
        chat_id,
        help_text,
        parse_mode="Markdown",
        reply_markup=ui_helpers.get_main_menu_keyboard(get_language(chat_id))
    )

@bot.message_handler(func=lambda m: True)
@rate_limited
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()
    session = user_sessions.get_session(chat_id)
    if not session:
        bot.send_message(chat_id, bot_message(chat_id, 'no_session_error'), parse_mode="Markdown")
        return

    state = session['state']
    inputs = session['inputs']
    try:
        # ========== Choose Language ==========
        if state == "choose_language":
            if text in ["English", "فارسی"]:
                language = "en" if text == "English" else "fa"
                inputs['language'] = language
                user_sessions.update_session(chat_id, "ask_crypto_pair", inputs)
                # Notify that the language is set
                if language == "en":
                    lang_set_msg = get_message("en", 'language_set_en')
                else:
                    lang_set_msg = get_message("fa", 'language_set_fa')
                bot.send_message(chat_id, lang_set_msg, parse_mode="Markdown")
                bot.send_message(
                    chat_id,
                    bot_message(chat_id, 'ask_crypto_pair'),
                    reply_markup=ui_helpers.get_predefined_crypto_keyboard(),
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")

        # ========== Ask Crypto Pair ==========
        elif state == "ask_crypto_pair":
            inputs['crypto_pair'] = text.upper()
            user_sessions.update_session(chat_id, "ask_total_investment", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_total_investment'), parse_mode="Markdown")

        # ========== Ask Total Investment ==========
        elif state == "ask_total_investment":
            try:
                inputs['total_investment'] = float(text)
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")
                return
            user_sessions.update_session(chat_id, "ask_start_date", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_start_date'), parse_mode="Markdown")

        # ========== Ask Start Date ==========
        elif state == "ask_start_date":
            try:
                datetime.strptime(text, "%Y-%m-%d")
                inputs['start_date'] = text
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'date_invalid_format'), parse_mode="Markdown")
                return
            user_sessions.update_session(chat_id, "ask_end_date", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_end_date'), parse_mode="Markdown")

        # ========== Ask End Date (with Validation) ==========
        elif state == "ask_end_date":
            try:
                end_dt = datetime.strptime(text, "%Y-%m-%d")
                start_dt = datetime.strptime(inputs['start_date'], "%Y-%m-%d")
                if end_dt < start_dt:
                    bot.send_message(chat_id, bot_message(chat_id, 'end_date_before_start'), parse_mode="Markdown")
                    return
                inputs['end_date'] = text
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'date_invalid_format'), parse_mode="Markdown")
                return

            user_sessions.update_session(chat_id, "ask_monthly_limit", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_monthly_limit'), parse_mode="Markdown")

        # ========== Ask Monthly Limit ==========
        elif state == "ask_monthly_limit":
            try:
                inputs['monthly_limit'] = float(text)
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")
                return
            user_sessions.update_session(chat_id, "ask_weekly_limit", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_weekly_limit'), parse_mode="Markdown")

        # ========== Ask Weekly Limit ==========
        elif state == "ask_weekly_limit":
            try:
                inputs['weekly_limit'] = float(text)
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")
                return
            user_sessions.update_session(chat_id, "ask_min_invest", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_min_invest'), parse_mode="Markdown")

        # ========== Ask Min Invest ==========
        elif state == "ask_min_invest":
            try:
                inputs['min_invest'] = float(text)
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")
                return
            user_sessions.update_session(chat_id, "ask_max_invest", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_max_invest'), parse_mode="Markdown")

        # ========== Ask Max Invest ==========
        elif state == "ask_max_invest":
            try:
                inputs['max_invest'] = float(text)
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")
                return
            user_sessions.update_session(chat_id, "ask_blind_freq1", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_blind_freq1'), parse_mode="Markdown")

        # ========== Ask Blind Freq #1 ==========
        elif state == "ask_blind_freq1":
            try:
                inputs['blind_freq1'] = int(text)
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")
                return
            user_sessions.update_session(chat_id, "ask_blind_freq2", inputs)
            bot.send_message(chat_id, bot_message(chat_id, 'ask_blind_freq2'), parse_mode="Markdown")

        # ========== Ask Blind Freq #2 ==========
        elif state == "ask_blind_freq2":
            try:
                inputs['blind_freq2'] = int(text)
            except ValueError:
                bot.send_message(chat_id, bot_message(chat_id, 'input_error'), parse_mode="Markdown")
                return

            # Next step: confirmation
            user_sessions.update_session(chat_id, "processing", inputs)
            confirm_text = bot_message(
                chat_id, 'confirm_inputs',
                crypto_pair=inputs.get('crypto_pair'),
                total_investment=inputs.get('total_investment'),
                start_date=inputs.get('start_date'),
                end_date=inputs.get('end_date'),
                monthly_limit=inputs.get('monthly_limit'),
                weekly_limit=inputs.get('weekly_limit'),
                min_invest=inputs.get('min_invest'),
                max_invest=inputs.get('max_invest'),
                blind_freq1=inputs.get('blind_freq1'),
                blind_freq2=inputs.get('blind_freq2')
            )
            bot.send_message(
                chat_id,
                confirm_text,
                parse_mode="Markdown",
                reply_markup=ui_helpers.get_confirmation_inline_keyboard(get_language(chat_id))
            )

        # ========== Processing State ==========
        elif state == "processing":
            bot.send_message(chat_id, bot_message(chat_id, 'processing'), parse_mode="Markdown")

        else:
            bot.send_message(chat_id, "Unexpected state. Please type /start to restart.", parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error processing input from {chat_id}: {e}", exc_info=True)
        bot.send_message(chat_id, bot_message(chat_id, 'error', error=str(e)), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def handle_confirmation(call):
    chat_id = call.message.chat.id
    session = user_sessions.get_session(chat_id)
    if not session:
        bot.answer_callback_query(call.id, bot_message(chat_id, 'no_session_error'))
        return

    if call.data == "confirm_yes":
        # Combine the "Inputs confirmed" text with the existing "processing" text if you wish:
        confirmed_msg = bot_message(chat_id, 'inputs_confirmed') + " " + bot_message(chat_id, 'processing')
        bot.edit_message_text(
            confirmed_msg,
            chat_id,
            call.message.message_id,
            parse_mode="Markdown"
        )
        thread = threading.Thread(target=run_pipeline, args=(chat_id, session['inputs']))
        thread.start()

    else:  # "confirm_no"
        bot.edit_message_text(
            bot_message(chat_id, 'operation_cancelled'),
            chat_id,
            call.message.message_id,
            parse_mode="Markdown"
        )
        user_sessions.delete_session(chat_id)

def run_pipeline(chat_id, inputs):
    lang = inputs.get('language', 'en')
    try:
        bot.send_message(chat_id, "🔄 Downloading data and starting analysis...", parse_mode="Markdown")
        init_db()
        symbol_pair = inputs['crypto_pair']
        start_date  = inputs['start_date']
        end_date    = inputs['end_date']

        # 1) Download crypto data
        download_binance_data(symbol_pair, start_date, end_date)
        bot.send_message(chat_id, "✅ Crypto data downloaded.", parse_mode="Markdown")

        # 2) Download & convert gold data
        start_shamsi = "1399-10-12"
        end_shamsi   = "1403-11-16"
        main_download_and_convert_gold(start_shamsi, end_shamsi)
        bot.send_message(chat_id, "✅ Gold data downloaded and converted.", parse_mode="Markdown")

        # 3) Run Crypto scenarios
        bot.send_message(chat_id, "🔹 Running crypto scenarios...", parse_mode="Markdown")
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
        crypto_blind1_df, crypto_blind1_sum = simulate_blind_dca(
            "crypto",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq1'],
            symbol=symbol_pair
        )
        crypto_blind2_df, crypto_blind2_sum = simulate_blind_dca(
            "crypto",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq2'],
            symbol=symbol_pair
        )

        # 4) Run Gold scenarios
        bot.send_message(chat_id, "🔹 Running gold scenarios...", parse_mode="Markdown")
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
        gold_blind1_df, gold_blind1_sum = simulate_blind_dca(
            "gold",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq1']
        )
        gold_blind2_df, gold_blind2_sum = simulate_blind_dca(
            "gold",
            inputs['total_investment'],
            start_date, end_date,
            inputs['blind_freq2']
        )

        # 5) Compute analytics & save
        crypto_df = get_crypto_data(symbol_pair, start_date, end_date)
        gold_df   = get_gold_data(start_date, end_date)
        analytics_crypto = compute_analytics(crypto_df, frequency='4h')
        analytics_gold   = compute_analytics(gold_df, frequency='1d')

        os.makedirs("data/excels", exist_ok=True)
        os.makedirs("data/charts", exist_ok=True)
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

        # 6) Prepare final report data
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

        # Final completion message
        bot.send_message(chat_id, bot_message(chat_id, 'pipeline_complete'), parse_mode="Markdown")

        # Generate final multi-scenario report in chosen language
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
        for png in [
            crypto_opt_png, crypto_blind1_png, crypto_blind2_png,
            gold_opt_png, gold_blind1_png, gold_blind2_png
        ]:
            if os.path.isfile(png):
                with open(png, 'rb') as f:
                    bot.send_photo(chat_id, f, caption=os.path.basename(png))

        # Send Excel files
        for xls in [
            crypto_opt_excel, crypto_blind1_excel, crypto_blind2_excel,
            gold_opt_excel, gold_blind1_excel, gold_blind2_excel
        ]:
            if os.path.isfile(xls):
                with open(xls, 'rb') as f:
                    bot.send_document(chat_id, f, caption=os.path.basename(xls))

        # Clear session and show main menu
        user_sessions.delete_session(chat_id)
        bot.send_message(
            chat_id,
            bot_message(chat_id, 'main_menu'),
            reply_markup=ui_helpers.get_main_menu_keyboard(get_language(chat_id)),
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Pipeline error for chat_id={chat_id}: {e}", exc_info=True)
        bot.send_message(chat_id, bot_message(chat_id, 'error', error=str(e)), parse_mode="Markdown")

if __name__ == "__main__":
    logger.info("Starting bot polling...")
    bot.infinity_polling()
