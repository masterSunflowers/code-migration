#   Author: masterSunflowers
#   Github: https://github.com/masterSunflowers/masterSunflowers
#   Date:   30/11/2024
#   Desc:   This file aims to parse a Java project and extract relevant information (class, method)
import argparse
import json
import os
import subprocess

import pandas as pd
import tree_sitter
import tree_sitter_java as tsjava
from tqdm import tqdm

JAVA = tree_sitter.Language(tsjava.language())
PARSER = tree_sitter.Parser(JAVA)
CLASS_LIKE = ["class_declaration", "enum_declaration", "record_declaration", "annotation_type_declaration", "interface_declaration"]

def normalize_code(code: str):
    lines_of_code = code.splitlines()
    redundant_space = len(lines_of_code[-1]) - 1
    for i in range(1, len(lines_of_code)):
        lines_of_code[i] = lines_of_code[i][redundant_space:]
    return "\n".join(lines_of_code)


def get_class_node_path(root_node: tree_sitter.Node, node: tree_sitter.Node):
    path = [node.child_by_field_name("name").text.decode("utf-8")]
    cur_node = node
    while cur_node.parent and cur_node.parent != root_node:
        cur_node = cur_node.parent
        if cur_node.type == "class_declaration":
            path.append(cur_node.child_by_field_name("name").text.decode("utf-8"))
    return ".".join(reversed(path))


def get_ast(code):
    try:
        tree = PARSER.parse(bytes(code, "utf-8"))
        return tree
    except Exception as e:
        raise e


def get_code(repo_dir, commit_hash, rev_path):
    cmd = f"cd {repo_dir} && " f"git show {commit_hash}:{rev_path}"
    # print(cmd)
    try:
        code = subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
        return code.replace("\r\n", "\n")
    except Exception as e:
        raise e


def get_code_updated(repo_dir, commit_hash, rev_path):
    versions = list(filter(lambda dir: "ver" in dir, os.listdir(repo_dir)))
    if commit_hash in versions[0]:
        file_path = os.path.join(repo_dir, versions[0], rev_path)
    else:
        file_path = os.path.join(repo_dir, versions[1], rev_path)
    with open(file_path, "r") as f:
        code = f.read()
    return code.replace("\r\n", "\n")


def parse_java_files(repo_dir, row):
    for rev_path in eval(row["java_added"]):
        ver2_code = get_code(repo_dir, row["end_commit"], rev_path)
        tree = get_ast(ver2_code)
        yield 2, None, rev_path, "Added", tree

    for rev_path in eval(row["java_deleted"]):
        ver1_code = get_code(repo_dir, row["prev_commit"], rev_path)
        tree = get_ast(ver1_code)
        yield 1, rev_path, None, "Deleted", tree

    for rev_path in eval(row["java_modified"]):
        ver2_code = get_code(repo_dir, row["end_commit"], rev_path)
        tree = get_ast(ver2_code)
        yield 2, rev_path, rev_path, "Modified", tree

        ver1_code = get_code(repo_dir, row["prev_commit"], rev_path)
        tree = get_ast(ver1_code)
        yield 1, rev_path, rev_path, "Modified", tree

    for dic in eval(row["java_renamed_modified"]):
        ver1_rev_path, ver2_rev_path, _ = dic.values()
        ver2_code = get_code(repo_dir, row["end_commit"], ver2_rev_path)
        tree = get_ast(ver2_code)
        yield 2, ver1_rev_path, ver2_rev_path, "Renamed-Modified", tree

        ver1_code = get_code(repo_dir, row["prev_commit"], ver1_rev_path)
        tree = get_ast(ver1_code)
        yield 1, ver1_rev_path, ver2_rev_path, "Renamed-Modified", tree


def get_definitions(
    version: int, ver1_path: str, ver2_path: str, file_mode: str, tree: tree_sitter.Tree
):
    root_node = tree.root_node
    lst_class_info = []
    package_name = None

    # Get package of file
    for node in root_node.children:
        if node.type == "package_declaration":
            package_name = node.text.decode("utf-8")

    # Traverse root node children recursively to get class and method definitions
    stack = []
    for child in root_node.children:
        if child.type in CLASS_LIKE:
            stack.append(child)
    while stack:
        node = stack.pop(0)
        tree_path = get_class_node_path(root_node, node)
        class_info = {
            "version": version,
            "ver1_path": ver1_path,
            "ver2_path": ver2_path,
            "definition": normalize_code(node.text.decode("utf-8")),
            "package": package_name,
            "tree_path": tree_path,
            "name": None,
            "modifiers": None,
            "superclass": None,
            "super_interfaces": None,
            "body": None,
            "start_point": {
                "row": node.start_point.row,
                "column": node.start_point.column,
            },
            "end_point": {
                "row": node.end_point.row,
                "column": node.end_point.column,
            },
            "file_mode": file_mode,
            "methods": [],
            "node_type": node.type
        }
        class_body = None
        lst_method_info = []
        for child in node.named_children:
            if child.type == "identifier":
                class_info["name"] = child.text.decode("utf-8")
            elif child.type == "modifiers":
                class_info["modifiers"] = child.text.decode("utf-8")
            elif child.type == "superclass":
                class_info["superclass"] = child.text.decode("utf-8")
            elif child.type == "super_interfaces":
                class_info["super_interfaces"] = child.named_children[0].text.decode("utf-8")
            elif child.type == "class_body":
                class_info["body"] = normalize_code(child.text.decode("utf-8"))
                class_body = child
        if class_body:
            for child in class_body.named_children:
                if child.type == "method_declaration":
                    method_info = {
                        "definition": normalize_code(child.text.decode("utf-8")),
                        "name": None,
                        "modifiers": None,
                        "return_type": None,
                        "parameters": [],
                        "body": None,
                        "start_point": {
                            "row": child.start_point.row,
                            "column": child.start_point.column,
                        },
                        "end_point": {
                            "row": child.end_point.row,
                            "column": child.end_point.column,
                        },
                    }
                    for c in child.named_children:
                        if c.type == "modifiers":
                            method_info["modifiers"] = c.text.decode("utf-8")
                    c = child.child_by_field_name("type")
                    method_info["return_type"] = c.text.decode("utf-8")
                    c = child.child_by_field_name("name")
                    method_info["name"] = c.text.decode("utf-8")
                    c = child.child_by_field_name("parameters")
                    for param in c.named_children:
                        if param.type == "formal_parameter":
                            param_type = param.named_children[0].text.decode(
                                "utf-8"
                            )
                            param_name = param.named_children[1].text.decode(
                                "utf-8"
                            )
                            method_info["parameters"].append(
                                {
                                    "type": param_type,
                                    "name": param_name,
                                }
                            )
                    c = child.child_by_field_name("body")
                    if c:
                        method_info["body"] = normalize_code(c.text.decode("utf-8"))
                    lst_method_info.append(method_info)
                elif child.type in CLASS_LIKE:
                    stack.append(child)
                elif child.type == "constructor_declaration":
                    constructor_info = {
                        "definition": normalize_code(child.text.decode("utf-8")),
                        "name": None,
                        "modifiers": None,
                        "return_type": None,
                        "parameters": [],
                        "body": None,
                        "start_point": {
                            "row": child.start_point.row,
                            "column": child.start_point.column,
                        },
                        "end_point": {
                            "row": child.end_point.row,
                            "column": child.end_point.column,
                        },
                    }
                    for c in child.named_children:
                        if c.type == "modifiers":
                            constructor_info["modifiers"] = c.text.decode("utf-8")
                    c = child.child_by_field_name("name")
                    constructor_info["name"] = c.text.decode("utf-8")
                    c = child.child_by_field_name("parameters")
                    for param in c.named_children:
                        if param.type == "formal_parameter":
                            param_type = param.named_children[0].text.decode(
                                "utf-8"
                            )
                            param_name = param.named_children[1].text.decode(
                                "utf-8"
                            )
                            constructor_info["parameters"].append(
                                {
                                    "type": param_type,
                                    "name": param_name,
                                }
                            )
                    c = child.child_by_field_name("body")
                    if c:
                        constructor_info["body"] = normalize_code(
                            c.text.decode("utf-8")
                        )
                    lst_method_info.append(constructor_info)
        class_info["methods"] = lst_method_info
        lst_class_info.append(class_info)
    return lst_class_info


def main(args):
    df = pd.read_csv(args.data_file)
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Parsing"):
        repo_dir = os.path.join(args.repo_storage, row["repo_name"])
        # repo_dir = os.path.join(args.repo_storage, row["id"])
        ver1_parsed_dir = os.path.join(
            args.data_storage, row["id"], f"parsed1__{row['prev_commit']}"
        )
        ver2_parsed_dir = os.path.join(
            args.data_storage, row["id"], f"parsed2__{row['end_commit']}"
        )
        os.makedirs(ver1_parsed_dir, exist_ok=True)
        os.makedirs(ver2_parsed_dir, exist_ok=True)
        for version, ver1_path, ver2_path, file_mode, tree in parse_java_files(
            repo_dir,
            row=row,
        ):
            lst_class_info = get_definitions(
                version, ver1_path, ver2_path, file_mode, tree
            )
            file_name = (
                "--".join(
                    os.path.normpath(ver1_path if version == 1 else ver2_path).split(
                        os.sep
                    )
                )
                + ".json"
            )
            if version == 1:
                with open(
                    os.path.join(ver1_parsed_dir, file_name),
                    "w",
                ) as f:
                    json.dump(lst_class_info, f, indent=4)
            else:
                with open(
                    os.path.join(ver2_parsed_dir, file_name),
                    "w",
                ) as f:
                    json.dump(lst_class_info, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-file", dest="data_file", help="CSV data file")
    parser.add_argument(
        "-r",
        "--repo-storage",
        dest="repo_storage",
        help="Path to repos storage",
    )
    parser.add_argument(
        "-s",
        "--data-storage",
        dest="data_storage",
        help="Where to store parse result",
    )
    args = parser.parse_args()

    main(args)
