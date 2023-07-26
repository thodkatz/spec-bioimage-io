from __future__ import annotations

from contextvars import ContextVar, Token
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple, Union

import pydantic
from pydantic import DirectoryPath, HttpUrl, PrivateAttr
from pydantic_core.core_schema import ErrorType
from typing_extensions import NotRequired, TypedDict

from bioimageio.spec._internal._warn import WarningLevel, WarningType


class ValidationContext(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        extra="forbid",
        frozen=True,
        validate_default=True,
    )
    root: Union[HttpUrl, DirectoryPath, None] = None
    """url/path serving as base to any relative file paths. Default provided as data field `root`.0"""
    warning_level: WarningLevel = 50
    """raise warnings of severity s as validation errors if s >= `warning_level`"""

    original_format: Tuple[int, int, int] = (99999, 0, 0)
    """original format version of the validation data set dynamically when validating resource descriptions."""

    collection_base_content: Dict[str, Any] = pydantic.Field(default_factory=dict, frozen=False)
    """Collection base content set dynamically during validation of collection resource descriptions."""

    _token: Token[ValidationContext] = PrivateAttr()

    def __enter__(self):
        self._token = validation_context_var.set(self)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):  # type: ignore
        validation_context_var.reset(self._token)


validation_context_var = ContextVar("_validation_context_var", default=ValidationContext())


class ValidationOutcome(TypedDict):
    loc: Tuple[Union[int, str], ...]
    msg: str


class ValidationError(ValidationOutcome):
    type: Union[ErrorType, str]


class ValidationWarning(ValidationOutcome):
    type: WarningType


class ValidationSummary(TypedDict):
    bioimageio_spec_version: str
    error: Union[str, Sequence[ValidationError], None]
    name: str
    source_name: str
    status: Union[Literal["passed", "failed"], str]
    traceback: NotRequired[Sequence[str]]
    warnings: NotRequired[Sequence[ValidationWarning]]


class LegacyValidationSummary(TypedDict):
    bioimageio_spec_version: str
    error: Union[None, str, Dict[str, Any]]
    name: str
    nested_errors: NotRequired[Dict[str, Dict[str, Any]]]
    source_name: str
    status: Union[Literal["passed", "failed"], str]
    traceback: Optional[List[str]]
    warnings: Dict[str, Any]
