#!/usr/bin/env python
# coding: utf-8

# # Scraping basics for Selenium
# 
# If you feel comfortable with scraping, you're free to skip this notebook.

# ## Part 0: Imports
# 
# Import what you need to use Selenium, and start up a new Chrome to use for scraping. You might want to copy from the [Selenium snippets](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-snippets/) page.
# 
# **You only need to do `driver = webdriver.Chrome()` once,** every time you do it you'll open a new Chrome instance. You'll only need to run it again if you close the window (or want another Chrome, for some reason).

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd


# In[2]:


driver = webdriver.Chrome()


# In[ ]:





# ## Part 1: Scraping by class
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-class.html, printing out the title, subhead, and byline.

# In[3]:


driver.get("http://jonathansoma.com/lede/static/by-class.html")
title = driver.find_element_by_class_name("title").text.strip()
subhead = driver.find_element_by_class_name("subhead").text.strip()
byline = driver.find_element_by_class_name("byline").text.strip()
print(f'{title}\n{subhead}\n{byline}')
    


# In[ ]:





# In[ ]:





# ## Part 2: Scraping using tags
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-tag.html, printing out the title, subhead, and byline.

# In[4]:


driver.get("http://jonathansoma.com/lede/static/by-tag.html")
title = driver.find_element_by_tag_name("h1").text.strip()
subhead = driver.find_element_by_tag_name("h3").text.strip()
byline = driver.find_element_by_tag_name("p").text.strip()
print(f'{title}\n{subhead}\n{byline}')


# In[ ]:





# In[ ]:





# ## Part 3: Scraping using a single tag
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-list.html, printing out the title, subhead, and byline.
# 
# > **This will be important for the next few:** if you scrape multiples, you have a list. Even though it's Seleninum, you can use things like `[0]`, `[1]`, `[-1]` etc just like you would for a normal list.

# In[5]:


driver.get("http://jonathansoma.com/lede/static/by-list.html")
info = driver.find_element_by_tag_name("body").text.strip()
print(info)


# In[ ]:





# In[ ]:





# ## Part 4: Scraping a single table row
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, printing out the title, subhead, and byline.

# In[6]:


driver.get("http://jonathansoma.com/lede/static/single-table-row.html")
info = driver.find_element_by_tag_name("tr")
print(info.find_elements_by_tag_name("td")[0].text.strip())
print(info.find_elements_by_tag_name("td")[1].text.strip())
print(info.find_elements_by_tag_name("td")[2].text.strip())


# In[7]:


#or
driver.get("http://jonathansoma.com/lede/static/single-table-row.html")
info = driver.find_elements_by_tag_name("td")
for item in info:
    print(item.text.strip())


# In[ ]:





# ## Part 5: Saving into a dictionary
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, saving the title, subhead, and byline into a single dictionary called `book`.
# 
# > Don't use pandas for this one!

# In[8]:


driver.get("http://jonathansoma.com/lede/static/single-table-row.html")
info = driver.find_element_by_tag_name("tr")
title = info.find_elements_by_tag_name("td")[0].text.strip()
subhead = info.find_elements_by_tag_name("td")[1].text.strip()
byline = info.find_elements_by_tag_name("td")[2].text.strip()

book = {'title' : title, 
        'subhead' : subhead, 
        'byline' : byline}


# In[9]:


book


# In[ ]:





# ## Part 6: Scraping multiple table rows
# 
# Scrape the content at http://jonathansoma.com/lede/static/multiple-table-rows.html, printing out each title, subhead, and byline.
# 
# > You won't use pandas for this one, either!

# In[10]:


driver.get("http://jonathansoma.com/lede/static/multiple-table-rows.html")

books = []
rows = driver.find_elements_by_tag_name("tr")

for row in rows:
    title = row.find_elements_by_tag_name("td")[0].text.strip()
    subhead = row.find_elements_by_tag_name("td")[1].text.strip()
    byline = row.find_elements_by_tag_name("td")[2].text.strip()
    print(f'{title}\n{subhead}\n{byline}')
    print("~*~")


# In[ ]:





# In[ ]:





# ## Part 7: Scraping an actual table
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a list of dictionaries.
# 
# > Don't use pandas here, either!

# In[11]:


driver.get("http://jonathansoma.com/lede/static/the-actual-table.html")

books = []
rows = driver.find_elements_by_tag_name("tr")

for row in rows:
    title = row.find_elements_by_tag_name("td")[0].text.strip()
    subhead = row.find_elements_by_tag_name("td")[1].text.strip()
    byline = row.find_elements_by_tag_name("td")[2].text.strip()
    
    books.append({'title' : title, 
        'subhead' : subhead, 
        'byline' : byline})
    
print(books)


# In[ ]:





# In[ ]:





# In[ ]:





# ## Part 8: Scraping multiple table rows into a list of dictionaries
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a pandas DataFrame.
# 
# > There are two ways to do this one! One uses just pandas, the other one uses the result from Part 7.

# In[12]:


df = pd.DataFrame(books)


# In[ ]:





# In[ ]:





# ## Part 9: Scraping into a file
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html and save it as `output.csv`

# In[13]:


driver.get("http://jonathansoma.com/lede/static/the-actual-table.html")

books = []
rows = driver.find_elements_by_tag_name("tr")

for row in rows:
    title = row.find_elements_by_tag_name("td")[0].text.strip()
    subhead = row.find_elements_by_tag_name("td")[1].text.strip()
    byline = row.find_elements_by_tag_name("td")[2].text.strip()
    
    books.append({'title' : title, 
        'subhead' : subhead, 
        'byline' : byline})
    
    

df = pd.DataFrame(books)
df.to_csv(r'/Users/shaneburke/Desktop/Data Foundations/scraping_basics_output.csv')


# In[ ]:





# In[ ]:




