@echo off
set "script_file_name=\setup_py_modu.bat"

REM get current path
set dirVar=%cd%
REM append the file name
set script_path=%cd%%script_file_name%
set script_path=^"%script_path%^"

echo Please enter time on which git report will be generated and e-mailed on weekdays.
set /p auto_time=[HH:MM]:

rem SchTasks /Create /SC DAILY /TN “git_task” /TR %script_path% /ST 09:44
SCHTASKS /Create /SC weekly /D MON,TUE,WED,THU,FRI /ST %auto_time% /TN TemcoGitReport /TR %script_path% /V1 /F
pause