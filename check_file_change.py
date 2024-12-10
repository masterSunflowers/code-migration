import pandas as pd
import subprocess
import os


repo_storage = "/drive1/phatnt/zTrans/data/repos"


# df = pd.read_csv("processed2.csv")
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


# def get_info_from_git_diff(repo_dir, commit1, commit2, file1, file2):

#     cmd = (
#         f"git config --global --add safe.directory {repo_dir} && "
#         f"cd {repo_dir} && "
#         f"git diff --name-status {commit1} {commit2}"
#     )
#     try:
#         res = subprocess.check_output(cmd, shell=True)
#         res = res.decode("utf-8").splitlines()
#         for line in res:
#             if line.startswith("R"):
#                 mode, old, new = line.split("\t")
#                 if old == file1 and new == file2:
#                     similarity_index = int(mode[1:])
#                     return similarity_index

#         else:
#             raise Exception("Something wrong")
#             return -1
#     except subprocess.CalledProcessError as e:
#         raise e


# cnt = 0
# cnt_identical = 0
# for _, row in df.iterrows():
#     diff_files = row["diff_files"]
#     if pd.isna(diff_files):
#         continue
#     diff_files = eval(diff_files)
#     if diff_files["Renamed"]:
#         for old, new in diff_files["Renamed"]:
#             cnt += 1
#             output_of_git_diff = get_info_from_git_diff(
#                 os.path.join(repo_storage, row["repoName"]),
#                 row["prev_commit"],
#                 row["endCommit"],
#                 old,
#                 new
#             )
#             if output_of_git_diff == 100:
#                 cnt_identical += 1
#             # previous = read_file_in_commit(os.path.join(repo_storage, row["repoName"]), old, row["prev_commit"])
#             # current = read_file_in_commit(os.path.join(repo_storage, row["repoName"]), new, row["endCommit"])
#             # if previous == current:
#             #     cnt_identical += 1

# print("Number of pair:", cnt)
# print("Only rename not change content", cnt_identical)


# df = pd.read_csv("processed3.csv")

# cnt = 0
# for _, row in df.iterrows():
#     diff_files = row["diff_files"]
#     if pd.isna(diff_files):
#         continue
#     diff_files = eval(diff_files)
#     if diff_files["Renamed-Modified"]:
#         for old, new, similarity_index in diff_files["Renamed-Modified"]:
#             if similarity_index < 80:
#                 with open("check.txt", "a") as f:
#                     f.write(str(similarity_index) + '\n')
#                     f.write(
#                         read_file_in_commit(
#                             os.path.join(repo_storage, row["repoName"]),
#                             old,
#                             row["prev_commit"],
#                         )
#                     )
#                     f.write("\n============================================\n")
#                     f.write(
#                         read_file_in_commit(
#                             os.path.join(repo_storage, row["repoName"]),
#                             new,
#                             row["endCommit"],
#                         )
#                     )
#                     f.write("\n============================================")
#                     f.write("\n============================================\n")

repo_dir = "/drive1/phatnt/zTrans/data/repos/EmiteGWT_emite"
prev_commit = "e0a9748a236d3166b661253b60f6b5c7f00dc9e9"
cur_commit = "6bce09ae519ce35bf592b75b110323292b01deef"

old_file_path = "src/main/java/com/calclab/emite/core/client/packet/PacketTestSuite.java"
new_file_path = "src/test/java/com/calclab/emite/core/client/packet/PacketTestSuite.java"

print(read_file_in_commit(repo_dir, old_file_path, prev_commit))
print("=" * 100)
print(read_file_in_commit(repo_dir, new_file_path, cur_commit))