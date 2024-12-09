import argparse
import pandas as pd
from tqdm import tqdm
import os
import subprocess
import re


def get_diff(repo_dir: str, file_path: str, prev_commit: str, cur_commit: str) -> str:
    cmd = (
        f"git config --global --add safe.directory {repo_dir} && "
        f"cd {repo_dir} && "
        f"git diff {prev_commit}:{file_path} {cur_commit}:{file_path}"
    )
    try:
        diff = subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
    except Exception as e:
        raise e
    return diff

def hunk_collection(diff: str) -> list:
    lines = diff.splitlines()
    hunks = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("@@ "):
            hunk = [lines[i]]
            while i + 1 < len(lines) and not lines[i + 1].startswith("@@ "):
                i += 1
                hunk.append(lines[i])
            hunks.append(hunk)
        else:
            i += 1
    return hunks

def range_of_change(hunk, sign: str):
    if not hunk:
        return []
    pattern = r"\@\@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? \@\@"
    match = re.search(pattern, hunk[0])
    if not match:
        return []
    if sign == "-":
        start_line = int(match.group(1))
        num_lines = int(match.group(2)) if match.group(2) else 1
    else:
        start_line = int(match.group(3))
        num_lines = int(match.group(4)) if match.group(4) else 1
    
    for idx, line in enumerate(hunk[1:]):
        if line.startswith(sign):
            num_lines += 1
        else:
            break
    return list(range(start_line, start_line + num_lines))

def annotate_method(
    parsed_storage: str,
    repo_name: str,
    file_path: str,
    diff: str,
    prev_commit: str,
    cur_commit: str,
):
    hunks = hunk_collection(diff)
    lst_changed_line_in_prev_file = []
    lst_changed_line_in_cur_file = []
    for hunk in hunks:
        change_lines_prev_file = range_of_change(hunk, "-")
        change_lines_cur_file = range_of_change(hunk, "+")
        lst_changed_line_in_prev_file.extend(change_lines_prev_file)
        lst_changed_line_in_cur_file.extend(change_lines_cur_file)
    
    methods_in_previous_file
    
    

def main(args):
    df = pd.read_csv(args.input)
    df = df[:4]
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Parsing"):
        if not pd.isna(row["diff_files"]):
            repo_dir = os.path.join(args.repos_dir, row["repoName"])
            file_map = eval(row["diff_files"])
            if file_map["Modified"]:
                for file_path in file_map["Modified"]:
                    diff = get_diff(
                        repo_dir, file_path, row["prev_commit"], row["endCommit"]
                    )
                    print(diff)
                    print("=" * 100)
                    annotate_method(
                        args.parsed_storage,
                        row["repoName"],
                        file_path,
                        diff,
                        row["prev_commit"],
                        row["endCommit"],
                    )
                    break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input")
    parser.add_argument("-p", "--parsed-storage", dest="parsed_storage")
    parser.add_argument("-r", "--repos-dir", dest="repos_dir")
    args = parser.parse_args()
    main(args)