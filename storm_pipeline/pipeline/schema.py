# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import fields, Schema, validate
from marshmallow_utils.fields import SanitizedUnicode

from invenio_records_resources.services.records.schema import BaseRecordSchema


def _not_blank(**kwargs):
    """Returns a non-blank validation rule.
    See:
        This code was adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/schema.py#L21
    ToDo:
        - Generalize the function for use in other modules.
        - Move to a general usable library.
    """
    max_ = kwargs.get("max", "")
    return validate.Length(
        error=f"Not empty string and less than {max_} characters allowed.",
        min=1,
        **kwargs,
    )


#
# Research Pipeline general metadata
#
class ResearchPipelineMetadataSchema(Schema):
    """Research project metadata field schema."""

    # General descriptions
    version = SanitizedUnicode()
    title = SanitizedUnicode(required=True, validate=_not_blank(max=250))
    description = SanitizedUnicode(validate=_not_blank(max=2000))


#
# Research Pipeline graph metadata
#
class NodeFileSchema(Schema):
    """Node File schema."""

    # ToDo: Do we need use enum here ?
    key = SanitizedUnicode(required=True)
    type = SanitizedUnicode(required=True, validate=_not_blank(max=6))
    checksum = SanitizedUnicode(required=True, validate=_not_blank(max=250))


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

    id = SanitizedUnicode(validate=_not_blank(max=100), required=True)
    graph = fields.Nested(GraphSchema)
    metadata = fields.Nested(ResearchPipelineMetadataSchema, required=True)
