import git
from tinydb import TinyDB, Query
from pprint import pprint

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# database path
db = TinyDB('config/db.json')

class UpdateDb:
    def __init__(self, repo_path):

        self.repo_path = repo_path

        # Create the repository, raises an error if it isn't one.
        self.repo = git.Repo(self.repo_path)

        # Get all the commits
        try:
            self.commits_list = list(self.repo.iter_commits())
        except ValueError:
            print "Error finding commit from \'%s\' repository !" %(repo_path.split('\\')[-1])
            self.commits_list = []
            pass

        self.get_items = Query()

    def update_db(self):
        # ----------------- Insert all the commit information -------------
        for commit in self.commits_list:
            parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA

            # If the commit already available do not insert the data into the database
            if not db.search(self.get_items.commit == commit.hexsha):
                db.insert(self.get_commit_data(commit, parent))

            # print dir(commit)

    def get_commit_data(self, commit, parent):
        list_file_info = []
        diffs = {
            diff.a_path: diff for diff in commit.diff(parent)
        }

        for objpath, stats in commit.stats.files.items():

            # Select the diff for the path in the stats
            diff = diffs.get(objpath)

            # If the path is not in the dictionary, it's because it was
            # renamed, so search through the b_paths for the current name.
            if not diff:
                for diff in diffs.values():
                    if diff.b_path == self.repo_path and diff.renamed:
                        break
            # ----- Dict: Single file information ------
            dict_file_obj = {
                "file": objpath,
                "addition": stats["insertions"],
                "deletion": stats["deletions"],
                # "size": self.diff_size(diff),
                # "type": self.diff_type(diff),
            }
            list_file_info.append(dict_file_obj)
        # ----- Dict: Single commit information ------
        dict_commit_info = {
            "path": self.repo_path,
            "commit": commit.hexsha,
            "commiter": commit.committer.name,
            "author": commit.author.name,
            "email": commit.author.email,
            "message": commit.message,
            "date": commit.committed_date,
            # "date": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(commit.committed_date)),
            "files": list_file_info,
        }
        # # print dir(commit)
        # # print dir(commit.diff())
        # print commit.diff.count
        # pprint(commit, indent=4)

        del list_file_info
        ''' # Debug 
        print (json.dumps(dict_commit_info, indent=4))
        '''
        return dict_commit_info

    def diff_size(self, diff):
        """
        Computes the size of the diff by comparing the size of the blobs.
        """
        if diff.b_blob is None and diff.deleted_file:
            # This is a deletion, so return negative the size of the original.
            return diff.a_blob.size * -1

        if diff.a_blob is None and diff.new_file:
            # This is a new file, so return the size of the new value.
            return diff.b_blob.size

        # Otherwise just return the size a-b
        return diff.a_blob.size - diff.b_blob.size

    def diff_type(self, diff):
        """
        Determines the type of the diff by looking at the diff flags.
        """
        if diff.renamed: return 'R'  # Renamed
        if diff.deleted_file: return 'D'  # Deleted
        if diff.new_file: return 'A'  # Added
        return 'M'  # Modified
