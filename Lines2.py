
# ==========================================
# SALES DATA ANALYSIS
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1. Create sales dataset

data = {
    "Product": [
        "Laptop", "Mobile", "Tablet", "Keyboard",
        "Mouse", "Monitor", "Laptop", "Mobile",
        "Tablet", "Keyboard", "Mouse", "Monitor"
    ],

    "Category": [
        "Electronics", "Electronics", "Electronics",
        "Accessories", "Accessories", "Electronics",
        "Electronics", "Electronics", "Electronics",
        "Accessories", "Accessories", "Electronics"
    ],

    "Quantity": [
        5, 10, 8, 20, 30, 6,
        4, 12, 5, 15, 25, 7
    ],

    "Price": [
        50000, 20000, 15000, 1000, 500, 12000,
        50000, 20000, 15000, 1000, 500, 12000
    ],

    "Region": [
        "Chennai", "Bangalore", "Mumbai", "Chennai",
        "Delhi", "Mumbai", "Bangalore", "Chennai",
        "Delhi", "Mumbai", "Chennai", "Bangalore"
    ]
}


# 2. Create DataFrame

df = pd.DataFrame(data)


# 3. Calculate total sales

df["Total_Sales"] = df["Quantity"] * df["Price"]


# 4. Display dataset

print("\nComplete Sales Dataset")
print(df)


# 5. Basic information

print("\nDataset Information")
print(df.info())


# 6. Statistical analysis

print("\nStatistical Summary")
print(df.describe())


# 7. Total revenue

total_revenue = df["Total_Sales"].sum()

print("\nTotal Revenue:", total_revenue)


# 8. Total quantity sold

total_quantity = df["Quantity"].sum()

print("Total Quantity Sold:", total_quantity)


# 9. Average product price

average_price = df["Price"].mean()

print("Average Price:", average_price)


# 10. Highest selling product transaction

highest_sale = df.loc[df["Total_Sales"].idxmax()]

print("\nHighest Sales Transaction")
print(highest_sale)


# 11. Lowest selling product transaction

lowest_sale = df.loc[df["Total_Sales"].idxmin()]

print("\nLowest Sales Transaction")
print(lowest_sale)


# 12. Sales by product

product_sales = df.groupby("Product")["Total_Sales"].sum()

print("\nSales By Product")
print(product_sales)


# 13. Sales by region

region_sales = df.groupby("Region")["Total_Sales"].sum()

print("\nSales By Region")
print(region_sales)


# 14. Sales by category

category_sales = df.groupby("Category")["Total_Sales"].sum()

print("\nSales By Category")
print(category_sales)


# 15. Sort products by revenue

sorted_sales = df.sort_values(
    by="Total_Sales",
    ascending=False
)

print("\nSorted Sales")
print(sorted_sales)


# 16. Filter high-value transactions

high_sales = df[df["Total_Sales"] > 100000]

print("\nHigh Value Transactions")
print(high_sales)


# 17. Filter Chennai sales

chennai_sales = df[df["Region"] == "Chennai"]

print("\nChennai Sales")
print(chennai_sales)


# 18. Calculate average quantity

average_quantity = df["Quantity"].mean()

print("\nAverage Quantity:", average_quantity)


# 19. Calculate standard deviation

sales_std = df["Total_Sales"].std()

print("Sales Standard Deviation:", sales_std)


# 20. Find duplicate records

duplicates = df.duplicated()

print("\nDuplicate Records")
print(df[duplicates])


# 21. Check missing values

print("\nMissing Values")
print(df.isnull().sum())


# 22. Find unique regions

print("\nAvailable Regions")
print(df["Region"].unique())


# 23. Count products

print("\nProduct Count")
print(df["Product"].value_counts())


# 24. Calculate percentage contribution

df["Sales_Percentage"] = (
    df["Total_Sales"] / total_revenue
) * 100

print("\nSales Percentage")
print(df[["Product", "Sales_Percentage"]])


# 25. NumPy calculations

sales_array = np.array(df["Total_Sales"])

print("\nNumPy Operations")
print("Maximum:", np.max(sales_array))
print("Minimum:", np.min(sales_array))
print("Mean:", np.mean(sales_array))
print("Median:", np.median(sales_array))


# 26. Top five transactions

top_five = df.nlargest(5, "Total_Sales")

print("\nTop Five Transactions")
print(top_five)


# 27. Export data to CSV

df.to_csv("sales_report.csv", index=False)

print("\nCSV file exported successfully!")


# 28. Product sales visualization

product_sales.plot(
    kind="bar",
    title="Product Wise Sales"
)

plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# 29. Region sales visualization

region_sales.plot(
    kind="pie",
    autopct="%1.1f%%",
    title="Region Wise Sales"
)

plt.ylabel("")
plt.tight_layout()
plt.show()


# 30. Final report

print("\n========== FINAL SALES REPORT ==========")

print("Total Revenue:", total_revenue)

print("Total Products:", df["Product"].nunique())

print("Total Transactions:", len(df))

print("Best Performing Region:", region_sales.idxmax())

print("Best Performing Product:", product_sales.idxmax())

print("Average Transaction Value:", df["Total_Sales"].mean())

print("\nAnalysis Completed!")
