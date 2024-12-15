import subprocess
import argparse
from typing import List
import pandas as pd
import os
from tqdm import tqdm


def map_files(repo_dir: str, prev_commit: str, end_commit: str):
    try:
        lst_diff_file = get_changed_files(
            repo_dir=repo_dir, prev_commit=prev_commit, end_commit=end_commit
        ).splitlines()
        file_map = {
            "Added": [],
            "Modified": [],
            "Deleted": [],
            "Renamed-Modified": [],
            "Renamed-Unchanged": [],
            "Java-Added": [],
            "Java-Deleted": [],
            "Java-Modified": [],
            "Java-Renamed-Modified": [],
            "Java-Renamed-Unchanged": [],
        }
        for diff_file in lst_diff_file:
            if diff_file.startswith("R"):
                mode, old_file, new_file = diff_file.split("\t")

                similarity_index = int(mode[1:])
                if similarity_index < 100:
                    file_map["Renamed-Modified"].append(
                        {
                            "ver1_path": old_file,
                            "ver2_path": new_file,
                            "similarity_index": similarity_index,
                        }
                    )
                    if old_file.endswith(".java") and new_file.endswith(".java"):
                        file_map["Java-Renamed-Modified"].append(
                            {
                                "ver1_path": old_file,
                                "ver2_path": new_file,
                                "similarity_index": similarity_index,
                            }
                        )

                else:
                    file_map["Renamed-Unchanged"].append(
                        {"ver1_path": old_file, "ver2_path": new_file}
                    )
                    if old_file.endswith(".java") and new_file.endswith(".java"):
                        file_map["Java-Renamed-Unchanged"].append(
                            {"ver1_path": old_file, "ver2_path": new_file}
                        )
            else:
                mode, file_path = diff_file.split("\t")

                if mode == "A":
                    file_map["Added"].append(file_path)
                    if file_path.endswith(".java"):
                        file_map["Java-Added"].append(file_path)
                elif mode == "M":
                    file_map["Modified"].append(file_path)
                    if file_path.endswith(".java"):
                        file_map["Java-Modified"].append(file_path)
                elif mode == "D":
                    file_map["Deleted"].append(file_path)
                    if file_path.endswith(".java"):
                        file_map["Java-Deleted"].append(file_path)
        return file_map
    except Exception as e:
        print(e)
        return None


def get_changed_files(repo_dir: str, prev_commit: str, end_commit: str):
    cmd = f"cd {repo_dir} && git diff --name-status {prev_commit} {end_commit}"
    try:
        diff_files = subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
        return diff_files
    except Exception as e:
        raise RuntimeError(e)


def get_diff_file_name(
    lst_repo_name: List[str],
    lst_prev_commit: List[str],
    lst_end_commit: List[str],
    repo_storage: str,
):
    assert (
        len(lst_repo_name) == len(lst_end_commit) == len(lst_prev_commit)
    ), "List repo name, list previous commit, and list end commit need to have same length"
    lst_added = []
    lst_deleted = []
    lst_modified = []
    lst_renamed_unchanged = []
    lst_renamed_modified = []
    lst_java_added = []
    lst_java_deleted = []
    lst_java_modified = []
    lst_java_renamed_unchanged = []
    lst_java_renamed_modified = []
    for repo_name, prev_commit, end_commit in tqdm(
        zip(lst_repo_name, lst_prev_commit, lst_end_commit),
        total=len(lst_repo_name),
        desc="Mapping file",
    ):
        repo_dir = os.path.join(repo_storage, repo_name)
        mapper = map_files(
            repo_dir=repo_dir, prev_commit=prev_commit, end_commit=end_commit
        )
        lst_added.append(mapper["Added"])
        lst_deleted.append(mapper["Deleted"])
        lst_modified.append(mapper["Modified"])
        lst_renamed_unchanged.append(mapper["Renamed-Unchanged"])
        lst_renamed_modified.append(mapper["Renamed-Modified"])
        lst_java_added.append(mapper["Java-Added"])
        lst_java_deleted.append(mapper["Java-Deleted"])
        lst_java_modified.append(mapper["Java-Modified"])
        lst_java_renamed_unchanged.append(mapper["Java-Renamed-Unchanged"])
        lst_java_renamed_modified.append(mapper["Java-Renamed-Modified"])

    return (
        lst_added,
        lst_deleted,
        lst_modified,
        lst_renamed_unchanged,
        lst_renamed_modified,
        lst_java_added,
        lst_java_deleted,
        lst_java_modified,
        lst_java_renamed_unchanged,
        lst_java_renamed_modified,
    )


def main(args):
    df = pd.read_csv(args.input)
    # Get diff file name
    (
        df["added"],
        df["deleted"],
        df["modified"],
        df["renamed_unchanged"],
        df["renamed_modified"],
        df["java_added"],
        df["java_deleted"],
        df["java_modified"],
        df["java_renamed_unchanged"],
        df["java_renamed_modified"],
    ) = get_diff_file_name(
        lst_repo_name=df["repo_name"],
        lst_prev_commit=df["prev_commit"],
        lst_end_commit=df["end_commit"],
        repo_storage=args.repo_storage,
    )

    df.to_csv(args.output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="Old data file")
    parser.add_argument("-o", "--output", dest="output", help="New data file")
    parser.add_argument("-r", "--repo-storage", dest="repo_storage")
    args = parser.parse_args()
    main(args)
