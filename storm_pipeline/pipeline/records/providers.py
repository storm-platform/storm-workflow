# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.records.providers import PIDRegisteredProvider


class ResearchPipelinePIDProvider(PIDRegisteredProvider):
    """Research pipeline PID provider."""

    pid_type = "pipeid"


__all__ = "ResearchPipelinePIDProvider"
