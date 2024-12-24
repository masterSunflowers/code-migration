import argparse
import json
import os
import re
import subprocess

import pandas as pd
from tqdm import tqdm
import difflib

cache = set()


def crawl_maven_lib(group_id, artifact_id, version, storage):
    if f"{artifact_id}-{version}.jar" in cache:
        return
    maven_central_link = (
        "https://repo1.maven.org/maven2/"
        f"{group_id.replace('.', '/')}/"
        f"{artifact_id}/"
        f"{version}/"
        f"{artifact_id}-{version}.jar"
    )
    cmd = f"cd {storage} && wget {maven_central_link}"
    try:
        res = subprocess.run(cmd, text=True, shell=True, capture_output=True)
        if res.returncode != 0:
            raise RuntimeError(f"STDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}")
        else:
            cache.add(f"{artifact_id}-{version}.jar")
    except Exception as e:
        raise e


def crawl(data_file: str, storage: str):
    df = pd.read_csv(data_file)
    with tqdm() as pbar:
        for _, row in df.iterrows():
            if row["id"] in [
                "Wimmics_corese__936a23e22cf1abaff09a49026927697e6b2171a7__936a23e22cf1abaff09a49026927697e6b2171a7",
                "structr_structr__569c38864cc772fddee47ff538c883828f39a87f__569c38864cc772fddee47ff538c883828f39a87f",
                "zalando_problem__1b987b88ecb5cc2c8df58ac8eda188fb2d6f5998__1b987b88ecb5cc2c8df58ac8eda188fb2d6f5998",
                "ForgeRock_openidm-community-edition__43689602ee8a67deb29ea8412c48410dcaa6b30a__43689602ee8a67deb29ea8412c48410dcaa6b30a",
                "apache_storm__3503dcea62c9bb9d004388773705ad362e7cc5dd__3503dcea62c9bb9d004388773705ad362e7cc5dd",
                "codenvy__8a0a2026919db64ed2a49c73f7950a1195c0efd7__8a0a2026919db64ed2a49c73f7950a1195c0efd7",
            ]:
                lib_pairs = eval(row["migration_info"])["lib_pairs"]
                for lib_pair in lib_pairs:
                    try:
                        from_group_id, from_artifact_id = lib_pair["from_lib"].split(
                            ":"
                        )
                        from_version = lib_pair["from_lib_version"]
                        crawl_maven_lib(
                            from_group_id,
                            from_artifact_id,
                            from_version,
                            storage,
                        )
                        pbar.update(1)
                        to_group_id, to_artifact_id = lib_pair["to_lib"].split(":")
                        to_version = lib_pair["to_lib_version"]
                        crawl_maven_lib(
                            to_group_id, to_artifact_id, to_version, storage
                        )
                        pbar.update(1)
                    except Exception as e:
                        print(e)


def extract_jar(lib_storage: str):
    def run(jar_path: str, output_path: str):
        cmd = (
            f"jar tf {jar_path} | "
            "grep '.class$' | "
            "tr / . | "
            "sed 's/\.class$//' | "
            f"xargs javap -public -cp {jar_path} > "
            f"{output_path}"
        )
        try:
            res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            if res.returncode != 0:
                raise RuntimeError(f"STDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}")
            else:
                return
        except Exception as e:
            raise e

    libs = os.listdir(lib_storage)
    for lib in tqdm(libs):
        jar_path = os.path.join(lib_storage, lib)
        output_path = os.path.join(lib_storage, lib.replace(".jar", ".txt"))
        run(jar_path, output_path)


def parse_public_api(storage: str):
    def run(lib_info_path: str):
        result = {}
        current_class = ""
        with open(lib_info_path, "r") as f:
            lines = f.read().splitlines()

        for line in lines:
            line = line.strip()
            class_match = re.match(
                r"^(?:public\s+)?((?:interface|final\s+class|class)\s+)([\w.]+)\s+",
                line,
            )
            if class_match:
                current_class = class_match.group(2)
                result[current_class] = {}
                continue

            method_match = re.match(
                r"(?:public\s+)(?:abstract\s+|final\s+|static\s+)*(?:[\w.<>]+\s+)?(\w+)\((.*?)\);$",
                line,
            )
            if method_match:
                method_name = method_match.group(1)
                parameters = method_match.group(2)
                # Add method to the current class's dictionary
                if current_class:  # Make sure we have a current class
                    result[current_class][method_name] = parameters
        return result

    lst_lib_info_file = filter(lambda x: x.endswith(".txt"), os.listdir(storage))
    for lib_info_file in lst_lib_info_file:
        lib_info_path = os.path.join(storage, lib_info_file)
        result = run(lib_info_path)
        # print(result)
        # print("=" * 100)
        with open(os.path.join(lib_info_path.replace(".txt", ".json")), "w") as f:
            json.dump(result, f)


def compare_code_snippets(old_code, new_code):
    """
    Compare two code snippets and show their differences.

    Args:
        old_code (str): The original code snippet
        new_code (str): The new code snippet
    """

    # Split the code into lines
    old_lines = old_code.splitlines()
    new_lines = new_code.splitlines()

    # Print unified diff format
    unified_diff = difflib.unified_diff(old_lines, new_lines, lineterm="")
    return unified_diff


def has_method_change(diff_text, from_lib_methods, to_lib_methods):
    lines = diff_text.splitlines()
    for line in lines:
        if line.startswith("-"):
            for method in from_lib_methods:
                if method in line:
                    return (True, line, from_lib_methods[method])
        elif line.startswith("+"):
            for method in to_lib_methods:
                if method in line:
                    return (True, line, to_lib_methods[method])
    return (False, None, None)


def get_list_method(storage, lib_name, lib_version):
    _, artifact_id = lib_name.split(":")
    file_name = f"{artifact_id}-{lib_version}.json"
    file_path = os.path.join(storage, file_name)
    with open(file_path, "r") as f:
        obj = json.load(f)
    methods = {}
    for key, value in obj.items():
        # Add class name, may be for constructor
        methods[key.split(".")[-1]] = key
        # Add all method of class
        for k, v in value.items():
            methods[k] = f"{key}:{k}({v})"

    return methods


def main(args):
    df = pd.read_csv(args.data_file)
    methods = pd.read_csv(args.method_file)
    lst_diff = []
    lst_lib_affected = []
    for _, row in tqdm(methods.iterrows(), total=len(methods)):
  
        lib_pairs = eval(df[df["id"] == row["migration_id"]].iloc[0]["migration_info"])[
            "lib_pairs"
        ]
        old_code = row["method_ver1"] if not pd.isna(row["method_ver1"]) else ""
        new_code = row["method_ver2"] if not pd.isna(row["method_ver2"]) else ""
        diff = compare_code_snippets(old_code, new_code)
        diff_text = "\n".join(
            list(
                filter(lambda line: line.startswith("-") or line.startswith("+"), diff)
            )[2:]
        )
        lst_diff.append(diff_text)
        lib_affected = []
        for lib_pair in lib_pairs:
            from_lib_methods = get_list_method(
                args.lib_storage, lib_pair["from_lib"], lib_pair["from_lib_version"]
            )
            to_lib_methods = get_list_method(
                args.lib_storage, lib_pair["to_lib"], lib_pair["to_lib_version"]
            )
            flag, match_line, method_api = has_method_change(diff_text, from_lib_methods, to_lib_methods)
            if flag:
                pair = f"{lib_pair['from_lib']}:{lib_pair['from_lib_version']}--{lib_pair['to_lib']}:{lib_pair['to_lib_version']}"
            
                lib_affected.append({
                    "lib_pair": pair,
                    "match_line": match_line,
                    "method_api": method_api
                })
        if lib_affected:
            lst_lib_affected.append(lib_affected)
        else:
            lst_lib_affected.append(None)

    methods["diff"] = lst_diff
    methods["lib"] = lst_lib_affected
    methods.to_csv(args.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-file", dest="data_file")
    parser.add_argument("-m", "--method-file", dest="method_file")
    parser.add_argument("-l", "--lib-storage", dest="lib_storage")
    parser.add_argument("-o", "--output-file", dest="output_file")
    args = parser.parse_args()
    main(args)
