#   Author: masterSunflowers
#   Github: https://github.com/masterSunflowers/masterSunflowers
#   Date:   30/11/2024
#   Desc:   This file aims to parse a Java project and extract relevant information (class, method)
import argparse
import json
import os
import subprocess
from typing import Dict, List

import pandas as pd
import tree_sitter
import tree_sitter_java as tsjava
from tqdm import tqdm

JAVA = tree_sitter.Language(tsjava.language())
PARSER = tree_sitter.Parser(JAVA)


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
    try:
        code = subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
        return code
    except Exception as e:
        raise e


def parse_java_files(
    repo_dir: str, file_map: Dict[str, List[str]], prev_commit: str, cur_commit: str
):
    for file_mode in file_map:
        if file_map[file_mode]:
            match file_mode:
                case "Added":
                    for rev_path in file_map[file_mode]:
                        current_code = get_code(repo_dir, cur_commit, rev_path)
                        tree = get_ast(current_code)
                        yield rev_path, tree, file_mode, cur_commit, None
                case "Modified":
                    for rev_path in file_map[file_mode]:
                        current_code = get_code(repo_dir, cur_commit, rev_path)
                        tree = get_ast(current_code)
                        yield rev_path, tree, file_mode, cur_commit, None

                        previous_code = get_code(repo_dir, prev_commit, rev_path)
                        tree = get_ast(previous_code)
                        yield rev_path, tree, file_mode, prev_commit, None
                case "Deleted":
                    for rev_path in file_map[file_mode]:
                        previous_code = get_code(repo_dir, prev_commit, rev_path)
                        tree = get_ast(previous_code)
                        yield rev_path, tree, file_mode, prev_commit, None
                case "Renamed":
                    for old_path, new_path in file_map[file_mode]:
                        current_code = get_code(repo_dir, cur_commit, new_path)
                        tree = get_ast(current_code)
                        yield new_path, tree, file_mode, cur_commit, old_path

                        previous_code = get_code(repo_dir, prev_commit, old_path)
                        tree = get_ast(previous_code)
                        yield old_path, tree, file_mode, prev_commit, new_path
                case _:
                    continue


def get_definitions(
    rev_path: str, tree: tree_sitter.Tree, file_mode: str, map_path: str = ""
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
        if child.type == "class_declaration":
            stack.append(child)
    while stack:
        node = stack.pop(0)
        tree_path = get_class_node_path(root_node, node)
        class_info = {
            "rev_path": rev_path,
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
            "map_path": map_path,
            "methods": [],
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
                class_info["super_interfaces"] = child.text.decode("utf-8")
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
                        elif c.type == "type_identifier":
                            method_info["return_type"] = c.text.decode("utf-8")
                        elif c.type == "identifier":
                            method_info["name"] = c.text.decode("utf-8")
                        elif c.type == "formal_parameters":
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
                        elif c.type == "block":
                            method_info["body"] = normalize_code(c.text.decode("utf-8"))
                    lst_method_info.append(method_info)
                elif child.type == "class_declaration":
                    stack.append(child)
                elif child.type == "constructor_declaration":
                    constructor_info = {
                        "definition": normalize_code(child.text.decode("utf-8")),
                        "name": None,
                        "modifiers": None,
                        "parameters": [],
                        "body": None,
                        "constructor": True,
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
                        elif c.type == "identifier":
                            constructor_info["name"] = c.text.decode("utf-8")
                        elif c.type == "formal_parameters":
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
                        elif c.type == "constructor_body":
                            constructor_info["body"] = normalize_code(
                                c.text.decode("utf-8")
                            )
                    lst_method_info.append(constructor_info)
        class_info["methods"] = lst_method_info
        lst_class_info.append(class_info)
    return lst_class_info


def main(args):
    df = pd.read_csv(args.input)
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Parsing"):
        if not pd.isna(row["diff_files"]):
            repo_dir = os.path.join(args.repos_dir, row["repoName"])
            file_map = eval(row["diff_files"])
            # Parse the AST for files in previous commit version and current commit version
            all_previous_class = []
            all_current_class = []
            for rev_path, tree, file_mode, commit_hash, map_path in parse_java_files(
                repo_dir,
                file_map,
                row["prev_commit"],
                row["endCommit"],
            ):
                lst_class_info = get_definitions(rev_path, tree, file_mode, map_path)
                if commit_hash == row["prev_commit"]:
                    all_previous_class.extend(lst_class_info)
                else:
                    all_current_class.extend(lst_class_info)

            if not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir, exist_ok=True)

            prev_identifier = row["repoName"] + "--" + row["prev_commit"] + ".json"
            with open(
                os.path.join(args.output_dir, prev_identifier),
                "w",
            ) as f:
                json.dump(all_previous_class, f, indent=4)

            cur_identifier = row["repoName"] + "--" + row["endCommit"] + ".json"
            with open(
                os.path.join(args.output_dir, cur_identifier),
                "w",
            ) as f:
                json.dump(all_current_class, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", required=True, help="Input data file")
    parser.add_argument(
        "--repos-dir",
        dest="repos_dir",
        required=True,
        help="Path to repos storage",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        required=True,
        help="Where to store parse result",
    )
    args = parser.parse_args()

    main(args)
