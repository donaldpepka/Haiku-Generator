import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

exe = Executable(
     script="VirtualPoet.py",
     base="Console",
     )

setup(  name="Virtual Poet",
        version="0.1",
        description="Birthday present!",
        options={"build_exe": build_exe_options},
        executables=[exe])
