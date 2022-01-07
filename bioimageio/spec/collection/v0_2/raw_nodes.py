""" raw nodes for the collection RDF spec

raw nodes are the deserialized equivalent to the content of any RDF.
serialization and deserialization are defined in schema:
RDF <--schema--> raw nodes
"""
import distutils.version
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, NewType, Union

from marshmallow import missing
from marshmallow.utils import _Missing

from bioimageio.spec.rdf.v0_2.raw_nodes import Author, Badge, CiteEntry, Maintainer, RDF
from bioimageio.spec.shared.raw_nodes import RawNode, URI

try:
    from typing import Literal, get_args
except ImportError:
    from typing_extensions import Literal, get_args  # type: ignore

FormatVersion = Literal[
    "0.2.0", "0.2.1", "0.2.2"
]  # newest format needs to be last (used to determine latest format version)


RDF_Update = NewType("RDF_Update", Dict[str, Any])


@dataclass
class CollectionEntry(RawNode):
    """ """

    source: URI = missing
    id: str = missing
    rdf_update: RDF_Update = missing

    def __init__(self, source=missing, id=missing, **rdf_update):
        self.source = source
        self.id = id
        self.rdf_update = RDF_Update(rdf_update)
        super().__init__()


@dataclass
class Collection(RDF):
    collection: List[Union[RDF_Update, CollectionEntry]] = missing

    # manual __init__ to allow for unknown kwargs
    def __init__(
        self,
        *,
        # ResourceDescription
        format_version: FormatVersion,
        name: str,
        type: str = missing,
        version: Union[_Missing, distutils.version.StrictVersion] = missing,
        # RDF
        attachments: Union[_Missing, Dict[str, Any]] = missing,
        authors: List[Author],
        badges: Union[_Missing, List[Badge]] = missing,
        cite: List[CiteEntry],
        config: Union[_Missing, dict] = missing,
        covers: Union[_Missing, List[Union[URI, Path]]] = missing,
        description: str,
        documentation: Path,
        git_repo: Union[_Missing, str] = missing,
        license: Union[_Missing, str] = missing,
        links: Union[_Missing, List[str]] = missing,
        maintainers: Union[_Missing, List[Maintainer]] = missing,
        tags: List[str],
        # collection RDF
        collection: List[Union[RDF_Update, CollectionEntry]],
        **unknown,
    ):
        self.collection = collection
        super().__init__(
            attachments=attachments,
            authors=authors,
            badges=badges,
            cite=cite,
            config=config,
            covers=covers,
            description=description,
            documentation=documentation,
            format_version=format_version,
            git_repo=git_repo,
            license=license,
            links=links,
            maintainers=maintainers,
            name=name,
            tags=tags,
            type=type,
            version=version,
        )
        self.unknown = unknown
