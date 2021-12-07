from marshmallow import RAISE

from bioimageio.spec.rdf.v0_2.schema import RDF
from bioimageio.spec.shared import fields
from bioimageio.spec.shared.schema import SharedBioImageIOSchema, WithUnknown
from . import raw_nodes


class _BioImageIOSchema(SharedBioImageIOSchema):
    raw_nodes = raw_nodes


class CollectionEntry(_BioImageIOSchema, WithUnknown):
    id_ = fields.String(required=True, data_key="id")
    source = fields.URL(required=True)
    links = fields.List(fields.String())


class Collection(_BioImageIOSchema, RDF):
    class Meta:
        unknown = RAISE

    application = fields.List(fields.Union([fields.Nested(CollectionEntry()), fields.Nested(RDF())]))
    collection = fields.List(fields.Union([fields.Nested(CollectionEntry()), fields.Nested(RDF())]))
    model = fields.List(fields.Union([fields.Nested(CollectionEntry()), fields.Nested(RDF())]))
    dataset = fields.List(fields.Union([fields.Nested(CollectionEntry()), fields.Nested(RDF())]))
    notebook = fields.List(fields.Union([fields.Nested(CollectionEntry()), fields.Nested(RDF())]))
