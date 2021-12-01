# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pipeline manager module for the Storm platform."""

from . import config

from .pipeline.resources.config import ResearchPipelineResourceConfig
from .pipeline.resources.resource import ResearchPipelineResource
from .pipeline.services.config import ResearchPipelineServiceConfig
from .pipeline.services.service import ResearchPipelineService


class StormPipeline(object):
    """storm-pipeline extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)

        app.extensions["storm-pipeline"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("STORM_PIPELINE_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize research pipeline services."""
        self.research_pipeline_service = ResearchPipelineService(
            ResearchPipelineServiceConfig
        )

    def init_resources(self, app):
        """Initialize research pipeline resources."""
        self.research_pipeline_resource = ResearchPipelineResource(
            ResearchPipelineResourceConfig, self.research_pipeline_service
        )
