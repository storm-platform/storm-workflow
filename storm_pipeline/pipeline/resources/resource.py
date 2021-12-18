# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import g
from flask_resources import route, response_handler, resource_requestctx

from storm_commons.admin.resource import AdminRecordResource
from storm_commons.resources.parsers import request_view_args


class ResearchPipelineResource(AdminRecordResource):
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
            route("POST", routes["add-graph-item"], self.add_compendium),
            route("DELETE", routes["delete-graph-item"], self.delete_compendium),
            # Status control
            route("POST", routes["finish-item"], self.finish_pipeline),
            # Access control
            route("POST", routes["add-item-agent"], self.admin_add_agent),
            route("DELETE", routes["remove-item-agent"], self.admin_remove_agent),
            route("GET", routes["list-item-agent"], self.admin_list_agents),
        ]

        return url_rules

    @request_view_args
    @response_handler()
    def add_compendium(self):
        """Read an item."""
        compendium = self.service.add_compendium(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["compendium_id"],
        )

        return compendium.to_dict(), 200

    @request_view_args
    @response_handler()
    def delete_compendium(self):
        """delete a compendium node from the pipeline."""
        compendium = self.service.delete_compendium(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["compendium_id"],
        )
        return compendium.to_dict(), 200

    @request_view_args
    @response_handler()
    def finish_pipeline(self):
        """Finish a research compendium."""
        compendium = self.service.finish_pipeline(
            g.identity,
            resource_requestctx.view_args["pid_value"],
        )
        return compendium.to_dict(), 200
