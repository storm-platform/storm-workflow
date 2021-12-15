# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Felipe Menino Carlos.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pipeline manager module for the Storm platform."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "pytest-invenio>=1.4.0",
]

extras_require = {
    "docs": [
        "Sphinx>=3,<4",
    ],
    "tests": tests_require,
}

extras_require["all"] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = []

install_requires = [
    "storm-compendium @ git+https://github.com/storm-platform/storm-compendium@main",
    "storm-graph @ git+https://github.com/storm-platform/storm-graph@main",
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("storm_pipeline", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="storm-pipeline",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords=["Storm Platform", "Research pipelines", "Invenio module"],
    license="MIT",
    author="Felipe Menino Carlos",
    author_email="felipe.carlos@inpe.br",
    url="https://github.com/storm-platform/storm-pipeline",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "invenio_config.module": [
            "storm_pipeline = storm_pipeline.config",
        ],
        "invenio_base.apps": [
            "storm_pipeline = storm_pipeline:StormPipeline",
        ],
        "invenio_base.api_apps": [
            "storm_pipeline = storm_pipeline:StormPipeline",
        ],
        "invenio_base.api_blueprints": [
            "storm_pipeline_api = storm_pipeline.views:create_research_pipeline_blueprint_api"
        ],
        "invenio_db.models": [
            "pipeline_record = storm_pipeline.pipeline.records.models"
        ],
        "invenio_search.mappings": [
            "pipeline = storm_pipeline.pipeline.records.mappings"
        ],
        "invenio_jsonschemas.schemas": [
            "pipeline = storm_pipeline.pipeline.records.jsonschemas"
        ]
        # 'invenio_access.actions': [],
        # 'invenio_admin.actions': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.api_apps': [],
        # 'invenio_base.api_blueprints': [],
        # 'invenio_base.blueprints': [],
        # 'invenio_celery.tasks': [],
        # 'invenio_db.models': [],
        # 'invenio_pidstore.minters': [],
        # 'invenio_records.jsonresolver': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 1 - Planning",
    ],
)
