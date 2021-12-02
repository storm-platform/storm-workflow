# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


import re

from pydash import py_

from typing import Dict, List
from marshmallow import ValidationError
from invenio_records.dictutils import dict_set

from invenio_access.permissions import system_process

from invenio_pidstore.errors import PIDAlreadyExists
from invenio_records_resources.services.records.components import ServiceComponent

from storm_graph import graph_json_from_manager, graph_manager_from_json
from storm_graph.models import Vertex


class PIDComponent(ServiceComponent):
    """PID generator component.

    See:
        This class is adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/services/components.py#L18
    """

    @classmethod
    def _validate(cls, pid_value):
        """Checks the validity of the provided pid value."""
        blop = re.compile("^[-\w]+$")
        if not bool(blop.match(pid_value)):
            raise ValidationError(
                "The ID should contain only letters with numbers or dashes.",
                field_name="id",
            )

    def create(self, identity, record=None, data=None, **kwargs):
        """Create a Research Project PID from its metadata."""
        data["id"] = data["id"].lower()
        self._validate(data["id"])
        record["id"] = data["id"]
        try:
            provider = record.__class__.pid.field._provider.create(record=record)
        except PIDAlreadyExists:
            raise ValidationError(
                "A Research Project with this identifier already exists.",
                field_name="id",
            )
        setattr(record, "pid", provider.pid)


class ResearchPipelineAccessComponent(ServiceComponent):
    """Access component to Research Project.

    See:
        This code is adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/services/components.py#L126
    """

    def _populate_access_and_validate(self, identity, data, record, **kwargs):
        if record is not None and "access" in data:
            record.setdefault("access", {})
            record["access"].update(data.get("access", {}))

    def _init_owners(self, identity, record, **kwargs):
        """Create a owner field into the record metadata."""
        is_system_process = system_process in identity.provides

        owners = []
        if not is_system_process:
            owners = [{"user": identity.id}]

        dict_set(record, "access.owned_by", owners)

    def _init_contributors(self, identity, record, **kwargs):
        """Create a contributor field into the record metadata."""
        is_system_process = system_process in identity.provides

        contributors = []
        if not is_system_process:
            contributors = [{"user": identity.id}]

        dict_set(record, "access.contributed_by", contributors)

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        self._populate_access_and_validate(identity, data, record, **kwargs)
        self._init_owners(identity, record, **kwargs)
        self._init_contributors(identity, record, **kwargs)

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._populate_access_and_validate(identity, data, record, **kwargs)

    def update_draft(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._populate_access_and_validate(identity, data, record, **kwargs)

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record.access = draft.access

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.access = record.access

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.access = record.access


class GraphComponent(ServiceComponent):
    """Service component for graph."""

    def create(self, identity, data=None, record=None, errors=None, **kwargs):
        """Define a new graph document in the record."""
        record.graph = {}


class CompendiaComponent(ServiceComponent):
    """Service component for compendia manipulation."""

    def _prepare_file_metadata(
        self, identity, files_definition: List, path: str, type_: str, rec_id: str
    ) -> Dict:
        """Prepare file as vertex metadata.

        Args:
            files_definition (list): List with the files definition (e.g., {"inputs": ["key": "file.txt"]}).

            path (str): Path from where the data to prepare will be extracted (e.g., inputs, metadata.inputs).

            type_ (str): data type (e.g., input, output)

            rec_id (str): Compendium Record id.
        Returns:
            Dict: Dictionary with the files metadata prepared to be used in the graph metadata.
        """
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
                                rec_id, file.get("key"), identity
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

    def add_compendium(self, identity, record=None, pipeline_record=None, **kwargs):
        """Add a new compendium in the research pipeline graph."""

        # creating the record.
        vertex = self._generate_metadata_vertex(identity, record)

        # adding the vertex to the graph.
        graph_manager = graph_manager_from_json({"graph": pipeline_record.get("graph")})
        graph_manager.add_vertex(vertex)

        # saving the updated graph.
        pipeline_record.update(graph_json_from_manager(graph_manager))

    def delete_compendium(self, identity, record=None, pipeline_record=None, **kwargs):
        """Remove a compendium from the graph (including its dependent neighbors)."""

        graph_manager = graph_manager_from_json({"graph": pipeline_record.get("graph")})
        graph_manager.delete_vertex(record.id)

        # saving the updated graph.
        pipeline_record.update(graph_json_from_manager(graph_manager))


__all__ = (
    "PIDComponent",
    "GraphComponent",
    "CompendiaComponent",
    "ResearchPipelineAccessComponent",
)
