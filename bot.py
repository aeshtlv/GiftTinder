import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, WEBAPP_URL

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with the web app button."""
    keyboard = [
        [InlineKeyboardButton("🎁 Gift Tinder", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎁 Добро пожаловать в Gift Tinder!\n\n"
        "Нажмите кнопку ниже, чтобы начать оценивать подарки других пользователей "
        "и найти тех, кто оценил ваши подарки!",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    help_text = """
🎁 Gift Tinder - Помощь

📱 Как использовать:
1. Нажмите кнопку "Gift Tinder" для запуска приложения
2. Свайпайте вправо для лайка, влево для дизлайка
3. При взаимном лайке произойдет мэтч!
4. Общайтесь с мэтчами в чате

⚙️ Команды:
/start - Запустить приложение
/help - Показать эту справку
/profile - Ваш профиль
/matches - Ваши мэтчи

🔒 Безопасность:
- Приложение работает только с вашими подарками
- Данные защищены Telegram WebApp API
- Никто не видит ваши личные данные

📞 Поддержка: @aeshtlv
    """
    
    await update.message.reply_text(help_text)

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📊 Мой профиль", web_app=WebAppInfo(url=f"{WEBAPP_URL}/profile"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👤 Профиль пользователя {user.first_name}\n\n"
        "Нажмите кнопку ниже, чтобы посмотреть свой профиль и статистику:",
        reply_markup=reply_markup
    )

async def matches_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user matches."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("💕 Мои мэтчи", web_app=WebAppInfo(url=f"{WEBAPP_URL}/matches"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "💕 Ваши мэтчи\n\n"
        "Нажмите кнопку ниже, чтобы посмотреть ваши мэтчи и начать общение:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    # Handle different button callbacks if needed
    if query.data == "start_app":
        keyboard = [
            [InlineKeyboardButton("🎁 Gift Tinder", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎁 Добро пожаловать в Gift Tinder!\n\n"
            "Нажмите кнопку ниже, чтобы начать:",
            reply_markup=reply_markup
        )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("matches", matches_command))
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot
    logger.info("Starting Gift Tinder Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 