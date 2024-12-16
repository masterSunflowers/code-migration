import subprocess
import os
import pandas as pd
from tqdm import tqdm


def read_file_in_commit(repo_storage, id, rev_path, commit_hash):
    repo_name = id.split("__")[0]
    repo_dir = os.path.join(repo_storage, repo_name)
    cmd = (
        f"git config --global --add safe.directory {repo_dir} && "
        f"cd {repo_dir} && "
        f"git cat-file -p {commit_hash}:{rev_path}"
    )
    try:
        res = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        return None
    return res.decode("utf-8")


def read_file_in_checkout(data_storage, id, rev_path, commit_hash):
    repo_dir = os.path.join(data_storage, id)
    versions = list(filter(lambda folder: "ver" in folder, os.listdir(repo_dir)))
    if commit_hash in versions[0]:
        file_path = os.path.join(repo_dir, versions[0], rev_path)
    else:
        file_path = os.path.join(repo_dir, versions[1], rev_path)

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    return code

def check_diff(code1, code2):
    return code1.replace("\r\n", "\n") != code2.replace("\r\n", "\n")

def check_data_builder():
    repo_storage = "/drive1/phatnt/zTrans/data/repos"
    data_storage = "/drive1/thieulvd/code-migration"
    df = pd.read_csv("/drive2/phatnt/zTrans/thieulvd/data/migrations_36_file.csv")
    cnt_diff = 0
    for index, row in tqdm(df.iterrows(), total=len(df)):
        id = row["id"]
        prev_commit = row["prev_commit"]
        end_commit = row["end_commit"]
        added = row["added"]
        deleted = row["deleted"]
        modified = row["modified"]
        renamed_unchanged = row["renamed_unchanged"]
        renamed_modified = row["renamed_modified"]
        for file in eval(modified):
            if file.endswith(".java"):
                code1 = read_file_in_commit(repo_storage, id, file, prev_commit)
                code2 = read_file_in_checkout(data_storage, id, file, prev_commit)
                cnt_diff += check_diff(code1, code2)
                code1 = read_file_in_commit(repo_storage, id, file, end_commit)
                code2 = read_file_in_checkout(data_storage, id, file, end_commit)
                cnt_diff += check_diff(code1, code2)
                print(cnt_diff)
                        
        for file in eval(added):
            if file.endswith(".java"):
                code1 = read_file_in_commit(repo_storage, id, file, end_commit)
                code2 = read_file_in_checkout(data_storage, id, file, end_commit)
                cnt_diff += check_diff(code1, code2)
                print(cnt_diff)
        
        for file in eval(deleted):
            if file.endswith(".java"):
                code1 = read_file_in_commit(repo_storage, id, file, prev_commit)
                code2 = read_file_in_checkout(data_storage, id, file, prev_commit)
                cnt_diff += check_diff(code1, code2)
                print(cnt_diff)
        
        for item in eval(renamed_modified):
            file1, file2, _ = item.values()
            if file1.endswith(".java"):
                code1 = read_file_in_commit(repo_storage, id, file1, prev_commit)
                code2 = read_file_in_checkout(data_storage, id, file1, prev_commit)
                cnt_diff += check_diff(code1, code2)
                print(cnt_diff)
            if file2.endswith(".java"):
                code1 = read_file_in_commit(repo_storage, id, file2, end_commit)
                code2 = read_file_in_checkout(data_storage, id, file2, end_commit)
                cnt_diff += check_diff(code1, code2)
                print(cnt_diff)
        
        for item in eval(renamed_unchanged):
            file1, file2 = item.values()
            if file1.endswith(".java"):
                code1 = read_file_in_commit(repo_storage, id, file1, prev_commit)
                code2 = read_file_in_checkout(data_storage, id, file1, prev_commit)
                cnt_diff += check_diff(code1, code2)
                print(cnt_diff)
            if file2.endswith(".java"):
                code1 = read_file_in_commit(repo_storage, id, file2, end_commit)
                code2 = read_file_in_checkout(data_storage, id, file2, end_commit)
                cnt_diff += check_diff(code1, code2)
                print(cnt_diff)
    return cnt_diff


print(check_data_builder())
