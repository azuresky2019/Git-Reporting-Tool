import time
import datetime
import glob
from git_api_handler import handle_api_datas
from requests_handler import *
from email_handler import Email
from html_creator import *
from cm_handler import *
from csv_generator import CSV

# ------- Main Function --------- #
def main():
    # usr = argv[1]
    # client_id = argv[2]
    # client_secret = argv[3]

    with open('config/user_infoUI.json', 'rb') as ui_file:
        ui_file_raw = json.load(ui_file)
        ui_file.close()

    # ----------- Temco Controls ---------------
    usr = ui_file_raw['username']
    client_id = ui_file_raw["client_id"]
    client_secret = ui_file_raw["client_secret"]
    # -------------------------------------------

    append_credentials = '?client_id=' + client_id + '&client_secret=' + client_secret

    # --- Files details ----------
    report_html_file_name = 'report-summary' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".html"

    st_date_time = datetime.datetime.now()

    report_csv_file_name = 'report' + time.strftime("--D%d-%m-%yT%H_%M_%S") + ".csv"
    report_html_file_name = "outputs/" + report_html_file_name
    report_csv_file_path = "outputs/" + report_csv_file_name

    #----- delete the lastly collected un-wanted files ------ #
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

    # ---- Create Source Monitor Report ----
    get_command_xml = MakeXMLSM(st_date_time)
    get_command_xml.set_command_xml()
    get_command_xml.gen_sm_report()

    # --------- Email Handling ------------
    attach_files = [None] * 3
    attach_files[0] = report_csv_file_name

    print attach_files[0]

    attach_files[1] = "Kiviat for ChkPoint_" + str(st_date_time.date().year) + "_" \
                      + str(st_date_time.date().month).zfill(2) + "_" + str(st_date_time.date().day).zfill(2) + "T" \
                      + str(st_date_time.time().hour) + "_" + str(st_date_time.time().minute) + "_" \
                      + str(st_date_time.time().second) + ".bmp"
    print  attach_files[1]

    attach_files[2] = "sm_report_" + str(st_date_time.date()) + "T" + str(st_date_time.time().hour) + "_" \
                      + str(st_date_time.time().minute) + "_" + str(st_date_time.time().second) + ".csv"

    print attach_files[2]
    mail = Email()
    print "Sending email ..."
    mail.email_report(attach_files, html_report)
    print "Email sent."

    # update to local repo
    # ---- Read list of backup repos from the stored repo list
    with open('config/dir_list.json', 'rb') as dir_file:
        git_dirs = json.load(dir_file)
        dir_file.close()

    for index_repo in range(0, total_repos):
        for dir in range(0, len(git_dirs)):
            # print "%s" %list_repo[index_repo]
            if list_repo[index_repo] in git_dirs[dir]:
                os.chdir(git_dirs[dir])
                print "Current working directory: %s" % os.getcwd()
                print "Updating repository: \"%s\". Please wait..." % (list_repo[index_repo])
                os.system("git pull origin master")
                pass


''' -------------- Main function call : --------------- '''
if __name__ == '__main__':
    # main(sys.argv)
    main()
