import os


class AppConfigValues:
    ENCRYPTION_KEY_SECRET = os.getenv("ENCRYPTION_KEY_SECRET", "ASuJ-vtjlvAuUdFDTdeMOHoCTjlS_dipLtp6_7rQ_kw=")
    AUTH_URL = os.getenv("AUTH_URL", "http://localhost:3001")
    PRODUCTS_URL = os.getenv("PRODUCTS_URL", "http://localhost:3004")
    CUSTOMERS_URL = os.getenv("CUSTOMERS_URL", "http://localhost:3002")
    SELLERS_URL = os.getenv("SELLERS_URL", "http://localhost:3005")
    INVENTORY_URL = os.getenv("INVENTORY_URL", "http://localhost:3003")
    ORDER_URL = os.getenv("ORDER_URL", "http://localhost:3006")
