import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# کلیدهای امنیتی (از متغیرهای محیطی خوانده می‌شوند)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# تنظیمات گوگل AI
genai.configure(api_key=GEMINI_API_KEY)

# پرامپت شخصیت‌سازی (لحن خودمونی + بی‌پردگی و فحش)
SYSTEM_PROMPT = """
تو یک رفیق خیلی خودمونی، لاتی، شوخ و بی‌پردگی در گپ تلگرامی هستی.
لحنت کاملا عامیانه، صمیمی و تهرونی باشه.
اجازه داری از کلمات و تکیه‌کلام‌های کوچه خیابونی ایرانی استفاده کنی.
خیلی رسمی یا عصا قورت‌داده حرف نزن! مثل یک رفیق صمیمی کلافه یا باحال توی گپ جواب بده.
جواب‌هات کوتاه و تلگرامی باشه (طولانی ننویس).
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چاکریم داداش! چه خبر؟ چی می‌خوای باز؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    try:
        # ارسال پیام به Gemini
        response = model.generate_content(user_text)
        reply_text = response.text
        await update.message.reply_text(reply_text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("دمت گرم گند زدی به سیستم، یکم دیگه دوباره بگو!")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Robot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
