# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_permissions.generators import SystemProcess
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from storm_project.project.services.security.generators.context import (
    ProjectRecordColaborator,
    UserInProject,
)


class ResearchPipelineRecordPermissionPolicy(RecordPermissionPolicy):
    """Access control configuration for research pipelines."""

    #
    # High level permissions
    #

    # Content creators and managers
    can_manage = [ProjectRecordColaborator(), SystemProcess()]

    # General users
    can_use = can_manage + [UserInProject()]

    #
    # Low level permissions
    #
    can_create = can_use

    can_read = can_use

    can_update = can_manage

    can_delete = can_manage

    can_search = can_use

    can_manage_compendium = can_manage
