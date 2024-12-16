import argparse
import os
import json
import pandas as pd
from tqdm import tqdm
import myers


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


def annotate_class(
    data_storage, id, prev_commit, end_commit, item, column, threshold: float = 50
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
                bclass["class_mode"] = "Added"
                bclass["ver2_tree_path"] = bclass["tree_path"]
                bclass["ver1_tree_path"] = ""
            with open(os.path.join(ver2_parsed_dir, new_file_name), "w") as f:
                json.dump(new_data, f, indent=4)
            return
        elif column == "java_deleted":
            with open(os.path.join(ver1_parsed_dir, old_file_name), "r") as f:
                old_data = json.load(f)
            for aclass in old_data:
                aclass["class_mode"] = "Deleted"
                aclass["ver1_tree_path"] = aclass["tree_path"]
                aclass["ver2_tree_path"] = ""
            with open(os.path.join(ver1_parsed_dir, old_file_name), "w") as f:
                json.dump(old_data, f, indent=4)
            return

        with open(os.path.join(ver1_parsed_dir, old_file_name), "r") as f:
            old_data = json.load(f)
        with open(os.path.join(ver2_parsed_dir, new_file_name), "r") as f:
            new_data = json.load(f)

        for aclass in old_data:
            for bclass in new_data:
                if aclass["tree_path"] == bclass["tree_path"]:
                    if aclass["definition"] == bclass["definition"]:
                        aclass["class_mode"] = "Unchanged"
                        bclass["class_mode"] = "Unchanged"
                    else:
                        aclass["class_mode"] = "Modified"
                        bclass["class_mode"] = "Modified"
                    aclass["ver2_tree_path"] = bclass["tree_path"]
                    aclass["ver1_tree_path"] = aclass["tree_path"]
                    bclass["ver1_tree_path"] = aclass["tree_path"]
                    bclass["ver2_tree_path"] = bclass["tree_path"]
                    break

        for aclass in old_data:
            if "class_mode" in aclass:
                continue

            # Check for rename
            max_similarity = 0
            best_match = None
            for bclass in new_data:
                if "class_mode" in bclass:
                    continue
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
                aclass["ver2_tree_path"] = best_match["tree_path"]
                aclass["ver1_tree_path"] = aclass["tree_path"]
                best_match["ver1_tree_path"] = aclass["tree_path"]
                best_match["ver2_tree_path"] = best_match["tree_path"]
                continue

            elif max_similarity > threshold:
                aclass["class_mode"] = "Renamed-Modified"
                best_match["class_mode"] = "Renamed-Modified"

                aclass["ver2_tree_path"] = best_match["tree_path"]
                aclass["ver1_tree_path"] = aclass["tree_path"]
                best_match["ver1_tree_path"] = aclass["tree_path"]
                best_match["ver2_tree_path"] = best_match["tree_path"]
                continue
        for aclass in old_data:
            if "class_mode" not in aclass:
                aclass["class_mode"] = "Deleted"
                aclass["ver1_tree_path"] = aclass["tree_path"]
                aclass["ver2_tree_path"] = ""

        for bclass in new_data:
            if "class_mode" not in bclass:
                bclass["class_mode"] = "Added"
                bclass["ver1_tree_path"] = ""
                bclass["ver2_tree_path"] = bclass["tree_path"]

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
        for col in [
            "java_added",
            "java_deleted",
            "java_modified",
            "java_renamed_modified",
        ]:
            for item in eval(row[col]):
                annotate_class(
                    args.data_storage,
                    row["id"],
                    row["prev_commit"],
                    row["end_commit"],
                    item,
                    col,
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Class Mapper")
    parser.add_argument("-d", "--data-file", dest="data_file", help="CSV data file")
    parser.add_argument("-s", "--data-storage", dest="data_storage")
    args = parser.parse_args()
    main(args)
