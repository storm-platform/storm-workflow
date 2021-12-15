# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from flask import current_app
from werkzeug.local import LocalProxy


current_pipeline_extension = LocalProxy(
    lambda: current_app.extensions["storm-pipeline"]
)
"""Helper proxy to get the current Storm Pipeline extension."""
