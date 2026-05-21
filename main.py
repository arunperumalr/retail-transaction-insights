import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RETAIL_CSV = BASE_DIR / "data_set" / "sample_retail_transactions.csv"
df = pd.read_csv(RETAIL_CSV)

# =========================
# Task 1: Data Preparation
# =========================

print("\nTask 1: Data Preparation")
print("*" * 26)
# Show all columns
pd.set_option("display.max_columns", None)
# Increase display width
pd.set_option("display.width", 1000)
# Full content inside each column without truncation
pd.set_option("display.max_colwidth", None)

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Extract useful date information
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()
df["DayOfWeek"] = df["Date"].dt.day_name()

# Convert Product column from string to list
# Counting products | exploding products into rows
df["Product"] = df["Product"].apply(literal_eval)

print(df.head())
# Reset
pd.reset_option("display.max_columns")
pd.reset_option("display.width")
pd.reset_option("display.max_colwidth")

# =========================
# Task 2: Basic Exploration
# =========================

print("\nTask 2: Basic Exploration")
print("*" * 26)
# Total transactions
print("\nTotal Transactions:", len(df))

# Unique customers
print("\nUnique Customers:", df["Customer_Name"].nunique())

# Top 5 most common products
all_products = df["Product"].explode()

top_products = all_products.value_counts().head(5)

print("\nTop 5 Products")
print("-" * 15)
print(top_products)

# Cities with highest transactions
top_cities = df["City"].value_counts()

print("\nTransactions by City")
print("-" * 21)
print(top_cities)

# =========================
# Task 3: Customer Behaviour
# =========================

print("\nTask 3: Customer Behaviour")
print("*" * 30)
# Average spending by customer category
avg_spending = df.groupby("Customer_Category")["Total_Cost"].mean()

print("\nAverage Spending by Customer Category")
print("-" * 40)
print(avg_spending)

# Preferred payment methods
payment_pref = pd.crosstab(
    df["Customer_Category"],
    df["Payment_Method"]
)

print("\nPayment Preferences")
print("-" * 20)
print(payment_pref)

# Average items per store type
avg_items = df.groupby("Store_Type")["Total_Items"].mean()

print("\nAverage Items per Store Type")
print("-" * 30)
print(avg_items)

# =========================
# Task 4: Promotion & Discount
# =========================
print("\nTask 4: Promotion & Discount")
print("*" * 30)
discount_impact = df.groupby("Discount_Applied")["Total_Cost"].mean()

print("\nDiscount Impact")
print("-" * 20)
print(discount_impact)

promotion_items = df.groupby("Promotion")["Total_Items"].mean()

print("\nAverage Items by Promotion")
print("-" * 30)
print(promotion_items)

promotion_cost = df.groupby("Promotion")["Total_Cost"].mean()

print("\nPromotion Effectiveness")
print("-" * 30)
print(promotion_cost)

# =========================
# Task 5: Seasonality
# =========================

print("\nTask 5: Seasonality")
print("*" * 26)

season_revenue = df.groupby("Season")["Total_Cost"].sum()

print("\nRevenue by Season")
print("-" * 20)
print(season_revenue)

# Average spending per season plot
season_avg = df.groupby("Season")["Total_Cost"].mean()

plt.figure(figsize=(8,5))
season_avg.plot(kind="bar")
plt.title("Average Spending Per Season")
plt.ylabel("Average Cost")
plt.xticks(rotation=0)
plt.show()

# =========================
# Task 6: Visualisations
# =========================

print("\nTask 6: Visualisations")
print("*" * 26)
# Transactions per city
plt.figure(figsize=(10,5))
df["City"].value_counts().plot(kind="bar")
plt.title("Transactions per City")
plt.ylabel("Count")
plt.show()

# Payment method distribution
plt.figure(figsize=(6,6))
df["Payment_Method"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.ylabel("")
plt.title("Payment Method Distribution")
plt.show()

# Monthly revenue trend
monthly_revenue = df.groupby(
    ["Year", "Month"]
)["Total_Cost"].sum()

print("\nMonthly Revenue")
print("*" * 20)
print(monthly_revenue)

# Heatmap revenue by season and customer category
pivot_table = df.pivot_table(
    values="Total_Cost",
    index="Season",
    columns="Customer_Category",
    aggfunc="sum"
)

plt.figure(figsize=(10,6))
sns.heatmap(pivot_table, annot=True, fmt=".0f")
plt.title("Revenue by Season and Customer Category")
plt.show()