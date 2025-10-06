import pandas as pd
import matplotlib.pyplot as mp
import matplotlib.ticker as mt
import xml.etree.ElementTree as ET



## Loading the initial File

DataTree = ET.parse(r'PythonPrograms\DataAnalyst\Pratice2\rows.xml')
DataRoot = DataTree.getroot()
rows = []

for record in DataRoot.findall(".//Record"):
    row = {
        "draw_data": record.findtext("row")
    }
    rows.append(row)


## Creating the Dataset and cleaning the data
DataSet = pd.DataFrame(rows)
DataSet = pd.read_xml(r"PythonPrograms\DataAnalyst\Pratice2\rows.xml", xpath=".//row")
DataSet = DataSet.drop(columns=["row","_id","_uuid","_position","_address"])


## Converting dates to datetime
DataSet["draw_date"] = pd.to_datetime(DataSet["draw_date"])


## Splitting the winning numbers to individual numbers
winningNumbers = DataSet["winning_numbers"].str.split(" ", expand=True)
winningNumbers.columns = [f"num_{i+1}" for i in range(winningNumbers.shape[1])]
DataSet = pd.concat([DataSet, winningNumbers], axis=1)
DataSet[winningNumbers.columns] = DataSet[winningNumbers.columns].apply(pd.to_numeric)



## Console-logged Basic Information

print("Total number of draws:")
results = DataSet["draw_date"].count()
formattedresults = "{:,}".format(results)
print(formattedresults)

print("Date Range:")
print(DataSet["draw_date"].min(), "to", DataSet["draw_date"].max())

print("Average multiplier:")
print(DataSet["multiplier"].mean())


## Graphing percantage of how often a number shows up
num_cols = ["num_1","num_2","num_3","num_4","num_5","num_6"]

all_numbers = pd.unique(DataSet[num_cols].values.ravel())
percent_of_nums = {}

for num in all_numbers:
    appears = DataSet[num_cols].apply(lambda row: num in row.values, axis=1)
    percent_of_nums[num] = appears.mean() * 100

percent_series = pd.Series(percent_of_nums).sort_values(ascending=False)

Data_NumberCount = DataSet[["num_1","num_2","num_3","num_4","num_5","num_6"]].melt(value_name="number")["number"].value_counts()
Data_NumberCount = (Data_NumberCount / Data_NumberCount.sum()) * 100
percent_series.head(10).sort_values().plot(kind="bar")

## Graph settings and Saving
mp.title("Top 10 most common Powerball numbers")
mp.xlabel("Number")
mp.xticks(rotation="horizontal")
mp.ylabel("Percantage of total draws")
mp.ylim(0,100)

mp.savefig("Top_common_Powerball_numbers.png",dpi = 300)


## Saving Cleaned Data format
DataSet.to_csv("cleaned_Powerball_Draws_Data.csv",index=False)
