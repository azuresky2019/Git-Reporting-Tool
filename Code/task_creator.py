import xml.etree.cElementTree as ET

class MakeXMLSCH:
    def __init__(self, week_days, date_time, command_path, working_dir):

        # -- Accumulate variables ---
        self.week_days = week_days
        self.date_time = date_time
        self.command_path = command_path
        self.working_dir = working_dir

        self.if_none_days = 0

        self.task = ET.Element("Task", version="1.2", xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task")

        # Generate RegistrationInfo
        self.RegistrationInfo = ET.SubElement(self.task, "RegistrationInfo")
        ET.SubElement(self.RegistrationInfo,
                      "Description").text = "This is a task for auto running  git report generator"

        # Generate Triggers
        self.Triggers = ET.SubElement(self.task, "Triggers")
        self.CalendarTrigger = ET.SubElement(self.Triggers, "CalendarTrigger")
        ET.SubElement(self.CalendarTrigger, "StartBoundary").text = str(date_time)
        ET.SubElement(self.CalendarTrigger, "Enabled").text = "true"
        self.ScheduleByWeek = ET.SubElement(self.CalendarTrigger, "ScheduleByWeek")
        DaysOfWeek = ET.SubElement(self.ScheduleByWeek, "DaysOfWeek")

        if (self.week_days["Sunday"]):
            Sunday = ET.SubElement(DaysOfWeek, "Sunday")
            pass

        if (self.week_days["Monday"]):
            Monday = ET.SubElement(DaysOfWeek, "Monday")
            pass

        if (self.week_days["Tuesday"]):
            Tuesday = ET.SubElement(DaysOfWeek, "Tuesday")
            pass

        if self.week_days["Wednesday"]:
            Wednesday = ET.SubElement(DaysOfWeek, "Wednesday")
            pass

        if self.week_days["Thursday"]:
            Thursday = ET.SubElement(DaysOfWeek, "Thursday")
            # self.if_none_days += 1
            pass

        if self.week_days["Friday"]:
            Friday = ET.SubElement(DaysOfWeek, "Friday")
            # self.if_none_days += 1
            pass

        if self.week_days["Saturday"]:
            Saturday = ET.SubElement(DaysOfWeek, "Saturday")
            # self.if_none_days += 1
            pass

        # Generate Principals
        self.Principals = ET.SubElement(self.task, "Principals")
        self.Principal = ET.SubElement(self.Principals, "Principal", id="Author")
        ET.SubElement(self.Principal, "LogonType").text = "InteractiveToken"
        ET.SubElement(self.Principal, "RunLevel").text = "LeastPrivilege"

        # Generate Settings
        self.Settings = ET.SubElement(self.task, "Settings")
        ET.SubElement(self.Settings, "MultipleInstancesPolicy").text = "IgnoreNew"
        ET.SubElement(self.Settings, "DisallowStartIfOnBatteries").text = "false"
        ET.SubElement(self.Settings, "StopIfGoingOnBatteries").text = "true"
        ET.SubElement(self.Settings, "AllowHardTerminate").text = "true"
        ET.SubElement(self.Settings, "StartWhenAvailable").text = "true"
        ET.SubElement(self.Settings, "RunOnlyIfNetworkAvailable").text = "false"

        self.IdleSettings = ET.SubElement(self.Settings, "IdleSettings")
        ET.SubElement(self.IdleSettings, "StopOnIdleEnd").text = "true"
        ET.SubElement(self.IdleSettings, "RestartOnIdle").text = "false"

        ET.SubElement(self.Settings, "AllowStartOnDemand").text = "true"
        ET.SubElement(self.Settings, "Enabled").text = "true"
        ET.SubElement(self.Settings, "Hidden").text = "false"
        ET.SubElement(self.Settings, "RunOnlyIfIdle").text = "false"
        ET.SubElement(self.Settings, "WakeToRun").text = "false"
        ET.SubElement(self.Settings, "ExecutionTimeLimit").text = "P3D"
        # ET.SubElement(self.Settings, "Priority").text = "7"

        self.Actions = ET.SubElement(self.task, "Actions", Context="Author")
        self.Exec = ET.SubElement(self.Actions, "Exec")
        ET.SubElement(self.Exec, "Command").text = self.command_path
        ET.SubElement(self.Exec, "WorkingDirectory").text = self.working_dir

        self.tree = ET.ElementTree(self.task)
        self.tree.write("config/temco_git_tool.xml")
    pass