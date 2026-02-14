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
            namespace = f"{namespace}{k}_{v}"
    cache_key = hashlib.md5(
        f"{func.__module__}:{func.__name__}:{args}:{kwargs_new}".encode()
    ).hexdigest()
    result_cache = f"{namespace}:{cache_key}"
    return result_cache


class CacheNamespace(enum.Enum):
    ONE_ORDER = "one_order"
    LIST_ORDER = "list_order"
