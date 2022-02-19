# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Workflow manager module for the Storm platform."""

import storm_workflow.config as config

from storm_workflow.workflow.resources.config import ResearchWorkflowResourceConfig
from storm_workflow.workflow.resources.resource import ResearchWorkflowResource
from storm_workflow.workflow.services.config import ResearchWorkflowServiceConfig
from storm_workflow.workflow.services.service import ResearchWorkflowService


class StormWorkflow(object):
    """storm-workflow extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        self.init_services(app)
        self.init_resources(app)

        app.extensions["storm-workflow"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("STORM_WORKFLOW_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize research workflow services."""
        self.research_workflow_service = ResearchWorkflowService(
            ResearchWorkflowServiceConfig
        )

    def init_resources(self, app):
        """Initialize research workflow resources."""
        self.research_workflow_resource = ResearchWorkflowResource(
            ResearchWorkflowResourceConfig, self.research_workflow_service
        )
