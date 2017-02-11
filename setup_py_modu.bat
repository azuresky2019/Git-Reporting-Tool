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

set "python_path=C:\Python27"
set "python_app_path=C:\Python27\python.exe"
set "pip_path=C:\Python27\Scripts\pip.exe"
set "pip_path_env=C:\Python27\Scripts"
rem set "app_path=../git_api_handler.py"
set "app_path=main.py"

rem echo %python_path%

echo Make sure that you have installed python 2.7.9 or higher.

if exist %python_path% (
    echo Found Python 2.7.x is installed.
    echo Adding "Python" path to environmental variables.
    rem setx /M PATH "%PATH%;%python_path%"
    setx PATH "%PATH%;%python_path%"
    if exist %pip_path% (
    	echo Found pip installed..
    	echo Adding "pip" path to environmental variables
    	rem setx /M PATH "%PATH%;%pip_path_env%"
    	setx PATH "%PATH%;%pip_path_env%"
    	echo Installing required modules...   	
    	%pip_path% install requests
 		%pip_path% install python-dateutil
 		%pip_path% install gitpython

 		%python_app_path% %app_path%

 		REM it is made to generate a report at first
 		rem var_unpack_supply.bat
 		rem ask for git username
 		rem set /p user="Enter username of your existing github account:"
 		rem set /p passw="Enter password of your existing github account:"
 		rem set /p repo_name="Enter the repositroy you want to make report of:"
 		rem %python_app_path% %app_path% %username% %password% %repo_name% 	 	
    	) else (
    	echo pip not installed. Please install "pip" or installe python 2.7.9 or 2.7.11 !
    	)
) else (
    echo Python not installed please install "python 2.7.9" or "python 2.7.11".
)