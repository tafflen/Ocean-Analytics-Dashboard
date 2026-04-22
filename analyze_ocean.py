import pandas as pd

df = pd.read_csv("ocean_raw_data.csv")

#// Block-1
print(df.shape)        # how many rows & columns
print(df.columns.tolist())  # all column names
print(df.head(3))      # first 3 rows

# //Block-2
print(df.info())     # shows column names, data types, and how many non-null values
print(df.describe())    # shows min, max, mean, std for every number column
print(df.isnull().sum())   # counts missing values per column


# //Block-3
# Q1: show only rows where Region is "Bay of Bengal"
bob = df[df["Region"] == "Bay of Bengal"]
print(bob.shape)   # how many rows are from Bay of Bengal?

# Q2: which rows have an anomaly?
anomalies = df[df["Anomaly_Flag"] == "Yes"]
print(anomalies[["Date", "Station", "Sea_Surface_Temp_C", "Wave_Height_m"]])

# Q3: top 5 highest wave height readings ever recorded
top_waves = df.sort_values("Wave_Height_m", ascending=False).head(5)
print(top_waves[["Date", "Station", "Region", "Wave_Height_m"]])

# Q4: rows where temp is above 30 degrees
hot = df[df["Sea_Surface_Temp_C"] > 30]
print(f"Days above 30°C: {len(hot)}")



# //Block-4
# avg temperature per region
print(df.groupby("Region")["Sea_Surface_Temp_C"].mean().round(2))

# avg wave height per station — sorted highest to lowest
wave_by_station = df.groupby("Station")["Wave_Height_m"].mean().round(2)
print(wave_by_station.sort_values(ascending=False))

# how many anomalies per month?
anomaly_counts = df[df["Anomaly_Flag"] == "Yes"].groupby("Month_Name")["Anomaly_Flag"].count()
print(anomaly_counts.sort_values(ascending=False))

# pivot table — avg temp for each Region × Season
# first add Season column if your data doesn't have it
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Pre-Monsoon"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

df["Season"] = df["Month"].apply(get_season)

pivot = df.pivot_table(values="Sea_Surface_Temp_C", index="Season", columns="Region", aggfunc="mean").round(2)
print(pivot)



# //Block-5
# check before cleaning
print("Before cleaning:")
print(df[["Sea_Surface_Temp_C", "Wave_Height_m", "Salinity_ppt"]].isnull().sum())

# fill missing values with monthly median
# why median and not mean? because mean gets pulled by extreme values (storms, anomalies)
# median is the "middle value" — more stable for ocean data

for col in ["Sea_Surface_Temp_C", "Wave_Height_m", "Salinity_ppt"]:
    df[col] = df.groupby("Month")[col].transform(lambda x: x.fillna(x.median()))

# check after cleaning
print("\nAfter cleaning:")
print(df[["Sea_Surface_Temp_C", "Wave_Height_m", "Salinity_ppt"]].isnull().sum())
# all should show 0 now

# save the clean file — this is what you'll use for all charts tomorrow
df.to_csv("ocean_clean.csv", index=False)
print("\nocean_clean.csv saved! Rows:", len(df))
