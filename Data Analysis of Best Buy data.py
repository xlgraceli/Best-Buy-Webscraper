#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import warnings
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np 


# In[31]:


df = pd.read_csv("/Users/shellyh/Desktop/SQL/best_buy_basedata_all_cleaned.csv")


# In[32]:


#  create the condition colomn
df["Condition"] = "Regular"
df.loc[~df['Open Box'].isna(), 'Condition'] = "Open Box"
df.loc[~df['Refurbished'].isna(), 'Condition'] = "Refurbished"


# In[33]:


df.head(15)


# In[34]:


plt.figure(figsize=(8, 6))
sns.boxplot(x='Condition', y='Discount%', data=df)
plt.xlabel('Condition')
plt.ylabel('Discount%')
plt.title('Boxplot of Discount based on Condition')
plt.show()
grouped_condition = df.groupby('Condition')['Discount%'].describe()
print(grouped_condition)


# In[113]:


non_zero_discount_counts = df[df['Discount%'] != 0].groupby('Date').size()
print(non_zero_discount_counts)

plt.figure(figsize=(8, 6))
non_zero_discount_counts.plot(kind='bar')
plt.xlabel('Date')
plt.ylabel('Count of non-zero discounts')
plt.title('Count of non-zero discounts per day')
plt.xticks(rotation=45)
plt.ylim(500, 630)  

plt.tight_layout()
plt.show()
# for now,周二稍多但是需要从长观察

non_zero_discount = df[df['Discount%'] != 0]

# 绘制Boxplot
plt.figure(figsize=(7, 5))
sns.boxplot(x='Date', y='Discount%', data=non_zero_discount)
plt.xlabel('Date')
plt.ylabel('Discount (non-zero)')
plt.title('Boxplot of non-zero discounts per day')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


grouped_non_zero_discount = non_zero_discount.groupby('Date')['Discount%'].describe()
print(grouped_non_zero_discount)


# In[111]:


brand_counts = df['Brand'].value_counts()

total_count = len(df)
brand_percentages = brand_counts / total_count * 100

# 合并占比小于2%的品牌为"其他"
threshold = 1.0  # 阈值设为2%
other_brands_percentage = brand_percentages[brand_percentages < threshold].sum()
brand_percentages = brand_percentages[brand_percentages >= threshold]
brand_percentages['Other'] = other_brands_percentage
print(brand_percentages)
# 绘制饼状图
plt.figure(figsize=(7, 7))
plt.pie(brand_percentages, labels=brand_percentages.index, autopct='%1.1f%%', startangle=140)
plt.title('Brand Distribution')
plt.show()

brand_avg_prices = df.groupby('Brand')['Regular Price'].mean()

top_brands = brand_counts.nlargest(10)
brand_avg_prices_top = brand_avg_prices[top_brands.index]
colors = plt.cm.viridis(np.arange(len(top_brands))/len(top_brands))

#create a bar chart to describe the top 10 brands by count and their average price
plt.figure(figsize=(8, 5))
plt.bar(top_brands.index, brand_avg_prices_top, color=colors)
plt.xlabel('Brand')
plt.ylabel('Average Price')
plt.title('Top 10 Brands by Count and Average Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(brand_avg_prices_top)

#初创公司，所以只分析前10
# 2000 左右的价格最多？


# In[112]:


brand_avg_discount = df.groupby('Brand')['Discount%'].mean()

top_brands = brand_counts.nlargest(10)
brand_avg_discount_top = brand_avg_discount[top_brands.index]
colors = plt.cm.viridis(np.arange(len(top_brands))/len(top_brands))

#create a bar chart to describe the top 10 brands by count and their average price
plt.figure(figsize=(8, 5))
plt.bar(top_brands.index, brand_avg_discount_top,color = colors)
plt.xlabel('Brand')
plt.ylabel('Average Discount')
plt.title('Top 10 Brands by Count and Average Discount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(brand_avg_discount_top)


# In[89]:


plt.figure(figsize=(10, 6))
scatter = plt.scatter(x= "Number of Customer Reviews", y = "Regular Price", alpha=0.7)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Customer Rating')

plt.xlabel('Number of Customer Reviews')
plt.ylabel('Price')
plt.title('Scatter Plot of Number of Customer Reviews vs. Price')
plt.show()

plt.figure(figsize=(10, 6))
scatter = plt.scatter(num_reviews, price, c=customer_rating, cmap='viridis', alpha=0.7)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Customer Rating')

plt.xlabel('Number of Customer Reviews')
plt.ylabel('Price')
plt.title('Scatter Plot of Number of Customer Reviews vs. Price')
plt.show()


# In[102]:


price = ["Sales Price", "Regular Price",'Number of Customer Reviews','Customer Rating']
Q1 = df[price].quantile(0.25)
Q3 = df[price].quantile(0.75)
IQR = Q3 - Q1

# define a function to remove outliers of sales price and regular price
def remove_outliers(col):
    lower_bound = Q1[col] - 5 * IQR[col]
    upper_bound = Q3[col] + 5 * IQR[col]
    return df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

# remove outliers
for col in price:
    df1 = remove_outliers(col)


# In[108]:


filtered_data = (price < 15000) & (num_reviews < 15000)

num_reviews = df['Number of Customer Reviews']
price = df['Regular Price']
customer_rating = df['Customer Rating']
plt.figure(figsize=(10, 6))
scatter = plt.scatter(num_reviews[filtered_data], price[filtered_data], c=customer_rating[filtered_data], cmap='viridis', alpha=0.7)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Customer Rating')

plt.xlabel('Number of Customer Reviews')
plt.ylabel('Price')
plt.title('Scatter Plot of Number of Customer Reviews vs. Price')
plt.show()


# In[ ]:




