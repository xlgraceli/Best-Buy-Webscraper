#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
import pandas as pd
import os
import datetime
import time
from bs4 import BeautifulSoup
from openpyxl import load_workbook


# In[7]:


#creating url
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
url = 'https://www.bestbuy.ca/api/v2/json/search?categoryid=21344&currentRegion=ON&include=facets%2C%20redirects&lang=en-CA&page={}'
pg_num = 1

#containers for the data
name_id = []
salePrice_id = []
regPrice_id = []
custRate_id = []
custReview_id = []

#contains all the data
results = []

today = datetime.date.today().strftime('%y%m%d')


# In[8]:


while True:
    #retrieves new response after loading each page
    response = requests.get(url.format(pg_num), headers=headers)
    data = response.json() #gets the data from the json web
    d = data['products'] #retrieves the data portion that contains 'products'
    
    #extracting required TV info under 'products' (name, sales price, regular price)
    for i in d:
        for key, value in i.items(): 
            if key == 'name':
                name_id.append(value.strip())
            if key == 'salePrice':
                salePrice_id.append(value)
            if key == 'regularPrice':
                regPrice_id.append(value)
            if key == 'customerRating':
                custRate_id.append(value)
            if key == 'customerRatingCount':
                custReview_id.append(value)
    #will load the next page of the website (if applicable)
    if data.get('totalPages') and int(data.get('currentPage')) < int(data.get('totalPages')):
        pg_num += 1
    else:
        break

#prints out the extracted info for the TVs
for name, salePrice, regPrice, custRate, custRev in zip(name_id, salePrice_id, regPrice_id, custRate_id, custReview_id):
    print(name)
    print("Sale Price:", salePrice)
    print("Regular Price:", regPrice)
    print("Customer Rating:", custRate)
    print("Number of Customer Reviews:", custRev)
    print("\n")

for name, salePrice, regPrice, custRate, custReview in zip(name_id, salePrice_id, regPrice_id, custRate_id, custReview_id):
    results.append({'Name': name, 'Sales Price': salePrice, 'Regular Price': regPrice, 'Customer Rating': custRate, 'Number of Customer Reviews': custReview})


######### Storing Data into Excel #########
#creating new Excel spreadsheet
df = pd.DataFrame(results)

#export to excel
excel_file = 'best_buy_scraped.xlsx'  
df.to_excel(excel_file, index=False, sheet_name=today)

print(f'Data saved to {excel_file}')



''' ### Testing ####
filename = 'best_buy_scraped.xlsx'
book = load_workbook(filename)
writer = pd.ExcelWriter(filename, engine='openpyxl') 
writer.book = book

# Step 2: Convert the Excel sheet to a pandas.DataFrame
df = pd.read_excel(filename, sheet_name=today)

# Step 3: Append the new data to the pandas.DataFrame
new_df = pd.DataFrame(results)
df = df.append(new_df, ignore_index=True)

# Step 4: Convert the pandas.DataFrame back to an openpyxl worksheet
writer.sheets = {ws.title: ws for ws in book.worksheets}
df.to_excel(writer, sheet_name=today, index=False)

# Step 5: Save the Excel file
writer.save()

'''



            


# In[ ]:




