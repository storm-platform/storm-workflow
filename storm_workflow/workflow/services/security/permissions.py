# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_access import superuser_access
from invenio_records_permissions.generators import SystemProcess
from invenio_records_permissions.policies.records import RecordPermissionPolicy

from storm_project.project.services.security.generators import (
    IfRecordOrProjectFinished,
    ProjectRecordUser,
)

from storm_workflow.workflow.services.security.generators import (
    WorkflowRecordCollaborator,
)


class ResearchWorkflowRecordPermissionPolicy(RecordPermissionPolicy):
    """Access control configuration for research workflows."""

    #
    # High level permissions
    #

    # Content creators and managers
    can_colaborate = [WorkflowRecordCollaborator(), SystemProcess()]

    # General users
    can_use = can_colaborate + [ProjectRecordUser(use_parent_access=False)]

    # Management requirements
    # if finished, only the system admin
    # can manage.
    can_manage = [
        IfRecordOrProjectFinished(
            field="is_finished",
            then_=[superuser_access],
            else_=can_colaborate,
        )
    ]

    #
    # Low level permissions
    #
    can_create = [
        IfRecordOrProjectFinished(
            field="is_finished",
            then_=[superuser_access],
            else_=can_use,
        )
    ]

    can_read = can_use
    can_search = can_use

    can_update = can_manage
    can_delete = can_manage
    can_finish = can_manage
    can_manage_access = can_manage

    can_manage_compendium = can_manage
