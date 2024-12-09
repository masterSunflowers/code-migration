#   Author: masterSunflowers
#   Github: https://github.com/masterSunflowers/masterSunflowers
#   Date:   30/11/2024
#   Desc:   This file aims to build data for the project
import argparse
import os
import subprocess
from typing import List
from file_mapper import map_files
import pandas as pd


def get_prev_commit(
    lst_repo_name: List[str], lst_cur_commit: List[str], repo_storage: str
):
    assert len(lst_repo_name) == len(
        lst_cur_commit
    ), "List repo name and list current commit need to have same length"
    lst_prev_commit = []
    for repo_name, cur_commit in zip(lst_repo_name, lst_cur_commit):
        repo_dir = os.path.join(repo_storage, repo_name)

        cmd = f"git config --global --add safe.directory {repo_dir} && cd {repo_dir} && git rev-parse {cur_commit}^"
        try:
            previous_commit = (
                subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
            )
            lst_prev_commit.append(previous_commit)
        except Exception:
            print(f"Error at {repo_name} and {cur_commit}")
            lst_prev_commit.append(None)

    return lst_prev_commit


def get_diff_file_name(
    lst_repo_name: List[str],
    lst_cur_commit: List[str],
    lst_prev_commit: List[str],
    repo_storage: str,
):
    assert (
        len(lst_repo_name) == len(lst_cur_commit) == len(lst_prev_commit)
    ), "List repo name, list current commit, and list previous commit need to have same length"
    lst_diff_file = []
    for repo_name, cur_commit, prev_commit in zip(
        lst_repo_name, lst_cur_commit, lst_prev_commit
    ):
        if pd.isna(prev_commit):
            lst_diff_file.append(None)
            continue
        repo_dir = os.path.join(repo_storage, repo_name)
        lst_diff_file.append(map_files(repo_dir, prev_commit, cur_commit))
    return lst_diff_file


def main(args):
    df = pd.read_csv(args.input)

    # # Get previous commit hash
    # lst_prev_commit = get_prev_commit(df['repoName'], df['startCommit'], args.repo_storage)
    # df['prev_commit'] = lst_prev_commit
    # print(df)
    # df.to_csv(args.output, index=False)

    # Get diff file name

    lst_diff_file = get_diff_file_name(
        df["repoName"], df["startCommit"], df["prev_commit"], args.repo_storage
    )
    df["diff_files"] = lst_diff_file
    df.to_csv(args.output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", type=str, required=True)
    parser.add_argument("--output", dest="output", type=str, required=True)
    parser.add_argument("--repo-storage", dest="repo_storage", type=str, required=True)
    args = parser.parse_args()
    main(args)
