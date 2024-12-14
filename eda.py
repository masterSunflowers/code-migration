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

# In[2]:


import pandas as pd

df = pd.read_parquet("official_original.parquet")
df


# In[3]:


df["repoName"].nunique()


# In[4]:


df["startCommit"].nunique()


# In[5]:


df["endCommit"].nunique()


# In[6]:


df["repo_start_end_commit"] = df.apply(lambda row: row["repoName"] + "__" + row["startCommit"] + "__" + row["endCommit"], axis=1)
df


# In[7]:


df["repo_start_end_commit"].nunique()


# In[8]:


df.info()


# In[9]:


# for i in range(len(df) - 1):
#     for j in range(i + 1, len(df)):
#         if df.iloc[i, 16] == df.iloc[j, 16] and df.iloc[i, 17] != df.iloc[j, 17]:
#             print(i, j)


# In[10]:


df.to_csv("official_added_id.csv", index=False)


# In[11]:


unique = df.groupby("repo_start_end_commit").apply(lambda x: x.sample(1, random_state=42))
unique


# In[12]:


unique.info()


# In[13]:


unique.head()


# In[15]:


unique.reset_index(drop=True, inplace=True)
unique


# In[16]:


new_data = pd.DataFrame({
    "repo_start_end_commit": unique["repo_start_end_commit"],
    "repo_name": unique["repoName"],
    "start_commit": unique["startCommit"],
    "end_commit": unique["endCommit"]
})
new_data


# In[17]:


new_data.to_csv("new_data_tmp.csv", index=False)


# In[18]:


df


# In[35]:


def get_info(repo_name: str, start_commit: str, end_commit: str, df: pd.DataFrame):
    records = df[(df["repoName"] == repo_name) & (df["startCommit"] == start_commit) & (df["endCommit"] == end_commit)]
    # print(records.info())
    if records.empty:
        raise Exception("No lib changes")
    migration_info = {
        "start_commit_changes": records.iloc[0]["startCommitChanges"],
        "end_commit_changes": records.iloc[0]["endCommitChanges"],
        "start_commit_message": records.iloc[0]["startCommitMessage"],
        "end_commit_message": records.iloc[0]["endCommitMessage"],
        "start_commit_time": records.iloc[0]["startCommitTime"],
        "end_commit_time": records.iloc[0]["endCommitTime"],
    }
    lib_pairs = []
    for _, record in records.iterrows():
        lib_pairs.append({
            "from_lib": record["fromLib"],
            "to_lib": record["toLib"],
            "pom_file": record["fileName"],
            "category": record["Category"]
        })
    migration_info["lib_pairs"] = lib_pairs
    return migration_info
        


# In[36]:


new_data["migration_info"] = new_data.apply(lambda row: get_info(row["repo_name"], row["start_commit"], row["end_commit"], df), axis=1)
new_data


# In[37]:


new_data.to_csv("new_data.csv", index=False)


# In[38]:


cnt = 0
for _, row in new_data.iterrows():
    cnt += len(row["migration_info"]["lib_pairs"])
print(cnt)


# In[39]:


print(len(df))


# In[40]:


new_data.rename(columns={"repo_start_end_commit": "id"}, inplace=True)
new_data


# In[41]:


new_data.to_csv("new_data.csv", index=False)


# In[42]:


sum(new_data["start_commit"] == new_data["end_commit"])


# In[ ]:


import os
repo_storage = "/drive1/phatnt/zTrans/data/repos"
for _, row in new_data.iterrows():
    repo_dir = os.path.join(repo_storage, row["repo_name"])
    cmd = f"cd {repo_dir}"

