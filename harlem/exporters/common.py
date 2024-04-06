from typing import IO, Optional

from pydantic import BaseModel


def dump_model_to_str(model: BaseModel, indent: Optional[int] = None) -> str:
    return model.model_dump_json(
        indent=indent, exclude_unset=True, exclude_none=True, by_alias=True
    )


def dump_model_to_dict(model: BaseModel) -> dict:
    return model.model_dump(exclude_unset=True, exclude_none=True, by_alias=True)


def save_to_io(model: BaseModel, destination: IO[str], indent: Optional[int]):
    destination.write(dump_model_to_str(model, indent))
