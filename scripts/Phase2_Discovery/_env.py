#!/usr/bin/env python3
"""
Shared environment helpers for the Phase 2 pipeline.

This module:
- resolves the repository root from the Phase2_Discovery directory;
- configures a writable Numba cache before Scanpy/Numba imports.
"""

from __future__ import annotations

import os
from pathlib import Path


# Phase2_Discovery/_env.py
# parents[0] = Phase2_Discovery
# parents[1] = scripts
# parents[2] = repository root
ROOT = str(Path(__file__).resolve().parents[2])

NUMBA_CACHE_DIR = os.path.join(
    ROOT, "data", "external", ".numba_cache"
)


def setup_numba_cache() -> str:
    """Set and create the writable Numba cache directory."""
    os.makedirs(NUMBA_CACHE_DIR, exist_ok=True)
    os.environ.setdefault("NUMBA_CACHE_DIR", NUMBA_CACHE_DIR)
    return NUMBA_CACHE_DIR
