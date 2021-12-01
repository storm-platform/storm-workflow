# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_records.systemfields import ConstantField, DictField

from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField, PIDField

from .models import ResearchPipelineMetadata
from .providers import ResearchPipelineIdProvider


class ResearchPipeline(Record):
    """ResearchPipeline API."""

    model_cls = ResearchPipelineMetadata

    # user will need to define the id.
    pid = PIDField("id", provider=ResearchPipelineIdProvider, create=False)
    schema = ConstantField("$schema", "local://pipeline/pipeline-v1.0.0.json")

    # record document fields
    is_finished = DictField("is_finished")
    graph = DictField(clear_none=True, create_if_missing=True)

    index = IndexField("pipeline-pipeline-v1.0.0", search_alias="pipeline")


__all__ = "ResearchPipeline"
