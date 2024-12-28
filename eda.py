import pandas as pd
import numpy as np
import json
import os
from tqdm import tqdm
df = pd.read_csv("data/final_total.csv")


# # How many files changed between two version
# lst_num_changed_files = []
# for i in tqdm(range(len(df)), total=len(df), desc="Statistic file"):
#     num_changed_files = []
#     for col in [
#         "java_added",
#         "java_deleted",
#         "java_modified",
#         "java_renamed_unchanged",
#         "java_renamed_modified",
#     ]:
#         num_changed_files.append(len(eval(df.loc[i, col])))
#     lst_num_changed_files.append(num_changed_files)

# cnt = 0
# for num_changed_files in lst_num_changed_files:
#     for i in range(5):
#         if num_changed_files[i] != 0:
#             break
#     else:
#         cnt += 1
# print("Num migration with no java file changed:", cnt)

# total_file_changes = sum([sum(x) for x in lst_num_changed_files])


# added, deleted, modified, renamed_unchanged, renamed_modified = np.array(
#     lst_num_changed_files
# ).sum(axis=0)
# print(
#     "{:<36} {:>8} ~ {:.2f}%".format(
#         "Num java file added:", added, added / total_file_changes * 100
#     )
# )
# print(
#     "{:<36} {:>8} ~ {:.2f}%".format(
#         "Num java file deleted:", deleted, deleted / total_file_changes * 100
#     )
# )
# print(
#     "{:<36} {:>8} ~ {:.2f}%".format(
#         "Num java file modified:", modified, modified / total_file_changes * 100
#     )
# )
# print(
#     "{:<36} {:>8} ~ {:.2f}%".format(
#         "Num java file renamed_unchanged:",
#         renamed_unchanged,
#         renamed_unchanged / total_file_changes * 100,
#     )
# )

# print("=" * 100)
# print("++++++++++STATISTIC++++++++++")


statistic_parsed1 = []
statistic_parsed2 = []
data_storage = "/drive1/thieulvd/code-migration-total"
migrations = list(df["id"])
for migration in tqdm(migrations, total=len(migrations), desc="Statistic class"):
    level1_parsed1_info = {}
    level1_parsed2_info = {}

    folder = os.path.join(data_storage, migration)
    for x in os.listdir(folder):
        if x.startswith("parsed1"):
            parsed1 = os.path.join(folder, x)
            flag = True
        elif x.startswith("parsed2"):
            parsed2 = os.path.join(folder, x)
            flag = True
        else:
            continue
    for file in os.listdir(parsed1):
        with open(os.path.join(parsed1, file), "r") as f:
            lst = json.load(f)
        for item in lst:
            level1_parsed1_info[item["class_mode"]] = (
                level1_parsed1_info.get(item["class_mode"], 0) + 1
            )
    for file in os.listdir(parsed2):
        with open(os.path.join(parsed2, file), "r") as f:
            lst = json.load(f)
        for item in lst:
            level1_parsed2_info[item["class_mode"]] = (
                level1_parsed2_info.get(item["class_mode"], 0) + 1
            )
    statistic_parsed1.append(level1_parsed1_info)
    statistic_parsed2.append(level1_parsed2_info)


class_parsed1 = pd.DataFrame(
    statistic_parsed1,
    columns=[
        "Modified",
        "Renamed-Modified",
        "Added",
        "Deleted",
        "Unchanged",
        "Renamed-Unchanged",
    ],
)
for col in class_parsed1:
    total = 0
    print(col)
    for x in class_parsed1[col]:
        if not pd.isna(x):
            total += x
    print(total)
    print("=" * 100)

class_parsed2 = pd.DataFrame(
    statistic_parsed2,
    columns=[
        "Modified",
        "Renamed-Modified",
        "Added",
        "Deleted",
        "Unchanged",
        "Renamed-Unchanged",
    ],
)
for col in class_parsed2:
    total = 0
    print(col)
    for x in class_parsed2[col]:
        if not pd.isna(x):
            total += x
    print(total)
    print("=" * 100)
    
    
statistic_parsed1 = []
statistic_parsed2 = []
method_modified_pairs = []
method_added = []
method_deleted = []
for migration in tqdm(migrations, total=len(migrations), desc="Statistic method"):
    level2_parsed1_info = {}
    level2_parsed2_info = {}
    folder = os.path.join(data_storage, migration)
    for x in os.listdir(folder):
        if x.startswith("parsed1"):
            parsed1 = os.path.join(folder, x)
        elif x.startswith("parsed2"):
            parsed2 = os.path.join(folder, x)
        else:
            continue
    # print("Parse version 1 directory:", parsed1)
    # print("Parse version 2 directory:", parsed2)
    # print("=" * 100)
    # print("Num diff file version 1:", len(os.listdir(parsed1)))
    # print("Num diff file version 2:", len(os.listdir(parsed2)))
    # print("=" * 100)
    cnt_methods = 0
    cnt_classes = 0
    ver1_method_modes = {}
    ver1_class_modes = {}
    for ver1_file_name in os.listdir(parsed1):
        ver1_file_path = os.path.join(parsed1, ver1_file_name)
        with open(ver1_file_path, "r") as f:
            ver1_classes = json.load(f)
        cnt_classes += len(ver1_classes)
        for ver1_class in ver1_classes:
            ver1_class_modes[ver1_class["class_mode"]] = (
                ver1_class_modes.get(ver1_class["class_mode"], 0) + 1
            )
            for method in ver1_class["methods"]:
                cnt_methods += 1
                ver1_method_modes[method["method_mode"]] = (
                    ver1_method_modes.get(method["method_mode"], 0) + 1
                )
    # print("Total classes in version 1:", cnt_classes)
    # print("Class mode info of version 1:", ver1_class_modes)
    # print("Total methods in version 1:", cnt_methods)
    # print("Method mode info of version 1:", ver1_method_modes)
    cnt_classes = 0
    cnt_methods = 0
    ver2_method_modes = {}
    ver2_class_modes = {}
    for ver2_file_name in os.listdir(parsed2):
        ver2_file_path = os.path.join(parsed2, ver2_file_name)
        with open(ver2_file_path, "r") as f:
            ver2_classes = json.load(f)
        cnt_classes += len(ver2_classes)
        for ver2_class in ver2_classes:
            ver2_class_modes[ver2_class["class_mode"]] = (
                ver2_class_modes.get(ver2_class["class_mode"], 0) + 1
            )
            for ver2_method in ver2_class["methods"]:
                cnt_methods += 1
                ver2_method_modes[ver2_method["method_mode"]] = (
                    ver2_method_modes.get(ver2_method["method_mode"], 0) + 1
                )
    # print("Total classes in version 2:", cnt_classes)
    # print("Class mode info of version 2:", ver2_class_modes)
    # print("Total methods in version 2:", cnt_methods)
    # print("Method mode info of version 2:", ver2_method_modes)
    # print("=" * 100)
    # print("=" * 100)
    statistic_parsed1.append(ver1_method_modes)
    statistic_parsed2.append(ver2_method_modes)

method_parsed1 = pd.DataFrame(
    statistic_parsed1,
    columns=[
        "Modified",
        "Renamed-Modified",
        "Added",
        "Deleted",
        "Unchanged",
        "Renamed-Unchanged",
    ],
)
for col in method_parsed1:
    total = 0
    print(col)
    for x in method_parsed1[col]:
        if not pd.isna(x):
            total += x
    print(total)
    print("=" * 100)

method_parsed2 = pd.DataFrame(
    statistic_parsed2,
    columns=[
        "Modified",
        "Renamed-Modified",
        "Added",
        "Deleted",
        "Unchanged",
        "Renamed-Unchanged",
    ],
)
for col in method_parsed2:
    total = 0
    print(col)
    for x in method_parsed2[col]:
        if not pd.isna(x):
            total += x
    print(total)
    print("=" * 100)


data_storage = "/drive1/thieulvd/code-migration-total"
method_modified_pairs = []
method_added = []
method_deleted = []
num_modified_method = 0
for migration in tqdm(migrations, total=len(migrations), desc="Pairing method"):
    folder = os.path.join(data_storage, migration)
    for x in os.listdir(folder):
        if x.startswith("parsed1"):
            parsed1 = os.path.join(folder, x)
        elif x.startswith("parsed2"):
            parsed2 = os.path.join(folder, x)
        else:
            continue
    for ver1_file_name in os.listdir(parsed1):
        ver1_file_path = os.path.join(parsed1, ver1_file_name)
        with open(ver1_file_path, 'r') as f:
            ver1_classes = json.load(f)
        for ver1_class in ver1_classes:
            for ver1_method in ver1_class["methods"]:
                if ver1_method["method_mode"] in ["Modified", "Renamed-Modified"]:
                    num_modified_method += 1
                    ver2_file_name = ver1_class["ver2_path"].replace("/", "--") + ".json"
                    ver2_file_path = os.path.join(parsed2, ver2_file_name)
                    with open(ver2_file_path, 'r') as f:
                        ver2_classes = json.load(f)
                    for ver2_class in ver2_classes:
                        if ver1_class["ver2_tree_path"] == ver2_class["ver2_tree_path"]:
                            for ver2_method in ver2_class["methods"]:
                                if ver1_method["ver2_signature"] == ver2_method["ver2_signature"]:
                                    record = {
                                        "migration_id": migration,
                                        "ver1_file_path": ver1_class["ver1_path"],
                                        "ver2_file_path": ver1_class["ver2_path"],
                                        "ver1_tree_path": ver1_class["ver1_tree_path"],
                                        "ver2_tree_path": ver1_class["ver2_tree_path"],
                                        "ver1_signature": ver1_method["ver1_signature"],
                                        "ver2_signature": ver1_method["ver2_signature"],
                                        "method_ver1": ver1_method["definition"],
                                        "method_ver2": ver2_method["definition"]
                                    }
                                    method_modified_pairs.append(record)
                elif ver1_method["method_mode"] == "Deleted":
                    record = {
                        "migration_id": migration,
                        "ver1_file_path": ver1_class["ver1_path"],
                        "ver1_tree_path": ver1_class["ver1_tree_path"],
                        "ver1_signature": ver1_method["ver1_signature"],
                        "method_ver1": ver1_method["definition"]
                    }
                    method_deleted.append(record)
   
    for ver2_file_name in os.listdir(parsed2):
        ver2_file_path = os.path.join(parsed2, ver2_file_name)
        with open(ver2_file_path, 'r') as f:
            ver2_classes = json.load(f)
        for ver2_class in ver2_classes:
            for ver2_method in ver2_class["methods"]:
                if ver2_method["method_mode"] == "Added":
                    record = {
                        "migration_id": migration,
                        "ver2_file_path": ver2_class["ver2_path"],
                        "ver2_tree_path": ver2_class["ver2_tree_path"],
                        "ver2_signature": ver2_method["ver2_signature"],
                        "method_ver2": ver2_method["definition"]
                    }   
                    method_added.append(record)
                    
print(num_modified_method)
print(len(method_modified_pairs))
print(len(method_added))
print(len(method_deleted))
method_modified = pd.DataFrame(method_modified_pairs)
method_added = pd.DataFrame(method_added)
method_deleted = pd.DataFrame(method_deleted)
method_modified.to_csv("data/method_modified.csv")
method_added.to_csv("data/method_added.csv")
method_deleted.to_csv("data/method_deleted.csv")