# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_db import db
from invenio_records.models import RecordMetadataBase


class ResearchPipelineMetadata(db.Model, RecordMetadataBase):
    """Research pipeline database model."""

    __tablename__ = "pipeline_research_pipeline"

    # Enables SQLAlchemy-Continuum versioning
    __version__ = {}


__all__ = "ResearchPipelineMetadata"
