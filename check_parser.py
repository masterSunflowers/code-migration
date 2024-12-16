import subprocess
import os

folder1 = "/drive1/thieulvd/code-migration-tmp"
folder2 = "/drive1/thieulvd/code-migration-tmp2"

folder1_files = []
folder2_files = []


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


def read_file_in_checkout(repo_dir, rev_path, commit_hash):
    versions = list(filter(lambda folder: "ver" in folder), os.listdir(repo_dir))
    if commit_hash in versions[0]:
        file_path = os.path.join(repo_dir, versions[0], rev_path)
    else:
        file_path = os.path.join(repo_dir, versions[1], rev_path)
    
    with open(file_path, "r") as f:
        code = f.read()
    return code

# for root, dirs, files in os.walk(folder1):
#     for file in files:
#         folder1_files.append(os.path.join(root, file))
        
# for root, dirs, files in os.walk(folder2):
#     for file in files:
#         folder2_files.append(os.path.join(root, file))

# for file in folder1_files:
#     text1 = open(file, 'r').read()
#     text2 = open(file.replace("code-migration-tmp", "code-migration-tmp2"), 'r').read()
#     if text1 != text2:
#         print(file)

import pandas as pd

df = pd.read_csv("data/migrations_36_file.csv")

df = 
