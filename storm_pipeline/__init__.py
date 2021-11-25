# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Felipe Menino Carlos.
#
# storm-pipeline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pipeline manager module for the Storm platform"""

from .ext import StormPipeline
from .version import __version__

__all__ = ('__version__', 'StormPipeline')
