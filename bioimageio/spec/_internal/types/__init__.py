from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Literal, NewType, Sequence, Tuple, TypeVar, Union

import annotated_types
from pydantic import StringConstraints
from typing_extensions import Annotated

from bioimageio.spec._internal.constants import DOI_REGEX, SI_UNIT_REGEX
from bioimageio.spec._internal.types._generated_spdx_license_type import DeprecatedLicenseId as DeprecatedLicenseId
from bioimageio.spec._internal.types._generated_spdx_license_type import LicenseId as LicenseId
from bioimageio.spec._internal.types._relative_path import FileSource as FileSource
from bioimageio.spec._internal.types._relative_path import RelativeFilePath as RelativeFilePath
from bioimageio.spec._internal.types._version import Version as Version
from bioimageio.spec._internal.types.field_validation import (
    AfterValidator,
    BeforeValidator,
    RestrictCharacters,
    capitalize_first_letter,
    validate_datetime,
    validate_identifier,
    validate_is_not_keyword,
    validate_orcid_id,
    validate_unique_entries,
)
from bioimageio.spec._internal.validation_context import ValidationContext as ValidationContext

T = TypeVar("T")
S = TypeVar("S", bound=Sequence[Any])

# types to describe RDF as pydantic models
NonEmpty = Annotated[S, annotated_types.MinLen(1)]

AxesStr = Annotated[str, RestrictCharacters("bitczyx"), AfterValidator(validate_unique_entries)]
AxesInCZYX = Annotated[str, RestrictCharacters("czyx"), AfterValidator(validate_unique_entries)]
CapitalStr = Annotated[NonEmpty[str], AfterValidator(capitalize_first_letter)]
Datetime = Annotated[datetime, BeforeValidator(validate_datetime)]
"""Timestamp in [ISO 8601](#https://en.wikipedia.org/wiki/ISO_8601) format
with a few restrictions listed [here](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat)."""
Identifier = Annotated[
    NonEmpty[str],
    AfterValidator(validate_identifier),
    AfterValidator(validate_is_not_keyword),
]
LowerCaseIdentifier = Annotated[Identifier, annotated_types.LowerCase]
ResourceId = NewType(
    "ResourceId",
    Annotated[
        NonEmpty[str],
        annotated_types.LowerCase,
        annotated_types.Predicate(lambda s: "\\" not in s and s[0] != "/" and s[-1] != "/"),
    ],
)
DatasetId = NewType("DatasetId", ResourceId)
FileName = str
OrcidId = Annotated[str, AfterValidator(validate_orcid_id)]
Sha256 = Annotated[str, annotated_types.Len(64, 64)]
SiUnit = Annotated[
    str,
    StringConstraints(min_length=1, pattern=SI_UNIT_REGEX),
    BeforeValidator(lambda s: s.replace("×", "·").replace("*", "·").replace(" ", "·") if isinstance(s, str) else s),
]
Unit = Union[Literal["px", "arbitrary intensity"], SiUnit]
UniqueTuple = Annotated[Tuple[T], AfterValidator(validate_unique_entries)]

FormatVersionPlaceholder = Literal["latest", "discover"]


# types as loaded from YAML 1.2 (with ruamel.yaml)
YamlLeafValue = Union[bool, date, datetime, float, int, str, None]
YamlArray = List["YamlValue"]  # YAML Array is cast to list, but...
YamlKey = Union[  # ... YAML Arrays are cast to tuples if used as key in mappings
    YamlLeafValue, Tuple[YamlLeafValue, ...]  # (nesting is not allowed though)
]
YamlMapping = Dict[YamlKey, "YamlValue"]  # YAML Mappings are cast to dict
YamlValue = Union[YamlLeafValue, YamlArray, YamlMapping]
RdfContent = Dict[str, YamlValue]
Doi = Annotated[str, StringConstraints(pattern=DOI_REGEX)]
