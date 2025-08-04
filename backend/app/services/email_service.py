"""
Сервис для отправки email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Optional
import structlog

from app.core.config import settings
from app.core.celery import celery

logger = structlog.get_logger()

class EmailService:
    """Сервис для отправки email"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME
        
        # Настройка Jinja2 для шаблонов
        template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
    
    async def send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Отправка email (синхронная версия для использования в Celery)"""
        try:
            # Создание сообщения
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            
            # Добавление текстовой версии
            if text_content:
                text_part = MIMEText(text_content, "plain", "utf-8")
                msg.attach(text_part)
            
            # Добавление HTML версии
            html_part = MIMEText(html_content, "html", "utf-8")
            msg.attach(html_part)
            
            # Отправка через SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info("Email sent successfully", to_email=to_email, subject=subject)
            return True
            
        except Exception as e:
            logger.error("Failed to send email", to_email=to_email, error=str(e))
            return False
    
    async def send_password_reset_email(self, email: str, reset_token: str) -> bool:
        """Отправка email для сброса пароля"""
        reset_url = f"{settings.CORS_ORIGINS.split(',')[0]}/reset-password?token={reset_token}"
        
        # Загрузка шаблона
        template = self.jinja_env.get_template("password_reset.html")
        html_content = template.render(
            reset_url=reset_url,
            app_name=settings.PROJECT_NAME
        )
        
        # Отправка через Celery (асинхронно)
        send_email_task.delay(
            to_email=email,
            subject="Сброс пароля",
            html_content=html_content
        )
        
        return True
    
    async def send_welcome_email(self, email: str, username: str) -> bool:
        """Отправка приветственного email"""
        template = self.jinja_env.get_template("welcome.html")
        html_content = template.render(
            username=username,
            app_name=settings.PROJECT_NAME,
            app_url=settings.CORS_ORIGINS.split(',')[0]
        )
        
        send_email_task.delay(
            to_email=email,
            subject=f"Добро пожаловать в {settings.PROJECT_NAME}!",
            html_content=html_content
        )
        
        return True
    
    async def send_article_notification(
        self, 
        email: str, 
        username: str,
        article_title: str,
        article_url: str,
        author_name: str
    ) -> bool:
        """Отправка уведомления о новой статье"""
        template = self.jinja_env.get_template("new_article.html")
        html_content = template.render(
            username=username,
            article_title=article_title,
            article_url=article_url,
            author_name=author_name,
            app_name=settings.PROJECT_NAME
        )
        
        send_email_task.delay(
            to_email=email,
            subject=f"Новая статья от {author_name}",
            html_content=html_content
        )
        
        return True

# Celery задача для отправки email
@celery.task
def send_email_task(to_email: str, subject: str, html_content: str, text_content: str = None):
    """Celery задача для отправки email"""
    email_service = EmailService()
    
    try:
        # Создание сообщения
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{email_service.from_name} <{email_service.from_email}>"
        msg["To"] = to_email
        
        # Добавление текстовой версии
        if text_content:
            text_part = MIMEText(text_content, "plain", "utf-8")
            msg.attach(text_part)
        
        # Добавление HTML версии
        html_part = MIMEText(html_content, "html", "utf-8")
        msg.attach(html_part)
        
        # Отправка через SMTP
        with smtplib.SMTP(email_service.smtp_host, email_service.smtp_port) as server:
            if settings.SMTP_TLS:
                server.starttls()
            
            server.login(email_service.smtp_user, email_service.smtp_password)
            server.send_message(msg)
        
        logger.info("Email sent successfully via Celery", to_email=to_email, subject=subject)
        return True
        
    except Exception as e:
        logger.error("Failed to send email via Celery", to_email=to_email, error=str(e))
        return False
