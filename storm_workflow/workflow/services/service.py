# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Dict

from storm_commons.admin.service import AdminRecordService
from storm_commons.services.links import ActionLinksTemplate
from storm_compendium import current_compendium_service

from invenio_records_resources.services.uow import RecordCommitOp, unit_of_work


class ResearchWorkflowService(AdminRecordService):
    """Research workflow service."""

    @property
    def links_item_tpl(self):
        """Item links template."""
        return ActionLinksTemplate(self.config.links_item, self.config.links_action)

    def _transform_compendium(
        self, identity, workflow_id, rec_id, component_action, uow=None
    ):
        """General operation for performing transformations on the graph (Updating, creating, deleting nodes).

        Args:
            identity (flask_principal.Identity): User identity

            workflow_id (str): Research Workflow id

            rec_id (str): Compendium Record id

            component_action (str): Name of the components actions that will be applied in the records.

        Returns:
            Dict: The updated Research Workflow document.

        Note:
            The transformation is done based on the components linked to the service.
        """
        # load workflow record
        workflow_record = self.record_cls.pid.resolve(workflow_id)

        # checking permissions
        self.require_permission(identity, "manage_compendium", record=workflow_record)

        # read record and files definitions
        record = current_compendium_service.read(identity, rec_id)

        self.run_components(
            component_action,
            identity,
            record=record,
            workflow_record=workflow_record,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(workflow_record, self.indexer))

        return self.result_item(
            self, identity, workflow_record, links_tpl=self.links_item_tpl
        )

    @unit_of_work()
    def add_compendium(self, identity, workflow_id, rec_id, uow=None):
        """Add a new compendium to the research workflow graph.

        Args:
            identity (flask_principal.Identity): User identity

            workflow_id (str): Research Workflow id

            rec_id (str): Compendium Record id
        Returns:
            Dict: The updated Research Workflow document.
        """

        return self._transform_compendium(
            identity, workflow_id, rec_id, "add_compendium", uow
        )

    @unit_of_work()
    def delete_compendium(self, identity, workflow_id, rec_id, uow=None):
        """Delete a compendium from the research workflow graph.

        Args:
            identity (flask_principal.Identity): User identity

            workflow_id (str): Research Workflow id

            rec_id (str): Compendium Record id
        Returns:
            Dict: The updated Research Workflow document.
        """

        return self._transform_compendium(
            identity, workflow_id, rec_id, "delete_compendium", uow
        )

    @unit_of_work()
    def finish_workflow(self, identity, workflow_id, uow=None):
        """Finish a research workflow.

        Args:
            identity (flask_principal.Identity): User identity

            workflow_id (str): Research Workflow id

        Returns:
            Dict: The updated Research Workflow document.
        """
        # load workflow record
        workflow_record = self.record_cls.pid.resolve(workflow_id)

        # checking permissions
        self.require_permission(identity, "finish", record=workflow_record)

        self.run_components(
            "finish",
            identity,
            record=workflow_record,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(workflow_record, self.indexer))

        return self.result_item(
            self, identity, workflow_record, links_tpl=self.links_item_tpl
        )
