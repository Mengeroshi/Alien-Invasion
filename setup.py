import cx_Freeze
from cx_Freeze import *
setup(
    name = "alien_invasion",
    options = {"build_exe":{"packages":["pygame"]}},
    executables = [
        Executable(
            "alien_invasion.py",

            )
        ]
    )      