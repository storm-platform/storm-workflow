# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import fields, Schema
from marshmallow_utils.fields import SanitizedUnicode

from storm_commons.schemas.validators import marshmallow_not_blank_field
from invenio_records_resources.services.records.schema import BaseRecordSchema


#
# Research Pipeline general metadata
#
class ResearchPipelineMetadataSchema(Schema):
    """Research project metadata field schema."""

    # General descriptions
    version = SanitizedUnicode()
    title = SanitizedUnicode(
        required=True, validate=marshmallow_not_blank_field(max=250)
    )
    description = SanitizedUnicode(validate=marshmallow_not_blank_field(max=2000))


#
# Research Pipeline graph metadata
#
class NodeFileSchema(Schema):
    """Node File schema."""

    key = SanitizedUnicode(required=True)
    type = SanitizedUnicode(required=True, validate=marshmallow_not_blank_field(max=6))
    checksum = SanitizedUnicode(
        required=True, validate=marshmallow_not_blank_field(max=250)
    )


class NodeMetadataSchema(Schema):
    """Node metadata schema."""

    files = fields.List(cls_or_instance=fields.Nested(NodeFileSchema()), required=True)


class NodeSchema(Schema):
    """Node schema."""

    metadata = fields.Nested(NodeMetadataSchema, required=True)


class EdgeRelatedFilesSchema(Schema):
    """Edge metadata related files schema."""

    key = SanitizedUnicode(required=True)


class EdgeMetadataSchema(Schema):
    """Edge metadata."""

    related_files = fields.List(
        cls_or_instance=fields.Nested(EdgeRelatedFilesSchema()), required=True
    )


class EdgeSchema(Schema):
    """Edge schema."""

    source = SanitizedUnicode(required=True)
    target = SanitizedUnicode(required=True)

    metadata = fields.Nested(EdgeMetadataSchema, required=True)


class GraphSchema(Schema):
    """Graph document schema."""

    directed = fields.Bool(required=True)
    type = SanitizedUnicode(required=True)

    nodes = fields.Dict(
        keys=fields.Str(), values=fields.Nested(NodeSchema), required=True
    )

    edges = fields.List(cls_or_instance=fields.Nested(EdgeSchema()), required=True)


class ResearchPipelineSchema(BaseRecordSchema):
    """Research pipeline schema."""

    id = SanitizedUnicode(validate=marshmallow_not_blank_field(max=20), required=True)
    graph = fields.Nested(GraphSchema)
    metadata = fields.Nested(ResearchPipelineMetadataSchema, required=True)
