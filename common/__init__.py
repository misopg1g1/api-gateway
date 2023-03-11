import fastapi.security

from .error_handling import add_custom_errors
from .cors_handling import handle_cors
from .response_messages import ResponseMessagesEnum

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="session/login")
token_schema = fastapi.security.HTTPBearer()
