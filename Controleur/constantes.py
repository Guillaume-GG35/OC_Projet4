#!/usr/bin/env python3

from rich.console import Console
import os

CONSOLE = Console()
DB = os.path.join("data", "tournaments", "data.json")
RAPPORTS = os.path.join("data", "reports", "")
STRING = "str"
NUMERIC = "num"
NUM_OR_EMPTY = "NumOrEmpty"
STR_OR_NUM = "StrOrNum"
STRNUM_OR_EMPTY = "StrNumOrEmpty"
