# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
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

from storm_workflow.workflow.records.api import ResearchWorkflow
from storm_workflow.workflow.schema import ResearchWorkflowSchema
from storm_workflow.workflow.services.components import (
    ResearchWorkflowGraphComponent,
    ResearchWorkflowCompendiaComponent,
)
from storm_workflow.workflow.services.security.permissions import (
    ResearchWorkflowRecordPermissionPolicy,
)


def is_not_finished(record, ctx):
    """Check if the workflow is not finished."""
    return not record.is_finished


class ResearchWorkflowServiceConfig(RecordServiceConfig):
    """ResearchWorkflow service configuration."""

    #
    # Common configurations
    #
    permission_policy_cls = ResearchWorkflowRecordPermissionPolicy

    #
    # Record configuration
    #
    record_cls = ResearchWorkflow

    schema = ResearchWorkflowSchema

    #
    # Components configuration
    #
    components = [
        RecordMetadataComponent,
        ResearchWorkflowGraphComponent,
        ResearchWorkflowCompendiaComponent,
        CustomPIDGeneratorComponent,
        RecordAccessDefinitionComponent,
        FinishStatusComponent,
    ]

    links_item = {
        "self": ProjectContextLink("{+api}/projects/{project_id}/workflows/{id}")
    }

    links_action = {
        "add-compendium": ProjectContextLink(
            "{+api}/projects/{project_id}/workflows/{id}/actions/add/compendium",
            when=is_not_finished,
        ),
        "delete-compendium": ProjectContextLink(
            "{+api}/projects/{project_id}/workflows/{id}/actions/delete/compendium",
            when=is_not_finished,
        ),
        "finish": ProjectContextLink(
            "{+api}/projects/{project_id}/workflows/{id}/actions/finish",
            when=is_not_finished,
        ),
    }

    links_search = project_context_pagination_links(
        "{+api}/projects/{project_id}/workflows{?args*}"
    )
