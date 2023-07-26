import datetime
import json
from typing import Optional, Sequence
from unittest import TestCase

from pathlib import Path
import pooch  # type: ignore
from pydantic import TypeAdapter
from ruamel.yaml import YAML

from bioimageio.spec import ResourceDescription
from bioimageio.spec.shared.validation import ValidationContext

yaml = YAML(typ="safe")

CURRENT_DATE = str(datetime.datetime.now().date())
BASE_URL = "https://bioimage-io.github.io/collection-bioimage-io/"


class TestBioimageioCollection(TestCase):
    DEBUG_SUBTEST_INDEX: Optional[int] = None
    resources: Sequence[str]
    collection: pooch.Pooch
    adapter: TypeAdapter[ResourceDescription]

    def setUp(self) -> None:
        self.adapter = TypeAdapter(ResourceDescription)
        with open(pooch.retrieve(BASE_URL + "collection.json", None), encoding="utf-8") as f:  # type: ignore
            collection_data = json.load(f)["collection"]

        collection_registry = {entry["rdf_source"].replace(BASE_URL, ""): None for entry in collection_data}
        self.resources = list(collection_registry)
        self.collection = pooch.create(  # type: ignore
            path=pooch.os_cache("bioimageio-collection") / CURRENT_DATE,  # type: ignore
            base_url="https://bioimage-io.github.io/collection-bioimage-io/",
            registry=collection_registry,
        )
        return super().setUp()

    def test_all(self):
        for idx, rdf in enumerate(self.resources):
            if self.DEBUG_SUBTEST_INDEX is not None and self.DEBUG_SUBTEST_INDEX != idx:
                continue
            with self.subTest(rdf=rdf):
                with Path(self.collection.fetch(rdf)).open(encoding="utf-8") as f:  #  type: ignore
                    data = yaml.load(f)

                with ValidationContext(root=Path(__file__).parent):
                    self.adapter.validate_python(data)
