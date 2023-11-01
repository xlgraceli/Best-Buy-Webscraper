#!/usr/bin/env python
# coding: utf-8

# # Web Scraper

# In[26]:


#import libraries
import datetime
import time
import requests
from bs4 import BeautifulSoup
import xlwt

"""
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
"""



# In[27]:


#define parameters
containers_id = []
prod_name_id = []
prod_code_id = []
prod_price_id = []
prod_price_current_id = []



# In[28]:


#connecting to website

url = 'https://www.bestbuy.ca/en-ca/category/televisions/21344'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
today = datetime.date.today().strftime('%y%m%d')
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, 'html.parser')



# In[29]:


#main function
def main():
    #containers = soup2.find_all('div', class_='col-xs-12_198le col-sm-4_13E9O col-lg-3_ECF8k x-productListItem productLine_2N9kG')
    try:
        '''
        #create excel document
        xl_book = xlwt.Workbook()
        xl_sheet = xl_book.add_sheet(today)
        xl_row = 0
        xl_sheet.write(xl_row, 0, 'Name')
        xl_sheet.write(xl_row, 0, 'Price')
        xl_row = xl_row + 1
        '''
        
        
        containers_id = soup.find_all('div', {'class': 'col-xs-8_1v0z0 col-sm-12_G_a2r productItemTextContainer_HocvR'})
        
        for items in containers_id:
            #extracting the names
            name = items.find('div', attrs={
                'class': 'productItemName_3IZ3c',          # Elements with class attribute
                'itemprop': 'name',                        # Elements with itemprop attribute
                'data-automation': 'productItemName'       # Elements with data-automation attribute
            }).get_text()
            prod_name_id.append(name)
            print(name)
            
            #extracting the prices
            price = items.find('span', {'class': 'screenReaderOnly_2mubv large_3uSI_'}).get_text()
            prod_price_id.append(price)
            print(price)
            
            
    finally:
        print("There are ", len(prod_price_id), "items")


# In[30]:


#run program
main()


# In[ ]:





# In[ ]:




