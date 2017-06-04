import HTML_table
import json
# from time_convert import TimeConvert

class HTML:
    def __init__(self, days):
        self.table_header = ["Project", "User", "Files changed", "Lines added", "Lines deleted"]
        self.html_lang = "<h4>Git commit report summary :</h4>" \
                    "<p>This is a summary of commits done approximately within last %d days by different users for " \
                         "different projects. Please find attached CSV version of this report. Thank you." \
                         "</p><p><i> Note: This is an automatically generated email, please do not reply.</i></p>" \
                         "<b> ------------------------------------------------------------------------------------" \
                         "-----------------------------------------------------------------------------------------" \
                         "-----------</b>" %days

    def encode_html(self, list_repo):
        total_repos = len(list_repo)
        list_commits = [self.table_header]
        for repo in range(0, total_repos):
            user_collection_file = 'output_jsons/' + list_repo[repo] + '-' + 'user_info.json'
            project_name = list_repo[repo]
            print "Processing data from repo: \"%d.%s\"." % (repo+1, list_repo[repo])
            with open(user_collection_file, 'rb') as users_file:
                user_details = json.load(users_file)
                users_file.close()
                total_users = len(user_details)
                for user in range(0, total_users):
                    user_name = user_details[user]["user"]
                    list_html_data = [None] * len(self.table_header)
                    list_html_data[0] = project_name
                    list_html_data[1] = user_name

                    if user_details[user]["file_exceed"]:
                        list_html_data[2] = ">" + str(user_details[user]["files_changed_total"])
                    else:
                        list_html_data[2] = str(user_details[user]["files_changed_total"])
                        pass

                    list_html_data[3] = str(user_details[user]["lines_added_total"])
                    list_html_data[4] = str(user_details[user]["lines_deleted_total"])
                    list_commits.append(list_html_data)
                    project_name = 0
                    pass
                pass
            pass
        table_html = HTML_table.table(list_commits)
        return self.html_lang + table_html
        pass

    def encode_html_local(self, list_project_based):

        list_commits = [self.table_header]

        for indx_repo, repo in enumerate(list_project_based):
            print "Processing data from repo: \"%d.%s\"." % (indx_repo+1, repo["project"])
            project_name = repo["project"]
            for user in repo["user_info"]:
                try:
                    user_name = str(user["user"])
                    list_html_data = [None] * len(self.table_header)
                    list_html_data[0] = project_name
                    list_html_data[1] = user_name
                    list_html_data[2] = user["files_changed_total"] if user["files_changed_total"] else '0'
                    list_html_data[3] = user["lines_added_total"] if user["lines_added_total"] else '0'
                    list_html_data[4] = user["lines_deleted_total"] if user["lines_deleted_total"] else '0'
                    list_commits.append(list_html_data)
                    project_name = 0
                except UnicodeEncodeError:
                    print "error Unicode encode html !"
                pass
            pass
        table_html = HTML_table.table(list_commits)
        return self.html_lang + table_html
        pass