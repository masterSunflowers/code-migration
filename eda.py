import pandas as pd
import os
import json

processed2 = pd.read_csv("thieulvd/processed2.csv")


for i in range(len(processed2)):
    print(
        eval(processed2.loc[i, "diff_files"])
        if not pd.isna(processed2.loc[i, "diff_files"])
        else None
    )
    print("=" * 100)


# # parsed_dir = "thieulvd/parsed"

# # prev_method_count = 0
# # cur_method_count = 0

# # for _, row in processed2.iterrows():
# #     if (
# #         not pd.isna(row["java_only_diff_files"])
# #         and row["java_only_diff_files"] != ""
# #     ):
# #         prev_identifier = row["repoName"] + "--" + row["prev_commit"]
# #         cur_identifier = row["repoName"] + "--" + row["startCommit"]
# #         methods_prev_commit = json.load(
# #             open(os.path.join(parsed_dir, prev_identifier, "method_info.json"))
# #         )
# #         methods_cur_commit = json.load(
# #             open(os.path.join(parsed_dir, cur_identifier, "method_info.json"))
# #         )
# #         prev_method_count += len(methods_prev_commit)
# #         cur_method_count += len(methods_cur_commit)

# # print(prev_method_count)
# # print(cur_method_count)

# df = pd.read_json("thieulvd/changed_methods.jsonl", lines=True)
# print(df.info())
# print(df.head())
# print(df.describe())
# print(df["repoName"].value_counts())
# print(df["repoName"].value_counts().describe())


# df_simplified = df.copy()
# df_simplified["file_path"] = df["prev_method"].apply(lambda x: x["file_path"])
# df_simplified["tree_path"] = df["prev_method"].apply(lambda x: x["tree_path"])
# df_simplified["prev_method"] = df["prev_method"].apply(lambda x: x["definition"])
# df_simplified["cur_method"] = df["cur_method"].apply(lambda x: x["definition"])
# df_simplified.drop(columns=["diff_files", "java_only_diff_files"], inplace=True)
# df_simplified.to_csv("thieulvd/changed_methods_simplified.csv", index=False)
