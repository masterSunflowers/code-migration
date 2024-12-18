#!/usr/bin/env python
# coding: utf-8

# # Init

# In[1]:


import pandas as pd
import numpy as np

seed = 18022004
np.random.seed(seed)


# In[2]:


original_df = pd.read_parquet("official_original.parquet")
original_df


# In[3]:


original_df["repoName"].nunique()


# ## Insight about log test library

# In[4]:


tolib_test_df = original_df[original_df["toLib"].str.contains("unit|test")]

tolib_test_df["repoName"].nunique()


# In[5]:


fromlib_test_df = original_df[original_df["fromLib"].str.contains("unit|test")]
fromlib_test_df["repoName"].nunique()


# In[6]:


tolib_test_df


# In[7]:


fromlib_test_df


# In[8]:


print(tolib_test_df.index)


# In[9]:


print(fromlib_test_df.index)


# In[10]:


print(len(set(tolib_test_df.index).intersection(set(fromlib_test_df.index))))
print(len(set(tolib_test_df.index).union(set(fromlib_test_df.index))))


# In[11]:


1297 / len(tolib_test_df)


# In[12]:


original_df[original_df["id"] == 3084].iloc[0]


# In[13]:


i = 3084

print(original_df.loc[i, "fromLib"])
print(original_df.loc[i, "toLib"])
print(original_df.loc[i, "repoName"])
print(original_df.loc[i, "fileName"])


# In[14]:


i = 3085

print(original_df.loc[i, "fromLib"])
print(original_df.loc[i, "toLib"])
print(original_df.loc[i, "repoName"])
print(original_df.loc[i, "fileName"])


# In[15]:


i = 3086

print(original_df.loc[i, "fromLib"])
print(original_df.loc[i, "toLib"])
print(original_df.loc[i, "repoName"])
print(original_df.loc[i, "fileName"])


# In[16]:


i = 3087

print(original_df.loc[i, "fromLib"])
print(original_df.loc[i, "toLib"])
print(original_df.loc[i, "repoName"])
print(original_df.loc[i, "fileName"])


# In[17]:


i = 3088

print(original_df.loc[i, "fromLib"])
print(original_df.loc[i, "toLib"])
print(original_df.loc[i, "repoName"])
print(original_df.loc[i, "fileName"])


# In[18]:


set(tolib_test_df.index) - set(fromlib_test_df.index)


# In[19]:


set(fromlib_test_df.index) - set(tolib_test_df.index)


# In[20]:


i = 9158
print(original_df.loc[i, "fromLib"])
print(original_df.loc[i, "toLib"])
print(original_df.loc[i, "repoName"])
print(original_df.loc[i, "fileName"])


# ***Cases that fromLib has different function than toLib***
# 
# - 1358
# 
# com.sun.jersey:jersey-bundle
# 
# org.glassfish.jersey.test-framework.providers:jersey-test-framework-provider-grizzly2
# 
# opensecuritycontroller_osc-core
# 
# osc-common/pom.xml
# 
# - 45
# ant:ant
# 
# org.apache.ant:ant-junit
# 
# wocommunity_wolips
# 
# woproject-ant-tasks/pom.xml
# 
# - 3093
# 
# httpunit:httpunit
# 
# xerces:xercesImpl
# 
# apache_archiva
# 
# archiva-modules/archiva-web/archiva-webdav/pom.xml
# 
# - 5286
# 
# junit:junit
# 
# org.springframework.boot:spring-boot-starter-web
# 
# VIPJoey_doe
# 
# mmc-dubbo-provider/pom.xml
# 
# - 6432
# 
# net.htmlparser.jericho:jericho-html
# 
# net.sourceforge.htmlunit:htmlunit
# 
# apache_cxf-fediz
# 
# systests/tests/pom.xml
# 
# - 9158
# 
# org.dom4j:dom4j
# 
# org.xmlunit:xmlunit-matchers
# 
# apache_maven-archetype
# 
# archetype-common/pom.xml

# ***Testing framework that not has test|unit***
# com.jayway.restassured:rest-assured
# 
# org.robolectric:robolectric
# 
# io.rest-assured:rest-assured
# 
# jmock:jmock
# 
# org.mockito:mockito-core
# 
# org.assertj:assertj-core

# In[21]:


tolib_log_df = original_df[original_df["toLib"].str.contains("log|slf4j")]

tolib_log_df["repoName"].nunique()


# In[22]:


fromlib_log_df = original_df[original_df["toLib"].str.contains("log|slf4j")]

fromlib_log_df["repoName"].nunique()


# In[23]:


tolib_log_df


# In[24]:


fromlib_log_df


# In[25]:


print(tolib_log_df.index)
print(fromlib_log_df.index)


# In[26]:


for lib in original_df["toLib"].sample(n=500):
    print(lib)


# In[27]:


hard_remove_log_test_repos = (
    set(original_df["repoName"].unique())
    - set(fromlib_log_df["repoName"].unique())
    - set(tolib_log_df["repoName"].unique())
    - set(fromlib_test_df["repoName"].unique())
    - set(tolib_test_df["repoName"].unique())
)
len(hard_remove_log_test_repos)


# In[28]:


# com.jayway.restassured:rest-assured
# org.robolectric:robolectric
# io.rest-assured:rest-assured
# jmock:jmock
# org.mockito:mockito-core
# org.assertj:assertj-core


# In[28]:


fromlib_addition_test_df = original_df[
    original_df["fromLib"].str.contains("rest-assured|robolectric|mock|assert")
]
fromlib_addition_test_df


# In[29]:


tolib_addition_test_df = original_df[
    original_df["toLib"].str.contains("rest-assured|robolectric|mock|assert")
]
tolib_addition_test_df


# In[30]:


hard_remove_log_test_repos = (
    hard_remove_log_test_repos
    - set(fromlib_addition_test_df["repoName"].unique())
    - set(tolib_addition_test_df["repoName"].unique())
)
print(len(hard_remove_log_test_repos))


# In[31]:


hard_remove_log_test_repos


# In[32]:


hard_remove_log_test_df = original_df[
    original_df["repoName"].isin(hard_remove_log_test_repos)
]
hard_remove_log_test_df


# # Insight about number of pair fromLib-toLib per repo

# In[34]:


migration_in_repo = dict(hard_remove_log_test_df["repoName"].value_counts())


# In[35]:


len(list(filter(lambda x: migration_in_repo[x] > 1, migration_in_repo)))


# In[36]:


repo_with_only_one_migration = list(
    filter(lambda x: migration_in_repo[x] == 1, migration_in_repo)
)
repo_with_only_one_migration


# In[37]:


len(repo_with_only_one_migration)


# In[38]:


check = dict(original_df["repoName"].value_counts())
check


# In[39]:


len(list(filter(lambda x: check[x] > 1, check)))


# In[40]:


982 / 1480


# In[41]:


one_df = original_df[original_df["repoName"].isin(repo_with_only_one_migration)]
one_df


# In[42]:


one_df.to_csv("demo.csv", index=False)


# In[43]:


sampled_df = one_df.sample(n=20, random_state=42)
sampled_df


# In[44]:


sampled_df.to_csv("sampled.csv", index=False)


# In[45]:


(one_df["startCommit"] == one_df["endCommit"]).value_counts()


# In[46]:


(sampled_df["startCommit"] == sampled_df["endCommit"]).value_counts()


# In[56]:


original_df["num_migration"] = original_df.groupby("repoName")["repoName"].transform(
    "count"
)
original_df


# In[57]:


original_df["num_migration"]


# In[58]:


13382 / 1480


# In[59]:


check = original_df.drop_duplicates(subset=["repoName"])
check.describe()


# # Check file change

# In[1]:


import pandas as pd

df = pd.read_csv("processed2.csv")
df.head()


# In[ ]:


import subprocess
def read_file_in_commit(repo_dir, rev_path, commit_hash):
    


# In[ ]:


for i in range(len(df)):
    diff_files = df["diff_files"].iloc[i]    
    if pd.isna(diff_files):
        continue
    diff_files = eval(diff_files)
    if diff_files["Renamed"]:
        


# In[1]:


import pandas as pd

df = pd.read_csv("data/sampled_50/tmp3.csv")
df.info()


# In[2]:


df_simplified = df.drop(columns=["diff_files"])
df_simplified.to_csv("methods_20_simplified.csv", index=False)


# In[ ]:





# # New check

# In[3]:


import pandas as pd

df = pd.read_parquet("data/official_original.parquet")
df


# In[35]:


df["repoName"].nunique()


# In[36]:


df["startCommit"].nunique()


# In[37]:


df["endCommit"].nunique()


# In[42]:


df["repo_start_end_commit"] = df.apply(lambda row: row["repoName"] + "__" + row["startCommit"] + "__" + row["endCommit"], axis=1)
df


# In[43]:


df["repo_start_end_commit"].nunique()


# In[44]:


df.info()


# In[47]:


for i in range(len(df) - 1):
    for j in range(i + 1, len(df)):
        if df.iloc[i, 16] == df.iloc[j, 16] and df.iloc[i, 17] != df.iloc[j, 17]:
            print(i, j)


# In[49]:


df.to_csv("official_added_id.csv", index=False)


# In[50]:


unique = df.groupby("repo_start_end_commit").apply(lambda x: x.sample(1, random_state=42))
unique


# In[51]:


unique.info()


# In[52]:


sampled = unique.sample(n=50, random_state=42)
sampled


# In[54]:


sampled.to_csv("sampled_50.csv", index=False)


# # EDA

# In[2]:


import pandas as pd
df = pd.read_csv("data/migrations_36_file.csv")
df.info()


# In[8]:


# How many files changed between two version
lst_num_changed_files = []
for i in range(len(df)):
    num_changed_files = []
    for col in ["java_added", "java_deleted", "java_modified", "java_renamed_unchanged", "java_renamed_modified"]:
        num_changed_files.append(len(eval(df.loc[i, col])))
    lst_num_changed_files.append(num_changed_files)
lst_num_changed_files


# In[36]:


cnt = 0
for num_changed_files in lst_num_changed_files:
    for i in range(5):
        if num_changed_files[i] != 0:
            break
    else:
        cnt += 1
print(cnt)


# In[9]:


total_file_changes = sum([sum(x) for x in lst_num_changed_files])
total_file_changes


# In[10]:


average_file_changes = total_file_changes / len(df)
average_file_changes


# In[41]:


import numpy as np
added, deleted, modified, renamed_unchanged, renamed_modified = np.array(lst_num_changed_files).sum(axis=0)
print("Num java file added:            \t", added,            "      ~\t", "{:.2f}%".format(added / total_file_changes * 100))
print("Num java file deleted:          \t", deleted,          "     ~\t", "{:.2f}%".format(deleted/ total_file_changes * 100))
print("Num java file modified:         \t", modified,         "    ~\t", "{:.2f}%".format(modified / total_file_changes * 100))
print("Num java file renamed_unchanged:\t", renamed_unchanged,        "       ~\t", "{:.2f}%".format(renamed_unchanged / total_file_changes * 100))
print("Num java file renamed_modified: \t", renamed_modified, "     ~\t", "{:.2f}%".format(renamed_modified / total_file_changes * 100))


# In[26]:


import os
data_storage = "/drive1/thieulvd/code-migration"
migrations = os.listdir(data_storage)


# In[34]:


import json
statistic_parsed1 = []
statistic_parsed2 = []
for migration in migrations:
    print(migration)
    level1_parsed1_info = {}
    level1_parsed2_info = {}
    folder = os.path.join(data_storage, migration)
    for x in os.listdir(folder):
        if x.startswith("parsed1"):
            parsed1 = os.path.join(folder, x)
        elif x.startswith("parsed2"):
            parsed2 = os.path.join(folder, x)
        else:
            continue
    for file in os.listdir(parsed1):
        with open(os.path.join(parsed1, file), "r") as f:
            lst = json.load(f)
        for item in lst:
            level1_parsed1_info[item["node_type"]] = level1_parsed1_info.get(item["node_type"], 0) + 1
    for file in os.listdir(parsed2):
        with open(os.path.join(parsed2, file), "r") as f:
            lst = json.load(f)
        for item in lst:
            level1_parsed2_info[item["node_type"]] = level1_parsed2_info.get(item["node_type"], 0) + 1
    statistic_parsed1.append(level1_parsed1_info)
    statistic_parsed2.append(level1_parsed2_info)
    


# In[33]:


statistic_parsed1


# In[37]:


df_parsed1 = pd.DataFrame(statistic_parsed1, columns=["class_declaration", "interface_declaration", "enum_declaration", "record_declaration", "annotation_type_declaration"])
df_parsed1


# In[38]:


df_parsed2 = pd.DataFrame(statistic_parsed2, columns=["class_declaration", "interface_declaration", "enum_declaration", "record_declaration", "annotation_type_declaration"])
df_parsed2


# In[39]:


df_parsed1.describe()


# In[51]:


import json
statistic_parsed1 = []
statistic_parsed2 = []
method_pairs = []
for migration in migrations:
    level1_parsed1_info = {}
    level1_parsed2_info = {}
    folder = os.path.join(data_storage, migration)
    for x in os.listdir(folder):
        if x.startswith("parsed1"):
            parsed1 = os.path.join(folder, x)
        elif x.startswith("parsed2"):
            parsed2 = os.path.join(folder, x)
        else:
            continue
    ver1_classes = []
    for file in os.listdir(parsed1):
        with open(os.path.join(parsed1, file), "r") as f:
            lst = json.load(f)
        for item in lst:
            if (item["file_mode"] == "Modified" or item["file_mode"] == "Renamed-Modified") and (item["class_mode"] == "Modified" or item["class_mode"] == "Renamed-Modified"):
                ver1_classes.append(item)
    for cls in ver1_classes:
        ver2_path = cls["ver2_path"]
        with open(os.path.join(parsed2, ver2_path.replace("/", "--") + ".json"), "r") as f:
            ver2_lst = json.load(f)
        other = None
        for item in ver2_lst:
            if item["ver2_tree_path"] == cls["ver2_tree_path"]:
                other = item
                break
        for ver1_method in cls["methods"]:
            if ver1_method["method_mode"] in ["Modified", "Renamed-Modified"]:
                ver2_method = None
                for method in other["methods"]:
                    if ver1_method["ver2_signature"] == method["ver2_signature"]:
                        ver2_method = method
                        break
                method_pairs.append((ver1_method, ver2_method))
print(len(method_pairs))


# In[53]:


code_only_method_pairs = []
for method_pair in method_pairs:
    code_only_method_pairs.append({
        "ver1": method_pair[0]["definition"],
        "ver2": method_pair[1]["definition"]
    })
x = pd.DataFrame(code_only_method_pairs)
x.head()


# In[54]:


x.describe()


# In[64]:


x.to_csv("/drive2/phatnt/zTrans/thieulvd/methods.csv", index=False)


# In[56]:


from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-base")
tokenizer


# In[65]:


x["len_ver1"] = x["ver1"].apply(lambda code: len(tokenizer(code)["input_ids"]))
x["len_ver2"] = x["ver2"].apply(lambda code: len(tokenizer(code)["input_ids"]))
x


# In[66]:


x.describe()


# In[69]:


print(x[x["len_ver1"] == 51545]["ver1"].iloc[0])


# In[ ]:




