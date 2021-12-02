# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services.records.components import MetadataComponent


from ..records.api import ResearchPipeline
from ..schema import ResearchPipelineSchema

from .permissions import ResearchPipelineRecordPermissionPolicy
from .components import (
    PIDComponent,
    ResearchPipelineAccessComponent,
    GraphComponent,
    CompendiaComponent,
)


class ResearchPipelineServiceConfig(RecordServiceConfig):
    """ResearchPipeline service configuration."""

    #
    # Common configurations
    #
    permission_policy_cls = ResearchPipelineRecordPermissionPolicy

    #
    # Record configuration
    #
    record_cls = ResearchPipeline

    schema = ResearchPipelineSchema

    #
    # Components configuration
    #
    components = [
        MetadataComponent,
        GraphComponent,
        CompendiaComponent,
        PIDComponent,
        ResearchPipelineAccessComponent,
    ]


__all__ = "ResearchPipelineServiceConfig"
