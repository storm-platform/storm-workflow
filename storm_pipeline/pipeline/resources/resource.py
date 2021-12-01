# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask_resources import route

from invenio_records_resources.resources.records.resource import RecordResource


class ResearchPipelineResource(RecordResource):
    """Research pipeline API resource."""

    def create_url_rules(self):
        """Routing for the views."""

        routes = self.config.routes
        url_rules = [
            # Base operations
            route("GET", routes["get-item"], self.read),
            route("GET", routes["list-item"], self.search),
            route("POST", routes["create-item"], self.create),
            route("PUT", routes["update-item"], self.update),
            route("DELETE", routes["delete-item"], self.delete),
            # Graph manipulation operations
            # route("POST", routes["add-graph-item"], self.delete),
            # route("POST", routes["delete-graph-item"], self.delete),
        ]

        return url_rules


__all__ = "ResearchPipelineResource"
