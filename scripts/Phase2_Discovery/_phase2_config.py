#!/usr/bin/env python3
"""
Shared configuration for the HuMicA Phase 2 pipeline.

All Phase 2 scripts use this module for:
- repository paths;
- HuMicA state labels and ordering;
- STRING MCL module names;
- expression-scale definition;
- reproducibility parameters;
- common output directories and logging.

This module contains configuration and lightweight helpers only.
"""

from __future__ import annotations

import logging
import os

from _env import ROOT


# ==========================================================================
# Paths
# ==========================================================================

MASTER_CHECKPOINT = os.path.join(
    ROOT, "checkpoints", "HuMicAtlas_validated.h5ad"
)

CANDIDATE_CHECKPOINT = os.path.join(
    ROOT, "checkpoints", "phase2_candidates.h5ad"
)

PRESENCE_TABLE = os.path.join(
    ROOT, "tables", "candidate_presence.csv"
)

TABLES_DIR = os.path.join(ROOT, "tables")
FIGURES_DIR = os.path.join(ROOT, "figures")
DOCS_DIR = os.path.join(ROOT, "docs")
METADATA_DIR = os.path.join(ROOT, "data", "metadata")
LOGS_DIR = os.path.join(ROOT, "logs")


# ==========================================================================
# HuMicA microglial states
# ==========================================================================

STATE_LABELS = {
    0: "Homeos1",
    1: "Inflam.DAM",
    2: "DIMs",
    3: "Ribo.DAM1",
    4: "Homeos2",
    5: "Ribo.DAM2",
    6: "Lipo.DAM",
    7: "MAC",
    8: "Homeos3",
}

STATE_GROUP = {
    "Homeos1": "Homeostatic",
    "Homeos2": "Homeostatic",
    "Homeos3": "Homeostatic",
    "Inflam.DAM": "DAM",
    "Ribo.DAM1": "DAM",
    "Ribo.DAM2": "DAM",
    "Lipo.DAM": "DAM",
    "DIMs": "DIM",
    "MAC": "Macrophage",
}

STATE_ORDER = [
    "Homeos1",
    "Homeos2",
    "Homeos3",
    "Inflam.DAM",
    "Ribo.DAM1",
    "Ribo.DAM2",
    "Lipo.DAM",
    "DIMs",
    "MAC",
]

STATE_KEY_MARKERS = {
    "Homeos1": "P2RY12, CX3CR1",
    "Homeos2": "GRID2",
    "Homeos3": "SERPINE1, CD83/DUSP1/FOS",
    "Inflam.DAM": "TMEM163, SPP1",
    "Ribo.DAM1": "SYT1, PCDH9 (ribosomal)",
    "Ribo.DAM2": "PLEKHA7, MECOM (ribosomal)",
    "Lipo.DAM": "GPNMB, PTPRG (lysosome/lipid)",
    "DIMs": "SLC2A3, CD83",
    "MAC": "CD163, MRC1 (border-associated)",
}

STATE_CLUSTER_COL = "V1_clusters"


# ==========================================================================
# STRING MCL modules
# ==========================================================================

STRING_CLUSTER_NAMES = {
    1: "PKA activation in glucagon signalling",
    2: "(cluster 2)",
    3: "(cluster 3)",
    4: "Epidermal growth factor receptor signaling pathway",
    5: "Rho protein signal transduction",
    6: "Eukaryotic Translation Elongation",
    7: "Apoptosis",
    8: "Blood microparticle",
    9: "Response to unfolded protein",
    10: "Sphingolipid metabolism",
}

# Original Phase 1 STRING modules.
STRING_MODULE_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Modules represented among the 41 Phase-2 candidates.
PHASE2_MODULE_IDS = [1, 4, 5, 6, 7, 8, 9, 10]


# ==========================================================================
# Analysis parameters
# ==========================================================================

RANDOM_SEED = 0

# The fixed HuMicA checkpoint stores SCT Pearson residuals in .X.
# Phase 2 uses this native scale directly.
EXPRESSION_MATRIX = "X"
EXPRESSION_SCALE_LABEL = "mean SCT Pearson residual"

# Within-module coherence method.
COHERENCE_METHOD = "spearman"

# score_genes control-gene pool.
SCORE_GENES_CTRL_SIZE = 50


# ==========================================================================
# Shared helpers
# ==========================================================================

def ensure_dirs() -> None:
    """Create Phase 2 output directories if they do not exist."""
    for directory in (
        TABLES_DIR,
        FIGURES_DIR,
        DOCS_DIR,
        METADATA_DIR,
        LOGS_DIR,
    ):
        os.makedirs(directory, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Return a shared console + file logger."""
    ensure_dirs()

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        os.path.join(LOGS_DIR, f"{name}.log")
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
