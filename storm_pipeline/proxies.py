# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from flask import current_app
from werkzeug.local import LocalProxy


current_workflow_extension = LocalProxy(
    lambda: current_app.extensions["storm-workflow"]
)
"""Helper proxy to get the current Storm Workflow extension."""


current_workflow_service = LocalProxy(
    lambda: current_app.extensions["storm-workflow"].research_workflow_service
)
"""Helper proxy to get the current Storm Workflow service extension."""
