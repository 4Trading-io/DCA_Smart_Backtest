"""
messages.py

This module stores all user-facing messages (prompts, errors, menus, etc.) for the Crypto & Gold DCA Analysis Bot.
It supports two languages:
    • English ('en')
    • Farsi ('fa')

Each message is crafted for clarity and engagement with ample spacing and attractive emoji embellishments.
"""

MESSAGES = {
    "en": {
        "welcome_intro": (
            "👋 **Welcome to the Crypto & Gold DCA Analysis Bot!**\n\n"
            "✨ **Discover the magic of Dollar-Cost Averaging (DCA)!**\n\n"
            "–––––––––––––––––––––––––––––––––––––––––––\n\n"
            "### What is DCA?\n\n"
            "Dollar-Cost Averaging (DCA) is an investment strategy where you invest a fixed amount of money at regular intervals—"
            "regardless of market fluctuations. This approach helps to smooth out the impact of short-term volatility and reduces "
            "the risk associated with market timing.\n\n"
            "–––––––––––––––––––––––––––––––––––––––––––\n\n"
            "### What does this bot do?\n\n"
            "1️⃣ **Historical Data Collection:**\n"
            "   • Retrieves historical price data for your chosen crypto pair (e.g., BTCUSDT, ETHUSDT) from Binance.\n"
            "   • Collects 1-gram gold prices (in local currency) from Navasan.\n"
            "   • Fetches the USD to Rial exchange rate from Navasan.\n\n"
            "2️⃣ **Gold Price Conversion:**\n"
            "   • Converts gold prices from local currency to USD for a fair comparison with cryptocurrencies priced in USDT.\n\n"
            "3️⃣ **DCA Simulation & Optimization:**\n"
            "   • Runs a blind DCA strategy using fixed-interval purchases.\n"
            "   • Employs an ILP model to determine the optimal buying strategy over your selected time period.\n\n"
            "4️⃣ **Comparison & Reporting:**\n"
            "   • Generates comprehensive reports, interactive charts, and Excel files to display the performance of each strategy.\n\n"
            "–––––––––––––––––––––––––––––––––––––––––––\n\n"
            "Let's start by selecting your preferred language."
        ),
        "choose_language": "🌍 **Please select your language:**",
        "language_set_en": "✅ *Language set to English!*",
        "language_set_fa": "✅ *Language set to فارسی!*",
        "ask_crypto_pair": (
            "🔸 **Step 1: Crypto Pair Selection**\n\n"
            "👉 *Enter the Binance crypto pair you wish to analyze.*\n"
            "For example: `BTCUSDT`, `ETHUSDT`, or `SOLUSDT`.\n\n"
            "Feel free to type it in or choose from the provided options."
        ),
        "ask_total_investment": (
            "🔸 **Step 2: Investment Amount**\n\n"
            "💰 *Enter your total investment budget in USDT.*\n"
            "For example: `10000`"
        ),
        "ask_start_date": (
            "🔸 **Step 3: Backtest Start Date**\n\n"
            "📅 *Enter the start date for the backtest (YYYY-MM-DD).*\n"
            "For example: `2024-01-01`"
        ),
        "ask_end_date": (
            "🔸 **Step 4: Backtest End Date**\n\n"
            "📅 *Enter the end date for the backtest (YYYY-MM-DD).*\n"
            "For example: `2025-02-01`"
        ),
        "ask_monthly_limit": (
            "🔸 **Step 5: Monthly Investment Limit**\n\n"
            "💳 *Enter the maximum amount you will invest per month (in USDT).*\n"
            "For example: `750`"
        ),
        "ask_weekly_limit": (
            "🔸 **Step 6: Weekly Investment Limit**\n\n"
            "💳 *Enter the maximum amount you will invest per week (in USDT).*\n"
            "For example: `200`"
        ),
        "ask_min_invest": (
            "🔸 **Step 7: Minimum Investment per Buy**\n\n"
            "📉 *Enter the minimum amount to invest per purchase (in USDT).*\n"
            "For example: `50`"
        ),
        "ask_max_invest": (
            "🔸 **Step 8: Maximum Investment per Buy**\n\n"
            "📈 *Enter the maximum amount to invest per purchase (in USDT).*\n"
            "For example: `50`"
        ),
        "ask_blind_freq1": (
            "🔸 **Step 9: Blind DCA Frequency (Strategy 1)**\n\n"
            "⏱️ *Enter the frequency (in days) for blind DCA purchases using Strategy 1.*\n"
            "For example: `7` "
        ),
        "ask_blind_freq2": (
            "🔸 **Step 10: Blind DCA Frequency (Strategy 2)**\n\n"
            "⏱️ *Enter the frequency (in days) for blind DCA purchases using Strategy 2.*\n"
            "For example: `14` "
        ),
        "confirm_inputs": (
            "✅ **Please review your inputs:**\n\n"
            "• **Crypto Pair:** `{crypto_pair}`\n"
            "• **Total Investment:** `{total_investment}` USDT\n"
            "• **Start Date:** `{start_date}`\n"
            "• **End Date:** `{end_date}`\n"
            "• **Monthly Limit:** `{monthly_limit}` USDT\n"
            "• **Weekly Limit:** `{weekly_limit}` USDT\n"
            "• **Minimum per Buy:** `{min_invest}` USDT\n"
            "• **Maximum per Buy:** `{max_invest}` USDT\n"
            "• **Blind DCA Frequency 1:** `{blind_freq1}` days\n"
            "• **Blind DCA Frequency 2:** `{blind_freq2}` days\n\n"
            "🔔 *Are these details correct?*"
        ),
        "processing": (
            "⌛ **Processing...**\n\n"
            "Your data is being downloaded and analyzed. Please hold tight—it may take a moment."
        ),
        "pipeline_complete": (
            "🎉 **Analysis Complete!**\n\n"
            "Your comprehensive Crypto & Gold DCA report is ready for review.\n"
            "Check out the detailed charts and Excel reports to see why DCA is a safe and powerful strategy."
        ),
        "error": (
            "🚨 **Oops! Something went wrong:**\n"
            "{error}\n\n"
            "Please try again or type /help for assistance."
        ),
        "input_error": (
            "⚠️ **Invalid Input!**\n"
            "The information you provided appears to be incorrect. Please double-check and try again."
        ),
        "help": (
            "💡 **Help Menu**\n\n"
            "Here are some useful commands:\n"
            "• **/start** - Restart the analysis process\n"
            "• **/help** - Display this help message\n\n"
            "Use the menu buttons below to navigate."
        ),
        "main_menu": (
            "🏠 **Main Menu**\n\n"
            "Please choose one of the options below:\n"
            "• **Start New Analysis**\n"
            "• **Help**"
        ),
        "no_session_error": "🚫 No active session found. Please type /start to begin a new session.",
        "operation_cancelled": "❌ Operation cancelled. Please type /start to restart.",
        "date_invalid_format": "❗ Invalid date format. Please use YYYY-MM-DD. Try again.",
        "end_date_before_start": (
            "⚠️ The end date cannot be earlier than the start date. "
            "Please enter a valid end date in the format YYYY-MM-DD."
        ),
        "inputs_confirmed": "✅ Inputs confirmed. Proceeding with analysis..."
    },
    "fa": {
        "welcome_intro": (
            "👋 **به ربات تحلیل DCA کریپتو و طلا خوش آمدید!**\n\n"
            "✨ **جادوی میانگین‌گیری هزینه (DCA) را کشف کنید!**\n\n"
            "–––––––––––––––––––––––––––––––––––––––––––\n\n"
            "### DCA چیست؟\n\n"
            "DCA (میانگین‌گیری هزینه) یک استراتژی سرمایه‌گذاری است که در آن شما با مبالغ ثابت و در فواصل زمانی منظم سرمایه‌گذاری می‌کنید، "
            "بدون توجه به نوسانات کوتاه‌مدت قیمت. این روش به شما کمک می‌کند تا از تأثیرات شدید نوسانات بازار کاسته و ریسک کلی سرمایه‌گذاری خود را کاهش دهید.\n\n"
            "–––––––––––––––––––––––––––––––––––––––––––\n\n"
            "### این ربات چه امکاناتی دارد؟\n\n"
            "1️⃣ **گردآوری داده‌های تاریخی:**\n"
            "   • دریافت داده‌های تاریخی جفت ارز کریپتویی شما (مثلاً BTCUSDT, ETHUSDT) از بایننس.\n"
            "   • جمع‌آوری قیمت طلای یک‌گرمی در ایران (به تومان) از نوآسان.\n"
            "   • دریافت نرخ تبدیل دلار به تومان از نوآسان.\n\n"
            "2️⃣ **تبدیل قیمت طلا به دلار:**\n"
            "   • تبدیل قیمت طلا از تومان به دلار برای مقایسه منصفانه با قیمت‌های کریپتو (قیمت‌گذاری در USDT).\n\n"
            "3️⃣ **شبیه‌سازی DCA و بهینه‌سازی:**\n"
            "   • اجرای استراتژی کور DCA با خریدهای دوره‌ای ثابت.\n"
            "   • استفاده از مدل ILP برای یافتن استراتژی بهینه خرید در بازه‌های زمانی مشخص.\n\n"
            "4️⃣ **مقایسه و گزارش:**\n"
            "   • تولید گزارش‌های جامع، نمودارهای تعاملی و فایل‌های اکسل جهت نمایش عملکرد استراتژی‌ها.\n\n"
            "–––––––––––––––––––––––––––––––––––––––––––\n\n"
            "بیایید با انتخاب زبان مورد نظر، فرآیند را آغاز کنیم."
            "لطفا تمامی اعداد را به انگلیسی وارد کنید"
        ),
        "choose_language": "🌍 **لطفاً زبان خود را انتخاب کنید:**",
        "language_set_en": "✅ *زبان به انگلیسی تنظیم شد!*",
        "language_set_fa": "✅ *زبان به فارسی تنظیم شد!*",
        "ask_crypto_pair": (
            "🔸 **مرحله ۱: انتخاب جفت ارز**\n\n"
            "👉 *جفت ارز بایننس مورد نظر خود را وارد کنید.*\n"
            "برای مثال: `BTCUSDT`، `ETHUSDT` یا `SOLUSDT`.\n\n"
            "می‌توانید تایپ کنید یا از گزینه‌های پیشنهادی استفاده نمایید."
        ),
        "ask_total_investment": (
            "🔸 **مرحله ۲: مقدار سرمایه‌گذاری**\n\n"
            "💰 *بودجه کل سرمایه‌گذاری خود (به دلار) را وارد کنید.*\n"
            "برای مثال: `10000`"
        ),
        "ask_start_date": (
            "🔸 **مرحله ۳: تاریخ شروع تحلیل**\n\n"
            "📅 *تاریخ شروع تحلیل را به فرمت YYYY-MM-DD وارد کنید.*\n"
            "برای مثال: `2024-01-01`"
        ),
        "ask_end_date": (
            "🔸 **مرحله ۴: تاریخ پایان تحلیل**\n\n"
            "📅 *تاریخ پایان تحلیل را به فرمت YYYY-MM-DD وارد کنید.*\n"
            "برای مثال: `2025-02-01`"
        ),
        "ask_monthly_limit": (
            "🔸 **مرحله ۵: حد سرمایه‌گذاری ماهانه**\n\n"
            "💳 *حداکثر مبلغ سرمایه‌گذاری ماهانه (به دلار) را وارد کنید.*\n"
            "برای مثال: `750`"
        ),
        "ask_weekly_limit": (
            "🔸 **مرحله ۶: حد سرمایه‌گذاری هفتگی**\n\n"
            "💳 *حداکثر مبلغ سرمایه‌گذاری هفتگی (به دلار) را وارد کنید.*\n"
            "برای مثال: `200`"
        ),
        "ask_min_invest": (
            "🔸 **مرحله ۷: حداقل سرمایه‌گذاری در هر خرید**\n\n"
            "📉 *کمترین مبلغ سرمایه‌گذاری در هر خرید (به دلار) را وارد کنید.*\n"
            "برای مثال: `50`"
        ),
        "ask_max_invest": (
            "🔸 **مرحله ۸: حداکثر سرمایه‌گذاری در هر خرید**\n\n"
            "📈 *بیشترین مبلغ سرمایه‌گذاری در هر خرید (به دلار) را وارد کنید.*\n"
            "برای مثال: `50`"
        ),
        "ask_blind_freq1": (
            "🔸 **مرحله ۹: فاصله زمانی کور DCA (استراتژی ۱)**\n\n"
            "⏱️ *تعداد روزهای مد نظر برای خریدهای کور DCA (استراتژی ۱) را وارد کنید.*\n"
            "برای مثال: `7` "
        ),
        "ask_blind_freq2": (
            "🔸 **مرحله ۱۰: فاصله زمانی کور DCA (استراتژی ۲)**\n\n"
            "⏱️ *تعداد روزهای مد نظر برای خریدهای کور DCA (استراتژی ۲) را وارد کنید.*\n"
            "برای مثال: `14` "
        ),
        "confirm_inputs": (
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
        "processing": (
            "⌛ **در حال پردازش...**\n\n"
            "لطفاً کمی صبر کنید؛ داده‌ها در حال دانلود و تحلیل می‌باشند. این فرایند ممکن است چند دقیقه طول بکشد."
        ),
        "pipeline_complete": (
            "🎉 **تحلیل تکمیل شد!**\n\n"
            "گزارش جامع **DCA کریپتو و طلا** شما آماده است.\n"
            "نمودارها و گزارش‌ها را بررسی کنید تا دریابید چرا DCA یک استراتژی امن و موثر است."
        ),
        "error": (
            "🚨 **متأسفیم! مشکلی پیش آمده:**\n"
            "{error}\n\n"
            "لطفاً دوباره تلاش کنید یا برای راهنما /help را وارد کنید."
        ),
        "input_error": (
            "⚠️ **ورودی نامعتبر!**\n"
            "به نظر می‌رسد اطلاعات وارد شده صحیح نمی‌باشد. لطفاً بررسی کنید و مجدداً تلاش نمایید."
        ),
        "help": (
            "💡 **راهنما**\n\n"
            "دستورات مفید:\n"
            "• **/start** - شروع مجدد فرایند\n"
            "• **/help** - نمایش این راهنما\n\n"
            "از دکمه‌های منو برای حرکت بین بخش‌ها استفاده کنید."
        ),
        "main_menu": (
            "🏠 **منوی اصلی**\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:\n"
            "• **شروع تحلیل جدید**\n"
            "• **راهنما**"
        ),
        "no_session_error": "🚫 جلسه فعالی یافت نشد. لطفاً /start را وارد کنید تا دوباره شروع کنیم.",
        "operation_cancelled": "❌ عملیات لغو شد. لطفاً /start را وارد کنید تا دوباره شروع کنیم.",
        "date_invalid_format": "❗ قالب تاریخ نامعتبر است. لطفاً از فرمت YYYY-MM-DD استفاده کنید و دوباره تلاش نمایید.",
        "end_date_before_start": (
            "⚠️ تاریخ پایان نباید قبل از تاریخ شروع باشد. "
            "لطفاً یک تاریخ پایان معتبر (YYYY-MM-DD) وارد کنید."
        ),
        "inputs_confirmed": "✅ ورودی‌ها تأیید شدند. در حال ادامه تحلیل..."
    }
}

def get_message(language, key, **kwargs):
    """
    Retrieve and format a message based on the specified language and key.
    This function fetches a message template from the MESSAGES dictionary.
    If the template includes placeholders (e.g., {crypto_pair}), they will be replaced
    by the corresponding keyword arguments.
    If an unsupported language is requested, the function falls back to English.
    If the key is missing, a debug message is printed and a default error message is returned.
    Parameters:
        language (str): The language code ('en' or 'fa').
        key (str): The message key.
        **kwargs: Additional parameters for message formatting.
    Returns:
        str: The formatted message ready for display.
    """
    if language not in MESSAGES:
        print(f"DEBUG: Unsupported language '{language}'. Falling back to English.")
        language = "en"
    message_template = MESSAGES[language].get(key)
    if message_template is None:
        print(f"DEBUG: Missing message for language '{language}' and key '{key}'.")
        return f"[Missing message for key: {key}]"
    return message_template.format(**kwargs)
