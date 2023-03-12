import os


class AppConfigValues:
    ENCRYPTION_KEY_SECRET = os.getenv("ENCRYPTION_KEY_SECRET", "ASuJ-vtjlvAuUdFDTdeMOHoCTjlS_dipLtp6_7rQ_kw=")
    SOME_MICROSERVICE_URL = os.getenv("SOME_MICROSERVICE_URL", "http://localhost:3001")
