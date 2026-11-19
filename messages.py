"""Contact form: validate, then send the message straight to my Gmail (no database)."""
import os
import re
import smtplib
import time
from email.message import EmailMessage

EMAIL_OK = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
MAX_NAME, MAX_EMAIL, MAX_SUBJECT, MAX_BODY, MIN_BODY = 80, 120, 100, 2000, 5

WINDOW_SECONDS, WINDOW_LIMIT = 600, 5       # max 5 messages per IP every 10 minutes
_recent = {}

def rate_limited(ip):
    now = time.time()
    hits = [t for t in _recent.get(ip, []) if now - t < WINDOW_SECONDS]
    if len(hits) >= WINDOW_LIMIT:
        _recent[ip] = hits
        return True
    hits.append(now)
    _recent[ip] = hits
    return False

def validate(form):
    name = ' '.join(form.get('name', '').split())
    email = form.get('email', '').strip()
    subject = ' '.join(form.get('subject', '').split())      # optional
    body = form.get('message', '').strip()

    if not name:
        return None, "Please tell me your name."
    if len(name) > MAX_NAME:
        return None, f"Your name is too long (max {MAX_NAME} characters)."
    if not EMAIL_OK.match(email) or len(email) > MAX_EMAIL:
        return None, "Please enter a valid email so I can reply."
    if len(subject) > MAX_SUBJECT:
        return None, f"The subject is too long (max {MAX_SUBJECT} characters)."
    if len(body) < MIN_BODY:
        return None, "Your message is a bit short. Write a few more words."
    if len(body) > MAX_BODY:
        return None, f"Your message is too long (max {MAX_BODY} characters)."
    return {'name': name, 'email': email, 'subject': subject, 'body': body}, None


def _setting(name):
    value = os.environ.get(name)
    if value:
        return value.strip()
    try:
        import gmail_settings
        return str(getattr(gmail_settings, name, '') or '').strip()
    except ImportError:
        return ''


def gmail_address():
    return _setting('GMAIL_ADDRESS')

last_error = ''

def _deliver(msg, address, password):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15) as smtp:
            smtp.login(address, password)
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise
    except (OSError, smtplib.SMTPException):
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(address, password)
            smtp.send_message(msg)


def send(clean):
    global last_error
    last_error = ''
    address = gmail_address()
    password = _setting('GMAIL_APP_PASSWORD').replace(' ', '')
    if not address or not password:
        last_error = "Missing GMAIL_ADDRESS or GMAIL_APP_PASSWORD in environment or gmail_settings.py"
        print("[contact]", last_error)
        return "Sorry, the message form isn't set up yet. Please use one of the other contacts below."
    try:
        msg = EmailMessage()
        msg['Subject'] = clean['subject'] or f"Portfolio message from {clean['name']}"
        msg['From'] = address
        msg['To'] = address
        msg['Reply-To'] = clean['email']
        msg.set_content(f"From: {clean['name']} <{clean['email']}>\n\n{clean['body']}")
        _deliver(msg, address, password)
        return None
    except smtplib.SMTPAuthenticationError:
        last_error = "Gmail rejected the login. Use a 16-character App Password, not your regular account password."
    except Exception as error:         
        last_error = f"{type(error).__name__}: {error}"
    print("[contact]", last_error)
    return "Sorry, your message could not be sent. Please try again later or use one of the other contacts below."