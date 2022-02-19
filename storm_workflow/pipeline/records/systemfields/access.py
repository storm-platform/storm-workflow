# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_accounts.models import User as InvenioUser

from storm_project.project.records.api import ResearchProject
from storm_project.project.records.models import ResearchProjectMetadata

from storm_commons.records.systemfields.models import Agent, AgentList
from storm_commons.records.systemfields.fields.access import RecordAccess


class WorkflowAgent(Agent):
    """Workflow access agent."""

    #
    # Supported types
    #
    agent_cls = {"user": InvenioUser, "project": ResearchProjectMetadata}

    #
    # Loaders
    #
    agent_cls_loaders = {
        "user": lambda x: InvenioUser.query.get(x),
        "project": lambda x: ResearchProject.pid.resolve(x).model,
    }


class WorkflowAgents(AgentList):
    """A list of Workflow Agents."""

    agent_cls = WorkflowAgent


class WorkflowAccess(RecordAccess):
    """Workflow access management."""

    owners_cls = WorkflowAgents
    contributors_cls = WorkflowAgents
