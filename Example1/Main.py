import pandas as pd
import json
import matplotlib.pyplot as mp



## Loading the initial Json file
with open(r'PythonPrograms\DataAnalyst\Pratice1\rows.json') as f:
    data = json.load(f)



## Setting the Data as a DataFrame
DataColumns = [col["name"] for col in data["meta"]["view"]["columns"]]
DataRows = data["data"]
Datafile = pd.DataFrame(DataRows,columns=DataColumns)

## Clean DataFrame without unneeded infortmation
Datafile = Datafile.drop(columns=["meta","sid", "id", "position","created_at","created_meta","updated_at","updated_meta"])



## Top 10 Counties by EV Registration's : Bar Chart
top_counties = Datafile["County"].value_counts().head(10)
top_counties.plot(kind="bar", figsize=(10,6))

mp.title("Top 10 counties by EV registrations")
mp.xlabel("Counties")
mp.ylabel("Number of EV's")
mp.tight_layout
mp.savefig("top_10_counties_by_EV_regis.png", dpi=300)


## EV Registration's by Model Year : Line Chart
mp.figure(figsize=(10,6))
num_regist_ModelYear = Datafile.groupby("Model Year").size()
num_regist_ModelYear = num_regist_ModelYear.sort_index()
num_regist_ModelYear.plot(kind="line",mark_right="o")

mp.title("Electric Vehicle Registrations by Model Year")
mp.xlabel("Model Year")
mp.ylabel("Number of EVs Registered")
mp.grid(True)
mp.tight_layout()
mp.savefig("evs_by_model_year.png", dpi=300)


## Console-Logged Basic Information

print("Total EV's registered in Washington State:")
results = Datafile["State"].size
formattedresults = "{:,}".format(results)
print(formattedresults)

print("Top 5 Makes by count:")
print(Datafile["Make"].value_counts().head())

print("Earlist Model Year:")
print(Datafile["Model Year"].min())

print("Newest Model Year:")
print(Datafile["Model Year"].max())

print("Top 10 EV Registrations by County:")
print(Datafile.groupby("County").size().sort_values(ascending=False).head(10))

print("Average Electric Range for Top 5 Makes")
results = Datafile["Electric Range"].value_counts().head().mean()
formattedresults = "{:,}".format(results)
print(formattedresults) 


## CSV File of the clean DataFrame

Datafile.to_csv("cleaned_ev_data.csv",index=False)
