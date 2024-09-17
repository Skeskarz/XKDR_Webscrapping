#!/usr/bin/env python
# coding: utf-8

# Installing and Updating Essential Libraries

# In[49]:


pip install --upgrade beautifulsoup4


# In[54]:


pip install geopandas folium plotly


# Importing Essential Libraries

# In[2]:


import pandas as pd
import bs4 
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


# Store the URL in a variable

# In[3]:


url = 'https://www.census2011.co.in/states.php'


# Acess the containts of the webpage

# In[4]:


HEADER = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})


# Request the webpage

# In[5]:


page = requests.get(url)

print(page)


# Parse the HTML content using BeautifulSoup

# In[6]:


soup = bs4.BeautifulSoup(page.text, 'html.parser')


# Find the 'table' in the HTML code of the web page

# In[7]:


table = soup.find('table')


# In[8]:


table


# Get the column headers for the table, which have 'th' tag

# In[9]:


titles = soup.find_all('th')


# In[10]:


titles


# Get only text by stripping off extra spaces

# In[11]:


tables_titles = [title.text.strip() for title in titles]# Get the column headers


# In[12]:


tables_titles


# Making an empty DataFrame with the extracted column names and store it in the df variable

# In[13]:


df = pd.DataFrame(columns = tables_titles )
df


# Extract the data rows which have the 'tr' code and run a for loop to populate the rows with data points which have 'td' tags, completeing our table

# In[14]:


col_data = table.find_all('tr')
for row in col_data[1:]:
    row_data = row.find_all('td')
    ind_row = [data.text.strip() for data in row_data]
    lenght = len(df)
    df.loc[lenght] = ind_row


# Getting the basic summary of the elements in the data set

# In[15]:


df.info()


# Data Cleaning and converting the necessary variables from object to float to do any further analysis

# In[16]:


df = df.replace(',', '', regex=True)
df = df.replace('%', '', regex=True)


# In[17]:


df['Population'] = df['Population'].astype(float)
df['Increase'] = df['Increase'].astype(float)
df['Area(Km2)'] = df['Area(Km2)'].astype(float)
df['Density'] = df['Density'].astype(float)
df['Literacy'] = df['Literacy'].astype(float)
df['Sex-Ratio'] = df['Sex-Ratio'].astype(float)


# Save the dataframe to local storage in .csv format

# In[18]:


df.to_csv('C:\\Users\\sharv\\Downloads\\Population_ScrappedGrowth17.csv', index = False)


# In[19]:


df.describe()


# Understanding basic distribution and attributes of the data along with basic Exploratory data analysis

# In[20]:


sns.heatmap# Compute the correlation matrix
correlation_matrix = df.corr()

# Visualize the correlation matrix using a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, linewidths=0.5)

# Focus on correlations with population growth
plt.title('Correlation Heatmap for Population Growth and Other Variables')
plt.show()


# Correlation Coefficent between two variables

# In[21]:


correlation = df[['Increase', 'Literacy']].corr().iloc[0, 1]

print(f"Correlation coefficient between Increase and Literacy: {correlation:.2f}")


# In[22]:


# Scatter plot with regression line
plt.figure(figsize=(10, 6))
sns.regplot(x='Increase', y='Literacy', data=df, scatter_kws={'color':'Black'}, line_kws={'color':'red'})
plt.title('Correlation between Growth of Population and Literacy')
plt.xlabel('Increase (%)')
plt.ylabel('Literacy')
plt.grid(True)
plt.show()


# In[23]:


# Plot histograms for numerical columns
df.hist(figsize=(14, 10), bins=30, edgecolor='black')
plt.tight_layout()
plt.show()


# In[24]:


# Pair plot for numerical features
sns.pairplot(df, diag_kind='kde')
plt.show()


# Creating visualisation to understand the elements of the data and its prevelance

# In[25]:


# Load shapefile for India's states (adjust the file path as necessary)
india_map = gpd.read_file(r"C:\Users\sharv\Downloads\External Place\India-State-and-Country-Shapefile-Updated-Jan-2020-master\India_State_Boundary.shp")

# Preview the map data
india_map.plot()
plt.show()


# In[26]:


# Merge the map data (shapefile) with the DataFrame 'df' based on state names from both datasets
merged = india_map.merge(df, how='left', left_on='State_Name', right_on='State')

# Check the merged data
print(merged.head())


# In[27]:


# Filter the DataFrame 'df' to keep only the rows where the 'State' column matches any 'State_Name' in the 'india_map' GeoDataFrame
df = df[df['State'].isin(india_map['State_Name'])]


# In[28]:


# Plotting the population growth heatmap
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
# Plot state boundaries
merged.boundary.plot(ax=ax, linewidth=1)

# Plot the heatmap with a reversed color map (lighter for low values, darker for high values)
merged.plot(column='Increase', cmap='PuBuGn', ax=ax, legend=True,
            legend_kwds={'label': "Population Growth (%)",
                         'orientation': "horizontal"})

# Adding data labels for literacy rate
for idx, row in merged.iterrows():
    plt.text(row['geometry'].centroid.x, row['geometry'].centroid.y, 
             f"{row['Increase']:.0f}", fontsize=8, color='Black',
             ha='center', va='center', weight='bold')
    
#Gviing the title and showing the ouput
plt.title('Population Growth by State in India')
plt.show()


# Comparison of Population Growth between two regions

# In[29]:


# Filter the DataFrame to include only 'North' and 'South'
df_filtered = df[df['State'].isin(['Bihar', 'Kerala'])]

# Sort the DataFrame by Population Growth for better visualization
df_sorted = df_filtered.sort_values(by='Increase', ascending=False)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Bar plot for Population Growth
bars = ax.bar(df_sorted['State'], df_sorted['Increase'], color='Purple')

# Add data labels
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', va='bottom', ha='center')

# Set title and labels
plt.title('Population Growth by State (Bihar and Kerala)', fontsize=14)
plt.xlabel('State', fontsize=12)
plt.ylabel('Population Growth (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate region names if needed

# Show the plot
plt.tight_layout()
plt.show()


# In[30]:


# Plotting the population growth heatmap
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Set background color to white
ax.set_facecolor('white')

# Plot state boundaries
merged.boundary.plot(ax=ax, linewidth=1, edgecolor='black')

# Plot the heatmap with a reversed color map (lighter for low values, darker for high values)
merged.plot(column='Literacy', cmap='Reds', ax=ax, legend=True,
            legend_kwds={'label': "Literacy Rate",
                         'orientation': "horizontal",
                         'shrink': 0.6},  # Shrinking the legend to fit better
            edgecolor='white')  # Boundary color inside the map

# Adding data labels for literacy rate
for idx, row in merged.iterrows():
    plt.text(row['geometry'].centroid.x, row['geometry'].centroid.y, 
             f"{row['Literacy']:.0f}", fontsize=8, color='Blue',
             ha='center', va='center', weight='bold')

# Set title with black text
plt.title('Literacy Rate by State in India', color='black')

# Show the plot
plt.show()


# In[31]:


# Plotting the population growth heatmap
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Plot state boundaries
merged.boundary.plot(ax=ax, linewidth=1)


# Plot the heatmap with a reversed color map (lighter for low values, darker for high values)
merged.plot(column='Density', cmap='twilight_r', ax=ax, legend=True,
            legend_kwds={'label': "Population Density (per Km²)",
                         'orientation': "horizontal"})
# Adding data labels for Density 
for idx, row in merged.iterrows():
    plt.text(row['geometry'].centroid.x, row['geometry'].centroid.y, 
             f"{row['Density']:.0f}", fontsize=6, color='Black',
             ha='center', va='center', weight='bold')

#Showing the output
plt.title('Population Density by State in India')
plt.show()


# In[32]:


fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Set background color to white
ax.set_facecolor('white')

# Plot state boundaries
merged.boundary.plot(ax=ax, linewidth=1, edgecolor='black')

# Plot the heatmap for Sex-Ratio with a color map (lighter for low values, darker for high values)
merged.plot(column='Sex-Ratio', cmap='viridis_r', ax=ax, legend=True,
            legend_kwds={'label': "Sex Ratio",
                         'orientation': "horizontal",
                         'shrink': 0.6},  # Shrinking the legend to fit better
            edgecolor='white')  # Boundary color inside the map

# Adding data labels for Sex Ratio
for idx, row in merged.iterrows():
    plt.text(row['geometry'].centroid.x, row['geometry'].centroid.y, 
             f"{row['Sex-Ratio']:.0f}", fontsize=8, color='Blue',
             ha='center', va='center', weight='bold')

# Set title with black text
plt.title('Sex Ratio by State in India', color='black')

# Show the plot
plt.show()


# Saving the analysis and changes done to a new csv inroder to retain the orginal scrapped file

# In[33]:


df.to_csv('C:\\Users\\sharv\\Downloads\\Population_ScrappedGrowth18.csv', index = False)


# Importing the newly saved csv as input for further analysis

# In[34]:


df = pd.read_csv('C:\\Users\\sharv\\Downloads\\Population_ScrappedGrowth18.csv')


# In[35]:


df.head()


# Classifying states to their respective regions to do a regionwise analysis and visualization 

# In[36]:


# Dictionary to map states to their specific regions
region_mapping = {
    "Uttar Pradesh": "North", "Bihar": "North", "Madhya Pradesh": "North", "Rajasthan": "North", 
    "Punjab": "North", "Haryana": "North", "Delhi": "North", "Uttarakhand": "North", 
    "Himachal Pradesh": "North", "Jammu and Kashmir": "North", "Chandigarh": "North",
    
    "Andhra Pradesh": "South", "Tamil Nadu": "South", "Karnataka": "South", 
    "Kerala": "South", "Puducherry": "South", "Lakshadweep": "South", "Andaman and Nicobar Islands": "South",
    
    "West Bengal": "East", "Orissa": "East", "Jharkhand": "East", "Assam": "East", 
    "Tripura": "East", "Meghalaya": "East", "Manipur": "East", "Nagaland": "East", 
    "Arunachal Pradesh": "East", "Sikkim": "East", "Chhattisgarh": "East", "Mizoram": "East",
    
    "Gujarat": "West", "Maharashtra": "West", "Goa": "West", "Dadra and Nagar Haveli": "West", "Daman and Diu": "West"
}

# Create a new column "Region" based on the mapping
df['Region'] = df['State'].map(region_mapping)


# In[37]:


df['Region'].value_counts()


# The code calculates and converts percentage values into decimals to derive actual population figures based on the given percentages.

# In[38]:


# Calculate the increase percentage as a decimal and store it in a new column 'Increase_percent'
df['Increase_percent'] = df['Increase']/100

# Calculate the change in population based on the increase percentage and store it in a new column 'Change in Population'
df['Change in Population'] = df['Population']* df['Increase_percent']

# Convert literacy percentage to a decimal and store it in a new column 'Literacy_Percent'
df['Literacy_Percent'] = df['Literacy']/100

# Calculate the literate population based on the total population and literacy percentage, and store it in a new column 'Literate Population'
df['Literate Population'] = (df['Population']/100) * df['Literacy_Percent']


# In[39]:


df.head()


# This code Calculates the total area of Each region (North, South, East, West)

# In[40]:


# Calculate the Total Regional Area
region_area_sum = df.groupby('Region')['Area(Km2)'].sum().reset_index()
region_area_sum.rename(columns={'Area(Km2)': 'Total Regional Area'}, inplace=True)

# Merge the total regional area back to the original DataFrame
df = df.merge(region_area_sum, on='Region', how='left')


# The code Calculates the Sex ratio for each region ( contains a error rectified further down)

# In[41]:


df['Number of Girls'] = (df['Sex-Ratio'] / (1000 + df['Sex-Ratio'])) * df['Population']


# In[56]:


# Sum the total number of girls for each region
region_girls_sum = df.groupby('Region')['Number of Girls'].sum().reset_index()
region_girls_sum.rename(columns={'Number of Girls': 'Total Regional Girls'}, inplace=True)


# (Error Recitified further down)

# In[57]:


# Merge the regional girls sum with the original DataFrame to get the regional totals
df = pd.merge(df, region_girls_sum, on='Region')

# Calculate the regional sex ratio
region_totals = df.groupby('Region').agg({
    'Population': 'sum',
    'Total Regional Girls': 'sum'
}).reset_index()
region_totals['Regional Sex Ratio'] = (region_totals['Total Regional Girls'] / (region_totals['Population'] - region_totals['Total Regional Girls'])) * 1000

# Merge the regional sex ratio back into the original DataFrame
df = pd.merge(df, region_totals[['Region', 'Regional Sex Ratio']], on='Region', how='left')


# The code Sums all the Population, The change in Population and the Literate Population for each state and groups it by their region

# In[68]:


# Group the DataFrame by 'Region' and sum the 'Population' for each region, resetting the index to create a new DataFrame
region_population_sum = df.groupby('Region')['Population'].sum().reset_index()

# Rename the 'Population' column to 'Total Regional Population' in the newly created DataFrame for clarity
region_population_sum.rename(columns={'Population': 'Total Regional Population'}, inplace=True)

#Similar code as above but with respect to Change in Population
region_change_population_sum = df.groupby('Region')['Change in Population'].sum().reset_index()
region_change_population_sum.rename(columns={'Change in Population': 'Total Regional Change in Population'}, inplace=True)

#Similar code as above but with respect to Literate Population
region_literate_population_sum = df.groupby('Region')['Literate Population'].sum().reset_index()
region_literate_population_sum.rename(columns={'Literate Population': 'Total Regional Literate Population'}, inplace=True)


# Merge the aggregated data back to the original DataFrame
df = df.merge(region_population_sum, on='Region', how='left')
df = df.merge(region_change_population_sum, on='Region', how='left')
df = df.merge(region_literate_population_sum, on='Region', how='left')


# In[59]:


df.head()


# The below code Creates New Variables that show the Density of Population in each reagion, the Growth Percent of Population in each region and the Litercy proportion in Each Region

# In[69]:


df['Regional Density'] = df['Total Regional Population'] / df['Total Regional Area']
df['Regional PopGrowth Percent' ] = (df['Total Regional Change in Population'] / df['Total Regional Population'])*100
df['Regional Literacy Level' ] = (df['Total Regional Literate Population'] / df['Total Regional Population'])*100


# In[ ]:





# In[71]:


df.head()


# In[63]:


df.describe()


# The code Below Calulates the Regional Sex-Ratio

# In[72]:


# Calculate the number of men in each region
df['Total Regional Men'] = df['Total Regional Population'] - df['Total Regional Girls']

# Calculate the sex ratio (number of girls per 1000 men)
df['Regional Sex Ratio'] = (df['Total Regional Girls'] / df['Total Regional Men']) * 1000


# In[73]:


df.head()


# The below Line Saves the new added variables to a csv file in local storage

# In[74]:


df.to_csv('C:\\Users\\sharv\\Downloads\\Population_ScrappedGrowth18.csv', index = False)


# The below section will create a seprate dataframe with just the Regional data for simplicity of analysis and drop the state and other duplicate columns

# In[75]:


# Drop columns that are not needed for the final DataFrame
columns_to_keep = [
    'Region', 'Total Regional Area', 'Total Regional Girls', 'Regional Sex Ratio', 'Total Regional Population', 'Total Regional Change in Population', 
    'Total Regional Literate Population', 'Regional Density', 'Regional PopGrowth Percent'
]

# Create the new DataFrame with aggregated regional data
unique_region_df = df[columns_to_keep].drop_duplicates().reset_index(drop=True)

print(unique_region_df)


# In[76]:


unique_region_df.head()


# Saves the new file to a separate csv file in the local storage

# In[77]:


unique_region_df.to_csv('C:\\Users\\sharv\\Downloads\\Regionwise_Censusdata5.csv', index = False)


# Below codes plot graphs of comparing each region (North, South, East, West) in different elements (Population Growth, Sex-ratio, Population Density)

# In[78]:


# Sort the DataFrame by Population Growth for better visualization
df_sorted = unique_region_df.sort_values(by='Regional PopGrowth Percent', ascending=False)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Bar plot for Population Growth
bars = ax.bar(df_sorted['Region'], df_sorted['Regional PopGrowth Percent'], color='skyblue')

# Add data labels
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', va='bottom', ha='center')

# Set title and labels
plt.title('Population Growth by Region', fontsize=14)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Population Growth', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate region names if needed

# Show the plot
plt.tight_layout()
plt.show()


# In[79]:


# Sort the DataFrame by Population Growth for better visualization
df_sorted = unique_region_df.sort_values(by='Regional Density', ascending=False)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Bar plot for Population Growth
bars = ax.bar(df_sorted['Region'], df_sorted['Regional Density'], color='Green')

# Add data labels
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', va='bottom', ha='center')

# Set title and labels
plt.title('Regional Density by Region', fontsize=14)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Regional Density', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate region names if needed

# Show the plot
plt.tight_layout()
plt.show()


# In[80]:


# Sort the DataFrame by Population Growth for better visualization
df_sorted = unique_region_df.sort_values(by='Regional Sex Ratio', ascending=False)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Bar plot for Population Growth
bars = ax.bar(df_sorted['Region'], df_sorted['Regional Sex Ratio'], color='Yellow')

# Add data labels
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', va='bottom', ha='center')

# Set title and labels
plt.title('Regional Sex Ratio', fontsize=14)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Regional Sex Ratio', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate region names if needed

# Show the plot
plt.tight_layout()
plt.show()


# The below code comapares Population Growth of two Regions

# In[81]:


# Filter the DataFrame to include only 'North' and 'South'
df_filtered = unique_region_df[unique_region_df['Region'].isin(['North', 'South'])]

# Sort the DataFrame by Population Growth for better visualization
df_sorted = df_filtered.sort_values(by='Regional PopGrowth Percent', ascending=False)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Bar plot for Population Growth
bars = ax.bar(df_sorted['Region'], df_sorted['Regional PopGrowth Percent'], color='Purple')

# Add data labels
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', va='bottom', ha='center')

# Set title and labels
plt.title('Population Growth by Region (North and South)', fontsize=14)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Population Growth (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Rotate region names if needed

# Show the plot
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




