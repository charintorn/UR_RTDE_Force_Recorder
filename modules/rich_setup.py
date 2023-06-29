import sys

sys.path.append("lib")

import inspect as inspt
from rich import print, inspect
from rich.console import Console
from rich.theme import Theme
from rich.traceback import install

install()

custom_theme = Theme(
    {
        "success": "green",
        "error": "red",
        "info": "dim cyan",
        "warning": "bright_yellow",
        "danger": "bold red",
    }
)

console = Console(theme=custom_theme)
