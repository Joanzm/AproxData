import sys
from cx_Freeze import setup, Executable

buildOptions = {
      'build_exe': {'include_files': [('View/', 'src/View/')]}
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(name = "InterPol",
      version = "0.1.0",
      description = "App for analyzing different interpolation algorithm.",
      author = "Jonas Anzmann",
      executables = [Executable("main.py", target_name="AproxData.exe", base=base, shortcut_name = 'Aprox', shortcut_dir = 'DesktopFolder', icon = 'View/AproxIcon.ico')],
      options = buildOptions)