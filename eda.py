#!/usr/bin/env python
# coding: utf-8

# # Init

# In[1]:


import pandas as pd
import numpy as np

seed = 18022004
np.random.seed(seed)


# In[51]:


original_df = pd.read_parquet("official_original.parquet")
original_df


# In[3]:


original_df["repoName"].nunique()


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


# In[29]:


fromlib_addition_test_df = original_df[
    original_df["fromLib"].str.contains("rest-assured|robolectric|mock|assert")
]
fromlib_addition_test_df


# In[30]:


tolib_addition_test_df = original_df[
    original_df["toLib"].str.contains("rest-assured|robolectric|mock|assert")
]
tolib_addition_test_df


# In[31]:


hard_remove_log_test_repos = (
    hard_remove_log_test_repos
    - set(fromlib_addition_test_df["repoName"].unique())
    - set(tolib_addition_test_df["repoName"].unique())
)
print(len(hard_remove_log_test_repos))


# In[32]:


hard_remove_log_test_repos


# In[33]:


hard_remove_log_test_df = original_df[
    original_df["repoName"].isin(hard_remove_log_test_repos)
]
hard_remove_log_test_df


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


# import subprocess
# def read_file_in_commit(repo_dir, rev_path, commit_hash):
    


# In[ ]:


# for i in range(len(df)):
#     diff_files = df["diff_files"].iloc[i]    
#     if pd.isna(diff_files):
#         continue
#     diff_files = eval(diff_files)
#     if diff_files["Renamed"]:
        


# In[ ]:




