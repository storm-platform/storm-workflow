# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def create_research_workflow_blueprint_api(app):
    """Create Workflow API Blueprint."""
    ext = app.extensions["storm-workflow"]

    return ext.research_workflow_resource.as_blueprint()


__all__ = "create_research_workflow_blueprint_api"
