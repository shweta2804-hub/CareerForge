from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings
from typing import List, Optional


class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.SMTP_USER,
            MAIL_PASSWORD=settings.SMTP_PASSWORD,
            MAIL_FROM=settings.EMAILS_FROM_EMAIL,
            MAIL_PORT=settings.SMTP_PORT,
            MAIL_SERVER=settings.SMTP_HOST,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
        self.fastmail = FastMail(self.conf)

    async def send_email(
        self,
        subject: str,
        recipients: List[EmailStr],
        body: str,
        html: Optional[str] = None
    ) -> bool:
        """Send email to recipients."""
        try:
            message = MessageSchema(
                subject=subject,
                recipients=recipients,
                body=body,
                html=html,
                subtype="html" if html else "plain",
            )
            await self.fastmail.send_message(message)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    async def send_new_drive_notification(
        self,
        student_email: EmailStr,
        student_name: str,
        company_name: str,
        drive_date: str,
        deadline: str
    ) -> bool:
        """Send notification about new placement drive."""
        subject = f"New Placement Drive: {company_name}"
        body = f"""
        Dear {student_name},

        A new placement drive has been announced!

        Company: {company_name}
        Drive Date: {drive_date}
        Application Deadline: {deadline}

        Log in to CareerForge to apply now!

        Best regards,
        CareerForge Team
        """
        html = f"""
        <html>
            <body>
                <h2>New Placement Drive Announcement</h2>
                <p>Dear {student_name},</p>
                <p>A new placement drive has been announced!</p>
                <ul>
                    <li><strong>Company:</strong> {company_name}</li>
                    <li><strong>Drive Date:</strong> {drive_date}</li>
                    <li><strong>Application Deadline:</strong> {deadline}</li>
                </ul>
                <p>Log in to <a href="{settings.FRONTEND_URL}">CareerForge</a> to apply now!</p>
                <p>Best regards,<br>CareerForge Team</p>
            </body>
        </html>
        """
        return await self.send_email(subject, [student_email], body, html)

    async def send_application_confirmation(
        self,
        student_email: EmailStr,
        student_name: str,
        company_name: str,
        application_id: int
    ) -> bool:
        """Send application confirmation email."""
        subject = f"Application Confirmed: {company_name}"
        body = f"""
        Dear {student_name},

        Your application for {company_name} has been successfully submitted!

        Application ID: {application_id}

        You can track your application status in the CareerForge portal.

        Best regards,
        CareerForge Team
        """
        html = f"""
        <html>
            <body>
                <h2>Application Confirmed</h2>
                <p>Dear {student_name},</p>
                <p>Your application for <strong>{company_name}</strong> has been successfully submitted!</p>
                <p><strong>Application ID:</strong> {application_id}</p>
                <p>You can track your application status in the <a href="{settings.FRONTEND_URL}">CareerForge</a> portal.</p>
                <p>Best regards,<br>CareerForge Team</p>
            </body>
        </html>
        """
        return await self.send_email(subject, [student_email], body, html)

    async def send_status_update(
        self,
        student_email: EmailStr,
        student_name: str,
        company_name: str,
        new_status: str
    ) -> bool:
        """Send application status update email."""
        subject = f"Application Status Update: {company_name}"
        body = f"""
        Dear {student_name},

        Your application status for {company_name} has been updated.

        New Status: {new_status}

        Log in to CareerForge for more details.

        Best regards,
        CareerForge Team
        """
        html = f"""
        <html>
            <body>
                <h2>Application Status Update</h2>
                <p>Dear {student_name},</p>
                <p>Your application status for <strong>{company_name}</strong> has been updated.</p>
                <p><strong>New Status:</strong> {new_status}</p>
                <p>Log in to <a href="{settings.FRONTEND_URL}">CareerForge</a> for more details.</p>
                <p>Best regards,<br>CareerForge Team</p>
            </body>
        </html>
        """
        return await self.send_email(subject, [student_email], body, html)