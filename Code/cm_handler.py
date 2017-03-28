import os
# from os import subprocess
import json
import xml.etree.cElementTree as ET

class MakeXMLSM:
    def __init__(self, st_date_time):

        self.st_date_time = st_date_time

        with open('config/config.json', 'rb') as config_sm:
            var_config_sm = json.load(config_sm)
            config_sm.close()

        self.prgm_lang = var_config_sm["pgm_lng"]
        self.src_dir = var_config_sm["prj_dir"]

        if self.prgm_lang == 'C':
            self.src_ext = "*.h,*.c"

        if self.prgm_lang == 'C++':
            self.src_ext = "*.h,*.cpp"

        elif self.prgm_lang == 'C#':
            self.src_ext = "*.cs"

        elif self.prgm_lang == 'Java':
            self.src_ext = "*.java"

        elif self.prgm_lang == "VB.NET":
            self.src_ext = "*.vb"

        elif self.prgm_lang == "HTML":
            self.src_ext = "*.htm;*.html;*.asp"

        elif self.prgm_lang == "Visual Basic":
            self.src_ext = "*.frm;*.cls;*.bas"

        elif self.prgm_lang == "Delphi":
            self.src_ext = "*.pas"

        self.get_current_dir = str(os.getcwd()) + "\\config\\"
        self.get_current_dir_op = str(os.getcwd()) + "\\outputs\\"
        # print get_current_dir

    def set_command_xml(self):
        self.sourcemonitor_commands = ET.Element("sourcemonitor_commands")

        self.write_log = ET.SubElement(self.sourcemonitor_commands, "write_log").text = "true"
        self.command = ET.SubElement(self.sourcemonitor_commands, "command")
        self.project_file = ET.SubElement(self.command, "project_file").text = self.get_current_dir + "temcoSM.smp"
        self.project_language = ET.SubElement(self.command, "project_language").text = str(self.prgm_lang)
        self.modified_complexity = ET.SubElement(self.command, "modified_complexity").text = "true"
        self.ignore_blank_lines = ET.SubElement(self.command, "ignore_blank_lines").text = "false"
        self.source_directory = ET.SubElement(self.command, "source_directory").text = str(self.src_dir)

        self.source_subdirectory_list = ET.SubElement(self.command, "source_subdirectory_list")
        self.exclude_subdirectories = ET.SubElement(self.source_subdirectory_list, "exclude_subdirectories").text = \
            "false"

        # -- get current date and time ----
        date_time = self.st_date_time
        date_now = date_time.date()
        time_now = date_time.time()
        date_time_now = str(date_now) + "T" + str(time_now)

        self.parse_utf8_files = ET.SubElement(self.command, "parse_utf8_files").text = "True"
        self.checkpoint_name = ET.SubElement(self.command, "checkpoint_name").text = "ChkPoint_" + str(date_now) + "T" \
                                                                                     + str(time_now.hour) + "_" \
                                                                                     + str(time_now.minute) + "_" \
                                                                                     + str(time_now.second)

        self.checkpoint_date = ET.SubElement(self.command, "checkpoint_date").text = str(date_time_now)

        self.show_measured_max_block_depth = ET.SubElement(self.command, "show_measured_max_block_depth").text = "True"
        self.file_extensions = ET.SubElement(self.command, "file_extensions").text = str(self.src_ext)
        self.include_subdirectories = ET.SubElement(self.command, "include_subdirectories").text = "true"
        self.ignore_headers_footers = ET.SubElement(self.command, "ignore_headers_footers").text = "2 DOC only"
        self.ignore_headers_footers = ET.SubElement(self.command, "ignore_headers_footers").text = "True"

        self.export = ET.SubElement(self.command, "export")

        self.export_file = ET.SubElement(self.export, "export_file").text = self.get_current_dir_op + "sm_report_" \
                                                                            + str(date_now) + "T" + str(time_now.hour) \
                                                                            + "_" + str(time_now.minute) \
                                                                            + "_"+ str(time_now.second) + ".csv"
        self.export_type = ET.SubElement(self.export, "export_type").text = "3 (project summary as CSV)"
        self.export_option = ET.SubElement(self.export, "export_option").text = "3 (export raw numbers instead of " \
                                                                                "percentages and ratios)"
        self.export_kiviat_file = ET.SubElement(self.export, "export_kiviat_file").text = self.get_current_dir_op + "Kiviat" \
                                                                                                                 " for @CHECKPOINT@.bmp"

        self.tree = ET.ElementTree(self.sourcemonitor_commands)
        self.tree.write("config/sourc_mn.xml")
        pass

    def gen_sm_report(self):
        os.system("sourcemonitor /c \"config/sourc_mn.xml\"")
        pass
    pass