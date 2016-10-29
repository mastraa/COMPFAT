
import sys
from cx_Freeze import setup, Executable

sys.path.append('librerie/gui')
sys.path.append('librerie')

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["tkinter","numpy","matplotlib"],"includes":["openpyxl","sqlite3"],"include_files":["fatData.db", "icon.ico"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Poseidon",
        version = "BETA_0.1",
        description = "Fatigue life prediction method",
        options = {"build_exe": build_exe_options},
        executables = [Executable(
									"main.py", base=base,
									icon="icon.ico",
									targetName="Poseidon.exe"
								)])