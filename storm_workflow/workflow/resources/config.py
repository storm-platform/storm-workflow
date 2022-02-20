# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import marshmallow as ma

from invenio_records_resources.resources import RecordResourceConfig


class ResearchWorkflowResourceConfig(RecordResourceConfig):
    """Research Workflow resource configuration."""

    blueprint_name = "storm_research_workflows"
    url_prefix = "/projects/<project_id>/workflows"

    # Request/Response configuration.
    request_view_args = {
        "user_type": ma.fields.String(
            validate=ma.fields.validate.OneOf(choices=["contributor"])
        ),
        "user_id": ma.fields.Int(),
        "pid_value": ma.fields.Str(),
        "compendium_id": ma.fields.Str(),
    }

    routes = {
        # Base operations
        "list-item": "",
        "create-item": "",
        "get-item": "/<pid_value>",
        "update-item": "/<pid_value>",
        "delete-item": "/<pid_value>",
        # Graph manipulation operations
        "add-graph-item": "/<pid_value>/actions/add/compendium/<compendium_id>",
        "delete-graph-item": "/<pid_value>/actions/delete/compendium/<compendium_id>",
        # Status control
        "finish-item": "/<pid_value>/actions/finish",
        # Access control
        "list-item-agent": "/<pid_value>/admin/agents",
        "add-item-agent": "/<pid_value>/admin/actions/add/<user_type>/<user_id>",
        "remove-item-agent": "/<pid_value>/admin/actions/remove/<user_type>/<user_id>",
    }
