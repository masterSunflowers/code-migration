- file_mapper.py -> dict[(added, deleted, modified, rename_modified, rename_unchanged), str: file relative path]
- class_parser.py -> parse class rename_modified/modified -> output parsed_n
- class_mapper.py -> add info into files parsed_n 
- method_mapper.py -> add info into files parsed_n 

# parsed_50
2 repo ver
<repo_name>--<prev_commit = start_commit-1>
    changed_files_name
        array of classes - usually 1
            class info
<repo_name>--<end_commit>
    changed_file_name


file_mapper.py
python thieulvd/file_mapper.py \
    --input <original_data_file> \
    --output <data_file> \
    --repo-storage /drive1/phatnt/zTrans/data/repos

class_paser.py
python thieulvd/class_parser.py \
    --input <data_file> \
    --repo-storage /drive1/phatnt/zTrans/data/repos \
    --output-dir <where_save_data>


class_mapper.py
python thieulvd/class_mapper.py \
    --input <data_file>
    --parsed-class <where_save-data>


method_mapper.py
python thieulvd/method_mapper.py \
    --input <data_file>
    --parsed-class <where_save-data>



