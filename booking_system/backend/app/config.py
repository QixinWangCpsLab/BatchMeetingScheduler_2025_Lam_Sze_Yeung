import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://appuser:apppass@localhost:3307/reservation")
APP_SECRET = os.getenv("APP_SECRET", "dev-secret")
BASE_URL = os.getenv("BASE_URL", "http://localhost")

SMTP_ENABLED = os.getenv("SMTP_ENABLED", "false").lower() == "true"
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", "15"))
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")
