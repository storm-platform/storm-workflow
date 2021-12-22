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
    FinishStatusComponent,
)
from storm_project.project.services.links import (
    ProjectContextLink,
    project_context_pagination_links,
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


def is_not_finished(record, ctx):
    """Check if the pipeline is not finished."""
    return not record.is_finished


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
        FinishStatusComponent,
    ]

    links_item = {
        "self": ProjectContextLink("{+api}/projects/{project_id}/pipelines/{id}")
    }

    links_action = {
        "add-compendium": ProjectContextLink(
            "{+api}/projects/{project_id}/pipelines/{id}/actions/add/compendium",
            when=is_not_finished,
        ),
        "delete-compendium": ProjectContextLink(
            "{+api}/projects/{project_id}/pipelines/{id}/actions/delete/compendium",
            when=is_not_finished,
        ),
        "finish": ProjectContextLink(
            "{+api}/projects/{project_id}/pipelines/{id}/actions/finish",
            when=is_not_finished,
        ),
    }

    links_search = project_context_pagination_links(
        "{+api}/projects/{project_id}/pipelines{?args*}"
    )
