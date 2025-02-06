# messages.py

MESSAGES = {
    'en': {
        # Welcome & Onboarding
        'welcome_intro': (
            "👋 **Welcome to the Crypto & Gold DCA Analysis Bot!**\n\n"
            "🌟 *Discover the magic of Dollar-Cost Averaging (DCA)!*\n\n"
            "This bot will show you why Dollar-Cost Averaging is a safe and effective investment strategy.\n"
            "Let's begin by selecting your language."
        ),
        'choose_language': "🌍 **Please select your language:**",
        'language_set_en': "✅ *Language set to English!*",
        'language_set_fa': "✅ *Language set to فارسی!*",

        # Data Input Prompts
        'ask_crypto_pair': (
            "🔹 **Step 1: Crypto Pair Selection**\n\n"
            "👉 *Enter the Binance crypto pair you wish to analyze.*\n"
            "For example: `BTCUSDT`, `ETHUSDT`, or `SOLUSDT`.\n\n"
            "You can type it or select from the options below."
        ),
        'ask_total_investment': (
            "🔹 **Step 2: Investment Amount**\n\n"
            "💰 *Enter your total investment budget in USDT.*\n"
            "For example: `10000`"
        ),
        'ask_start_date': (
            "🔹 **Step 3: Backtest Start Date**\n\n"
            "📅 *Enter the start date (YYYY-MM-DD).*\n"
            "For example: `2024-01-01`"
        ),
        'ask_end_date': (
            "🔹 **Step 4: Backtest End Date**\n\n"
            "📅 *Enter the end date (YYYY-MM-DD).*\n"
            "For example: `2025-02-01`"
        ),
        'ask_monthly_limit': (
            "🔹 **Step 5: Monthly Investment Limit**\n\n"
            "💳 *Enter the maximum amount you will invest per month (USDT).*\n"
            "For example: `750`"
        ),
        'ask_weekly_limit': (
            "🔹 **Step 6: Weekly Investment Limit**\n\n"
            "💳 *Enter the maximum amount you will invest per week (USDT).*\n"
            "For example: `200`"
        ),
        'ask_min_invest': (
            "🔹 **Step 7: Minimum Investment per Buy**\n\n"
            "📉 *Enter the minimum amount to invest per purchase (USDT).*\n"
            "For example: `50`"
        ),
        'ask_max_invest': (
            "🔹 **Step 8: Maximum Investment per Buy**\n\n"
            "📈 *Enter the maximum amount to invest per purchase (USDT).*\n"
            "For example: `50`"
        ),
        'ask_blind_freq1': (
            "🔹 **Step 9: Blind DCA Frequency (Strategy 1)**\n\n"
            "⏱️ *Enter the frequency (in days) for Strategy 1 blind DCA purchases.*\n"
            "For example: `7` days"
        ),
        'ask_blind_freq2': (
            "🔹 **Step 10: Blind DCA Frequency (Strategy 2)**\n\n"
            "⏱️ *Enter the frequency (in days) for Strategy 2 blind DCA purchases.*\n"
            "For example: `14` days"
        ),

        # Confirmation & Process Messages
        'confirm_inputs': (
            "✅ **Please review your inputs:**\n\n"
            "• **Crypto Pair:** `{crypto_pair}`\n"
            "• **Total Investment:** `{total_investment}` USDT\n"
            "• **Start Date:** `{start_date}`\n"
            "• **End Date:** `{end_date}`\n"
            "• **Monthly Limit:** `{monthly_limit}` USDT\n"
            "• **Weekly Limit:** `{weekly_limit}` USDT\n"
            "• **Min per Buy:** `{min_invest}` USDT\n"
            "• **Max per Buy:** `{max_invest}` USDT\n"
            "• **Blind DCA Frequency 1:** `{blind_freq1}` days\n"
            "• **Blind DCA Frequency 2:** `{blind_freq2}` days\n\n"
            "🔔 *Are these details correct?*"
        ),
        'processing': (
            "⏳ **Processing...**\n\n"
            "Your data is being downloaded and analyzed. Please wait a few moments."
        ),
        'pipeline_complete': (
            "🎉 **Analysis Complete!**\n\n"
            "Your detailed Crypto & Gold DCA report is ready!\n"
            "Check the charts and reports to see why DCA is a safe, powerful strategy."
        ),

        # Error & Help Messages
        'error': (
            "🚨 **Oops! Something went wrong:**\n"
            "{error}\n\n"
            "Please try again or type /help for assistance."
        ),
        'input_error': (
            "⚠️ **Invalid Input!**\n"
            "The data you entered seems incorrect. Please check and try again."
        ),
        'help': (
            "💡 **Help Menu**\n\n"
            "• **/start** - Restart the analysis process\n"
            "• **/help** - Display this help message\n\n"
            "Use the menu buttons below to navigate."
        ),
        'main_menu': (
            "🏠 **Main Menu**\n\n"
            "Choose an option below:\n"
            "• **Start New Analysis**\n"
            "• **Help**"
        ),

        # Newly Added Keys for Hard-Coded Strings:
        'no_session_error': "No active session found. Please type /start to begin.",
        'operation_cancelled': "Operation cancelled. Please type /start to begin again.",
        'date_invalid_format': "Invalid date format. Please use YYYY-MM-DD. Try again.",
        'end_date_before_start': (
            "⚠️ The end date cannot be earlier than the start date. "
            "Please enter a valid end date (YYYY-MM-DD)."
        ),
        'inputs_confirmed': "Inputs confirmed.",
    },

    'fa': {
        # خوشامدگویی و شروع
        'welcome_intro': (
            "👋 **به ربات تحلیل DCA کریپتو و طلا خوش آمدید!**\n\n"
            "🌟 *جادوی میانگین‌گیری هزینه (DCA) را کشف کنید!*\n\n"
            "این ربات به شما نشان می‌دهد که چرا DCA یک استراتژی سرمایه‌گذاری امن و موثر است.\n"
            "بیایید با انتخاب زبان شروع کنیم."
        ),
        'choose_language': "🌍 **لطفاً زبان خود را انتخاب کنید:**",
        'language_set_en': "✅ *زبان به انگلیسی تنظیم شد!*",
        'language_set_fa': "✅ *زبان به فارسی تنظیم شد!*",

        # پرسش‌های ورودی
        'ask_crypto_pair': (
            "🔹 **مرحله ۱: انتخاب جفت ارز**\n\n"
            "👉 *جفت ارز بایننس مورد نظر خود را وارد کنید.*\n"
            "برای مثال: `BTCUSDT`، `ETHUSDT`، یا `SOLUSDT`.\n\n"
            "می‌توانید تایپ کنید یا از گزینه‌های پیشنهادی استفاده نمایید."
        ),
        'ask_total_investment': (
            "🔹 **مرحله ۲: مقدار سرمایه‌گذاری**\n\n"
            "💰 *بودجه کل سرمایه‌گذاری خود (به دلار) را وارد کنید.*\n"
            "برای مثال: `10000`"
        ),
        'ask_start_date': (
            "🔹 **مرحله ۳: تاریخ شروع تحلیل**\n\n"
            "📅 *تاریخ شروع تحلیل را به فرمت* **YYYY-MM-DD** *وارد کنید.*\n"
            "برای مثال: `2024-01-01`"
        ),
        'ask_end_date': (
            "🔹 **مرحله ۴: تاریخ پایان تحلیل**\n\n"
            "📅 *تاریخ پایان تحلیل را به فرمت* **YYYY-MM-DD** *وارد کنید.*\n"
            "برای مثال: `2025-02-01`"
        ),
        'ask_monthly_limit': (
            "🔹 **مرحله ۵: حد سرمایه‌گذاری ماهانه**\n\n"
            "💳 *حداکثر مبلغ سرمایه‌گذاری ماهانه (به دلار) را وارد کنید.*\n"
            "برای مثال: `750`"
        ),
        'ask_weekly_limit': (
            "🔹 **مرحله ۶: حد سرمایه‌گذاری هفتگی**\n\n"
            "💳 *حداکثر مبلغ سرمایه‌گذاری هفتگی (به دلار) را وارد کنید.*\n"
            "برای مثال: `200`"
        ),
        'ask_min_invest': (
            "🔹 **مرحله ۷: حداقل سرمایه‌گذاری در هر خرید**\n\n"
            "📉 *کمترین مبلغ سرمایه‌گذاری در هر خرید (به دلار) را وارد کنید.*\n"
            "برای مثال: `50`"
        ),
        'ask_max_invest': (
            "🔹 **مرحله ۸: حداکثر سرمایه‌گذاری در هر خرید**\n\n"
            "📈 *بیشترین مبلغ سرمایه‌گذاری در هر خرید (به دلار) را وارد کنید.*\n"
            "برای مثال: `50`"
        ),
        'ask_blind_freq1': (
            "🔹 **مرحله ۹: فاصله زمانی کور DCA (استراتژی ۱)**\n\n"
            "⏱️ *تعداد روزهایی که برای خریدهای کور DCA (استراتژی ۱) مد نظر دارید را وارد کنید.*\n"
            "برای مثال: `7` روز"
        ),
        'ask_blind_freq2': (
            "🔹 **مرحله ۱۰: فاصله زمانی کور DCA (استراتژی ۲)**\n\n"
            "⏱️ *تعداد روزهایی که برای خریدهای کور DCA (استراتژی ۲) مد نظر دارید را وارد کنید.*\n"
            "برای مثال: `14` روز"
        ),

        # تأیید ورودی‌ها
        'confirm_inputs': (
            "✅ **لطفاً ورودی‌های خود را مرور کنید:**\n\n"
            "• **جفت ارز:** `{crypto_pair}`\n"
            "• **بودجه کل:** `{total_investment}` دلار\n"
            "• **تاریخ شروع:** `{start_date}`\n"
            "• **تاریخ پایان:** `{end_date}`\n"
            "• **حد ماهانه:** `{monthly_limit}` دلار\n"
            "• **حد هفتگی:** `{weekly_limit}` دلار\n"
            "• **حداقل در هر خرید:** `{min_invest}` دلار\n"
            "• **حداکثر در هر خرید:** `{max_invest}` دلار\n"
            "• **فاصله کور DCA اول:** `{blind_freq1}` روز\n"
            "• **فاصله کور DCA دوم:** `{blind_freq2}` روز\n\n"
            "🔔 *آیا این اطلاعات صحیح هستند؟*"
        ),
        'processing': (
            "⏳ **در حال پردازش...**\n\n"
            "لطفاً صبور باشید؛ داده‌ها دانلود و تحلیل می‌شوند. این فرایند ممکن است چند دقیقه طول بکشد."
        ),
        'pipeline_complete': (
            "🎉 **تحلیل تکمیل شد!**\n\n"
            "گزارش جامع **DCA کریپتو و طلا** شما آماده است.\n"
            "نمودارها و گزارش‌ها را بررسی کنید تا دریابید چرا DCA یک استراتژی امن و موثر است."
        ),
        'error': (
            "🚨 **متأسفیم! مشکلی پیش آمده:**\n"
            "{error}\n\n"
            "لطفاً دوباره تلاش کنید یا برای راهنما /help را وارد کنید."
        ),
        'input_error': (
            "⚠️ **ورودی نامعتبر!**\n"
            "به نظر می‌رسد داده وارد شده صحیح نیست. لطفاً بررسی کنید و مجدداً تلاش نمایید."
        ),
        'help': (
            "💡 **راهنما**\n\n"
            "دستورات مفید:\n"
            "• **/start** - شروع مجدد\n"
            "• **/help** - نمایش این راهنما\n\n"
            "از دکمه‌های منو برای حرکت بین بخش‌ها استفاده کنید."
        ),
        'main_menu': (
            "🏠 **منوی اصلی**\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n"
            "• **شروع تحلیل جدید**\n"
            "• **راهنما**"
        ),

        # Newly Added Keys for Hard-Coded Strings:
        'no_session_error': "جلسه‌ای یافت نشد. لطفاً /start را وارد کنید تا دوباره شروع کنیم.",
        'operation_cancelled': "عملیات لغو شد. لطفاً /start را وارد کنید تا دوباره شروع کنیم.",
        'date_invalid_format': (
            "قالب تاریخ نامعتبر است. لطفاً از YYYY-MM-DD استفاده کنید و دوباره تلاش کنید."
        ),
        'end_date_before_start': (
            "⚠️ تاریخ پایان نباید قبل از تاریخ شروع باشد. لطفاً دوباره وارد کنید."
        ),
        'inputs_confirmed': "ورودی‌ها تأیید شدند.",
    }
}


def get_message(language, key, **kwargs):
    """
    Retrieve and format a message by language and key.
    Uses Telegram Markdown formatting.
    """
    try:
        return MESSAGES[language][key].format(**kwargs)
    except KeyError:
        print(f"DEBUG: Missing message for language '{language}' and key '{key}'")
        return f"[Missing message for key: {key}]"
