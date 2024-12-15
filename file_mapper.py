import subprocess
import argparse

def map_files(repo_dir: str, prev_commit: str, cur_commit: str):
    try:
        lst_diff_file = get_changed_files(
            repo_dir, prev_commit, cur_commit
        ).splitlines()
        file_map = {
            "Added": [],
            "Modified": [],
            "Deleted": [],
            "Renamed-Modified": [],
            "Renamed-Unchanged": [],
        }
        for diff_file in lst_diff_file:
            if diff_file.startswith("R"):
                mode, old_file, new_file = diff_file.split("\t")
                if old_file.endswith(".java") and new_file.endswith(".java"):
                    similarity_index = int(mode[1:])
                    if similarity_index < 100:
                        file_map["Renamed-Modified"].append(
                            (old_file, new_file, similarity_index)
                        )
                    else:
                        file_map["Renamed-Unchanged"].append((old_file, new_file))
            else:
                mode, file_path = diff_file.split("\t")
                if file_path.endswith(".java"):
                    if mode == "A":
                        file_map["Added"].append(file_path)
                    elif mode == "M":
                        file_map["Modified"].append(file_path)
                    elif mode == "D":
                        file_map["Deleted"].append(file_path)
        return file_map
    except Exception as e:
        print(e)
        return None


def get_changed_files(repo_dir: str, prev_commit: str, cur_commit: str):
    cmd = f"git config --global --add safe.directory {repo_dir} && cd {repo_dir} && git diff --name-status {prev_commit} {cur_commit}"
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
    ), "List repo name, list current commit, and list previous commit need to have same length"
    lst_diff_file = []
    for repo_name, cur_commit, prev_commit in zip(
        lst_repo_name, lst_end_commit, lst_prev_commit
    ):
        if pd.isna(prev_commit):
            lst_diff_file.append(None)
            continue
        repo_dir = os.path.join(repo_storage, repo_name)
        lst_diff_file.append(map_files(repo_dir, prev_commit, cur_commit))
    return lst_diff_file


def main(args):
    df = pd.read_csv(args.input)

    # Get previous commit hash
    lst_prev_commit = get_prev_commit(
        df["repoName"], df["startCommit"], args.repo_storage
    )
    df["prev_commit"] = lst_prev_commit
    print(df)
    df.to_csv(args.output, index=False)

    # # Get diff file name
    # lst_diff_file = get_diff_file_name(
    #     df["repoName"], df["endCommit"], df["prev_commit"], args.repo_storage
    # )
    # df["diff_files"] = lst_diff_file
    # df.to_csv(args.output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", type=str, required=True)
    parser.add_argument("-o", "--output", dest="output", type=str, required=True)
    parser.add_argument(
        "-r", "--repo-storage", dest="repo_storage", type=str, required=True
    )
    args = parser.parse_args()
    main(args)