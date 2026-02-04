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
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 465
        
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.use_tls = settings.SMTP_USE_TLS
        self.from_name = settings.EMAIL_FROM_NAME
        self.from_address = settings.EMAIL_FROM_ADDRESS
        print("sett",settings.SMTP_PASSWORD,settings.SMTP_USER)
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
                print("Login")
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
        student_id:str
        
    ) -> bool:
        """Send welcome email to new student"""
        
        # Build verification link if token provided
        
        
        # Simple HTML email (no template required)
        html_content =f"""
                <!DOCTYPE html>
                <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 8px; overflow: hidden;">
                        
                        <div style="background: #0f4c81; color: #ffffff; padding: 25px; text-align: center;">
                            <h1>🎓 Welcome to Edvantage</h1>
                            <p>Empowering oil & gas professionals</p>
                        </div>

                        <div style="padding: 25px; color: #333;">
                            <h2>Hello {student_name},</h2>
                            
                            <p>
                                Welcome to <strong>Edvantage</strong> — your learning platform for
                                world-class training, consultancy, and industry connections in the
                                oil & gas sector.
                            </p>

                            <div style="background: #f1f5f9; padding: 15px; border-radius: 6px; margin: 20px 0;">
                                <p><strong>Student ID:</strong> ED-LE-{student_id}</p>
                                <p><strong>Email:</strong> {student_email}</p>
                            </div>

                          <p>
    You can now log in and begin your learning journey with us.
</p>

<div style="text-align: center; margin: 30px 0;">
    <a href="https://www.edvantage.org.in/login"
       target="_blank"
       style="
            display: inline-block;
            background-color: #0f4c81;
            color: #ffffff;
            text-decoration: none;
            padding: 14px 28px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
       ">
        🔐 Log in to Edvantage
    </a>
</div>

<p style="font-size: 14px; color: #666;">
    If the button doesn’t work, copy and paste this link into your browser:<br>
    <a href="https://www.edvantage.org.in/login" target="_blank">
        https://www.edvantage.org.in/login
    </a>
</p>


                            <p>
                                Best regards,<br>
                                <strong>Edvantage Team</strong>
                            </p>
                        </div>

                        <div style="background: #f9fafb; padding: 15px; text-align: center; font-size: 14px;">
                            <p>Connect with us</p>
                            <a href="https://www.linkedin.com/company/edvantagelearning/" target="_blank">LinkedIn</a> |
                            <a href="https://www.youtube.com/@edvantagelearning3858" target="_blank">YouTube</a> |
                            <a href="https://www.instagram.com/edvantage_learning" target="_blank">Instagram</a>
                        </div>

                    </div>
                </body>
                </html>
                """
        
        
        return await self.send_email(
            to_email=student_email,
            subject=f"Welcome {student_name}! - Edvantage Learning",
            html_content=html_content
        )
    
    async def send_password_reset(
        self,
        email: str,
        reset_token: str
    ) -> bool:
        """Send password reset email"""
        
        
        
              








        
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