#!/usr/bin/env python
# coding: utf-8

# # Texas Cosmetologist Violations
# 
# Texas has a system for [searching for license violations](https://www.tdlr.texas.gov/cimsfo/fosearch.asp). You're going to search for cosmetologists!

# ## Setup: Import what you'll need to scrape the page
# 
# We'll be using Selenium for this, *not* BeautifulSoup and requests.

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

driver = webdriver.Chrome()


# ## Starting your search
# 
# Starting from [here](https://www.tdlr.texas.gov/cimsfo/fosearch.asp), search for **cosmetologist violations** for people with the last name **Nguyen**.

# In[2]:


driver.get("https://www.tdlr.texas.gov/cimsfo/fosearch.asp")

cosmetologist_field = driver.find_element_by_xpath("/html/body/div/div/div[2]/div[1]/div/section/div/div/table/tbody/tr/td/form/table/tbody/tr[3]/td/select/option[10]")
cosmetologist_field.click()

last_name = driver.find_element_by_id("pht_lnm")
last_name.send_keys("Nguyen")

submit_button = driver.find_element_by_xpath("/html/body/div/div/div[2]/div[1]/div/section/div/div/table/tbody/tr/td/form/table/tbody/tr[18]/td/input[1]")
submit_button.click()


# ## Scraping
# 
# Once you are on the results page, do this.

# ### Loop through each result and print the entire row
# 
# Okay wait, that's a heck of a lot. Use `[:10]` to only do the first ten (`listname[:10]` gives you the first ten).

# In[3]:


table = driver.find_element_by_tag_name("tbody")
rows = table.find_elements_by_tag_name("tr")
for row in rows[:10]:
    print(row.text.strip())


# ### Loop through each result and print each person's name
# 
# You'll get an error because the first one doesn't have a name. How do you make that not happen?! If you want to ignore an error, you use code like this:
# 
# ```python
# try:
#    # try to do something
# except:
#    # Instead of stopping on an error, it'll jump down here instead
#    print("It didn't work')
# ```
# 
# It should help you out. If you don't want to print anything, you can type `pass` instead of the `print` statement. Most people use `pass`, but it's also nice to print out debug statements so you know when/where it's running into errors.
# 
# **Why doesn't the first one have a name?**

# In[4]:


for row in rows[:10]:
    try:
        print(row.find_elements_by_class_name("results_text")[0].text.strip())
    except:
        print("it didn't work")
        
        
#First one is the heading


# ## Loop through each result, printing each violation description ("Basis for order")
# 
# > - *Tip: You'll get an error even if you're ALMOST right - which row is causing the problem?*
# > - *Tip: You can get the HTML of something by doing `.get_attribute('innerHTML')` - it might help you diagnose your issue.*
# > - *Tip: Or I guess you could just skip the one with the problem...*

# In[5]:


#got rid of heading and added tenth row

for row in rows[1:11]:
    try:
        print(row.find_elements_by_tag_name("td")[2].text.strip())
        print("~*~*~")
    except:
        print("oops")


# ## Loop through each result, printing the complaint number
# 
# - TIP: Think about the order of the elements

# In[6]:


for row in rows[1:11]:
    try:
        print(row.find_elements_by_class_name("results_text")[5].text.strip())
    except:
        print("it didn't work")


# ## Saving the results
# 
# ### Loop through each result to create a list of dictionaries
# 
# Each dictionary must contain
# 
# - Person's name
# - Violation description
# - Violation number
# - License Numbers
# - Zip Code
# - County
# - City
# 
# Create a new dictionary for each result (except the header).
# 
# > *Tip: If you want to ask for the "next sibling," you can't use `find_next_sibling` in Selenium, you need to use `element.find_element_by_xpath("following-sibling::div")` to find the next div, or `element.find_element_by_xpath("following-sibling::*")` to find the next anything.

# In[7]:


cases = []

for row in rows[1:11]:
    name = row.find_elements_by_class_name("results_text")[0].text.strip()
    description = row.find_elements_by_tag_name("td")[2].text.strip()
    violation_number = row.find_elements_by_class_name("results_text")[5].text.strip()
    license_number = row.find_elements_by_class_name("results_text")[4].text.strip()
    zip_code = row.find_elements_by_class_name("results_text")[3].text.strip()
    county = row.find_elements_by_class_name("results_text")[2].text.strip()
    city = row.find_elements_by_class_name("results_text")[1].text.strip()
    
    cases.append({'name' : name,
                  'description' : description, 
                  'violation number' : violation_number,
                  'license number' : license_number,
                  'zip code' : zip_code,
                  'county' : county,
                  'city' : city})

print(cases)
                  


# ### Save that to a CSV
# 
# - Tip: Use `pd.DataFrame` to create a dataframe, and then save it to a CSV.

# In[8]:


df = pd.DataFrame(cases)

df


# In[9]:


df.to_csv(r'/Users/shaneburke/Desktop/Data Foundations/10-homework/texas_cosmetology_violations.csv', index=False)


# ### Open the CSV file and examine the first few. Make sure you didn't save an extra weird unnamed column.

# In[10]:


csv_check = pd.read_csv("texas_cosmetology_violations.csv")
csv_check.head(10)


# ## Let's do this an easier way
# 
# Use Selenium and `pd.read_html` to get the table as a dataframe.

# In[11]:


new = pd.read_html(driver.page_source)[0]
#Saw page source here: https://stackoverflow.com/questions/45394374/trying-to-scrape-table-using-pandas-from-seleniums-result


# In[12]:


new


# In[ ]:




