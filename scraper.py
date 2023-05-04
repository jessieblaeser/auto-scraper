#!/usr/bin/env python
# coding: utf-8

# # Building a scraper for a newsite
# 
# The goal is to get the headline of each article, the author, a link, and the section the article belongs in. For this proof-of-concept, we are going to be scraping [The Oklahoman](https://www.oklahoman.com/) homepage. The output will be saved in ```oklahoman.csv```
# 
# Today's date: May 3, 2023

# In[2]:


import pandas as pd

import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.oklahoman.com/')
soup_doc = BeautifulSoup(response.text)

homepage = soup_doc.find(class_='gnt_cw')

#making our list to loop through using css selector
stories = homepage.select('div a')


# ### The loop below will pull out every headline and href on the page

my_list = []

for story in stories: 
    my_dict = {}
    try:
        my_dict['headline'] = story.text
        my_dict['href'] = story['href']
    except: 
        pass
    my_list.append(my_dict)

len(my_list)

#turn list into df
df = pd.DataFrame(my_list)
df

#clean
df.headline = df.headline.str.strip()


#cleaning dataframe
df.drop(df[df.headline.str.contains('more in', case=False, na=False) | 
  (df.headline == 'Contests')| 
  (df.headline == 'Comics') | 
  (df.headline == 'ENTER NOW!') |
  (df.headline == 'Anniversaries') |
  (df.headline == 'High school reunions')].index, inplace=True)

df = df.reset_index(drop=True)
df

#you can see the df is not perfect, but it's close enough! export below
df.to_csv('oklahoman.csv', index=False)




