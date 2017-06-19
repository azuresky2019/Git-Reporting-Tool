import time
import datetime
import glob
import git
from git_api_handler import handle_api_datas
from requests_handler import *
from email_handler import Email
from html_creator import *
from cm_handler import *
from csv_generator import CSV
from update_database import UpdateDb
from time_convert import TimeConvert
from tinydb import Query, TinyDB

db = TinyDB('config/db.json')

class BackendLocal:
    def __init__(self):
        # self.git_dirs = prj_dirs

        self.myQuery = Query()
        self.time_manlp = TimeConvert()
        self.report_csv_file_name = 'report' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".csv"
        self.report_html_file_name = "outputs/" + 'report-summary' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".html"
        self.report_csv_file_path = "outputs/" + self.report_csv_file_name

    def update_db(self, prjDir):

        for repos in prjDir:
            # --- Database being updated -----
            repo = UpdateDb(repos)
            print "Updating databse from : %s repository " % repos
            try:
                repo.update_db()
            except AttributeError:
                "Print error update to databse : %s" %repos
        print "finished updating !!"

    def get_user_list(self, pathPrj):

        queryData = db.search(self.myQuery.author.exists() & (self.myQuery.path == pathPrj))

        auth_details = []

        for auth in queryData:
            list_username = []
            list_username.append(auth["author"])
            if not auth["author"] == auth["commiter"]:
                list_username.append(auth["commiter"])
            dict_auth_detail = {
                "user": list_username,
                "email": auth["email"]
            }
            auth_details.append(dict_auth_detail)

        new_list_user = []
        for num, i in enumerate(auth_details):
            if i not in new_list_user:
                new_list_user.append(i)

        for dictionary in new_list_user:
            actual_email = dictionary.get('email')
            for dictionary_search in new_list_user:
                if dictionary != dictionary_search and actual_email == dictionary_search.get('email'):
                    users = dictionary_search.get('user')
                    for user in users:
                        dictionary.get('user', []).append(user)
                        try:
                            new_list_user.remove(dictionary_search)
                        except ValueError:
                            pass
        return new_list_user

    def get_user_based_info(self, contrib_involved, project_commits, days):

        project_commits_date_sorted = []

        for commit in project_commits:
            # print (type(x["date"]), x["date"])
            if self.time_manlp.get_days_back_from_today(commit["date"]) < days:
                project_commits_date_sorted.append(commit)

        del project_commits

        list_users = [None] * len(contrib_involved)

        # ---- Collect user info ---
        for user in range(0, len(contrib_involved)):
            dict_user_templ = {
                "user": contrib_involved[user]["user"][0],
                "email": contrib_involved[user]["email"],
                "lines_added_total": None,
                "lines_deleted_total": None,
                "files_changed_total": None,
                "commits": [None]
            }

            list_users[user] = dict_user_templ
            lines_added_accm = 0
            lines_deleted_accm = 0
            files_changed = 0
            list_commit = []
            try:
                for commit in range(0, len(project_commits_date_sorted)):  # contrib_involved
                    commit_lines_deleted = 0
                    commit_lines_added = 0
                    if list_users[user]["email"] == project_commits_date_sorted[commit]["email"]:
                        for files in project_commits_date_sorted[commit]["files"]:
                            commit_lines_deleted += int(files["deletion"])
                            commit_lines_added += int(files["addition"])

                        dict_commit_templ = {"sha": project_commits_date_sorted[commit]["commit"],
                                             "message": project_commits_date_sorted[commit]["message"],
                                             "date": self.time_manlp.time_stamp_to_human(
                                                 project_commits_date_sorted[commit]["date"]),
                                             "files_changed": len(project_commits_date_sorted[commit]["files"]),
                                             "lines_added": commit_lines_added,
                                             "lines_deleted": commit_lines_deleted,
                                             "total_changes": commit_lines_deleted + commit_lines_added
                                             }

                        no_of_flies_changed = len(project_commits_date_sorted[commit]["files"])
                        files_changed += no_of_flies_changed
                        pass
                        list_commit.append(dict_commit_templ)

                        lines_added_accm += commit_lines_added
                        lines_deleted_accm += commit_lines_deleted
                        pass

                del commit_lines_added, commit_lines_deleted

                list_users[user]["lines_added_total"] = lines_added_accm
                list_users[user]["lines_deleted_total"] = lines_deleted_accm
                list_users[user]["files_changed_total"] = files_changed
                list_users[user]["commits"] = list_commit

                del list_commit, files_changed, lines_added_accm, lines_deleted_accm
                pass
            except UnboundLocalError:
                pass
                # print "Found no commits within %d days for %s." %(days, contrib_involved[0]["user"][0])
        return list_users


class BackendGithub:

    def __init__(self, config_info):

        self.ui_file_raw = config_info

        # ----------- Github Credentials -------------------
        self.usr = self.ui_file_raw['user']
        self.client_id = self.ui_file_raw["id"]
        self.client_secret = self.ui_file_raw["secret"]
        # --------------------------------------------------

        self.append_credentials = '?client_id=' + self.client_id + '&client_secret=' + self.client_secret

        # --- Files details ----------
        self.report_html_file_name = 'report-summary' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".html"

        self.st_date_time = datetime.datetime.now()

        self.report_csv_file_name = 'report' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".csv"
        self.report_html_file_name = "outputs/" + self.report_html_file_name
        self.report_csv_file_path = "outputs/" + self.report_csv_file_name

        self.get_repos = "https://api.github.com/users/" + self.usr + "/repos" + self.append_credentials

    def del_old_files(self):
        # ----- delete the lastly collected un-wanted files ------ #
        os.chdir('output_jsons/')
        filelist = glob.glob("*.json")
        for f in filelist:
            os.remove(f)
            print "Deleted: %s" %f
        print "------ Deleted JSONs containing user information -------"
        # Change directory to normal
        os.chdir('..')

    def get_repo_list(self):
        user_repos = get_json_url(self.get_repos)
        self.total_repos = len(user_repos)
        self.list_repo = [None] * self.total_repos
        for repo in range(0, self.total_repos):
            self.list_repo[repo] = user_repos[repo]["name"]
            pass
        pass

    def accumulate_data(self):

        for repo in range(0, self.total_repos):
            print "Handling Project: '%d.%s'" % (repo + 1, self.list_repo[repo])
            handle_api_datas(self.usr, self.append_credentials, self.list_repo[repo])
            pass
        print "Done getting all the files."
            # TODO log and email notification on error

    def report_stuffs(self):
        try:
            # ------- CSV report handling --------
            print "Creating a CSV report."
            csv_file = CSV()
            csv_file.get_report(self.report_csv_file_path, self.list_repo)
            print "Finished generating a report."

            # --------- HTML Handling ------------ ##
            htm = HTML(days_back)
            print "Creating an HTML document."
            html_report = htm.encode_html(self.list_repo)
            print "Created an HTML document."

            # Write HTML to a file for test and debug purpose
            with open(self.report_html_file_name, "wb") as test_file:
                test_file.write(html_report)
                test_file.close()

            # --- Single file attachments ----
            attach_file = "outputs/" + self.report_csv_file_name
            print attach_file

            mail = Email()
            print "Sending email ..."
            mail.email_report(attach_file, html_report)
            print "Email sent."
        except:
            print "Sending email [error] ..."
            error_mail = Email()
            print "Email sent [error]."
            error_mail.error_email()
            # TODO maintain Log
            pass

def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

# ------- Main Function --------- #
def main():

    # ------------- Read config file -------------------
    try:
        with open('config/config.json', 'rb') as ui_file:
            ui_file_raw = json.load(ui_file)
            ui_file.close()
    except: # TODO maintain LOG
        pass
    global days_back
    days_back = ui_file_raw["history"]

    # ----------- If the repository is github type --------------------
    if ui_file_raw["repo_type_github"]:
        # --- The following method call should be in the same sequence
        gitRepo = BackendGithub(ui_file_raw)
        gitRepo.del_old_files()
        gitRepo.get_repo_list()
        gitRepo.accumulate_data()
        gitRepo.report_stuffs()

    # -------------- if the repository is local type --------------------
    else:

        # ------------- Read dir_files -------------------
        try:
            with open('config/dir_list.json', 'rb') as dir_file:
                raw_git_dirs = json.load(dir_file)
                dir_file.close()
        except:
            pass

        # ------------------------ Make Commits first ----------------------------
        for dires in raw_git_dirs:
            if not is_git_repo(dires):
                try:
                    git.Repo.init(dires, bare=False)
                    print "Initialized repository : \'%s\'" % dires
                except:
                    print "Couldn't initialize repository : \'%s\'" % dires
                pass
            repo = git.Repo(dires)
            index = repo.index
            flag_successful_index = False
            try:
                print "Indexing items from \'%s\' working directory !" % dires
                repo.git.add(A=True)
                # repo.git.add(u=True)
                flag_successful_index = True
            except:
                print "Error indexing : \'%s\'" % dires
                pass
            if flag_successful_index:
                try:
                    author = git.Actor('Temco Tech', 'tech_temco@outlook.com')
                    committer = git.Actor('Temco Tech', 'tech_temco@outlook.com')
                    # commit by commit message and author and committer
                    index.commit("Auto commit by git report tool", author=author, committer=committer)
                    print "Made commit on %s" % dires
                except:
                    print "Error commiting : %s" % dires
                    pass
            pass

        try:
            git_dirs = []
            for dirs in raw_git_dirs:
                if os.path.exists(dirs):
                    git_dirs.append(dirs)

            # --- Create a backend local object
            backEndHandle = BackendLocal()
            # --- update data to database
            backEndHandle.update_db(git_dirs)

            # ---- Get contributors involved in the project ---
            contrib_involved = []
            for path in git_dirs:
                contrib_involved.append(backEndHandle.get_user_list(path))

            # ------- create a query object -------
            myQuery = Query()

            # --- get the commits for the project
            list_project = []
            for num, path in enumerate(git_dirs):
                project_commits = db.search((myQuery.path == path))
                dict_prj_based_info = {
                    "project": path.split('\\')[-1],
                    "user_info": backEndHandle.get_user_based_info(contrib_involved[num], project_commits, days_back)
                }
                list_project.append(dict_prj_based_info)
            del contrib_involved

            # ---- CSV write information ----------
            my_csv_write = CSV()
            my_csv_write.get_report_local(backEndHandle.report_csv_file_path, list_project)

            # ----------------- HTML write operation -------------------
            htm = HTML(days_back)
            print "Creating an HTML document."
            html_report = htm.encode_html_local(list_project)
            print "Created an HTML document."

            # Write HTML to a file for test and debug purpose
            with open(backEndHandle.report_html_file_name, "wb") as test_file:
                test_file.write(html_report)
                test_file.close()

            mail = Email()
            print "Sending email ..."
            mail.email_report(backEndHandle.report_csv_file_path, html_report)
            print "Email sent."
        except:
            print "Sending email [error] ..."
            error_mail = Email()
            print "Email sent [error]."
            error_mail.error_email()
            # TODO maintain Log
            pass
    pass

''' -------------- Main function call : --------------- '''
if __name__ == '__main__':
    # main(sys.argv)
    main()
