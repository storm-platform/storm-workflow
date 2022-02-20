# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Workflow manager module for the Storm platform."""

from .ext import StormWorkflow
from .version import __version__

__all__ = ("__version__", "StormWorkflow")
