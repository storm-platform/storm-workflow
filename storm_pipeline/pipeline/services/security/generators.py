# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_project.project.services.security.generators import (
    ProjectRecordAgent,
)

class PipelineRecordCollaborator(ProjectRecordAgent):
    """Generator to define if the user is a collaborator of the
    project associated to the defined pipeline."""

    def _select_record_agent(self, record, **kwargs):
        # note: Is assumed that the attribute `access` is a `RecordAccessField`.
        return record.access.owners, record.access.contributors
