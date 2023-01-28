:: Convert .svg file to .ico file via inkscape and magick

@echo off
setlocal enabledelayedexpansion
set filename=%1
set sizes=16 24 32 48 58 64 80 96 120 128 152 180 256 512 1024

mkdir ..\build\IconExport
for %%s in (%sizes%) do (
	inkscape -w %%s -h %%s -o ..\build\IconExport\%%s.png %filename%
)

cd ..\build\IconExport

set var=
for %%s in (%sizes%) do (
	set var=!var!%%s.png 
)
magick convert !var! icon.ico