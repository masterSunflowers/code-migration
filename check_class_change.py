import os

import pandas as pd
import json
import subprocess

df = pd.read_csv("data/sampled_50/tmp2.csv")
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


num_added = 0
num_deleted = 0
num_modified_previous = 0
num_modified_current = 0
num_renamed_modified_previous = 0
num_renamed_modified_current = 0
num_renamed_unchanged_previous = 0
num_renamed_unchanged_current = 0
num_unchanged_previous = 0
num_unchanged_current = 0
total_previous = 0
total_current = 0

lst_renamed_modified_previous = []
lst_renamed_modified_current = []


path_to_parsed = "/drive2/phatnt/zTrans/thieulvd/parsed-50"
for _, row in df.iterrows():
    if pd.isna(row["diff_files"]):
        continue
    diff_files = eval(row["diff_files"])
    for mode in diff_files:
        if mode in ["Modified", "Renamed-Modified"]:
            parsed_prev = os.path.join(
                path_to_parsed, row["repoName"] + "--" + row["prev_commit"]
            )
            parsed_cur = os.path.join(
                path_to_parsed, row["repoName"] + "--" + row["endCommit"]
            )
            for item in diff_files[mode]:
                if mode == "Modified":
                    old_file = new_file = item
                else:
                    old_file, new_file, _ = item

                parsed_old_file = old_file.replace("/", "--") + ".json"
                parsed_new_file = new_file.replace("/", "--") + ".json"
                with open(os.path.join(parsed_prev, parsed_old_file), "r") as f:
                    old_classes = json.load(f)
                with open(os.path.join(parsed_cur, parsed_new_file), "r") as f:
                    new_classes = json.load(f)

                for aclass in old_classes:
                    total_previous += 1
                    match aclass["class_mode"]:
                        case "Deleted":
                            num_deleted += 1
                        case "Modified":
                            num_modified_previous += 1
                            print(aclass["repo_name"])
                            print(aclass["rev_path"])
                            print(aclass["commit"])
                            print("=" * 100)
                        case "Unchanged":
                            num_unchanged_previous += 1
                        case "Renamed-Unchanged":
                            num_renamed_unchanged_previous += 1
                        case "Renamed-Modified":
                            num_renamed_modified_previous += 1
                            lst_renamed_modified_previous.append(aclass)

                for bclass in new_classes:
                    total_current += 1
                    match bclass["class_mode"]:
                        case "Added":
                            num_added += 1
                        case "Modified":
                            num_modified_current += 1
                            print(bclass["repo_name"])
                            print(bclass["rev_path"])
                            print(bclass["commit"])
                            print("=" * 100)
                        case "Unchanged":
                            num_unchanged_current += 1
                        case "Renamed-Unchanged":
                            num_renamed_unchanged_current += 1
                        case "Renamed-Modified":
                            num_renamed_modified_current += 1
                            lst_renamed_modified_current.append(bclass)

print("Total previous", total_previous)
print("Total current", total_current)
print("Deleted", num_deleted)
print("Added", num_added)
print("Modified previous", num_modified_previous)
print("Modified current", num_modified_current)
print("Unchanged previous", num_unchanged_previous)
print("Unchanged current", num_unchanged_current)
print("Renamed-Unchanged previous", num_renamed_unchanged_previous)
print("Renamed-Unchanged current", num_renamed_unchanged_current)
print("Renamed-Modified previous", num_renamed_modified_previous)
print("Renamed-Modified current", num_renamed_modified_current)

