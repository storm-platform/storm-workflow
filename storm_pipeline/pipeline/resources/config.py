# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import marshmallow as ma

from invenio_records_resources.resources import RecordResourceConfig


class ResearchPipelineResourceConfig(RecordResourceConfig):
    """Research Pipeline resource configuration."""

    blueprint_name = "storm_research_pipelines"
    url_prefix = "/projects/<project_id>/pipelines"

    request_view_args = {"pid_value": ma.fields.Str(), "compendium_id": ma.fields.Str()}

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
    }
