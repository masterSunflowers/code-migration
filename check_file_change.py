import pandas as pd
import subprocess
import os


repo_storage = "/drive1/phatnt/zTrans/data/repos"


def read_file_in_commit(repo_dir, rev_path, commit_hash):
    cmd = (
        f"git config --global --add safe.directory {repo_dir} && "
        f"cd {repo_dir} && "
        f"git show {commit_hash}:{rev_path}"
    )
    try:
        res = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return None
    return res.decode("utf-8")


def get_info_from_git_diff(repo_dir, commit1, commit2, file1, file2):
    cmd = (
        f"git config --global --add safe.directory {repo_dir} && "
        f"cd {repo_dir} && "
        f"git diff --name-status {commit1} {commit2}"
    )
    try:
        res = subprocess.check_output(cmd, shell=True)
        res = res.decode("utf-8").splitlines()
        for line in res:
            if line.startswith("R"):
                mode, old, new = line.split("\t")
                if old == file1 and new == file2:
                    similarity_index = int(mode[1:])
                    return similarity_index

        else:
            raise Exception("Something wrong")
    except subprocess.CalledProcessError as e:
        raise e


# ==============================================================================

df = pd.read_csv("data/migrations_36_file.csv")
num_has_java_diff_file = 0
num_has_modified_file = 0
num_java_file_added = 0
num_java_file_deleted = 0
num_java_file_modified = 0
num_java_file_renamed_modified = 0
num_java_file_renamed_unchanged = 0
for _, row in df.iterrows():
    added = eval(row["java_added"])
    deleted = eval(row["java_added"])
    modified = eval(row["java_modified"])
    renamed_modified = eval(row["java_renamed_modified"])
    renamed_unchanged = eval(row["java_renamed_unchanged"])
    if added or deleted or modified or renamed_modified or renamed_unchanged:
        num_has_java_diff_file += 1
    if modified or renamed_modified:
        num_has_modified_file += 1

    num_java_file_added += len(added)
    num_java_file_deleted += len(deleted)
    num_java_file_modified += len(modified)
    num_java_file_renamed_modified += len(renamed_modified)
    num_java_file_renamed_unchanged += len(renamed_unchanged)


print("Number of Java files added: ", num_java_file_added)
print("Number of Java files deleted: ", num_java_file_deleted)
print("Number of Java files modified: ", num_java_file_modified)
print("Number of Java files renamed and modified: ", num_java_file_renamed_modified)
print("Number of Java files renamed and unchanged: ", num_java_file_renamed_unchanged)

print("Number of commits that have Java file changes: ", num_has_java_diff_file)
print("Number of commits that have modified Java files: ", num_has_modified_file)

print(
    "Num diff java files: ",
    num_java_file_added
    + num_java_file_deleted
    + num_java_file_modified
    + num_java_file_renamed_unchanged
    + num_java_file_renamed_modified,
)
