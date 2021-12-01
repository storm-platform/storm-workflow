# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def create_research_pipeline_blueprint_api(app):
    """Create Pipeline API Blueprint."""
    ext = app.extensions["storm-pipeline"]

    return ext.research_pipeline_resource.as_blueprint()


__all__ = "create_research_pipeline_blueprint_api"
