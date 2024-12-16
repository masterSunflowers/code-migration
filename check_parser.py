import subprocess
import os

folder1 = "/drive1/thieulvd/code-migration-tmp2"
folder2 = "/drive1/thieulvd/code-migration-tmp3"

folder1_files = []
folder2_files = []


for root, dirs, files in os.walk(folder1):
    for file in files:
        folder1_files.append(os.path.join(root, file))
        
for root, dirs, files in os.walk(folder2):
    for file in files:
        folder2_files.append(os.path.join(root, file))

for file in folder1_files:
    text1 = open(file, 'r').read().replace("\r\n", "\n")
    text2 = open(file.replace("code-migration-tmp2", "code-migration-tmp3"), 'r').read().replace("\r\n", "\n")
    if text1 != text2:
        print(file)
