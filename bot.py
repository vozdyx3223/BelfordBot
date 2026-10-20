import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# TOKEN берём из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Не найден BOT_TOKEN")


# Веб-сервер для Render
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Belford Team Bot is running!"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


# Главное меню
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Прайсы", callback_data="prices")],
        [InlineKeyboardButton("📚 Информация", callback_data="info")],
        [InlineKeyboardButton("💎 Premium", callback_data="premium")],
        [InlineKeyboardButton("📞 Поддержка", callback_data="support")],
    ]

    return InlineKeyboardMarkup(keyboard)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 BELFORD TEAM\n\n"
        "Добро пожаловать!\n\n"
        "Здесь вы можете ознакомиться с обучением "
        "криптотрейдингу от BELFORD TEAM.\n\n"
        "Выберите нужный раздел:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


# Обработка кнопок
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "prices":
        text = (
            "📊 ПРАЙСЫ\n\n"
            "БАЗОВЫЙ КУРС\n"
            "Цена: УКАЖИ ЦЕНУ\n\n"
            "💎 PREMIUM\n"
            "Цена: УКАЖИ ЦЕНУ\n\n"
            "Для покупки обратитесь в поддержку."
        )

    elif query.data == "info":
        text = (
            "📚 ИНФОРМАЦИЯ\n\n"
            "На обучении вы узнаете:\n\n"
            "• Основы криптотрейдинга\n"
            "• Анализ рынка\n"
            "• Работа с графиками\n"
            "• Торговая стратегия\n"
            "• Управление рисками"
        )

    elif query.data == "premium":
        text = (
            "💎 PREMIUM\n\n"
            "Расширенная программа обучения "
            "и дополнительные материалы.\n\n"
            "Цена: УКАЖИ ЦЕНУ\n\n"
            "Для покупки обратитесь в поддержку."
        )

    elif query.data == "support":
        text = (
            "📞 ПОДДЕРЖКА\n\n"
            "По вопросам обучения и покупки "
            "обращайтесь к администратору:\n\n"
            "@YOUR_USERNAME"
        )

    else:
        text = "Неизвестная команда."

    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Кнопка "Назад"
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🤖 BELFORD TEAM\n\n"
        "Выберите нужный раздел:",
        reply_markup=main_menu()
    )


# Запуск Telegram-бота
def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        CallbackQueryHandler(back, pattern="^back$")
    )
    application.add_handler(
        CallbackQueryHandler(buttons)
    )

    application.run_polling()


# Запускаем веб-сервер отдельно
threading.Thread(
    target=run_web,
    daemon=True
).start()


# Запускаем Telegram
run_bot()