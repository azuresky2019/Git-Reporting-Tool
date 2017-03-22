@echo off

rem :: BatchGotAdmin
rem :-------------------------------------
rem REM  --> Check for permissions
rem     IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
rem >nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
rem ) ELSE (
rem >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
rem )

rem REM --> If error flag set, we do not have admin.
rem if '%errorlevel%' NEQ '0' (
rem     echo Requesting administrative privileges...
rem     goto UACPrompt
rem ) else ( goto gotAdmin )

rem :UACPrompt
rem     echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
rem     set params = %*:"=""
rem     echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

rem     "%temp%\getadmin.vbs"
rem     del "%temp%\getadmin.vbs"
rem     exit /B

rem :gotAdmin
rem     pushd "%CD%"
rem     CD /D "%~dp0"
rem :--------------------------------------

setlocal EnableDelayedExpansion

rem set "python_path=C:\Python27"
rem set "python_app_path=C:\Python27\python.exe"
set "pip_path=C:\Python27\Scripts\pip.exe"
rem set "pip_path_env=C:\Python27\Scripts"
rem set "app_path=../git_api_handler.py"
set "app_path=app_backend.py"

%python_app_path% %app_path%

pause