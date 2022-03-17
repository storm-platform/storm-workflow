# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_
from typing import Dict, List

from storm_graph.models import Vertex
from storm_graph import graph_json_from_manager, graph_manager_from_json

from invenio_records_resources.services.records.components import ServiceComponent


class ResearchWorkflowGraphComponent(ServiceComponent):
    """Service component for graph."""

    def create(self, identity, data=None, record=None, errors=None, **kwargs):
        """Define a new graph document in the record."""
        record.graph = {}


class ResearchWorkflowCompendiaComponent(ServiceComponent):
    """Service component for compendia manipulation."""

    def _prepare_file_metadata(
        self, identity, files_definition: List, path: str, type_: str, rec_id: str
    ):
        """Prepare file as vertex metadata.

        Args:
            files_definition (list): List with the files definition (e.g., {"inputs": ["key": "file.txt"]}).

            path (str): Path from where the data to prepare will be extracted (e.g., inputs, metadata.inputs).

            type_ (str): data type (e.g., input, output)

            rec_id (str): Compendium Record id.
        Returns:
            Dict: Dictionary with the files metadata prepared to be used in the graph metadata.
        """

        # temporary solution: in the future, the file manipulation will be done
        # from the record object with systemfields. For now, we import the compendium
        # services.
        from storm_compendium import current_compendium_service

        return (
            py_.chain(files_definition)
            .get(path)
            .map(
                lambda file: {
                    **file,
                    "type": type_,
                    "checksum": (
                        py_.get(
                            current_compendium_service.files.read_file_metadata(
                                identity, rec_id, file.get("key")
                            ).data,
                            "checksum",
                        ).replace("md5:", "")
                    ),
                }
            )
            .value()
        )

    def _generate_metadata_vertex(self, identity, record):
        """Create a metadata vertex from a record.

        Args:
            identity (flask_principal.Identity): User identity

            record (invenio_record.Record): Record

        Returns:
            storm_graph.models.Vertex: Created metadata vertex.
        """
        record_files_definition = py_.get(record.data, "metadata.execution.data")

        # creating the vertex object
        record_files = py_.concat(
            self._prepare_file_metadata(
                identity, record_files_definition, "inputs", "input", record.id
            ),
            self._prepare_file_metadata(
                identity, record_files_definition, "outputs", "output", record.id
            ),
        )

        return Vertex(name=record.id, files=record_files)

    def add_compendium(self, identity, record=None, workflow_record=None, **kwargs):
        """Add a new compendium in the research workflow graph."""

        # creating the record.
        vertex = self._generate_metadata_vertex(identity, record)

        # adding the vertex to the graph.
        graph_manager = graph_manager_from_json(
            {"graph": workflow_record.get("graph")}, validate=False
        )
        graph_manager.add_vertex(vertex)

        # saving the updated graph.
        workflow_record.update(graph_json_from_manager(graph_manager))

    def delete_compendium(self, identity, record=None, workflow_record=None, **kwargs):
        """Remove a compendium from the graph (including its dependent neighbors)."""

        graph_manager = graph_manager_from_json(
            {"graph": workflow_record.get("graph")}, validate=False
        )
        graph_manager.delete_vertex(record.id)

        # saving the updated graph.
        workflow_record.update(graph_json_from_manager(graph_manager))
