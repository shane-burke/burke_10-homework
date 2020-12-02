#!/usr/bin/env python
# coding: utf-8

# ## Logging on
# 
# Use Selenium to visit https://webapps1.chicago.gov/buildingrecords/ and accept the agreement.
# 
# > Think about when you use `.find_element_...` and when you use `.find_elementSSS_...`

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
#get_ipython().system('pip install html5lib')
import html5lib

import pandas as pd

driver = webdriver.Chrome()


# In[2]:


driver.get("https://webapps1.chicago.gov/buildingrecords/")

agree = driver.find_elements_by_name("agreement")[0]
agree.click()

submit = driver.find_element_by_id("submit")
submit.click()


# ## Searching
# 
# Search for **400 E 41ST ST**.

# In[3]:


address_search = driver.find_element_by_id("fullAddress")
address_search.send_keys("400 E 41ST ST")

submit = driver.find_element_by_id("submit")
submit.click()


# ## Saving tables with pandas
# 
# Use pandas to save a CSV of all **permits** to `Permits - 400 E 41ST ST.csv`. Note that there are **different sections of the page**, not just one long permits table.

# In[4]:


building_permits = pd.read_html(driver.page_source, flavor='html5lib')[0]


# In[5]:


building_permits.head(10)


# ## Saving tables the long way
# 
# Save a CSV of all DOB inspections to `Inspections - 400 E 41ST ST.csv`, but **you also need to save the URL to the inspection**. As a result, you won't be able to use pandas, you'll need to use a loop and create a list of dictionaries.
# 
# You can use Selenium (my recommendation) or you can feed the source to BeautifulSoup. You should have approximately 157 rows.
# 
# You'll probably need to find the table first, then the rows inside, then the cells inside of each row. You'll probably use lots of list indexing. I might recommend XPath for finding the table.
# 
# *Tip: If you get a "list index out of range" error, it's probably due to an issue involving `thead` vs `tbody` elements. What are they? What are they for? What's in them? There are a few ways to troubleshoot it.*

# In[6]:


dob_inspections = []

table_body = driver.find_elements_by_tag_name("tbody")[2]
rows = table_body.find_elements_by_tag_name("tr")

for row in rows:
    inspection_number = row.find_elements_by_tag_name("td")[0].text.strip()
    inspection_date = row.find_elements_by_tag_name("td")[1].text.strip()
    status = row.find_elements_by_tag_name("td")[2].text.strip()
    type_description = row.find_elements_by_tag_name("td")[3].text.strip()
    url = row.find_elements_by_tag_name("a")[0].get_attribute("href")
     
    dob_inspections.append({'inspection number' : inspection_number, 
                            'inspection date' : inspection_date, 
                            'status' : status,
                            'type description' : type_description,
                            'url' : url})

    
#print(dob_inspections)

#Found out how to get the href text in a link with this:
#https://stackoverflow.com/questions/19664253/selenium-how-to-get-the-content-of-href-within-some-targeted-class
#Could have also made an f string of the link format by piping INSP#


# In[7]:


inspections_df = pd.DataFrame(dob_inspections)

inspections_df.to_csv("Inspections - 400 E 41ST ST.csv", index=False)

inspections_df.head(10)


# ### Loopity loops
# 
# > If you used Selenium for the last question, copy the code and use it as a starting point for what we're about to do!
# 
# If you click the inspection number, it'll open up a new window that shows you details of the violations from that visit. Count the number of violations for each visit and save it in a new column called **num_violations**.
# 
# Save this file as `Inspections - 400 E 41ST ST - with counts.csv`.
# 
# Since it opens in a new window, we have to say "Hey Selenium, pay attention to that new window!" We do that with `driver.switch_to.window(driver.window_handles[-1])` (each window gets a `window_handle`, and we're just asking the driver to switch to the last one.). A rough sketch of what your code will look like is here:
# 
# ```python
# # Click the link that opens the new window
# 
# # Switch to the new window/tab
# driver.switch_to.window(driver.window_handles[-1])
# 
# # Do your scraping in here
# 
# # Close the new window/tab
# driver.close()
# 
# # Switch back to the original window/tab
# driver.switch_to.window(driver.window_handles[0])
# ```
# 
# You'll want to play around with them individually before you try it with the whole set - the ones that pass are very different pages than the ones with violations! There are a few ways to get the number of violations, some easier than others.

# In[8]:


dob_inspections_with_count = []

table_body = driver.find_elements_by_tag_name("tbody")[2]
rows = table_body.find_elements_by_tag_name("tr")

for row in rows:
    inspection_number = row.find_elements_by_tag_name("td")[0].text.strip()
    inspection_date = row.find_elements_by_tag_name("td")[1].text.strip()
    status = row.find_elements_by_tag_name("td")[2].text.strip()
    type_description = row.find_elements_by_tag_name("td")[3].text.strip()
    url = row.find_elements_by_tag_name("a")[0].get_attribute("href")
    
    url_element = row.find_elements_by_tag_name("a")[0]
    
    num_violations = 0
    if status == "FAILED":
        url_element.click()
        driver.switch_to.window(driver.window_handles[-1])
        try:
            table_body = driver.find_elements_by_tag_name("tbody")[0]
            table_rows = table_body.find_elements_by_tag_name("tr")
            num_violations = len(table_rows)
        except: 
            num_violations = 0
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    dob_inspections_with_count.append({'inspection number' : inspection_number, 
                            'inspection date' : inspection_date, 
                            'status' : status,
                            'type description' : type_description,
                            'number of violations' : num_violations,
                            'url' : url})

driver.close()


# In[9]:


dob_inspections_with_count[0:5]


# In[10]:


inspections_with_count_df = pd.DataFrame(dob_inspections_with_count)


# In[11]:


inspections_with_count_df.head(10)


# In[ ]:





# In[ ]:




