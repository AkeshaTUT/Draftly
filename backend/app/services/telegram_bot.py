# Телеграм бот для уведомлений
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.core.config import settings

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Телеграм бот для уведомлений"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.app = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        await update.message.reply_text(
            f"Добро пожаловать в {settings.PROJECT_NAME}!\n\n"
            "Этот бот будет присылать вам уведомления о новых комментариях, "
            "лайках и других активностях на ваших статьях.\n\n"
            f"Ваш Chat ID: {update.effective_chat.id}"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        await update.message.reply_text(
            "Доступные команды:\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать эту справку\n"
            "/status - Статус подписки на уведомления"
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /status"""
        chat_id = update.effective_chat.id
        # TODO: Проверить статус пользователя в базе данных
        await update.message.reply_text(
            f"Chat ID: {chat_id}\n"
            "Статус: Активен\n"
            "Уведомления: Включены"
        )
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        if not self.app:
            self.app = Application.builder().token(self.token).build()
        
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
    
    async def send_notification(self, chat_id: str, message: str):
        """Отправка уведомления пользователю"""
        if not self.app:
            self.setup_handlers()
        
        try:
            await self.app.bot.send_message(chat_id=chat_id, text=message)
            logger.info(f"Notification sent to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send notification to {chat_id}: {e}")
    
    def run(self):
        """Запуск бота"""
        if not self.token:
            logger.error("Telegram bot token not configured")
            return
        
        self.setup_handlers()
        self.app.run_polling()

# Инициализация бота
telegram_bot = TelegramBot()

if __name__ == "__main__":
    telegram_bot.run()
