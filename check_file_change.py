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

#==============================================================================

df = pd.read_csv(".csv")
num_repo_not_na = 0
num_repo_has_java_diff_file = 0
num_java_diff_files = 0
num_java_modify_files = 0
cnt = 0
for _, row in df.iterrows():
    diff_files = row["diff_files"]
    if pd.isna(diff_files):
        continue
    diff_files = eval(diff_files)
    if diff_files["Renamed-Modified"]:
        for old, new, similarity_index in diff_files["Renamed-Modified"]:
            if similarity_index < 80:
                with open("check.txt", "a") as f:
                    f.write(str(similarity_index) + '\n')
                    f.write(
                        read_file_in_commit(
                            os.path.join(repo_storage, row["repoName"]),
                            old,
                            row["prev_commit"],
                        )
                    )
                    f.write("\n============================================\n")
                    f.write(
                        read_file_in_commit(
                            os.path.join(repo_storage, row["repoName"]),
                            new,
                            row["endCommit"],
                        )
                    )
                    f.write("\n============================================")
                    f.write("\n============================================\n")


#==============================================================================

# repo_dir = "/drive1/phatnt/zTrans/data/repos/apache_dubbo-admin"
# prev_commit = "80013ffc38b3d737bd891a2b574ef75a93450bd9"
# cur_commit = "995e06b547cb7554c99deb3129fca19b2c35aa8b"

# old_file_path = "dubbo-admin-backend/src/main/java/org/apache/dubbo/admin/service/impl/OverrideServiceImpl.java"
# new_file_path = "dubbo-admin-backend/src/main/java/org/apache/dubbo/admin/service/impl/OverrideServiceImpl.java"

# print(read_file_in_commit(repo_dir, old_file_path, prev_commit))
# print("=" * 100)
# print(read_file_in_commit(repo_dir, new_file_path, cur_commit))