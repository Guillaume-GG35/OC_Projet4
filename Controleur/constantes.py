#!/usr/bin/env python3

from rich.console import Console
import os

CONSOLE = Console()
CHEMIN_DB = os.path.join("data", "tournaments")
CHEMIN_DB_TOURNOIS = os.path.join("data", "tournaments", "historique", "")
CHEMIN_BACKUP_TOURNOIS = os.path.join("data", "backup", "historique", "")
CHEMIN_BACKUP_DB = os.path.join("data", "backup", "")
DB = os.path.join("data", "tournaments", "data.json")
RAPPORTS = os.path.join("data", "reports", "")
STRING = "str"
NUMERIC = "num"
NUM_OR_EMPTY = "NumOrEmpty"
STR_OR_NUM = "StrOrNum"
STRNUM_OR_EMPTY = "StrNumOrEmpty"
