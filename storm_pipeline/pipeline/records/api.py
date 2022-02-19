# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.records.api import Record
from storm_commons.records.systemfields.fields.access import RecordAccessField
from invenio_records_resources.records.systemfields import IndexField, PIDField

from invenio_records.systemfields import ConstantField, DictField

from storm_workflow.workflow.records.models import ResearchWorkflowMetadata
from storm_workflow.workflow.records.systemfields.access import WorkflowAccess
from storm_workflow.workflow.records.providers import ResearchWorkflowPIDProvider


class ResearchWorkflow(Record):
    """Research Workflow High-level API."""

    pid = PIDField("id", provider=ResearchWorkflowPIDProvider, create=False)
    schema = ConstantField("$schema", "local://workflow/workflow-v1.0.0.json")

    access = RecordAccessField(access_obj_class=WorkflowAccess)

    model_cls = ResearchWorkflowMetadata
    index = IndexField("workflow-workflow-v1.0.0", search_alias="workflow")

    graph = DictField(clear_none=True, create_if_missing=True)
    is_finished = DictField("is_finished", create_if_missing=True)
