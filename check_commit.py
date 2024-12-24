import os
import pandas as pd
import subprocess
from tqdm import tqdm


###############################################################################
# CHECK IF START AND END COMMIT STILL IN REPOSITORY, GET PREV COMMIT OF START COMMIT
###############################################################################
new_data = pd.read_csv("data/new_data.csv")
repo_storage = "/drive1/phatnt/zTrans/data/repos"
lst_start = []
lst_end = []
lst_prev_commit = []
for idx, row in tqdm(new_data.iterrows(), total=len(new_data), desc="Checking"):
    repo_dir = os.path.join(repo_storage, row["repo_name"])
    try:
        cmd = f"git config --global --add safe.directory {repo_dir} && cd {repo_dir} && git rev-parse {row['start_commit']}^"
        res = subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
        print(res)
        lst_prev_commit.append(res)
        start_flag = True
    except Exception:
        start_flag = False
        lst_prev_commit.append(None)
        print("Error")

    try:
        cmd = f"git config --global --add safe.directory {repo_dir} && cd {repo_dir} && git rev-parse {row['end_commit']}^"
        res = subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
        end_flag = True
        print(res)
    except Exception:
        end_flag = False
        print("Error")

    lst_start.append(start_flag)
    lst_end.append(end_flag)

new_data["start_commit_existed"] = lst_start
new_data["end_commit_exitsted"] = lst_end
new_data["oke"] = [start and end for start, end in zip(lst_start, lst_end)]
new_data["prev_commit"] = lst_prev_commit
new_data.to_csv("data/new_data_check.csv", index=False)
print(new_data["oke"].value_counts())


###############################################################################
# CHECK CASES START COMMIT IN REPOSITORY BUT END COMMIT NOT
###############################################################################
# new_data = pd.read_csv("new_data_check.csv")

# for idx, row in new_data[
#     (~new_data["prev_commit"].isna()) & (~new_data["oke"])
# ].iterrows():
#     print(row["repo_name"], row["start_commit"], row["end_commit"])


###############################################################################
# GET SAMPLE 36 MIGRATIONS TO BUILD PIPELINE
###############################################################################
# import pandas as pd

# new_data = pd.read_csv("data/new_data_check.csv")
# sampled_50 = pd.read_csv("data/sampled_50/tmp2.csv")

# lst_id = []
# for _, row in sampled_50.iterrows():
#     if not pd.isna(row["prev_commit"]):
#         lst_id.append(row["repoName"] + "__" + row["startCommit"] + "__" + row["endCommit"])
    
# migrations = new_data[new_data["id"].isin(lst_id)]
# migrations_36 = migrations.copy()
# migrations_36.reset_index(drop=True, inplace=True)
# migrations_36.to_csv("data/migrations_36.csv", index=False)
