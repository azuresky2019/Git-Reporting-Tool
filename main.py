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

       # --------------------------------------

    # ----------- Temco Controls ---------------
    usr = "temcocontrols"
    client_id = ""
    client_secret = ""
    # -------------------------------------------

    append_credentials = '?client_id=' + client_id + '&client_secret=' + client_secret

    # --- Files details ----------
    report_html_file_name = 'report-summary' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".html"
    report_csv_file_name = 'report' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".csv"
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
    print "Searching for git repo on local computer. It may take a while."
    git_dirs = [root
                for root, dirs, files in os.walk("C:\\")
                for name in dirs
                if name.endswith(".git")]
    for dir in range(0, len(git_dirs)):
        print "%s" % git_dirs[dir]
        pass

    for index_repo in range(0, total_repos):
        for dir in range(0, len(git_dirs)):
            # print "%s" %list_repo[index_repo]
            if list_repo[index_repo] in git_dirs[dir]:
                print  "Found repo : %s at %s" % (list_repo[index_repo], git_dirs[dir])
                os.chdir(git_dirs[dir])
                print "Current working directory: %s" % os.getcwd()
                repo = git.Repo()
                for remote in repo.remotes:
                    print "Updating remote: \"%s\" from repository: \"%s\". Please wait..." % (
                        str(remote), list_repo[index_repo])
                    remote.pull()
                pass

''' -------------- Main function call : --------------- '''
if __name__ == '__main__':
    # main(sys.argv)
    main()
