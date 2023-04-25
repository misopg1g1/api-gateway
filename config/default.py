import os


class AppConfigValues:
    ENCRYPTION_KEY_SECRET = os.getenv("ENCRYPTION_KEY_SECRET", "ASuJ-vtjlvAuUdFDTdeMOHoCTjlS_dipLtp6_7rQ_kw=")
    AUTH_URL = os.getenv("AUTH_URL", "http://localhost:3001")
    PRODUCTS_URL = os.getenv("PRODUCTS_URL", "http://localhost:3002")
    INVENTORY_URL = os.getenv("INVENTORY_URL", "http://localhost:3001")

