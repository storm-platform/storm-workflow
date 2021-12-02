# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from typing import Dict

from invenio_records_resources.services.uow import RecordCommitOp, unit_of_work
from invenio_records_resources.services.records import RecordService

from storm_compendium import current_compendium_service


class ResearchPipelineService(RecordService):
    """Research pipeline service."""

    def _transform_compendium(
        self, identity, pipeline_id, rec_id, component_action, uow=None
    ):
        """General operation for performing transformations on the graph (Updating, creating, deleting nodes).

        Args:
            identity (flask_principal.Identity): User identity

            pipeline_id (str): Research Pipeline id

            rec_id (str): Compendium Record id

            component_action (str): Name of the components actions that will be applied in the records.

        Returns:
            Dict: The updated Research Pipeline document.

        Note:
            The transformation is done based on the components linked to the service.
        """

        # checking permissions
        self.require_permission(identity, "manage_compendium")

        # read record and files definitions
        record = current_compendium_service.read(rec_id, identity)

        # load pipeline record
        pipeline_record = self.record_cls.pid.resolve(pipeline_id)

        self.run_components(
            component_action,
            identity,
            record=record,
            pipeline_record=pipeline_record,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(pipeline_record, self.indexer))

        return self.result_item(
            self, identity, pipeline_record, links_tpl=self.links_item_tpl
        )

    @unit_of_work()
    def add_compendium(self, identity, pipeline_id, rec_id, uow=None):
        """Add a new compendium to the research pipeline graph.

        Args:
            identity (flask_principal.Identity): User identity

            pipeline_id (str): Research Pipeline id

            rec_id (str): Compendium Record id
        Returns:
            Dict: The updated Research Pipeline document.
        """

        return self._transform_compendium(
            identity, pipeline_id, rec_id, "add_compendium", uow
        )

    @unit_of_work()
    def delete_compendium(self, identity, pipeline_id, rec_id, uow=None):
        """Delete a compendium from the research pipeline graph.

        Args:
            identity (flask_principal.Identity): User identity

            pipeline_id (str): Research Pipeline id

            rec_id (str): Compendium Record id
        Returns:
            Dict: The updated Research Pipeline document.
        """

        return self._transform_compendium(
            identity, pipeline_id, rec_id, "delete_compendium", uow
        )


__all__ = "ResearchPipelineService"
