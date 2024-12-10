#   Author: masterSunflowers
#   Github: https://github.com/masterSunflowers/masterSunflowers
#   Date:   01/11/2024
#   Desc:   This file ...
import argparse
import os
import json
import pandas as pd


def main(args):
    df = pd.read_csv(args.input)
    mapped_method = []
    for _, row in df.iterrows():
        if (
            not pd.isna(row["java_only_diff_files"])
            and row["java_only_diff_files"] != ""
        ):
            prev_identifier = row["repoName"] + "--" + row["prev_commit"]
            cur_identifier = row["repoName"] + "--" + row["startCommit"]
            methods_prev_commit = json.load(
                open(
                    os.path.join(
                        args.parsed_dir, prev_identifier, "method_info.json"
                    )
                )
            )
            methods_cur_commit = json.load(
                open(
                    os.path.join(
                        args.parsed_dir, cur_identifier, "method_info.json"
                    )
                )
            )
            for prev_method in methods_prev_commit:
                for cur_method in methods_cur_commit:
                    if (
                        prev_method["file_path"] == cur_method["file_path"]
                        and prev_method["tree_path"] == cur_method["tree_path"]
                        and prev_method["parameters"]
                        == cur_method["parameters"]
                        and (
                            (
                                "constructor" in prev_method
                                and "constructor" in prev_method
                            )
                            or (
                                prev_method["return_type"]
                                == cur_method["return_type"]
                            )
                        )
                        and prev_method["modifiers"] == cur_method["modifiers"]
                        and prev_method["definition"]
                        != cur_method["definition"]
                    ):
                        mapped_method.append(
                            {
                                **dict(row),
                                "prev_method": prev_method,
                                "cur_method": cur_method,
                            }
                        )

    pd.DataFrame(mapped_method).to_json(
        args.output, orient="records", lines=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input file path", required=True)
    parser.add_argument("--output", help="Output file path", required=True)
    parser.add_argument(
        "--parsed-dir",
        dest="parsed_dir",
        help="Where store parsed files",
        required=True,
    )
    args = parser.parse_args()
    main(args)
