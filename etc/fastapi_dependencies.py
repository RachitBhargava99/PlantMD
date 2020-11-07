from fastapi import Request

from typing import Union


def get_user_id(request: Request) -> Union[None, int]:
    return request.state.user_id
