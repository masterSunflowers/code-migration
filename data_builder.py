"""This file aims to build 2 version of repository by repo_name, start_commit and end_commit"""

import argparse
import os
import pandas as pd
import subprocess
from tqdm import tqdm


def main(args):
    df = pd.read_csv(args.data_file)
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Creating"):
        repo_dir = os.path.join(args.repo_storage, row["repo_name"])
        ver1_dir = os.path.join(
            args.data_storage, row["id"], f"ver1__{row['prev_commit']}"
        )
        ver2_dir = os.path.join(
            args.data_storage, row["id"], f"ver2__{row['end_commit']}"
        )
        os.makedirs(ver1_dir, exist_ok=True)
        os.makedirs(ver2_dir, exist_ok=True)

        copy_ver1_cmd = (
            f"cd {repo_dir} && "
            "git stash && "
            f"git checkout {row['prev_commit']} && "
            f"cp -r {repo_dir}/* {ver1_dir} && "
            f"rm -rf {ver1_dir}/.git"
        )
        copy_ver2_cmd = (
            f"cd {repo_dir} && "
            "git stash && "
            f"git checkout {row['end_commit']} && "
            f"cp -r {repo_dir}/* {ver2_dir} && "
            f"rm -rf {ver2_dir}/.git"
        )

        copy_ver1_cmd_proc = subprocess.run(
            copy_ver1_cmd, shell=True, capture_output=True, text=True
        )
        if copy_ver1_cmd_proc.returncode != 0:
            raise RuntimeError(
                f"Can not copy version 1 to new dir\t{row['repo_name']}\t{row['prev_commit']}"
            )

        copy_ver2_cmd_proc = subprocess.run(
            copy_ver2_cmd, capture_output=True, shell=True, text=True
        )
        if copy_ver2_cmd_proc.returncode != 0:
            raise RuntimeError(
                f"Can not copy version 2 to new dir\t{row['repo_name']}\t{row['end_commit']}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--data-file", dest="data_file", help="CSV Data file path"
    )
    parser.add_argument(
        "-r", "--repo-storage", dest="repo_storage", help="Where stored repos"
    )
    parser.add_argument(
        "-s",
        "--data-storage",
        dest="data_storage",
        help="Where to store 2 version of code",
    )
    args = parser.parse_args()
    main(args)
