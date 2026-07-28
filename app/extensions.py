from gatevault import TokenManager
from .config import settings

tm = TokenManager(settings.secret_key, settings.access_token_expiry, settings.refresh_token_expiry)

