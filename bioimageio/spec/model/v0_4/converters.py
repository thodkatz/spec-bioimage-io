import copy
from typing import Any, Dict

from marshmallow import missing

from bioimageio.spec.exceptions import UnconvertibleError


def convert_model_from_v0_3(data: Dict[str, Any]) -> Dict[str, Any]:
    from bioimageio.spec.model import v0_3

    data = copy.deepcopy(data)

    data = v0_3.converters.maybe_convert(data)
    v0_3.schema.Model().validate(data)

    data.pop("language", None)
    data.pop("framework", None)

    architecture = data.pop("source", missing)
    architecture_sha256 = data.pop("sha256", missing)
    kwargs = data.pop("kwargs", missing)
    pytorch_state_dict_weights_entry = data.get("weights", {}).get("pytorch_state_dict")
    if pytorch_state_dict_weights_entry is not None:
        if architecture is not missing:
            pytorch_state_dict_weights_entry["architecture"] = architecture

        if architecture_sha256 is missing:
            raise UnconvertibleError("Missing 'sha256' which is now required.")

        pytorch_state_dict_weights_entry["architecture_sha256"] = architecture_sha256

        if architecture_sha256 is not missing:
            pytorch_state_dict_weights_entry["kwargs"] = kwargs

    torchscript_weights_entry = data.get("weights", {}).pop("pytorch_script", None)
    if torchscript_weights_entry is not None:
        data["weights"]["torchscript"] = torchscript_weights_entry

    data["format_version"] = "0.4.0"

    return data


def maybe_convert(data: Dict[str, Any]) -> Dict[str, Any]:
    """auto converts model 'data' to newest format"""
    major, minor, patch = map(int, data.get("format_version", "0.3.0").split("."))
    if major == 0 and minor < 4:
        data = convert_model_from_v0_3(data)

    if data["format_version"] == "0.4.0":
        data["format_version"] = "0.4.1"

    # remove 'future' from config if no other than the used future entries exist
    config = data.get("config", {})
    if config.get("future") == {}:
        del config["future"]

    # remove 'config' if now empty
    if data.get("config") == {}:
        del data["config"]

    return data
