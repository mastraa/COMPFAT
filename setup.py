from distutils.core import setup
import py2exe

import sys

sys.path.append('librerie/gui')
sys.path.append('librerie')
import mainGui

setup(windows=["main.py"],
	data_files=[("",['fatData.db']),("librerie",["librerie/gui/maingui.py"])],
	options={"py2exe":{
			"includes":["openpyxl","sqlite3"],
			"packages":["tkinter","numpy","visvis"]}
	}) 