from typing import Any, Dict, Union

import pydantic


def is_valid_orcid_id(orcid_id: str):
    """adapted from stdnum.iso7064.mod_11_2.checksum()"""
    check = 0
    for n in orcid_id:
        check = (2 * check + int(10 if n == "X" else n)) % 11
    return check == 1


def ensure_raw(value: Union[pydantic.BaseModel, Any]) -> Union[Dict[str, Any], Any]:
    if isinstance(value, pydantic.BaseModel):
        return value.model_dump(exclude_unset=True, exclude_defaults=False, exclude_none=False)
    else:
        return value
