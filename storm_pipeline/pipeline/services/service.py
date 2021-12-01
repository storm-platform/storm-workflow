# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records import RecordService


class ResearchPipelineService(RecordService):
    """Research pipeline service."""


__all__ = "ResearchPipelineService"
