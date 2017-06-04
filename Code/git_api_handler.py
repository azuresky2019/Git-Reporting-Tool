import json
from requests_handler import *
from time_convert import *

days_to_count = 7
grab_commits_qty = 15

time_stuff = TimeConvert()

def handle_api_datas(user_id, credentials, repo_name):
    all_commits_details_file = 'api_jsons/' + repo_name + '-' + 'all_commits_details.json'
    all_commits_details_file_sorted = 'api_jsons/' + repo_name + '-' + 'all_commits_sorted.json'
    user_based_collection_file = 'output_jsons/' + repo_name + '-' + 'user_info.json'

    # root URL
    api_url = "https://api.github.com/"
    # branch URL
    get_branch_info_url = api_url + "repos/" + user_id + "/" + repo_name + "/branches" + credentials
    # Commits ULR
    get_commit_info_url = api_url + "repos/" + user_id + "/" + repo_name + "/commits" + credentials
    # Contributors URL
    get_contributor_info_url = api_url + "repos/" + user_id + "/" + repo_name + "/contributors" + credentials

    branch_info = get_json_url(get_branch_info_url)  # Get information about all branches
    branches = len(branch_info)
    all_json = []

    # Manipulate individual branch and commits
    for branch in range(0, branches):
        # list_sha_branches.append(branch_info[branch]['commit']['sha'])
        # print '------------------------ BRANCH : %d ------------------------------' % branch
        # Pull 5 more commits from each branch
        get_more_commits_url = api_url + "repos/" + user_id + "/" + repo_name + "/commits?per_page=" + str(
            grab_commits_qty) + "&sha=" + branch_info[branch]['commit']['sha'] + '&' + credentials[1:len(credentials)]
        # print get_more_commits_url

        more_sha_json = get_json_url(get_more_commits_url)  # Collected more SHA Commits
        commits_per_branch = len(more_sha_json)
        # Grab each commits information
        for new_commit in range(0, commits_per_branch):
            # print '--------------------- COMMIT : %d -------------------------------' % new_commit

            single_commit_json_url = api_url + "repos/" + user_id + "/" + repo_name + "/commits/" \
                                     + more_sha_json[new_commit]['sha'] + credentials
            single_commit_json_deb = api_url + "repos/" + user_id + "/" + repo_name + "/commits/" \
                                     + more_sha_json[new_commit]['sha']
            # print single_commit_json_url
            print "Getting commit: \"%s\"" % more_sha_json[new_commit]["commit"]["message"]  # For debug purpose
            single_commit_info = get_json_url(single_commit_json_url)
            all_json.append(single_commit_info)  # append all JSONs into a list
        pass
    pass

    # Get information about contributors
    contributor_info = get_json_url(get_contributor_info_url)
    contrib_involved = len(contributor_info)
    dict_contrib_info = {}
    list_contrib_keys = ["user", "contributions"]
    list_contrib_vals = [None] * len(list_contrib_keys)  # Create a list to store values as per the keys
    list_all_contrib_info = []

    for contrib in range(0, contrib_involved):
        list_contrib_vals[0] = contributor_info[contrib]["login"]
        list_contrib_vals[1] = contributor_info[contrib]["contributions"]

        # Create a dictionary here :
        for contrib_key in range(0, len(list_contrib_keys)):
            dict_contrib_info[list_contrib_keys[contrib_key]] = list_contrib_vals[contrib_key]
        # append all dictionary to a list
        list_all_contrib_info.append(dict(dict_contrib_info))

    # ------------- Sort array here ---------------------
    total_commits = len(all_json)
    sorted_commits = []
    for i in range(0, contrib_involved):
        for j in range(0, total_commits):
            try:
                if all_json[j]["committer"]["login"] == list_all_contrib_info[i]["user"]:
                    sorted_commits.append(all_json[j])
            except TypeError:
                print 'Found invalid JSON data !'
                pass
            pass
        pass

    # ------------------- Filter by date --------------
    date_sorted_commits = []
    for commit in range(0, len(sorted_commits)):
        # print "Date : " + sorted_commits[commit]["commit"]["committer"]["date"]
        if time_stuff.compare_time(time_stuff.to_local_raw(sorted_commits[commit]["commit"]["committer"]["date"])) < days_to_count:
            date_sorted_commits.append(sorted_commits[commit])
            pass
        pass

    del sorted_commits
    sorted_commits = date_sorted_commits

    # with open("output_jsons/test_dump.json", 'wb') as filtered_one:
    #     json.dump(sorted_commits, filtered_one)
    #     filtered_one.close()

    list_users = [None] * contrib_involved

    # ---- Collect user info ---
    for user in range(0, contrib_involved):
        dict_user_templ = {
            "user": list_all_contrib_info[user]["user"],
            "contributions": list_all_contrib_info[user]["contributions"],
            "lines_added_total": None,
            "lines_deleted_total": None,
            "files_changed_total": None,
            "file_exceed": None,
            "commits": [None]
        }
        list_users[user] = dict_user_templ
        lines_added = 0
        lines_deleted = 0
        lines_added_accm = 0
        lines_deleted_accm = 0
        files_changed = 0
        list_commit = []
        for commit in range(0, len(sorted_commits)):  # contrib_involved
            if list_users[user]["user"] == sorted_commits[commit]["committer"]["login"]:
                dict_commit_templ = {"sha": sorted_commits[commit]["sha"],
                                     "message": sorted_commits[commit]["commit"]["message"],
                                     "date": sorted_commits[commit]["commit"]["committer"]["date"],
                                     "files_changed": len(sorted_commits[commit]["files"]),
                                     "lines_added": sorted_commits[commit]["stats"]["additions"],
                                     "lines_deleted": sorted_commits[commit]["stats"]["deletions"],
                                     "total_changes": sorted_commits[commit]["stats"]["total"], "files": [None]}

                no_of_flies_changed = len(sorted_commits[commit]["files"])
                files_changed += no_of_flies_changed
                list_changed_files = []
                for file in range(0, no_of_flies_changed):
                    lines_added_accm += int(sorted_commits[commit]["files"][file]["additions"])
                    lines_deleted_accm += int(sorted_commits[commit]["files"][file]["deletions"])
                    dict_file_templ = {
                        "file_name": sorted_commits[commit]["files"][file]["filename"],
                        "status": sorted_commits[commit]["files"][file]["status"],
                        "lines_added": sorted_commits[commit]["files"][file]["additions"],
                        "lines_deleted": sorted_commits[commit]["files"][file]["deletions"],
                        "total_changes": sorted_commits[commit]["files"][file]["changes"]
                    }
                    list_changed_files.append(dict_file_templ)
                pass
                dict_commit_templ["files"] = list_changed_files
                del list_changed_files
                list_commit.append(dict_commit_templ)

                lines_added += int(sorted_commits[commit]["stats"]["additions"])
                lines_deleted += int(sorted_commits[commit]["stats"]["deletions"])
                pass

        list_users[user]["lines_added_total"] = lines_added
        list_users[user]["lines_deleted_total"] = lines_deleted
        list_users[user]["files_changed_total"] = files_changed
        list_users[user]["commits"] = list_commit

        # ---- Identify whether changed files are only 300 or more
        if (lines_added_accm > lines_added or lines_added_accm > lines_deleted) and (files_changed >= 300):
            list_users[user]["file_exceed"] = True
        else:
            list_users[user]["file_exceed"] = False
            pass
        del list_commit, lines_added, lines_deleted, files_changed, lines_added_accm, lines_deleted_accm
        pass
    pass
    del sorted_commits

    with open(user_based_collection_file, 'wb') as all_users_file:
        json.dump(list_users, all_users_file)
        all_users_file.close()
