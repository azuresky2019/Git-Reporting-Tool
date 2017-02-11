import json
import csv
from utc_to_local import to_local


class CSV:
    def __init__(self):
        self.table_header = ["Project", "User", "Total files changed", "Total lines added", "Total lines deleted"]

    def get_report(self, report_csv_file_path, list_repo):
        total_repos = len(list_repo)
        with open(report_csv_file_path, 'wb') as report_csv_file:
            csv_file_writer = csv.DictWriter(report_csv_file, fieldnames=self.table_header)
            csv_file_writer.writeheader()

            for repo in range(0, total_repos):
                user_based_collection_file = 'output_jsons/' + list_repo[repo] + '-' + 'user_info.json'

                print "Collecting data from repo: \"%d.%s\"." % (repo + 1, list_repo[repo])

                csv_file_writer.writerow({
                    "Project": list_repo[repo]
                })
                with open(user_based_collection_file, 'rb') as users_details_file:
                    user_details_raw = json.load(users_details_file)
                    users_details_file.close()

                    total_users = len(user_details_raw)

                    for user in range(0, total_users):
                        csv_file_writer.writerow({
                            "User": user_details_raw[user]["user"],
                            "Total files changed": user_details_raw[user]["files_changed_total"],
                            "Total lines added": user_details_raw[user]["lines_added_total"],
                            "Total lines deleted": user_details_raw[user]["lines_deleted_total"],
                        })
                        pass

        report_csv_file.close()
        pass
