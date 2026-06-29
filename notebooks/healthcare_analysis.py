import pandas as pd
import numpy as np

# ── LOAD DATA ──────────────────────────────────────────────────
claims   = pd.read_csv("data/claims.csv", parse_dates=["service_date"])
patients = pd.read_csv("data/patients.csv")
providers= pd.read_csv("data/providers.csv")

print(f"Loaded {len(claims):,} claims")

# ── KEY METRICS ────────────────────────────────────────────────

total_billed  = claims["billed_amount"].sum()
total_paid    = claims["paid_amount"].sum()
denial_rate   = (claims["claim_status"] == "Denied").mean() * 100
avg_los       = claims["length_of_stay"].mean()

# The :, adds commas to big numbers. .2f = 2 decimal places
print(f"Total Billed  : ${total_billed:,.2f}")
print(f"Total Paid    : ${total_paid:,.2f}")
print(f"Denial Rate   : {denial_rate:.1f}%")
print(f"Avg Stay      : {avg_los:.1f} days")

# ── CLEANING ───────────────────────────────────────────────────

# 1. Fill missing denial reasons
#    (only denied claims have a reason — others are blank/null)
#    We replace blank with "N/A" so it doesn't cause errors
claims["denial_reason"] = claims["denial_reason"].fillna("N/A")

# 2. Check for duplicate claim IDs (there shouldn't be any)
dupes = claims.duplicated(subset=["claim_id"]).sum()
print(f"Duplicate claims: {dupes}")   # should be 0

# 3. Add helper columns we'll need for analysis
claims["year"]  = claims["service_date"].dt.year          # extract year
claims["month"] = claims["service_date"].dt.to_period("M").astype(str)  # "2023-04"

# Group ages into bands: 18–30, 31–45, etc.
claims["age_band"] = pd.cut(
    claims["patient_age"],
    bins=[0, 30, 45, 60, 75, 100],
    labels=["18–30", "31–45", "46–60", "61–75", "75+"]
)

print("✅ Cleaning complete!")

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")  # makes charts look clean

# ── CHART 1: Claim Status Pie Chart ────────────────────────────
status_counts = claims["claim_status"].value_counts()

plt.figure(figsize=(6, 6))           # size of the chart
plt.pie(
    status_counts,                   # the numbers
    labels=status_counts.index,      # the labels (Approved, Denied, etc.)
    autopct="%1.1f%%",               # show percentages
    colors=["#2ecc71", "#e74c3c", "#f39c12"]  # green, red, orange
)
plt.title("Claim Status Distribution", fontweight="bold")
plt.savefig("visuals/01_claim_status.png")   # saves the image
plt.show()                                    # displays it
print("✅ Chart 1 saved!")

# ── CHART 2: Denial Rate by Diagnosis ─────────────────────────
denial_by_diag = (
    claims.groupby("diagnosis_name")
    .apply(lambda x: (x["claim_status"] == "Denied").mean() * 100)
    .sort_values(ascending=True)   # ascending=True puts highest at top in horizontal bar
    .reset_index(name="denial_rate")
)

fig, ax = plt.subplots(figsize=(10, 6))

# barh = horizontal bar chart (h = horizontal)
# color_palette creates a gradient of colors from green to red
bars = ax.barh(
    denial_by_diag["diagnosis_name"],
    denial_by_diag["denial_rate"],
    color=sns.color_palette("RdYlGn_r", len(denial_by_diag))
)
ax.set_xlabel("Denial Rate (%)", fontsize=11)
ax.set_title("Claim Denial Rate by Diagnosis", fontweight="bold", fontsize=13)

# Add % labels at end of each bar
for bar in bars:
    ax.text(
        bar.get_width() + 0.2,               # just to the right of the bar
        bar.get_y() + bar.get_height() / 2,  # vertically centered
        f"{bar.get_width():.1f}%",           # show like "21.3%"
        va="center", fontweight="bold", fontsize=9
    )

plt.tight_layout()
plt.savefig("visuals/02_denial_by_diagnosis.png", bbox_inches="tight")
plt.show()
print("✅ Chart 2 saved!")

# ── CHART 3: Monthly Claims Volume & Paid Amount Trend ───────
monthly = (
    claims.groupby("month")
    .agg(
        claim_count=("claim_id", "count"),      # count rows per month
        total_paid=("paid_amount", "sum")        # sum paid amounts per month
    )
    .reset_index()
)

fig, ax1 = plt.subplots(figsize=(14, 5))

# ax2 = second y-axis on the RIGHT side of the chart
# twinx() means "share the same x-axis but have a separate y-axis"
ax2 = ax1.twinx()

# Line chart on left axis (blue) — claim count
ax1.plot(
    monthly["month"],
    monthly["claim_count"],
    color="#3498db", linewidth=2, marker="o", markersize=4,
    label="# Claims"
)

# Bar chart on right axis (orange) — paid amount
ax2.bar(
    monthly["month"],
    monthly["total_paid"] / 1e6,
    alpha=0.3,          # alpha=0.3 makes bars semi-transparent so line shows through
    color="#e67e22",
    label="Paid ($M)"
)

ax1.set_xlabel("Month")
ax1.set_ylabel("Number of Claims", color="#3498db")
ax2.set_ylabel("Paid Amount ($M)", color="#e67e22")
ax1.set_title("Monthly Claims Volume & Paid Amount Trend", fontweight="bold", fontsize=13)

# Only show every 4th month label so they don't overlap
step = max(1, len(monthly) // 12)
ax1.set_xticks(range(0, len(monthly), step))
ax1.set_xticklabels(
    [monthly["month"].iloc[i] for i in range(0, len(monthly), step)],
    rotation=45, ha="right"
)

plt.tight_layout()
plt.savefig("visuals/03_monthly_trend.png", bbox_inches="tight")
plt.show()
print("✅ Chart 3 saved!")

# ── CHART 4: Average Approved Claim Cost by Specialty ───────
specialty_cost = (
    claims[claims["claim_status"] == "Approved"]   # filter: only approved
    .groupby("specialty")["paid_amount"].mean()     # average paid per specialty
    .sort_values(ascending=False)                   # highest first
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 6))
palette = sns.color_palette("Blues_d", len(specialty_cost))

bars = ax.barh(
    specialty_cost["specialty"],
    specialty_cost["paid_amount"],
    color=palette[::-1]   # [::-1] reverses the color list so darkest = longest bar
)
ax.set_xlabel("Average Paid Amount ($)")
ax.set_title("Average Approved Claim Cost by Specialty", fontweight="bold", fontsize=13)

# Format x axis numbers with dollar signs and commas
import matplotlib.ticker as mticker
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
)

# Add $ labels at end of each bar
for bar in bars:
    ax.text(
        bar.get_width() + 200,
        bar.get_y() + bar.get_height() / 2,
        f"${bar.get_width():,.0f}",
        va="center", fontsize=9
    )

plt.tight_layout()
plt.savefig("visuals/04_cost_by_specialty.png", bbox_inches="tight")
plt.show()
print("✅ Chart 4 saved!")

# ── CHART 5: Top Denial Reasons ───────────────────────────────
denial_reasons = (
    claims[claims["claim_status"] == "Denied"]   # only denied claims
    ["denial_reason"]                             # just the denial_reason column
    .value_counts()                               # count each reason
    .head(6)                                      # top 6 reasons only
    .reset_index()
)
denial_reasons.columns = ["reason", "count"]

fig, ax = plt.subplots(figsize=(10, 5))
palette = sns.color_palette("OrRd", len(denial_reasons))

bars = ax.barh(
    denial_reasons["reason"],
    denial_reasons["count"],
    color=palette[::-1]
)
ax.set_title("Top Denial Reasons", fontweight="bold", fontsize=13)
ax.set_xlabel("Number of Denied Claims")

# Add count labels at end of each bar
for bar in bars:
    ax.text(
        bar.get_width() + 5,
        bar.get_y() + bar.get_height() / 2,
        str(int(bar.get_width())),   # convert to integer so no decimals
        va="center", fontsize=9
    )

plt.tight_layout()
plt.savefig("visuals/05_denial_reasons.png", bbox_inches="tight")
plt.show()
print("✅ Chart 5 saved!")

# ── CHART 6: Average Approved Claim Cost by Age Band ───────
age_cost = (
    claims[claims["claim_status"] == "Approved"]
    .groupby("age_band", observed=True)["paid_amount"].mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(
    age_cost["age_band"].astype(str),    # convert age_band to string for x axis
    age_cost["paid_amount"],
    color=sns.color_palette("YlOrRd", len(age_cost))   # yellow to red gradient
)
ax.set_title("Average Approved Claim Cost by Age Band", fontweight="bold", fontsize=13)
ax.set_xlabel("Age Band")
ax.set_ylabel("Average Paid Amount ($)")
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
)

# Add $ labels on top of each bar
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 100,
        f"${bar.get_height():,.0f}",
        ha="center", va="bottom", fontsize=9
    )

plt.tight_layout()
plt.savefig("visuals/06_cost_by_age.png", bbox_inches="tight")
plt.show()
print("✅ Chart 6 saved!")

# ── FINAL SUMMARY TABLE ──────────────────────────────────────
print("\n🎉 ALL CHARTS SAVED in visuals/ folder!")
print("\n── SUMMARY BY DIAGNOSIS ──")
summary = (
    claims.groupby("diagnosis_name")
    .agg(
        total_claims  = ("claim_id",       "count"),
        total_billed  = ("billed_amount",  "sum"),
        denial_rate   = ("claim_status",   lambda x: f"{(x=='Denied').mean()*100:.1f}%"),
    )
    .sort_values("total_billed", ascending=False)
    .reset_index()
)
print(summary.to_string(index=False))
summary.to_csv("reports/claims_summary.csv", index=False)
print("\n✅ Summary saved to reports/claims_summary.csv")