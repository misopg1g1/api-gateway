import os


class AppConfigValues:
    ENCRYPTION_KEY_SECRET = os.getenv("ENCRYPTION_KEY_SECRET", "ASuJ-vtjlvAuUdFDTdeMOHoCTjlS_dipLtp6_7rQ_kw=")
    AUTH_URL = os.getenv("AUTH_URL", "http://localhost:3001")
    PRODUCTS_URL = os.getenv("PRODUCTS_URL", "http://localhost:3004")
    CUSTOMERS_URL = os.getenv("CUSTOMERS_URL", "http://localhost:3002")
    SELLERS_URL = os.getenv("SELLERS_URL", "http://localhost:3005")
    INVENTORY_URL = os.getenv("INVENTORY_URL", "http://localhost:3003")
    ORDERS_URL = os.getenv("ORDERS_URL", "http://localhost:3006")
    RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_PORT = os.getenv("RABBIT_PORT", "5672")
    RABBIT_USER = os.getenv("RABBIT_USER", "user")
    RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD", "secret")
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "secret")
