import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from datetime import datetime
import httpx
from app.core.config import settings


class AlertService:
    def __init__(self):
        self.email_enabled = bool(getattr(settings, 'smtp_host', None))
        self.smtp_host = getattr(settings, 'smtp_host', 'localhost')
        self.smtp_port = getattr(settings, 'smtp_port', 587)
        self.smtp_user = getattr(settings, 'smtp_user', None)
        self.smtp_password = getattr(settings, 'smtp_password', None)
        self.alert_from = getattr(settings, 'alert_from', 'alerts@milintel.local')
        self.alert_to = getattr(settings, 'alert_to', '').split(',') if getattr(settings, 'alert_to', None) else []

        self.slack_enabled = bool(getattr(settings, 'slack_webhook_url', None))
        self.slack_webhook_url = getattr(settings, 'slack_webhook_url', None)

    async def send_email_alert(self, subject: str, body: str, html: bool = False) -> bool:
        """Send an email alert."""
        if not self.email_enabled or not self.alert_to:
            return False

        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.alert_from
            msg['To'] = ', '.join(self.alert_to)
            msg['Subject'] = subject

            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            await asyncio.get_event_loop().run_in_executor(
                None,
                self._send_smtp,
                msg
            )
            return True
        except Exception as e:
            print(f"Failed to send email alert: {e}")
            return False

    def _send_smtp(self, msg: MIMEMultipart):
        """Send SMTP message (blocking, run in executor)."""
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)

    async def send_slack_alert(self, text: str, blocks: Optional[List[dict]] = None) -> bool:
        """Send a Slack alert via webhook."""
        if not self.slack_enabled or not self.slack_webhook_url:
            return False

        try:
            payload = {"text": text}
            if blocks:
                payload["blocks"] = blocks

            async with httpx.AsyncClient() as client:
                response = await client.post(self.slack_webhook_url, json=payload, timeout=10)
                response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
            return False

    async def send_event_alert(self, event_data: dict) -> bool:
        """Send an alert for a high-importance event."""
        success = False

        # Prepare event details
        title = event_data.get('title', 'Unknown Event')
        importance = event_data.get('importance', 0)
        event_type = event_data.get('event_type', 'Unknown')
        summary = event_data.get('summary_en') or event_data.get('summary_zh', '')
        location = f"{event_data.get('location_lat', 'N/A')}, {event_data.get('location_lng', 'N/A')}"

        # Send email
        if self.email_enabled:
            subject = f"[HIGH IMPORTANCE] {title} (Importance: {importance})"
            body = f"""
High importance event detected:

Title: {title}
Type: {event_type}
Importance: {importance}
Location: {location}
Time: {event_data.get('event_time', 'Unknown')}

Summary:
{summary}

Actors: {', '.join(event_data.get('actors', []))}
Equipment: {', '.join(event_data.get('equipment', []))}
            """
            success = await self.send_email_alert(subject, body) or success

        # Send Slack
        if self.slack_enabled:
            text = f"🚨 *High Importance Event Detected*\n*{title}*\nImportance: {importance} | Type: {event_type}"
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🚨 High Importance Event: {title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Type:*\n{event_type}"},
                        {"type": "mrkdwn", "text": f"*Importance:*\n{importance}/5"},
                        {"type": "mrkdwn", "text": f"*Location:*\n{location}"},
                        {"type": "mrkdwn", "text": f"*Time:*\n{event_data.get('event_time', 'Unknown')}"}
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Summary:*\n{summary[:500]}"
                    }
                }
            ]
            success = await self.send_slack_alert(text, blocks) or success

        return success

    async def send_quota_alert(self, source: str, usage_percent: float) -> bool:
        """Send an alert when quota threshold is reached."""
        subject = f"[QUOTA ALERT] {source} quota at {usage_percent:.1f}%"
        body = f"""
Source {source} has reached {usage_percent:.1f}% of its daily quota.

Consider adjusting poll settings or investigating potential issues.
        """
        text = f"⚠️ *Quota Alert*: {source} at {usage_percent:.1f}% of daily quota"

        success = await self.send_email_alert(subject, body) or False
        success = await self.send_slack_alert(text) or success

        return success


# Global alert service instance
alert_service = AlertService()
