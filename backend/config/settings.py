import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    """Base configuration for all environments"""
    
    # ===== FLASK & SECURITY =====
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    DEBUG = False
    TESTING = False
    
    # ===== DATABASE =====
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///travel_agent.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_ECHO = os.getenv("DB_ECHO", "False").lower() == "true"
    DB_POOL_SIZE = 10
    DB_POOL_RECYCLE = 3600
    
    # ===== JWT & AUTHENTICATION =====
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    JWT_ALGORITHM = "HS256"
    
    # ===== CORS =====
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    
    # ===== FRONTEND =====
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # ===== AMADEUS FLIGHT API =====
    AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
    AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
    AMADEUS_API_BASE_URL = os.getenv("AMADEUS_API_BASE_URL", "https://test.api.amadeus.com")
    AMADEUS_TIMEOUT = int(os.getenv("AMADEUS_TIMEOUT", "10"))
    
    # ===== GOOGLE APIs =====
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    GOOGLE_OAUTH_REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:5000/auth/gmail/callback")
    GOOGLE_TRANSLATE_ENABLED = os.getenv("ENABLE_MULTILINGUAL", "False").lower() == "true"
    
    # ===== GMAIL CONFIGURATION =====
    GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")
    GMAIL_TOKEN_PICKLE_FILE = os.getenv("GMAIL_TOKEN_PICKLE_FILE", "token.pickle")
    GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
    GMAIL_SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.readonly'
    ]
    
    # ===== OPENAI CONFIGURATION =====
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_INTENT_DETECTION_ENABLED = os.getenv("OPENAI_INTENT_DETECTION_ENABLED", "False").lower() == "true"
    OPENAI_TIMEOUT = 30
    
    # ===== TRANSPORT APIs =====
    SKYSCANNER_API_KEY = os.getenv("SKYSCANNER_API_KEY")
    BOOKING_COM_API_KEY = os.getenv("BOOKING_COM_API_KEY")
    TRAINLINE_API_KEY = os.getenv("TRAINLINE_API_KEY")
    ROME2RIO_API_KEY = os.getenv("ROME2RIO_API_KEY")
    
    # ===== VISA & DOCUMENT VERIFICATION =====
    SHERPA_VISA_API_KEY = os.getenv("SHERPA_VISA_API_KEY")
    DOCUMENT_VERIFICATION_API_KEY = os.getenv("DOCUMENT_VERIFICATION_API_KEY")
    
    # ===== PAYMENT GATEWAYS =====
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
    PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
    PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")
    
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
    
    # ===== CURRENCY & EXCHANGE RATE =====
    EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
    FIXER_API_KEY = os.getenv("FIXER_API_KEY")
    SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "THB"]
    BASE_CURRENCY = "USD"
    
    # ===== LOGGING & MONITORING =====
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/travel_agent.log")
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    
    # ===== EMAIL NOTIFICATIONS =====
    EMAIL_SERVICE = os.getenv("EMAIL_SERVICE", "smtp")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@travel-agent.com")
    
    # ===== WEATHER API =====
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_SERVICE = os.getenv("WEATHER_SERVICE", "openweathermap")
    
    # ===== LOCAL SEARCH & RECOMMENDATIONS =====
    FOURSQUARE_CLIENT_ID = os.getenv("FOURSQUARE_CLIENT_ID")
    FOURSQUARE_CLIENT_SECRET = os.getenv("FOURSQUARE_CLIENT_SECRET")
    YELP_API_KEY = os.getenv("YELP_API_KEY")
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    
    # ===== MULTILINGUAL SUPPORT =====
    ENABLE_MULTILINGUAL = os.getenv("ENABLE_MULTILINGUAL", "False").lower() == "true"
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
    SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "zh", "ja", "hi", "pt"]
    
    # ===== CACHING =====
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "False").lower() == "true"
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # ===== FILE UPLOAD =====
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/")
    ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "docx"}
    
    # ===== RATE LIMITING =====
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS_PER_HOUR = int(os.getenv("RATE_LIMIT_REQUESTS_PER_HOUR", "1000"))
    
    # ===== API CONFIGURATION =====
    API_TIMEOUT_SECONDS = int(os.getenv("API_TIMEOUT_SECONDS", "30"))
    MAX_RETRIES = 3
    RETRY_BACKOFF_FACTOR = 0.5
    
    # ===== DEPLOYMENT =====
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    
    # ===== PAGINATION =====
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///travel_agent.db")
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000"]


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    CACHE_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Ensure PostgreSQL is used in production
    if not os.getenv("DATABASE_URL"):
        raise ValueError("DATABASE_URL environment variable must be set in production")
    if "sqlite" in SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLite cannot be used in production. Use PostgreSQL.")


# Environment-specific configuration selection
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
