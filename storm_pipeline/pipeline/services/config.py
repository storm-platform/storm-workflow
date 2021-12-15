# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services import RecordServiceConfig

from storm_commons.services.components import (
    CustomPIDGeneratorComponent,
    RecordMetadataComponent,
    RecordAccessDefinitionComponent,
)

from storm_pipeline.pipeline.records.api import ResearchPipeline
from storm_pipeline.pipeline.schema import ResearchPipelineSchema

from storm_pipeline.pipeline.services.components import (
    ResearchPipelineGraphComponent,
    ResearchPipelineCompendiaComponent,
)

from storm_pipeline.pipeline.services.security.permissions import (
    ResearchPipelineRecordPermissionPolicy,
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
        RecordMetadataComponent,
        ResearchPipelineGraphComponent,
        ResearchPipelineCompendiaComponent,
        CustomPIDGeneratorComponent,
        RecordAccessDefinitionComponent,
    ]


__all__ = "ResearchPipelineServiceConfig"
