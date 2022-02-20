# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workflow is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_db import db
from invenio_records.models import RecordMetadataBase


class ResearchWorkflowMetadata(db.Model, RecordMetadataBase):
    """Research workflow database model."""

    __tablename__ = "workflow_research_workflows"

    # Enables SQLAlchemy-Continuum versioning
    __version__ = {}
