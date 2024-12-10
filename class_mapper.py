import argparse
import os
import json
import pandas as pd
from tqdm import tqdm
from difflib import SequenceMatcher
# import subprocess

# repos_storage = "/drive1/phatnt/zTrans/data/repos"


# def read_file_in_commit(repo_name, rev_path, commit_hash):
#     repo_dir = os.path.join(repos_storage, repo_name)
#     cmd = (
#         f"git config --global --add safe.directory {repo_dir} && "
#         f"cd {repo_dir} && "
#         f"git show {commit_hash}:{rev_path}"
#     )
#     # print(cmd)
#     try:
#         res = subprocess.check_output(cmd, shell=True)
#     except subprocess.CalledProcessError:
#         return None
#     return res.decode("utf-8")
def get_similarity_index(code1, code2):
    # Calculate similarity ratio using SequenceMatcher
    similarity = SequenceMatcher(None, code1, code2).ratio()
    # Convert to percentage and round to 2 decimal places
    return round(similarity * 100, 2)


def annotate_class(
    parsed_class, repo, prev_commit, cur_commit, file_path, mode, threshold: int = 0.5
):
    if mode == "Modified":
        old = file_path
        new = file_path
    elif mode == "Renamed-Modified":
        old, new, _ = file_path
    else:
        raise ValueError(f"Unknown mode: {mode}")

    output_prev = os.path.join(parsed_class, repo + "--" + prev_commit)
    output_cur = os.path.join(parsed_class, repo + "--" + cur_commit)
    old_file_name = os.path.normpath(old).replace(os.sep, "--") + ".json"
    new_file_name = os.path.normpath(new).replace(os.sep, "--") + ".json"
    with open(os.path.join(output_prev, old_file_name), "r") as f:
        old_data = json.load(f)
    with open(os.path.join(output_cur, new_file_name), "r") as f:
        new_data = json.load(f)

    for aclass in old_data:
        mapped = False
        for bclass in new_data:
            if aclass["tree_path"] == bclass["tree_path"]:
                mapped = True
                if aclass["definition"] == bclass["definition"]:
                    aclass["class_mode"] = "Unchanged"
                    bclass["class_mode"] = "Unchanged"
                else:
                    aclass["class_mode"] = "Modified"
                    bclass["class_mode"] = "Modified"
                    break
        if mapped:
            continue

        # Check for rename
        max_similarity = 0
        best_match = None
        for bclass in new_data:
            if (
                get_similarity_index(aclass["definition"], bclass["definition"])
                > max_similarity
            ):
                max_similarity = get_similarity_index(
                    aclass["definition"], bclass["definition"]
                )
                best_match = bclass
        if max_similarity == 100:
            aclass["class_mode"] = "Renamed-Unchanged"
            best_match["class_mode"] = "Renamed-Unchanged"
            aclass["map_tree_path"] = best_match["tree_path"]
            best_match["map_tree_path"] = aclass["tree_path"]
            continue
        elif max_similarity > threshold:
            aclass["class_mode"] = "Renamed-Modified"
            best_match["class_mode"] = "Renamed-Modified"
            aclass["map_tree_path"] = best_match["tree_path"]
            best_match["map_tree_path"] = aclass["tree_path"]
            continue
    for aclass in old_data:
        if "class_mode" not in aclass:
            aclass["class_mode"] = "Deleted"

    for bclass in new_data:
        if "class_mode" not in bclass:
            bclass["class_mode"] = "Added"

    with open(os.path.join(output_prev, old_file_name), "w") as f:
        json.dump(old_data, f, indent=4)
    with open(os.path.join(output_cur, new_file_name), "w") as f:
        json.dump(new_data, f, indent=4)


def main(args):
    df = pd.read_csv(args.input)
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Parsing"):
        if not pd.isna(row["diff_files"]):
            file_map = eval(row["diff_files"])
            for mode in file_map:
                if mode in ["Modified", "Renamed-Modified"]:
                    for item in file_map[mode]:
                        annotate_class(
                            args.parsed_class,
                            row["repoName"],
                            row["prev_commit"],
                            row["endCommit"],
                            item,
                            mode,
                        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Class Mapper")
    parser.add_argument("-i", "--input", dest="input", help="Input CSV file")
    parser.add_argument("-p", "--parsed-class", dest="parsed_class")
    args = parser.parse_args()
    main(args)
