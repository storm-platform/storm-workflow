# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_accounts.models import User as InvenioUser

from storm_project.project.records.api import ResearchProject
from storm_project.project.records.models import ResearchProjectMetadata

from storm_commons.records.systemfields.models import Agent, AgentList
from storm_commons.records.systemfields.fields.access import RecordAccess


class PipelineAgent(Agent):
    """Pipeline access agent."""

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


class PipelineAgents(AgentList):
    """A list of Pipeline Agents."""

    agent_cls = PipelineAgent


class PipelineAccess(RecordAccess):
    """Pipeline access management."""

    owners_cls = PipelineAgents
    contributors_cls = PipelineAgents
