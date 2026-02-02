# app/services/email.py
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import logging
from typing import Dict, Any
from config import settings  # Import your existing settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Use settings from your existing config
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.use_tls = settings.SMTP_USE_TLS
        self.from_name = settings.EMAIL_FROM_NAME
        self.from_address = settings.EMAIL_FROM_ADDRESS
        
        # Setup templates if directory exists
        template_dir = Path(settings.EMAIL_TEMPLATES_DIR)
        if template_dir.exists():
            self.env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=True
            )
        else:
            self.env = None
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str = None,
        text_content: str = None
    ) -> bool:
        """Send email - minimal version"""
        
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_address}>"
            message["To"] = to_email
            
            if text_content:
                message.attach(MIMEText(text_content, "plain"))
            
            if html_content:
                message.attach(MIMEText(html_content, "html"))
            
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=self.use_tls
            ) as smtp:
                await smtp.login(self.smtp_user, self.smtp_password)
                await smtp.send_message(message)
            
            logger.info(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    # ESSENTIAL STUDENT EMAILS
    async def send_student_welcome(
        self,
        student_email: str,
        student_name: str,
        student_id: str,
        verification_token: str = None
    ) -> bool:
        """Send welcome email to new student"""
        
        # Build verification link if token provided
        verification_link = ""
        if verification_token and hasattr(settings, 'FRONTEND_URL'):
            verification_link = f"{settings.FRONTEND_URL}/verify/{verification_token}"
        
        # Simple HTML email (no template required)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: #4CAF50; color: white; padding: 20px; text-align: center;">
                    <h1>🎓 Welcome to Student Platform!</h1>
                </div>
                
                <div style="padding: 20px; background: #f9f9f9;">
                    <h2>Hello {student_name},</h2>
                    <p>Your student account has been successfully created.</p>
                    
                    <div style="background: white; padding: 15px; margin: 20px 0; border-radius: 5px;">
                        <h3>Your Student Details:</h3>
                        <p><strong>Student ID:</strong> {student_id}</p>
                        <p><strong>Email:</strong> {student_email}</p>
                    </div>
                    
                    {verification_link and f'''
                    <div style="text-align: center; margin: 25px 0;">
                        <a href="{verification_link}" 
                           style="background: #2196F3; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 5px;">
                            Verify Your Email
                        </a>
                    </div>
                    '''}
                    
                    <p>You can now login to your student portal.</p>
                    
                    <p>Best regards,<br>
                    <strong>{self.from_name}</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(
            to_email=student_email,
            subject=f"Welcome {student_name}! - Student Platform",
            html_content=html_content
        )
    
    async def send_password_reset(
        self,
        email: str,
        reset_token: str
    ) -> bool:
        """Send password reset email"""
        
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset_token}"
        
        html_content = f"""
        <div style="padding: 20px;">
            <h2>Password Reset Request</h2>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_link}" 
               style="background: #FF5722; color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 5px; display: inline-block;">
                Reset Password
            </a>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </div>
        """
        
        return await self.send_email(
            to_email=email,
            subject="Reset Your Password - Student Platform",
            html_content=html_content
        )
    
    async def send_simple_notification(
        self,
        to_email: str,
        subject: str,
        message: str
    ) -> bool:
        """Send simple text notification"""
        return await self.send_email(
            to_email=to_email,
            subject=subject,
            text_content=message
        )

# Create a global instance for easy access
email_service = EmailService()