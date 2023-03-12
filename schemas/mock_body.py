from .base_body import BaseBody

from pydantic import Field


class MockBody(BaseBody):
    a: int = Field(..., example=3)
