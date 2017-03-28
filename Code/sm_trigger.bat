@echo off
rem setx path "%path%;C:\Program Files (x86)\SourceMonitor"
rem IF NOT EXIST "C:\Program Files (x86)\SourceMonitor" (
	rem setx path "%path%;C:\Program Files\SourceMonitor"
	rem )

rem IF NOT EXIST "C:\Program Files\SourceMonitor" 
	rem setx path "%path%;C:\Program Files (x86)\SourceMonitor"
	rem echo Hello there !
	rem
sourcemonitor /c "config/sourc_mn.xml"
 