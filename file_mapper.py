import subprocess

def map_files(repo_dir: str, prev_commit: str, cur_commit: str):
    try:
        lst_diff_file = get_changed_files(repo_dir, prev_commit, cur_commit).splitlines()
        file_map = {"Added": [], "Modified": [], "Deleted": [], "Renamed-Modified": [], "Renamed-Unchanged": []}
        for diff_file in lst_diff_file:
            if diff_file.startswith("R"):
                mode, old_file, new_file = diff_file.split("\t")
                if old_file.endswith(".java") and new_file.endswith(".java"):
                    similarity_index = int(mode[1:])
                    if similarity_index < 100:
                        file_map["Renamed-Modified"].append((old_file, new_file, similarity_index))
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
        diff_files = (
            subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
        )
        return diff_files
    except Exception as e:
        raise RuntimeError(e)