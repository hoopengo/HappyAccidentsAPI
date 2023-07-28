from functools import lru_cache

from .errors import TokenValidationError

__all__ = []


@lru_cache()
def validate_token(token: str) -> bool:
    """
    Validate Telegram token
    """
    if not isinstance(token, str):
        raise TokenValidationError(
            f"Token is invalid! It must be 'str' type instead of {type(token)} type."
        )

    if any(x.isspace() for x in token):
        message = "Token is invalid! It can't contains spaces."
        raise TokenValidationError(message)

    return True
