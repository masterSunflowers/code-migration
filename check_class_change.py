import os

import pandas as pd
import json

df = pd.read_csv("processed3.csv")

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


path_to_parsed = "/drive2/phatnt/zTrans/thieulvd/final_parsed_tmp"
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
                        case "Unchanged":
                            num_unchanged_previous += 1
                        case "Renamed-Unchanged":
                            num_renamed_unchanged_previous += 1
                        case "Renamed-Modified":
                            num_renamed_modified_previous += 1
                
                for bclass in new_classes:
                    total_current += 1
                    match bclass["class_mode"]:
                        case "Added":
                            num_added += 1
                            print(row["repoName"])
                            print(old_file)
                            print(new_file)
                        case "Modified":
                            num_modified_current += 1
                        case "Unchanged":
                            num_unchanged_current += 1
                        case "Renamed-Unchanged":
                            num_renamed_unchanged_current += 1
                        case "Renamed-Modified":
                            num_renamed_modified_current += 1

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
                        