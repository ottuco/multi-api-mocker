from dataclasses import dataclass, asdict
from typing import Any, Optional
from typing import List, Dict


@dataclass
class MockConfiguration:
    url: str
    method: str
    responses: List[Dict[str, Any]]


@dataclass
class ResponseKwargs:
    text: Optional[str] = None
    status_code: Optional[int] = None
    json: Optional[Any] = None
    exc: Optional[Exception] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ResponseKwargs instance into a
        dictionary, filtering out None values.
        """
        return {k: v for k, v in asdict(self).items() if v is not None}
