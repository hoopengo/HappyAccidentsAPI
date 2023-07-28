from aiohttp import ClientResponse, web_exceptions

__all__ = [
    "TokenRequired",
    "TokenValidationError",
]


def handle_error(response: ClientResponse, data: dict):
    base = {
        "headers": response.headers,
        "reason": str(data),
        "text": str(data.get("detail")),
    }
    if response.status == 401:
        raise web_exceptions.HTTPUnauthorized(**base)
    elif response.status == 429:
        raise web_exceptions.HTTPTooManyRequests(**base)
    elif response.status == 500:
        raise web_exceptions.HTTPInternalServerError(**base)
    else:
        base_error = web_exceptions.HTTPClientError
        base_error.status_code = response.status
        raise base_error(**base)


class TokenRequired(Exception):
    pass


class TokenValidationError(Exception):
    pass
