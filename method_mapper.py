import argparse
import json
import os

import myers
import pandas as pd
from tqdm import tqdm


def get_similarity_index(old: str, new: str) -> float:
    def get_lines(text: str) -> list[str]:
        return text.replace("\r\n", "\n").strip().splitlines()

    def get_changes(old: list[str], new: list[str]) -> list[tuple[str, str]]:
        changes = myers.diff(old, new)
        return changes

    old_lines = get_lines(old)
    new_lines = get_lines(new)
    changes = get_changes(old_lines, new_lines)

    num_unchanged_lines = sum(1 for op, _ in changes if op == "k")

    # Calculate similarity
    total_lines = len(old_lines) + len(new_lines)
    if total_lines == 0:
        similarity = 100.0
    else:
        similarity = round(2 * num_unchanged_lines / total_lines * 100, 2)

    return similarity


def _annotate(lst_method_prev, lst_method_cur, threshold: float):
    for amethod in lst_method_prev:
        mapped = False
        for bmethod in lst_method_cur:
            if (
                amethod["name"] == bmethod["name"]
                and amethod["parameters"] == bmethod["parameters"]
            ):
                mapped = True
                if amethod["definition"] == bmethod["definition"]:
                    amethod["method_mode"] = "Unchanged"
                    bmethod["method_mode"] = "Unchanged"
                else:
                    amethod["method_mode"] = "Modified"
                    bmethod["method_mode"] = "Modified"
                break
        if mapped:
            continue
    
    for amethod in lst_method_prev:
        if "method_mode" in amethod:
            continue
        
        max_similarity = 0
        best_match = None
        for bmethod in lst_method_cur:
            if "method_mode" in bmethod:
                continue
            similarity = get_similarity_index(amethod["definition"], bmethod["definition"])
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = bmethod
        
        if max_similarity == 100:
            amethod["method_mode"] = "Renamed-Unchanged"
            best_match["method_mode"] = "Renamed-Unchanged"
            continue
        elif max_similarity > threshold:
            amethod["method_mode"] = "Renamed-Modified"
            best_match["method_mode"] = "Renamed-Modified"
            amethod["map_method"] = (best_match["name"], best_match["parameters"])
            best_match["map_method"] = (amethod["name"], amethod["parameters"]) 
            continue
    for amethod in lst_method_prev:
        if "method_mode" not in amethod:
            amethod["method_mode"] = "Deleted"

    for bmethod in lst_method_cur:
        if "method_mode" not in bmethod:
            bmethod["method_mode"] = "Added"   
    
    return lst_method_prev, lst_method_cur    

def annotate_method(
    parsed_class, repo, prev_commit, cur_commit, file_path, mode, threshold: float = 50
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
        if aclass["class_mode"] == "Modified":
            for bclass in new_data:
                if aclass["tree_path"] == bclass["tree_path"]:
                    aclass["methods"], bclass["methods"] = _annotate(
                        aclass["methods"], bclass["methods"], threshold
                    )
                    break
        elif aclass["class_mode"] == "Renamed-Modified":
            for bclass in new_data:
                if aclass["map_tree_path"] == bclass["tree_path"]:
                    aclass["methods"], bclass["methods"] = _annotate(
                        aclass["methods"], bclass["methods"], threshold
                    )
                    break

        else:
            continue

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
                        annotate_method(
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
