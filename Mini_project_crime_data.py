

import pandas as pd
import numpy as np
import pymysql

import matplotlib.pyplot as plt
import seaborn as sns

import folium




import warnings
warnings.filterwarnings("ignore")


# ## 1. Database Setup and Import :
# 
# - Create a MySQL database.
# 
# - Load the provided crime dataset into the MySQL database.

# ## 2. Database Connection :
# 
#    - Use PyMySQL to establish a connection to the database in Pycharm or VS code.
# 
#    - Verify the successful import of data in pycharm.



conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = "123456789",
    db = 'odin_mini_capstone'
)

try:
    with conn.cursor() as curr:
        query = "SELECT * FROM crime_data"
        curr.execute(query)

        column_names = [column[0] for column in curr.description]
        results = curr.fetchall()

        df = pd.DataFrame(results, columns = column_names)


except pymysql.Error as e:
    print("Error:",e)
finally:
    conn.close()




df.head()


# ## 3. Data Exploration:
# 
#    - Retrieve basic statistics on the dataset, such as the total number of records and unique values in specific columns.
# 
#    - Identify the distinct crime codes and their descriptions.

# ## Basic statistics on the dataset,
# 



df.info()




# Converting the data type of two columns to datetime
df['Date_Rptd'] = pd.to_datetime(df['Date_Rptd'], errors='coerce')
df['DATE_OCC'] = pd.to_datetime(df['DATE_OCC'], errors='coerce')




df.info()




df.nunique()




df.describe()


# ### Distinct crime codes and their descriptions
# 



unique_codes = df[['Crm_Cd','Crm_Cd_Desc']].drop_duplicates()
unique_codes.style.hide()


# ## 4. Temporal Analysis:
# 
#    - Analyze the temporal aspects of the data.
# 
#    - Determine trends in crime occurrence over time.



# Sorting the date columns
sorted_rptd = sorted(df['Date_Rptd'])
sorted_Occ = sorted(df['DATE_OCC'])




# Distribution of Crime Reported Dates

plt.figure(figsize =(15,5))
# sns.distplot(df['Date_Rptd'])
plt.hist(df['Date_Rptd'],bins=10,edgecolor="black")
plt.title('Distribution of Crime Reported Dates')
plt.xlabel('Reported-Date')
plt.xticks(rotation=90)
plt.show()




# Distribution of Crime Occurrence Dates
plt.figure(figsize =(15,5))
plt.hist(df['DATE_OCC'],bins=10,edgecolor="black")
plt.title('Distribution of Crime Occurrence Dates')
plt.xlabel('Occurrence-Date')
plt.xticks(rotation=90)
plt.show()




# Line Chart of Crime Reported Date vs Crime Occurrence Date

plt.figure(figsize =(15,10))
y = sorted_Occ
x = sorted_rptd
plt.plot(x,y)

plt.title('CRIME REPORTED vs CRIME OCCURRED')
plt.xlabel('Reported-Date')
plt.ylabel('Occurrence-Date')
plt.xticks(rotation=45)
plt.grid(True)

plt.show()




df.columns




# Distribution of crime reportedbased on crime code.
plt.figure(figsize=(15, 6))
sns.distplot(df['Crm_Cd'])
plt.title('Distribution of Reported Crimes based on Crime Code')
plt.xlabel('Crime Code')
plt.xticks(rotation=45)
plt.show()




# Count of crime reportedbased on crime code.
plt.figure(figsize=(15, 6))
sns.countplot(df['Crm_Cd'])
plt.title('Count of Reported Crimes based on Crime Code')
plt.xlabel('Crime Code')
plt.ylabel('Count of Reported Crimes')
plt.xticks(rotation=45)
plt.show()


# ## 5. Spatial Analysis:
# 
#    - Utilize the geographical information (Latitude and Longitude) to perform spatial analysis.
# 
#    - Visualize crime hotspots on a map.



df[['LAT','LON']]




# Latitude and Longitude to perform spatial analysis
plt.figure(figsize=(15, 10))
plt.scatter(df['LON'], df['LAT'], color='red', marker='o', s=100)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Latitude and Longitude Data')
plt.grid(True)
plt.show()




df1 = df[['LAT','LON']]




# Visualize crime hotspots on a map.
# Visualizing with Folium
m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=10)
for index, row in df.iterrows():
    folium.Marker([row['LAT'], row['LON']]).add_to(m)


display(m)




# Count of area where crime Reported

plt.figure(figsize=(10, 5))
sns.countplot(x=df['AREA_NAME'])
plt.title('Count of area where crimes Reported')
plt.xlabel('Area Reported')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()




# Count of Locations where crime Reported

plt.figure(figsize=(10, 60))
sns.countplot(y=df['Location'])
plt.title('Count of Locations where crimes Reported')
plt.xlabel('Area Reported')
plt.ylabel('Count')
plt.show()


# ## 6. Victim Demographics:
# 
#    - Investigate the distribution of victim ages and genders.
# 
#    - Identify common premises descriptions where crimes occur.



# Distribution of victim ages and genders.
plt.figure(figsize=(10, 5))
sns.distplot(df['Vict_Age'])
plt.title('Distribution of Victim age')
plt.xlabel('Victim-Age')
plt.show()




# Victim Age Range vs Gender
plt.figure(figsize=(20,10))
sns.boxplot(y = df['Vict_Sex'], x = df['Vict_Age'],orient="h")
plt.title('Range of Victim Age in each Gender')
plt.ylabel('Gender')
plt.ylabel('Age')

plt.show()




# Distribution of Age and Gender
plt.figure(figsize=(10,7))  #width , height
sns.scatterplot(x=df['Vict_Sex'],y=df['Vict_Age'],marker="o",hue=df['Vict_Sex'])
plt.title("Distribution of Victim Ages and Genders ")
plt.ylabel('Age')
plt.xlabel('Gender')
plt.legend(loc='upper right', title='Gender')
plt.grid(linestyle=":")
plt.show()




#Crime rates between different sex
cr = df.groupby(['Vict_Sex']).size()
cr




# Common premises where crimes occur.
plt.figure(figsize=(10, 15))
sns.countplot(y=df['Premis_Desc'])
plt.title('Common Premises Description')
plt.ylabel('Reported-Premises')
plt.xlabel('Count')
plt.show()


# ## 7. Status Analysis:
# 
#    - Examine the status of reported crimes.
# 
#    - Classify crimes based on their current status.



# The status of reported crimes
status_counts =  df['Status'].value_counts()
print("Status of Reported Crimes:")
print(status_counts)




# Crimes based on their current status.
pd.set_option('display.max_rows', None)
status_crime_counts = df.groupby(['Status', 'Crm_Cd_Desc']).size()
print("Classification of Crimes Based on Status:")
print(status_crime_counts)


# ### Q1. Where are the geographical hotspots for reported crimes?

# The geographical hotspots for reported crimes are between Latitude 34 and 34.1 & Longitude -118.30 and -118.20.

# ### Q2. What is the distribution of victim ages in reported crimes?

# The distribution of victim ages in reported crimes is slightly right skewed and majority of age lie between 20 - 55

# ### Q3. Is there a significant difference in crime rates between male and female victims?

# Yes, there is significant difference in crime ratese between male and female there are 155 Female victims and 278 Male victims.

# ### Q4. Where do most crimes occur based on the "Location" column?

# Based on Location column most crimes occur in "800 N ALAMEDA ST" second by "700W 7th St" and looking at Area the "Cental" area is where most crimes occur.

# ### Q5. What is the distribution of reported crimes based on Crime Code?

# The distribution of reported crimes based on Crime Code in Right Skewed with most crime codes being 330 - "BURGLARY FROM VEHICLE" seconded by 624 - "BATTERY - SIMPLE ASSAULT".















