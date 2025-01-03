from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseModel(_BaseModel):
    """Base Pydantic model."""

    model_config = ConfigDict()