import xml.etree.cElementTree as ET

task = ET.Element("Task", version="1.2", xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task")

# Generate RegistrationInfo
RegistrationInfo = ET.SubElement(task, "RegistrationInfo")
ET.SubElement(RegistrationInfo, "Description").text = "Temco Git report tool"

# Generate Triggers
Triggers = ET.SubElement(task, "Triggers")
CalendarTrigger = ET.SubElement(Triggers, "CalendarTrigger")
ET.SubElement(CalendarTrigger, "StartBoundary").text = "2017-03-05T16:13:00.000"
ET.SubElement(CalendarTrigger, "Enabled").text = "true"
ScheduleByWeek = ET.SubElement(CalendarTrigger, "ScheduleByWeek")
DaysOfWeek = ET.SubElement(ScheduleByWeek, "DaysOfWeek")

Sunday = ET.SubElement(DaysOfWeek, "Sunday")
# TODO insert Days here

# Generate Principals
Principals = ET.SubElement(task, "Principals")
Principal = ET.SubElement(Principals, "Principal", id="Author")
ET.SubElement(Principal, "LogonType").text = "InteractiveToken"
ET.SubElement(Principal, "RunLevel").text = "LeastPrivilege"

# Generate Settings
Settings = ET.SubElement(task, "Settings")
ET.SubElement(Settings, "MultipleInstancesPolicy").text = "IgnoreNew"
ET.SubElement(Settings, "DisallowStartIfOnBatteries").text = "false"
ET.SubElement(Settings, "StopIfGoingOnBatteries").text = "true"
ET.SubElement(Settings, "AllowHardTerminate").text = "true"
ET.SubElement(Settings, "StartWhenAvailable").text = "true"
ET.SubElement(Settings, "RunOnlyIfNetworkAvailable").text = "false"

IdleSettings = ET.SubElement(Settings, "IdleSettings")
ET.SubElement(IdleSettings, "StopOnIdleEnd").text = "true"
ET.SubElement(IdleSettings, "RestartOnIdle").text = "false"

ET.SubElement(Settings, "AllowStartOnDemand").text = "true"
ET.SubElement(Settings, "Enabled").text = "true"
ET.SubElement(Settings, "Hidden").text = "false"
ET.SubElement(Settings, "RunOnlyIfIdle").text = "false"
ET.SubElement(Settings, "WakeToRun").text = "false"
ET.SubElement(Settings, "ExecutionTimeLimit").text = "P3D"
# ET.SubElement(Settings, "Priority").text = "7"

Actions = ET.SubElement(task, "Actions", Context="Author")
Exec = ET.SubElement(Actions, "Exec")
ET.SubElement(Exec, "Command").text = "C:\\TemcoNepal\\app_backend.exe"
ET.SubElement(Exec, "WorkingDirectory").text = "C:\TemcoNepal\\"

tree = ET.ElementTree(task)
tree.write("TestSch.xml")
