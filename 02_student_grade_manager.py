
# ==========================================
# SALES FORECASTING AND ANALYSIS SYSTEM
# ==========================================

import pandas as pd
import numpy as np
from datetime import datetime


# ------------------------------------------
# SAMPLE HISTORICAL SALES DATA
# ------------------------------------------

sales_data = {

    "Month": [

        "Jan", "Feb", "Mar", "Apr",

        "May", "Jun", "Jul", "Aug",

        "Sep", "Oct", "Nov", "Dec"

    ],

    "Sales": [

        1200, 1350, 1400, 1500,

        1600, 1550, 1700, 1800,

        1750, 1900, 2100, 2200

    ]

}


# ------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------

df = pd.DataFrame(sales_data)


# ------------------------------------------
# DISPLAY HISTORICAL DATA
# ------------------------------------------

def display_history():

    print("\n========== HISTORICAL SALES ==========")

    print(df.to_string(index=False))


# ------------------------------------------
# TOTAL SALES
# ------------------------------------------

def calculate_total_sales():

    total = df["Sales"].sum()

    print("\nTotal Sales:", total)

    return total


# ------------------------------------------
# AVERAGE SALES
# ------------------------------------------

def calculate_average_sales():

    average = df["Sales"].mean()

    print("\nAverage Sales:", round(average, 2))

    return average


# ------------------------------------------
# HIGHEST SALES
# ------------------------------------------

def highest_sales():

    index = df["Sales"].idxmax()

    month = df.loc[index, "Month"]

    sales = df.loc[index, "Sales"]

    print("\nHighest Sales Month:", month)

    print("Highest Sales:", sales)


# ------------------------------------------
# LOWEST SALES
# ------------------------------------------

def lowest_sales():

    index = df["Sales"].idxmin()

    month = df.loc[index, "Month"]

    sales = df.loc[index, "Sales"]

    print("\nLowest Sales Month:", month)

    print("Lowest Sales:", sales)


# ------------------------------------------
# MONTHLY GROWTH
# ------------------------------------------

def calculate_growth():

    df["Growth"] = df["Sales"].pct_change() * 100

    print("\n========== MONTHLY GROWTH ==========")

    print(df[["Month", "Sales", "Growth"]])


# ------------------------------------------
# MOVING AVERAGE
# ------------------------------------------

def moving_average():

    df["Moving_Average"] = (

        df["Sales"].rolling(window=3).mean()

    )

    print("\n========== MOVING AVERAGE ==========")

    print(df[["Month", "Sales", "Moving_Average"]])


# ------------------------------------------
# SIMPLE LINEAR FORECAST
# ------------------------------------------

def linear_forecast():

    x = np.arange(len(df))

    y = df["Sales"].values

    slope, intercept = np.polyfit(x, y, 1)

    future_months = np.arange(12, 24)

    predictions = slope * future_months + intercept

    predictions = np.maximum(predictions, 0)

    forecast_df = pd.DataFrame({

        "Month_Number": future_months + 1,

        "Forecast_Sales": predictions

    })

    print("\n========== NEXT 12 MONTHS FORECAST ==========")

    print(forecast_df.round(2).to_string(index=False))

    return predictions


# ------------------------------------------
# MAPE CALCULATION
# ------------------------------------------

def calculate_mape(actual, predicted):

    actual = np.array(actual)

    predicted = np.array(predicted)

    valid = actual != 0

    if not np.any(valid):

        return None

    errors = (

        np.abs(

            (actual[valid] - predicted[valid])

            / actual[valid]

        )

    ) * 100

    mape = np.mean(errors)

    return mape


# ------------------------------------------
# FORECAST ACCURACY
# ------------------------------------------

def calculate_accuracy(mape):

    if mape is None:

        print("MAPE cannot be calculated.")

        return

    accuracy = 100 - mape

    print("\nMAPE:", round(mape, 2), "%")

    print("Forecast Accuracy:", round(accuracy, 2), "%")


# ------------------------------------------
# TRAIN TEST SPLIT
# ------------------------------------------

def test_forecast():

    train = df["Sales"].iloc[:9].values

    actual = df["Sales"].iloc[9:].values

    x_train = np.arange(len(train))

    slope, intercept = np.polyfit(

        x_train,

        train,

        1

    )

    x_test = np.arange(9, 12)

    predicted = slope * x_test + intercept

    predicted = np.maximum(predicted, 0)

    print("\n========== FORECAST VS ACTUAL ==========")

    comparison = pd.DataFrame({

        "Month": df["Month"].iloc[9:].values,

        "Actual": actual,

        "Predicted": predicted.round(2)

    })

    print(comparison.to_string(index=False))

    mape = calculate_mape(actual, predicted)

    calculate_accuracy(mape)


# ------------------------------------------
# DEMAND CLASSIFICATION
# ------------------------------------------

def classify_demand():

    average = df["Sales"].mean()

    print("\n========== DEMAND CLASSIFICATION ==========")

    for index, row in df.iterrows():

        if row["Sales"] > average * 1.2:

            category = "High Demand"

        elif row["Sales"] < average * 0.8:

            category = "Low Demand"

        else:

            category = "Normal Demand"

        print(row["Month"], ":", category)


# ------------------------------------------
# INVENTORY RECOMMENDATION
# ------------------------------------------

def inventory_recommendation():

    average = df["Sales"].mean()

    safety_stock = average * 0.2

    lead_time = 2

    reorder_point = (

        (average / 30) * lead_time

        + safety_stock

    )

    print("\n========== INVENTORY RECOMMENDATION ==========")

    print("Average Monthly Demand:", round(average, 2))

    print("Safety Stock:", round(safety_stock, 2))

    print("Lead Time:", lead_time, "months")

    print("Reorder Point:", round(reorder_point, 2))


# ------------------------------------------
# SALES TREND
# ------------------------------------------

def sales_trend():

    first = df["Sales"].iloc[0]

    last = df["Sales"].iloc[-1]

    if last > first:

        print("\nSales Trend: Increasing")

    elif last < first:

        print("\nSales Trend: Decreasing")

    else:

        print("\nSales Trend: Stable")


# ------------------------------------------
# EXPORT DATA
# ------------------------------------------

def export_data():

    df.to_csv("sales_analysis.csv", index=False)

    print("\nData exported successfully!")


# ------------------------------------------
# MAIN APPLICATION
# ------------------------------------------

def main():

    while True:

        print("\n========== SALES FORECASTING SYSTEM ==========")

        print("1. Display Historical Sales")

        print("2. Total Sales")

        print("3. Average Sales")

        print("4. Highest Sales")

        print("5. Lowest Sales")

        print("6. Monthly Growth")

        print("7. Moving Average")

        print("8. Forecast Next 12 Months")

        print("9. Test Forecast Accuracy")

        print("10. Demand Classification")

        print("11. Inventory Recommendation")

        print("12. Sales Trend")

        print("13. Export CSV")

        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            display_history()

        elif choice == "2":

            calculate_total_sales()

        elif choice == "3":

            calculate_average_sales()

        elif choice == "4":

            highest_sales()

        elif choice == "5":

            lowest_sales()

        elif choice == "6":

            calculate_growth()

        elif choice == "7":

            moving_average()

        elif choice == "8":

            linear_forecast()

        elif choice == "9":

            test_forecast()

        elif choice == "10":

            classify_demand()

        elif choice == "11":

            inventory_recommendation()

        elif choice == "12":

            sales_trend()

        elif choice == "13":

            export_data()

        elif choice == "0":

            print("Exiting application...")

            break

        else:

            print("Invalid option!")


if __name__ == "__main__":

    main()
