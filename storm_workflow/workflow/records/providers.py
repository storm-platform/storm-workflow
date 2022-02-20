# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.records.providers import PIDRegisteredProvider


class ResearchWorkflowPIDProvider(PIDRegisteredProvider):
    """Research workflow PID provider."""

    pid_type = "wfid"


__all__ = "ResearchWorkflowPIDProvider"
