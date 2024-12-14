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

df = pd.read_csv("data/sampled_50/tmp2.csv")
num_not_na = 0
num_has_java_diff_file = 0
num_has_modified_file = 0
num_java_diff_file = 0
num_java_file_added = 0
num_java_file_deleted = 0
num_java_file_modified = 0
num_java_file_renamed_modified = 0
num_java_file_renamed_unchanged = 0
for _, row in df.iterrows():
    diff_files = row["diff_files"]
    if pd.isna(diff_files):
        continue
    num_not_na += 1
    diff_files = eval(diff_files)
    if (
        diff_files["Added"]
        or diff_files["Deleted"]
        or diff_files["Modified"]
        or diff_files["Renamed-Modified"]
        or diff_files["Renamed-Unchanged"]
    ):
        num_has_java_diff_file += 1
        if diff_files["Modified"] or diff_files["Renamed-Modified"]:
            num_has_modified_file += 1

    num_java_file_added += len(diff_files["Added"])
    num_java_file_deleted += len(diff_files["Deleted"])
    num_java_file_modified += len(diff_files["Modified"])
    num_java_file_renamed_modified += len(diff_files["Renamed-Modified"])
    num_java_file_renamed_unchanged += len(diff_files["Renamed-Unchanged"])


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
