from typing import Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import jwt


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        bearer_payload = self.get_bearer_token(request.headers.get('Authorization'))
        if bearer_payload is None:
            request.state.user_id = None
        else:
            request.state.user_id = bearer_payload.get('id')
        response = await call_next(request)
        return response

    @staticmethod
    def get_bearer_token(bearer_header: str) -> Union[None, dict]:
        if bearer_header is None or not bearer_header.startswith('Bearer'):
            return None
        try:
            token = ' '.join(bearer_header.split(' ')[1:])
            return jwt.decode(token, "SECRET_POG", algorithms=['HS256'])
        except IndexError:
            return None
        except jwt.exceptions.InvalidSignatureError:
            return None

    @staticmethod
    def generate_bearer_token(bearer_payload: dict) -> str:
        return jwt.encode(bearer_payload, "SECRET_POG", algorithm='HS256')
