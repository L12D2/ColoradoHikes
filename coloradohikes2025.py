#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 21:09:14 2025

@author: liamthompson

Fun data project to look at some basic stats of mountain elevation from summer 2025 hikes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from scipy.stats import norm

# create mountain df 
data = {
    "Peak": [
        "Bear Peak", "1st and 2nd Flatirons", "Twinsisters Peak", "Black Elk Peak",
        "Flagstaff Mountain", "Mt Sanitas", "Green Mountain", "Mt Neva",
        "Quarter to 5 (unnamed)", "Battle Mountain", "Mt Lady Washington",
        "South Boulder Peak", "Mt Lincoln", "Mt Bross", "Mt Cameron",
        "Mt Democrat", "Grays Peak", "Torrey’s Peak", "The Sawtooth",
        "Mt Bierstadt", "Mt Blue Sky"
    ],
    
    "Elevation_ft": [
        8459, 7191, 11418, 7244,
        6983, 6863, 8148, 12849,
        12290, 12044, 13277,
        8549, 14295, 14178, 14238,
        14152, 14278, 14267, 13786,
        14065, 14265
    ],
    
    "Date": [
        "2024-05-26", "2024-06-16", "2024-06-07", "2024-06-14",
        "2024-05-28", "2024-06-09", "2024-05-31", "2024-06-19",
        "2024-06-19", "2024-06-21", "2024-06-21",
        "2024-06-22", "2024-06-28", "2024-06-28", "2024-06-28",
        "2024-06-28", "2024-07-04", "2024-07-04", "2024-07-12",
        "2024-07-12", "2024-07-12"
    ]
}

df = pd.DataFrame(data)
df["time"] = pd.to_datetime(df["Date"])

# stats.linegress time handling 
df["numeric"] = (df["time"] - df["time"].min()).dt.total_seconds()

print(df)

# slr
fig, ax = plt.subplots(figsize=(10, 7))

# stats of line of best fit 
slope, intercept, r_value, p_value, std_err = stats.linregress(df["numeric"], df["Elevation_ft"])
fitted = slope * df["numeric"] + intercept

#print(p_value)
#print(r_value)
#print(std_err)

plt.scatter(df["time"], df["Elevation_ft"], color = "k", label = "Summit Elevation", s = 75)
plt.plot(df["time"], fitted, color = "green", label = "Line of Best Fit", lw = 3)

plt.xlabel("", size = 15)
plt.ylabel("Elevation (ft)", size = 15)
plt.title("Elevation v. Time", size = 18, fontweight = "bold")

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter(' %b\n %d'))
ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune=None, steps=[1, 2, 3, 4, 5, 6, 7, 10]))

plt.xticks(size = 13)
plt.yticks(size = 13)

# annotate fig 
annotation_text = (
    f"Intercept: {intercept:.2f} ft\n"
    f"R-value: {r_value:.3f}\n"
    f"P-value: {p_value:.3e}"
)

ax.text(0.73, 0.05, annotation_text, transform=ax.transAxes,
        fontsize=13, verticalalignment='bottom',
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white",  alpha=0.8))

plt.legend(fontsize = 13)
plt.tight_layout()
plt.show()

# Hist
fig, ax = plt.subplots(figsize=(10, 7))
counts, bins, _ = plt.hist(df["Elevation_ft"], bins=len(df["Peak"]), 
                           color="green", edgecolor="black", linewidth=1.2)

# normal dist
mean, std = norm.fit(df["Elevation_ft"])
x_vals = np.linspace(df["Elevation_ft"].min(), df["Elevation_ft"].max(), 200)
normal_vals = norm.pdf(x_vals, mean, std) * len(df["Elevation_ft"]) * (bins[1] - bins[0])
plt.axvline(x=mean, color='black', linestyle='--', label='Mean Elevation (ft)')

plt.plot(x_vals, normal_vals, color="blue", lw=2.5, label="Normal Curve")

plt.title("Summit Histogram", size = 18, fontweight = "bold")
plt.xlabel("Elevation (ft)", size = 15)
plt.ylabel("N", size = 15)

plt.xticks(size = 13)
plt.yticks(size = 13)

plt.legend(fontsize=13)
plt.tight_layout()
plt.show()



