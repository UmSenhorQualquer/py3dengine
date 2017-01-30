set WINPYDIR=C:\Users\swp\Python\WinPython-32bit-2.7.10.3\python-2.7.10
set WINPYVER=2.7.10.3
set HOME=%WINPYDIR%\..\settings
set WINPYARCH="WIN32"

set PATH=%WINPYDIR%\Lib\site-packages\PyQt4;%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%WINPYDIR%\..\tools;

rem keep nbextensions in Winpython directory, rather then %APPDATA% default
set JUPYTER_DATA_DIR=%WINPYDIR%\..\settings

set PROJECTNAME=py3DSceneEditorApp
set BUILDSETTINGSDIR=%WORKSPACE%\build_settings\win
set MAINSCRIPT=%WORKSPACE%\py3DSceneEditor\__main__.py
set BUILDOUTDIR=%WORKSPACE%\build
set DISTOUTDIR=%WORKSPACE%\dist
set ICONNAME=cf_icon_128x128.ico

python setup.py --version 	> software_version.txt
"C:\Program Files\Git\bin\git.exe" rev-list  --all --count > git_version.txt
SET /p DEV_VERSION= < software_version.txt
SET /p GIT_VERSION= < git_version.txt
SET DEV_VERSION=%DEV_VERSION%.build-%GIT_VERSION%
DEL software_version.txt
DEL git_version.txt


rem echo %WORKSPACE%
rem echo %PROJECTNAME%
rem echo %BUILDSETTINGSDIR%
rem echo %MAINSCRIPT%
rem echo %BUILDOUTDIR%
rem echo %DISTOUTDIR%

@RD /S /Q %BUILDOUTDIR%
@RD /S /Q %DISTOUTDIR%

pip uninstall -y pyforms
pip install https://github.com/UmSenhorQualquer/pyforms/archive/master.zip
pip show pyforms

pip uninstall -y py3DEngine
pip install "%WORKSPACE%\py3DEngine_distribution"

rem echo "Running pyinstaller --additional-hooks-dir %BUILDSETTINGSDIR%\hooks --name %PROJECTNAME% --icon %BUILDSETTINGSDIR%\%ICONNAME% --onefile %MAINSCRIPT%"

pyinstaller --additional-hooks-dir "%BUILDSETTINGSDIR%\hooks" --name "%PROJECTNAME%_v%DEV_VERSION%" --icon "%BUILDSETTINGSDIR%\%ICONNAME%" --onefile "%MAINSCRIPT%"
