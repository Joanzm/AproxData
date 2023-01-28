import sys
from cx_Freeze import setup, Executable

appVersion = "0.1.0"

buildOptions = {
      'build_exe': {'build_exe': 'build/%s/AproxData'%(sys.platform),'include_files': [('View/', 'src/View/')]}
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(name = "AproxData",
      version = appVersion,
      description = "App for analyzing different interpolation algorithm.",
      author = "Jonas Anzmann",
      executables = [Executable("main.py", target_name="AproxData.exe", base=base, shortcut_name = 'Aprox', shortcut_dir = 'DesktopFolder', icon = 'View/AproxIcon.ico')],
      options = buildOptions)