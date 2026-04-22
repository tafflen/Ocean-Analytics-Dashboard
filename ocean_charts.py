import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("ocean_clean.csv")


# ===Block 1 — Line chart: temperature trend across months====

# avg temp per month across all stations
monthly_temp = df.groupby("Month")["Sea_Surface_Temp_C"].mean().round(2)

plt.figure(figsize=(10, 5))
plt.plot(monthly_temp.index, monthly_temp.values, marker="o", color="#1D9E75", linewidth=2)

plt.title("Average sea surface temperature by month")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.xticks(range(1, 13), ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("chart_temp_trend.png")
plt.show()




# ===Block 2 — Bar chart: wave height by station===

wave_by_station = df.groupby("Station")["Wave_Height_m"].mean().round(2).sort_values(ascending=False)

plt.figure(figsize=(10, 5))
bars = plt.bar(wave_by_station.index, wave_by_station.values, color="#378ADD", edgecolor="white")

# add value on top of each bar
for bar, val in zip(bars, wave_by_station.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             str(val), ha="center", va="bottom", fontsize=10)

plt.title("Average wave height by station")
plt.xlabel("Station")
plt.ylabel("Wave height (m)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("chart_wave_station.png")
plt.show()




# ===Block 3 — Line chart: monthly anomaly count (the June spike)===

anomaly_by_month = df[df["Anomaly_Flag"] == "Yes"].groupby("Month_Name")["Anomaly_Flag"].count()

# force correct month order
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
anomaly_by_month = anomaly_by_month.reindex(month_order, fill_value=0)

plt.figure(figsize=(10, 5))
plt.plot(anomaly_by_month.index, anomaly_by_month.values,
         marker="o", color="#D85A30", linewidth=2)

# highlight June
june_val = anomaly_by_month["June"]
plt.annotate(f"June peak: {june_val}",
             xy=("June", june_val),
             xytext=("August", june_val + 2),
             arrowprops=dict(arrowstyle="->", color="black"),
             fontsize=10)

plt.title("Monthly anomaly count — June monsoon spike")
plt.xlabel("Month")
plt.ylabel("Number of anomalies")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("chart_anomaly_spike.png")
plt.show()




# ===Block 4 — Heatmap: temperature across seasons and regions===

pivot = df.pivot_table(
    values="Sea_Surface_Temp_C",
    index="Season",
    columns="Region",
    aggfunc="mean"
).round(2)

# force season order
season_order = ["Winter", "Pre-Monsoon", "Monsoon", "Post-Monsoon"]
pivot = pivot.reindex(season_order)

plt.figure(figsize=(8, 5))
sns.heatmap(pivot,
            annot=True,          # show numbers inside cells
            fmt=".1f",           # 1 decimal place
            cmap="YlOrRd",       # yellow → orange → red (cool to hot)
            linewidths=0.5,
            cbar_kws={"label": "Avg temp (°C)"})

plt.title("Sea surface temperature — season vs region")
plt.xlabel("Region")
plt.ylabel("Season")
plt.tight_layout()
plt.savefig("chart_heatmap.png")
plt.show()




# ===Block 5 — Subplots: all 4 charts in one figure===
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Indian ocean monitoring dashboard — key findings", fontsize=14, fontweight="bold")

# chart 1 - temp trend
monthly_temp = df.groupby("Month")["Sea_Surface_Temp_C"].mean().round(2)
axes[0, 0].plot(monthly_temp.index, monthly_temp.values, marker="o", color="#1D9E75", linewidth=2)
axes[0, 0].set_title("Avg temperature by month")
axes[0, 0].set_xticks(range(1, 13))
axes[0, 0].set_xticklabels(["J","F","M","A","M","J","J","A","S","O","N","D"])
axes[0, 0].grid(axis="y", linestyle="--", alpha=0.5)

# chart 2 - wave height by station
wave_by_station = df.groupby("Station")["Wave_Height_m"].mean().round(2).sort_values(ascending=False)
axes[0, 1].bar(wave_by_station.index, wave_by_station.values, color="#378ADD")
axes[0, 1].set_title("Avg wave height by station")
axes[0, 1].tick_params(axis="x", rotation=30)

# chart 3 - anomaly spike
anomaly_by_month = df[df["Anomaly_Flag"] == "Yes"].groupby("Month_Name")["Anomaly_Flag"].count()
anomaly_by_month = anomaly_by_month.reindex(month_order, fill_value=0)
axes[1, 0].plot(anomaly_by_month.index, anomaly_by_month.values, marker="o", color="#D85A30", linewidth=2)
axes[1, 0].set_title("Monthly anomaly count")
axes[1, 0].tick_params(axis="x", rotation=30)
axes[1, 0].grid(axis="y", linestyle="--", alpha=0.5)

# chart 4 - heatmap
pivot = df.pivot_table(values="Sea_Surface_Temp_C", index="Season", columns="Region", aggfunc="mean").round(2)
pivot = pivot.reindex(["Winter","Pre-Monsoon","Monsoon","Post-Monsoon"])
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", ax=axes[1, 1], linewidths=0.5)
axes[1, 1].set_title("Temp by season & region")

axes[1, 1].set_yticklabels(axes[1, 1].get_yticklabels(), rotation=0)

plt.tight_layout()
plt.savefig("ocean_dashboard_charts.png", dpi=150)
plt.show()

print("All charts saved!")
