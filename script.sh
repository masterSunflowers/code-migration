# data_builder.py
python data_builder.py -d data/final_total.csv -r /drive1/phatnt/zTrans/data/repos -s /drive1/thieulvd/code-migration-total
# file_mapper.py
# python file_mapper.py -i data/total_migration.csv -o data/total_migration_diff.csv -r /drive1/phatnt/zTrans/data/repos
# class_parser.py
python parser.py -d data/final_total.csv -s /drive1/thieulvd/code-migration-total
# class_mapper.py
python class_mapper.py -d data/final_total.csv -s /drive1/thieulvd/code-migration-total
# method_mapper.py
python method_mapper.py -d data/final_total.csv -s /drive1/thieulvd/code-migration-total
# extract method pair
