# import sys
import time
import os
import glob
from git_api_handler import handle_api_datas
from requests_handler import *
from email_handler import Email
from html_creator import *
from csv_generator import CSV
import git


# ------- Main Function --------- #
def main():
    # usr = argv[1]
    # client_id = argv[2]
    # client_secret = argv[3]

    # ------ My git secrets ------------
    usr = "lomassubedi"
    client_id = "b6d44a3c6be9d41d5a84"
    client_secret = "9c54db3cbcc716e9991b696782aae8b715d49e1c"
    # --------------------------------------

    # ----------- Temco Controls ---------------
    # usr = "temcocontrols"
    # client_id = "f648725de5a50e0b04f0"
    # client_secret = "350ef686de82c4a8da4fac161cc1f333820e4b4d"
    # -------------------------------------------

    append_credentials = '?client_id=' + client_id + '&client_secret=' + client_secret

    # --- Files details ----------
    report_html_file_name = 'report-summary' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".html"
    report_csv_file_name = 'report' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".csv"
    dir_scan_flag = 'config/dir_scan_flag.json'
    dir_list = 'config/dir_list.json'
    report_html_file_name = "outputs/" + report_html_file_name
    report_csv_file_path = "outputs/" + report_csv_file_name

    # ----- delete the lastly collected un-wanted files ------ #
    os.chdir('output_jsons/')
    filelist = glob.glob("*.json")
    for f in filelist:
        os.remove(f)
        print "Deleted: %s" %f
    print "------ Deleted JSONs containing user information -------"
    # Change directory to normal
    os.chdir('..')

    get_repos = "https://api.github.com/users/" + usr + "/repos" + append_credentials

    user_repos = get_json_url(get_repos)
    total_repos = len(user_repos)
    list_repo = [None] * total_repos
    for repo in range(0, total_repos):
        list_repo[repo] = user_repos[repo]["name"]
        pass

    for repo in range(0, total_repos):
        print "Handling Project: '%d.%s'" % (repo + 1, list_repo[repo])
        handle_api_datas(usr, append_credentials, list_repo[repo])
        pass
    print "Done getting all the files."

    # ------- CSV report handling --------
    print "Creating a CSV report."
    csv_file = CSV()
    csv_report = csv_file.get_report(report_csv_file_path, list_repo)
    print "Finished generating a report."

    # --------- HTML Handling ------------ ##
    htm = HTML()
    print "Creating an HTML document."
    html_report = htm.encode_html(list_repo)
    print "Created an HTML document."

    # Write HTML to a file for test and debug purpose
    with open(report_html_file_name, "wb") as test_file:
        test_file.write(html_report)
        test_file.close()

    # --------- Email Handling ------------
    mail = Email()
    print "Sending email ..."
    mail.email_report(report_csv_file_path, report_csv_file_name, html_report)
    print "Email sent."

    # update to local repo
    # --- Find local repository -----------
    # --- Save searched locations ---------
    try:
        with open(dir_scan_flag, 'rb') as dir_scan_flag_file:
            json.load(dir_scan_flag_file)
            dir_scan_flag_file.close()

    except IOError:
        dict_user_templ = {
            "dir_scan_state":False,
        }
        with open(dir_scan_flag, 'wb') as dir_scan_flag_file:
            json.dump(dict_user_templ, dir_scan_flag_file)
            dir_scan_flag_file.close()

        print "Searching for git repo on local computer. It may take a while."
        git_dirs = [root
                    for root, dirs, files in os.walk("G:\\TEMCO\\git_test\\")  # change path here
                    for name in dirs
                    if name.endswith(".git")]

        list_monitor_repo = []

        for ind_repo_dir in range(0, len(git_dirs)):
            user_input = raw_input(
                "\nDo you want to add repo at \"%s\" on monitor ? [Y or N]:" % str(git_dirs[ind_repo_dir]))
            if "Y" in user_input or "y" in user_input:
                list_monitor_repo.append(git_dirs[ind_repo_dir])
            else:
                print "Ignored repo at \"%s\" !\n" % str(git_dirs[ind_repo_dir])
                pass
            pass
        with open(dir_list, 'wb') as dir_list_file:
            json.dump(list_monitor_repo, dir_list_file)
            dir_list_file.close()
        del list_monitor_repo
        pass

    with open(dir_list, 'rb') as dir_list_file:
        raw_dir_list = json.load(dir_list_file)
        dir_list_file.close()

    for dir_ind in range(0, len(raw_dir_list)):
        os.chdir(raw_dir_list[dir_ind])
        print "Current working directory: %s" % os.getcwd()
        repo = git.Repo()
        for remote in repo.remotes:
            print "Updating remote: \"%s\" from repository: \"%s\". Please wait..." % (
                str(remote), raw_dir_list[dir_ind])
            try:
                remote.pull()
            except:
                print "Update to local repo was unsuccessful!"
                pass
            pass
        pass

''' -------------- Main function call : --------------- '''
if __name__ == '__main__':
    # main(sys.argv)
    main()
