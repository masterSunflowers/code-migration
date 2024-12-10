import argparse
import pandas as pd
import os
import json

def compare_sig(sig1, sig2):
    if sig1[0] != sig2[0]:
        return False
    if len(sig1[1]) != len(sig2[1]):
        return False
    for i in range(len(sig1[1])):
        if sig1[1][i] != sig2[1][i]:
            return False
    return True

def main(args):
    df = pd.read_csv(args.input)
    records = []
    for _, row in df.iterrows():
        if pd.isna(row["diff_files"]):
            continue
        diff_files = eval(row["diff_files"])
        for mode in diff_files:
            if mode in ["Modified", "Renamed-Modified"]:
                parsed_prev = os.path.join(
                    args.parsed_dir, row["repoName"] + "--" + row["prev_commit"]
                )
                parsed_cur = os.path.join(
                    args.parsed_dir, row["repoName"] + "--" + row["endCommit"]
                )
                for item in diff_files[mode]:
                    if mode == "Modified":
                        old_file = new_file = item
                    else:
                        old_file, new_file, _ = item

                    parsed_old_file = old_file.replace("/", "--") + ".json"
                    parsed_new_file = new_file.replace("/", "--") + ".json"
                    with open(os.path.join(parsed_prev, parsed_old_file), "r") as f:
                        old_classes = json.load(f)
                    with open(os.path.join(parsed_cur, parsed_new_file), "r") as f:
                        new_classes = json.load(f)

                    for aclass in old_classes:
                        if aclass["class_mode"] not in ["Modified", "Renamed-Modified"]:
                            continue
                        if aclass["class_mode"] == "Modified":
                            mapped_tree_path = aclass["tree_path"]
                        else:
                            mapped_tree_path = aclass["map_tree_path"]

                        bclass = None
                        for cls in new_classes:
                            if cls["tree_path"] == mapped_tree_path:
                                bclass = cls
                        if not bclass:
                            raise Exception("No mapped class found")

                        old_methods = aclass["methods"]
                        new_methods = bclass["methods"]
                        for method in old_methods:
                            if method["method_mode"] not in [
                                "Modified",
                                "Renamed-Modified",
                            ]:
                                continue
                            if method["method_mode"] == "Modified":
                                mapped_sig = (method["name"], method["parameters"])
                            else:
                                mapped_sig = method["map_method"]

                            bmethod = None
                            for m in new_methods:
                                if compare_sig((m["name"], m["parameters"]), mapped_sig):
                                    bmethod = m
                            if not bmethod:
                                print(mapped_sig)
                                raise Exception("No mapped method found")
                            

                            new_record = {
                                **row,
                                "old_file": old_file,
                                "new_file": new_file,
                                "old_class": aclass["tree_path"],
                                "new_class": bclass["tree_path"],
                                "old_method_sig": (
                                    method["name"],
                                    method["parameters"],
                                ),
                                "new_method_sig": (
                                    bmethod["name"],
                                    method["parameters"],
                                ),
                                "old_method_code": method["definition"],
                                "new_method_code": bmethod["definition"],
                            }

                            records.append(new_record)
    res = pd.DataFrame(records)
    res.to_csv(args.output, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Input CSV file")
    parser.add_argument("-o", "--output", type=str, help="Output CSV file")
    parser.add_argument("-p", "--parse-dir", dest="parsed_dir")
    args = parser.parse_args()
    main(args)
