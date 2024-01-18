import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns


def CorrectWeatherType(value):
    if value.upper() == "FREEZING RAIN/DRIZZLE":
        return "OTHER"
    elif value.upper() == "FOG/SMOKE/HAZE":
        return "OTHER"
    elif value.upper() == "SLEET/HAIL":
        return "OTHER"
    elif value.upper() == "BLOWING SNOW":
        return "OTHER"
    elif value.upper() == "SEVERE CROSS WIND GATE":
        return "OTHER"
    elif value.upper() == "BLOWING SAND, SOIL, DIRT":
        return "OTHER"
    else:
        return value.upper()


# Categorize accidents based on time ranges
def categorize_time(hour):
    if 5 <= hour <= 8:
        return 'Early Morning'
    elif 9 <= hour <= 12:
        return 'Late Morning'
    elif 13 <= hour <= 17:
        return 'Afternoon'
    elif 18 <= hour <= 21:
        return 'Evening'
    else:
        return 'Night'


""" Takes daata in from a .csv file and reading it into a dataframe"""

# Replace 'input.csv' with the path to your CSV file
csv_file = 'Traffic_Crashes_-_Crashes.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

print("CSV file has been read into the data frame")

""" This part of the code shows the amount of accidents at unique speeds"""

speed_column = 'POSTED_SPEED_LIMIT'

# Filter the data to exclude speeds over 45
filtered_df = df[df[speed_column] <= 45]

# Group the filtered data by speed and count the number of accidents at each speed
speed_counts = filtered_df[speed_column].value_counts().sort_index().reset_index()
speed_counts.columns = [speed_column, 'Accident Count']

# Create the bar chart
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.bar(speed_counts[speed_column], speed_counts['Accident Count'])

# Customize the plot labels and title
plt.xlabel('Speed')
plt.ylabel('Total Number of Accidents')
plt.title('Total Number of Accidents at Unique Speeds (Speed <= 45)')

# Show the plot
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.grid(True, axis='y')  # Show grid lines on the y-axis
print("Speed of Accident graph is done")

"""This section of the code shows the time of day that accidents happened split into 5 distinct time periods as a %"""

# Apply the categorize_time function to create a new 'Time Category' column
df['Time Category'] = df['CRASH_HOUR'].apply(categorize_time)

# Step 3: Count the number of accidents in each category
accident_counts = df['Time Category'].value_counts()

accident_percentages = df['Time Category'].value_counts(normalize=True) * 100

# Define unique colors for each category
colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightblue']

# Step 4: Create a pie chart with unique colors
plt.figure(figsize=(8, 8))
plt.pie(accident_percentages, labels=accident_percentages.index, autopct='%1.1f%%', colors=colors)
plt.title('Accidents by Time of Day (Percentage)')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show the pie chart
print("Crash Hour percentage graph is done")

"""This section of the code shows the number of accidents by different weather conditions"""
df['WEATHER_CONDITION'] = df['WEATHER_CONDITION'].apply(CorrectWeatherType)
weather_counts = df['WEATHER_CONDITION'].value_counts()

# Generate a list of unique colors for each weather condition
unique_colors = plt.cm.viridis(range(len(weather_counts)))

# Step 3: Create a bar graph with unique colors
plt.figure(figsize=(12, 6))
weather_counts.plot(kind='bar', color=unique_colors)
plt.title('Accidents by Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=45)
plt.tight_layout()

print("Weather Condition graph is done")

"""This section produces a geographical heatmap of the accidents that happened """

# Load GeoDataFrame from shapefile
shapefile_path = 'BeatMap.shp'
chicago_beats = gpd.read_file(shapefile_path)

# Assuming 'BEAT_OF_OCCURRENCE' is the correct column in df
beat_counts = df['BEAT_OF_OCCURRENCE'].value_counts().reset_index()
beat_counts.columns = ['beat_num', 'OCCURRENCE_COUNT']

# Convert 'beat_num' column to numeric in chicago_beats
# Remove non-numeric values from 'beat_num' column
chicago_beats = chicago_beats[chicago_beats['beat_num'].str.isnumeric()]

# Convert 'beat_num' column to numeric
chicago_beats['beat_num'] = pd.to_numeric(chicago_beats['beat_num'], errors='coerce')

# Convert 'beat_num' column to numeric in beat_counts
beat_counts['beat_num'] = pd.to_numeric(beat_counts['beat_num'], errors='coerce')

# Merge DataFrames on 'beat_num'
merged_beats = pd.merge(chicago_beats, beat_counts, on='beat_num', how='left')

# Plot the merged GeoDataFrame
merged_beats.plot(column='OCCURRENCE_COUNT', cmap='Blues', legend=True)
plt.title('Chicago Police Beats with Traffic Crash Counts')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
print("Heat map is finished")

"""This section of the code shows the crashes on a per Month from 2013 to 2023"""

# Count the number of crashes at each hour
Month_count = df['CRASH_MONTH'].value_counts().sort_index()

# Plot the bar chart
plt.figure(figsize=(12, 6))
Month_count.plot(kind='bar', color='red')
plt.title('Number of Accidents per Month')
plt.xlabel('Month of the Year')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=0)

print("Crash Month Graph has been made")

"""This section of the code shows the crashes on a per hour of the week from 2013 to 2023"""

# Count the number of crashes at each hour
hour_count = df['CRASH_HOUR'].value_counts().sort_index()

# Plot the bar chart
plt.figure(figsize=(12, 6))
hour_count.plot(kind='bar', color='darkred')
plt.title('Number of Accidents at Each Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=0)

print("Crash Hour Graph has been made")

"""This section of the code shows the crashes on a per day of the week from 2013 to 2023"""

# Count the number of crashes at each hour
day_count = df['CRASH_DAY_OF_WEEK'].value_counts().sort_index()

# Plot the bar chart
plt.figure(figsize=(12, 6))
day_count.plot(kind='bar', color='mediumpurple')
plt.title('Number of Accidents per Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Accidents')
plt.xticks(rotation=0)

print("Crashes per day of week has been made")

"""This section of the code graphs the trend of accidents YoY from 2013 to 2023"""

df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'], format='%m/%d/%Y %I:%M:%S %p')

# Create separate columns for month and year
df['Month'] = df['CRASH_DATE'].dt.month
df['Year'] = df['CRASH_DATE'].dt.year

# Count the number of occurrences for each month and year combination
monthly_counts = df.groupby(['Year', 'Month']).size().reset_index(name='Count')

# Plotting the data
plt.figure(figsize=(12, 7))

# Loop through unique years and plot a line for each year
for year in monthly_counts['Year'].unique():
    year_data = monthly_counts[monthly_counts['Year'] == year]
    plt.plot(year_data['Month'], year_data['Count'], label=str(year))

# Set labels and title
plt.title('Number of Occurrences by Year and Month')
plt.xlabel('Month')
plt.ylabel('Count')

# Show a legend to identify each line with a specific year
plt.legend(title='Year', bbox_to_anchor=(1.005, 1), loc='upper left')

print("YoY accident graph is finished")

"""Seaborn heat map showing correlation between crash type and traffic type"""

# Create a cross-tabulation of the two columns
cross_tab = pd.crosstab(df['CRASH_HOUR'], df['CRASH_DAY_OF_WEEK'])

# Creating the heatmap using Seaborn
plt.figure(figsize=(16, 10))
sns.heatmap(cross_tab, annot=True, cmap="YlGnBu", fmt='g')

# Set labels and title
plt.title('Frequency Matrix of Crash Hours Versus day of the week')
plt.xlabel('Crash Day of the Week')
plt.ylabel('Crash Hour')

print("seaborn heatmap is finished")

"""Creates two graphs of the alignment of crashes that happen and on what kind of street they happen on as well"""

filtered_df = df[(df['POSTED_SPEED_LIMIT'] >= 30) & (df['POSTED_SPEED_LIMIT'] <= 40)]

trafficway_counts = filtered_df['TRAFFICWAY_TYPE'].value_counts()
alignment_counts = filtered_df['ALIGNMENT'].value_counts()

plt.figure(figsize=(12, 12))
trafficway_counts.plot(kind='bar', color='skyblue')
plt.title("Bar Chart of Trafficway Type at Speeds Between 30 and 40 mph")
plt.xlabel("Trafficway Type")
plt.ylabel("Number of Accidents")

plt.figure(figsize=(12, 6))
plt.tick_params(axis='x', labelsize=8)
alignment_counts.plot(kind='bar', color='lightgreen')
plt.title("Bar Chart of Alignment Type at Speeds Between 30 and 40 mph")
plt.xlabel("Alignment Type")
plt.ylabel("Number of Accidents")
# Show the plot

"""Produces a graph that shows the type of Traffic control that is present where an accident occured"""

type_count = df['TRAFFIC_CONTROL_DEVICE'].value_counts()

plt.figure(figsize=(8,8))
type_count.plot(kind='bar', color='green')
plt.title("Type of Traffic Control at Accidents")
plt.xlabel("Traffic Device")
plt.ylabel("Number of Accidents")
print("Graph of Traffic control type is finished")

plt.show()

