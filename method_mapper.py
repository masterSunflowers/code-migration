import argparse
import json
import os

import myers
import pandas as pd
from tqdm import tqdm
from typing import Union, Dict
from pprint import pprint


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


def create_method_signature(method: dict) -> str:
    try:
        signature = (
            method["name"] + "__" + method["parameters"]
        )
        return signature
    except Exception as e:
        print(method["name"])
        print(method["parameters"])
        raise e
    


def _annotate(lst_method_prev, lst_method_cur, threshold: float):
    for amethod in lst_method_prev:
        amethod["ver1_signature"] = create_method_signature(amethod)
        for bmethod in lst_method_cur:
            bmethod["ver2_signature"] = create_method_signature(bmethod)
            if amethod["ver1_signature"] == bmethod["ver2_signature"]:
                if amethod["definition"] == bmethod["definition"]:
                    amethod["method_mode"] = "Unchanged"
                    bmethod["method_mode"] = "Unchanged"
                    amethod["ver2_signature"] = bmethod["ver2_signature"]
                    bmethod["ver1_signature"] = amethod["ver1_signature"]
                else:
                    amethod["method_mode"] = "Modified"
                    bmethod["method_mode"] = "Modified"
                    amethod["ver2_signature"] = bmethod["ver2_signature"]
                    bmethod["ver1_signature"] = amethod["ver1_signature"]
                break

    for amethod in lst_method_prev:
        if "method_mode" in amethod:
            continue

        max_similarity = 0
        best_match = None
        for bmethod in lst_method_cur:
            if "method_mode" in bmethod:
                continue
            similarity = get_similarity_index(
                amethod["definition"], bmethod["definition"]
            )
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = bmethod

        if max_similarity == 100:
            amethod["method_mode"] = "Renamed-Unchanged"
            best_match["method_mode"] = "Renamed-Unchanged"
            amethod["ver1_signature"] = create_method_signature(amethod)
            best_match["ver2_signature"] = create_method_signature(best_match)
            amethod["ver2_signature"] = best_match["ver2_signature"]
            best_match["ver1_signature"] = amethod["ver1_signature"]
            continue
        elif max_similarity > threshold:
            amethod["method_mode"] = "Renamed-Modified"
            best_match["method_mode"] = "Renamed-Modified"
            amethod["ver1_signature"] = create_method_signature(amethod)
            best_match["ver2_signature"] = create_method_signature(best_match)
            amethod["ver2_signature"] = best_match["ver2_signature"]
            best_match["ver1_signature"] = amethod["ver1_signature"]
            continue

    for amethod in lst_method_prev:
        if "method_mode" not in amethod:
            amethod["method_mode"] = "Deleted"
            amethod["ver1_signature"] = create_method_signature(amethod)
            amethod["ver2_signature"] = ""
            continue

    for bmethod in lst_method_cur:
        if "method_mode" not in bmethod:
            # print("Enter here method mode added")
            # print(bmethod)
            # print("=" * 100)
            bmethod["method_mode"] = "Added"
            bmethod["ver2_signature"] = create_method_signature(bmethod)
            bmethod["ver1_signature"] = ""
            continue

    return lst_method_prev, lst_method_cur


def annotate_method(
    data_storage: str,
    id: str,
    prev_commit: str,
    end_commit: str,
    item: Union[str, Dict[str, str]],
    column: str,
    threshold: float = 50,
):
    try:
        if column == "java_added":
            old = ""
            new = item
        elif column == "java_deleted":
            old = item
            new = ""
        elif column == "java_modified":
            old = item
            new = item
        else:
            old = item["ver1_path"]
            new = item["ver2_path"]

        ver1_parsed_dir = os.path.join(data_storage, id, f"parsed1__{prev_commit}")
        ver2_parsed_dir = os.path.join(data_storage, id, f"parsed2__{end_commit}")
        old_file_name = os.path.normpath(old).replace(os.sep, "--") + ".json"
        new_file_name = os.path.normpath(new).replace(os.sep, "--") + ".json"
        if column == "java_added":
            with open(os.path.join(ver2_parsed_dir, new_file_name), "r") as f:
                new_data = json.load(f)
            for bclass in new_data:
                for bmethod in bclass["methods"]:
                    bmethod["method_mode"] = "Added"
                    bmethod["ver2_signature"] = create_method_signature(bmethod)
                    bmethod["ver1_signature"] = ""
            with open(os.path.join(ver2_parsed_dir, new_file_name), "w") as f:
                json.dump(new_data, f, indent=4)
            return
        elif column == "java_deleted":
            with open(os.path.join(ver1_parsed_dir, old_file_name), "r") as f:
                old_data = json.load(f)
            for aclass in old_data:
                for amethod in aclass["methods"]:
                    amethod["method_mode"] = "Deleted"
                    amethod["ver1_signature"] = create_method_signature(amethod)
                    amethod["ver2_signature"] = ""
            with open(os.path.join(ver1_parsed_dir, old_file_name), "w") as f:
                json.dump(old_data, f, indent=4)
            return

        with open(os.path.join(ver1_parsed_dir, old_file_name), "r") as f:
            old_data = json.load(f)
        with open(os.path.join(ver2_parsed_dir, new_file_name), "r") as f:
            new_data = json.load(f)

        for aclass in old_data:
            if aclass["class_mode"] in ["Modified", "Renamed-Modified"]:
                for bclass in new_data:
                    if aclass["ver2_tree_path"] == bclass["ver2_tree_path"]:
                        aclass["methods"], bclass["methods"] = _annotate(
                            aclass["methods"], bclass["methods"], threshold
                        )
                        break
            else:
                continue

        for aclass in old_data:
            if aclass["class_mode"] in ["Unchanged", "Renamed-Unchanged"]:
                for amethod in aclass["methods"]:
                    amethod["method_mode"] = "Unchanged"
                    signature = create_method_signature(amethod)
                    amethod["ver1_signature"] = signature
                    amethod["ver2_signature"] = signature
            elif aclass["class_mode"] == "Deleted":
                for amethod in aclass["methods"]:
                    amethod["method_mode"] = "Deleted"
                    amethod["ver1_signature"] = create_method_signature(amethod)
                    amethod["ver2_signature"] = ""

        for bclass in new_data:
            if bclass["class_mode"] in ["Unchanged", "Renamed-Unchanged"]:
                for bmethod in bclass["methods"]:
                    bmethod["method_mode"] = "Unchanged"
                    signature = create_method_signature(bmethod)
                    bmethod["ver2_signature"] = signature
                    bmethod["ver1_signature"] = signature
            elif bclass["class_mode"] == "Added":
                for bmethod in bclass["methods"]:
                    bmethod["method_mode"] = "Added"
                    bmethod["ver2_signature"] = create_method_signature(bmethod)
                    bmethod["ver1_signature"] = ""

        with open(os.path.join(ver1_parsed_dir, old_file_name), "w") as f:
            json.dump(old_data, f, indent=4)
        with open(os.path.join(ver2_parsed_dir, new_file_name), "w") as f:
            json.dump(new_data, f, indent=4)

    except Exception as e:
        print(f"Error processing {id} {item}")
        raise e


def main(args):
    df = pd.read_csv(args.data_file)
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Parsing"):
        # if (
        #     row["id"]
        #     == "structr_structr__569c38864cc772fddee47ff538c883828f39a87f__569c38864cc772fddee47ff538c883828f39a87f"
        # ):
            for col in [
                "java_added",
                "java_deleted",
                "java_modified",
                "java_renamed_modified",
            ]:
                for item in eval(row[col]):
                    annotate_method(
                        args.data_storage,
                        row["id"],
                        row["prev_commit"],
                        row["end_commit"],
                        item,
                        col,
                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-file", dest="data_file", help="CSV data file")
    parser.add_argument("-s", "--data-storage", dest="data_storage")
    args = parser.parse_args()
    main(args)
