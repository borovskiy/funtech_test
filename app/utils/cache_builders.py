import enum
import hashlib
from typing import Any, Callable, Dict, Optional, Tuple

from starlette.requests import Request
from starlette.responses import Response



def order_key_builder(
        func: Callable[..., Any],
        namespace: str = "",
        *,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
) -> str:
    kwargs_new = {}
    for k, v in kwargs.items():
        if isinstance(v, (int, float, str, bool, type(None))):
            kwargs_new.update({k:v})
        if k == "order_id":
            namespace = get_key_order_cache(v)
    return namespace

def get_key_order_cache(order_id: str) -> str:
    return f"fastapi-cache:order_id_{order_id}"

class CacheNamespace(enum.Enum):
    ONE_ORDER = "one_order"
    LIST_ORDER = "list_order"
