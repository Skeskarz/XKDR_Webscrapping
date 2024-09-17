#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[5]:


import requests
import bs4
import pandas as pd

# Initialize an empty DataFrame to store the scraped data from all pages
df_all = pd.DataFrame()

for i in range(1, 514):
    # URL for the NCLT website set for parsing multiple pages
    url = f'https://nclt.gov.in/order-date-wise-search?bench=bXVtYmFp&start_date=MDEvMDcvMjAyNA==&end_date=MTYvMDkvMjAyNA==&page={i}'
    
    # Send a GET request to the URL
    page = requests.get(url)
    
    # Check if the request was successful
    if page.status_code == 200:
        print(f"Request successful for page {i}")
    else:
        print(f"Request failed for page {i}, status code: {page.status_code}")
        continue
    
    # Parse the content using BeautifulSoup and LXML parser
    soup = bs4.BeautifulSoup(page.content, 'lxml') #Using LXML because incase the HTML code might be broken 
    
    # Find the table element
    tables = soup.find('table')
    
    # Ensure that the table exists on the page
    if tables:
        # Get all the header titles
        titles = soup.find_all('th')
        
        # Extract the text of titles
        tables_titles = [title.text.strip() for title in titles]
        
        # Create a new DataFrame with the extracted titles as columns
        df = pd.DataFrame(columns=tables_titles)
        
        # Extract the table row data
        col_data = tables.find_all('tr')
        
        # Loop through the rows and populate the DataFrame
        for row in col_data[1:]:
            row_data = row.find_all('td')
            ind_row = [data.text.strip() for data in row_data]
            
            # Append the row data to the DataFrame
            if len(ind_row) == len(df.columns):
                df.loc[len(df)] = ind_row
        
        # Append the current DataFrame to the main DataFrame
        df_all = pd.concat([df_all, df], ignore_index=True)
        
    else:
        print(f"No table found on page {i}")



# In[23]:


# Display last few rows of the final DataFrame
df_all.tail()


# In[27]:


#Save the dataframe to CSV on the local Storage
df_all.to_csv('C:\\Users\\sharv\\Downloads\\NCLT2.csv', index = False)


# In[ ]:





# In[ ]:





# In[ ]:




