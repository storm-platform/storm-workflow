# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.base import BaseProvider

from invenio_pidstore.errors import PIDDoesNotExistError, PIDAlreadyExists


class ResearchPipelineIdProvider(BaseProvider):

    pid_type = "pipeid"
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name."""

    object_type = "rec"
    """Type of object."""

    default_status = PIDStatus.REGISTERED
    """Research pipeline IDs with an object are by default registered."""

    @classmethod
    def create(cls, record, **kwargs):
        """Create a new Research Pipeline identifier.
        Args:
            record (Research Pipeline): The Research Pipeline record.
            kwargs (dict): Dict to hold generated pid_value and status.
        Returns:
            ResearchPipelineIdProvider: A `ResearchPipelineIdProvider` instance.
        See:
            For more extra parameters, please see the
            `https://invenio-pidstore.readthedocs.io/en/latest/api.html#invenio_pidstore.providers.base.BaseProvider`.
        """
        kwargs["pid_value"] = record["id"]
        kwargs["status"] = cls.default_status
        kwargs["object_type"] = cls.object_type
        kwargs["object_uuid"] = record.model.id
        return super(ResearchPipelineIdProvider, cls).create(**kwargs)

    @classmethod
    def update(cls, pid, new_value):
        """`Update the value of the ResearchPipeline identifier`.
        Args:
            pid (str): Persistent Identifier type.
            new_value (str): The new string value.
        Returns:
            ResearchPipelineIdProvider: A `ResearchPipelineIdProvider` instance.
        """
        try:
            existing_pid = cls.get(new_value).pid
        except PIDDoesNotExistError:
            pass
        else:
            raise PIDAlreadyExists(existing_pid.pid_type, existing_pid.pid_value)
        pid.pid_value = new_value
        return cls(pid)


__all__ = "ResearchPipelineIdProvider"
