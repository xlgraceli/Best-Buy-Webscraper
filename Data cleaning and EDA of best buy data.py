#!/usr/bin/env python
# coding: utf-8

# In[255]:


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import warnings
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np 


# In[269]:


df = pd.read_excel("/Users/shellyh/Desktop/SQL/best_buy_cleaned.xlsx")

df.head(5)


# In[270]:


df.info()


# In[271]:


df.isnull().sum()


# In[272]:


df.nunique()


# In[273]:


df = df.replace('NaN', pd.NA)


# In[274]:


df['Discount Price'] = df['Regular Price'] - df['Sales Price']
df['Discount%']=df['Discount Price']/df['Regular Price']*100
df['Size'] = df['Size'].str.strip(" ''-")
df['Size'] = df['Size'].astype(float)
df.head(5)


# In[282]:


df['Brand'] = df['Brand'].str.lower().str.strip()
brand_counts = df['Brand'].value_counts()
brand_avg_prices = df.groupby('Brand')['Regular Price'].mean()

top_brands = brand_counts.nlargest(10)
brand_avg_prices_top = brand_avg_prices[top_brands.index]

#create a bar chart to describe the top 10 brands by count and their average price
plt.figure(figsize=(10, 6))
plt.bar(top_brands.index, brand_avg_prices_top)
plt.xlabel('Brand')
plt.ylabel('Average Price')
plt.title('Top 10 Brands by Count and Average Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(brand_counts,brand_avg_prices)


# In[276]:


filtered_df = df[df['Number of Customer Reviews'] <= 15000]

# create a scatter plot to describe the customer rating vs number of customer reviews
plt.figure(figsize=(10, 6))
plt.scatter(filtered_df['Customer Rating'], filtered_df['Number of Customer Reviews'], alpha=0.5)
plt.xlabel('Customer Rating')
plt.ylabel('Number of Customer Reviews')
plt.title('Customer Rating vs Number of Customer Reviews (Number of Reviews <= 15000)')
plt.grid(True)
plt.tight_layout()
plt.show()


# In[277]:


selected_columns = ["Sales Price", "Regular Price", "Customer Rating", "Number of Customer Reviews"]

# Calculate summary statistics for the selected columns
summary_statistics = df[selected_columns].describe()

# Display the summary statistics
print(summary_statistics)


# In[278]:


price = ["Sales Price", "Regular Price"]
Q1 = df[price].quantile(0.25)
Q3 = df[price].quantile(0.75)
IQR = Q3 - Q1

# define a function to remove outliers of sales price and regular price
def remove_outliers(col):
    lower_bound = Q1[col] - 8 * IQR[col]
    upper_bound = Q3[col] + 8 * IQR[col]
    return df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

# remove outliers
for col in price:
    df1 = remove_outliers(col)


# In[279]:


#create a box plot of sales price and regular price after removing outliers 
selected_data = ["Sales Price", "Regular Price"]
plt.figure(figsize=(10, 6))
sns.boxplot(data=df1[selected_data])
plt.title('Boxplot of Sales Price, Regular Price')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.show()


# In[280]:


bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
df['Discount% Range'] = pd.cut(df['Discount%'], bins=bins, labels=labels, include_lowest=True)

# calculate the count of discount% in each interval
discount_counts = df['Discount% Range'].value_counts()

# plot a discount bar chart for intervals
plt.figure(figsize=(10, 6))
plt.bar(discount_counts.index, discount_counts.values)

plt.xlabel('Discount% Range')
plt.ylabel('Count')
plt.title('Discount% Interval Bar Chart')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

