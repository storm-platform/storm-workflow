# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.records.api import Record
from storm_commons.records.systemfields.fields.access import RecordAccessField
from invenio_records_resources.records.systemfields import IndexField, PIDField

from invenio_records.systemfields import ConstantField, DictField

from storm_pipeline.pipeline.records.models import ResearchPipelineMetadata
from storm_pipeline.pipeline.records.systemfields.access import PipelineAccess
from storm_pipeline.pipeline.records.providers import ResearchPipelineIdProvider


class ResearchPipeline(Record):
    """Research Pipeline High-level API."""

    pid = PIDField("id", provider=ResearchPipelineIdProvider, create=False)
    schema = ConstantField("$schema", "local://pipeline/pipeline-v1.0.0.json")

    access = RecordAccessField(access_obj_class=PipelineAccess)

    model_cls = ResearchPipelineMetadata
    index = IndexField("pipeline-pipeline-v1.0.0", search_alias="pipeline")

    is_finished = DictField("is_finished")
    graph = DictField(clear_none=True, create_if_missing=True)


__all__ = "ResearchPipeline"
