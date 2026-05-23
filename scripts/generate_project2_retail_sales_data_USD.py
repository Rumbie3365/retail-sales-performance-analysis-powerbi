"""
Project 2: Retail Sales Performance Analysis
Synthetic Sales Data Generator - USD Version

Purpose:
    Generates a safe, synthetic retail sales dataset for a data analyst portfolio project.
    The dataset is designed for Excel, SQL Server / T-SQL and Power BI dashboard practice.

Currency:
    USD ($)

Data source note:
    This dataset is synthetic and was generated for portfolio use.
    It does not contain real customers, real transactions, or private company data.

Outputs:
    data/Fact_Sales.csv
    data/Dim_Product.csv
    data/Dim_Customer.csv
    data/Dim_Date.csv
    data/Sales_Targets.csv
    data/Returns.csv
    data/Monthly_Summary.csv
    data/Category_Summary.csv
    data/Province_Summary.csv
    data/Channel_Summary.csv
    data/Segment_Summary.csv

How to run:
    1. Install Python 3.
    2. Install packages:
       pip install pandas numpy
    3. Run:
       python generate_project2_retail_sales_data_USD.py
"""

from __future__ import annotations

import random
from pathlib import Path
from datetime import timedelta

import numpy as np
import pandas as pd


SEED = 42
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"
NUMBER_OF_ORDERS = 1000
NUMBER_OF_CUSTOMERS = 500

OUTPUT_ROOT = Path("project2_sales_analysis_generated_USD")
DATA_DIR = OUTPUT_ROOT / "data"

random.seed(SEED)
np.random.seed(SEED)


def choose_weighted(options: list[str], weights: list[float]) -> str:
    """Return one option based on weighted probabilities."""
    return random.choices(options, weights=weights, k=1)[0]


def clean_currency(value: float) -> float:
    """Round currency values to two decimals."""
    return round(float(value), 2)


def make_date_dimension(start_date: str, end_date: str) -> pd.DataFrame:
    """Create a date dimension table for Power BI relationships."""
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    dim_date = pd.DataFrame({"Date": dates})
    dim_date["Year"] = dim_date["Date"].dt.year
    dim_date["Quarter"] = "Q" + dim_date["Date"].dt.quarter.astype(str)
    dim_date["Month_No"] = dim_date["Date"].dt.month
    dim_date["Month_Name"] = dim_date["Date"].dt.strftime("%B")
    dim_date["YearMonth"] = dim_date["Date"].dt.strftime("%Y-%m")
    dim_date["Week_Number"] = dim_date["Date"].dt.isocalendar().week.astype(int)
    dim_date["Day_Name"] = dim_date["Date"].dt.strftime("%A")
    dim_date["Is_Weekend"] = dim_date["Day_Name"].isin(["Saturday", "Sunday"])

    return dim_date


def build_dataset() -> dict[str, pd.DataFrame]:
    """Build all fact and dimension tables."""

    products = [
        ("P1001", "Laptop Pro 14", "Technology", "Laptops", 679, 469, 2022, "PrimeSource"),
        ("P1002", "Laptop Lite 13", "Technology", "Laptops", 489, 352, 2021, "Apex Supply Co"),
        ("P1003", "Business Laptop 15", "Technology", "Laptops", 599, 419, 2022, "PrimeSource"),
        ("P1004", "Chromebook Edu", "Technology", "Laptops", 299, 224, 2021, "MetroTrade"),
        ("P1005", "Wireless Mouse", "Technology", "Accessories", 10, 5, 2020, "Apex Supply Co"),
        ("P1006", "Keyboard Combo", "Technology", "Accessories", 24, 13, 2020, "MetroTrade"),
        ("P1007", "USB-C Dock", "Technology", "Accessories", 85, 54, 2023, "PrimeSource"),
        ("P1008", "External SSD 1TB", "Technology", "Storage", 75, 48, 2022, "TechDirect"),
        ("P1009", "HDMI Cable", "Technology", "Accessories", 6, 3, 2019, "TechDirect"),
        ("P1010", "A4 Copy Paper Box", "Office Supplies", "Paper & Stationery", 25, 15, 2019, "OfficeHub"),
        ("P1011", "Premium Notebook", "Office Supplies", "Paper & Stationery", 5, 2.5, 2019, "OfficeHub"),
        ("P1012", "Ballpoint Pen Pack", "Office Supplies", "Paper & Stationery", 4, 2, 2019, "OfficeHub"),
        ("P1013", "Printer Toner Black", "Office Supplies", "Printing", 65, 44, 2020, "PrintWell"),
        ("P1014", "Ink Cartridge Colour", "Office Supplies", "Printing", 30, 19, 2020, "PrintWell"),
        ("P1015", "Desk Organiser", "Office Supplies", "Desk Accessories", 13, 7, 2021, "OfficeHub"),
        ("P1016", "Stapler Heavy Duty", "Office Supplies", "Desk Accessories", 9, 4.5, 2019, "OfficeHub"),
        ("P1017", "Lever Arch File Pack", "Office Supplies", "Filing", 8, 4, 2019, "PaperPro"),
        ("P1018", "Whiteboard Marker Set", "Office Supplies", "Presentation", 8, 4, 2020, "PaperPro"),
        ("P1019", "Ergonomic Chair", "Furniture", "Chairs", 145, 95, 2021, "FurniCo"),
        ("P1020", "Office Desk 1200mm", "Furniture", "Desks", 189, 129, 2020, "FurniCo"),
        ("P1021", "Boardroom Table", "Furniture", "Tables", 459, 318, 2022, "FurniCo"),
        ("P1022", "Filing Cabinet 4 Drawer", "Furniture", "Storage", 109, 69, 2020, "SteelWorks"),
        ("P1023", "Bookshelf 5 Tier", "Furniture", "Storage", 85, 54, 2021, "SteelWorks"),
        ("P1024", "Reception Chair", "Furniture", "Chairs", 58, 36, 2019, "FurniCo"),
        ("P1025", "Microwave 30L", "Home & Kitchen", "Appliances", 95, 64, 2020, "HomeMart"),
        ("P1026", "Kettle Stainless Steel", "Home & Kitchen", "Small Appliances", 24, 14, 2019, "HomeMart"),
        ("P1027", "Toaster 4 Slice", "Home & Kitchen", "Small Appliances", 38, 23, 2020, "HomeMart"),
        ("P1028", "Air Fryer 5L", "Home & Kitchen", "Appliances", 109, 73, 2022, "KitchenLine"),
        ("P1029", "Cookware Set", "Home & Kitchen", "Cookware", 79, 50, 2021, "KitchenLine"),
        ("P1030", "Dinner Set 16 Piece", "Home & Kitchen", "Dining", 42, 24, 2019, "KitchenLine"),
        ("P1031", "Corporate Shirt", "Apparel", "Workwear", 16, 7, 2019, "StyleWorks"),
        ("P1032", "Safety Shoes", "Apparel", "Footwear", 45, 27, 2020, "SafeStep"),
        ("P1033", "Reflective Jacket", "Apparel", "Workwear", 20, 11, 2020, "SafeStep"),
        ("P1034", "Laptop Backpack", "Apparel", "Bags", 30, 17, 2021, "StyleWorks"),
        ("P1035", "Rain Jacket", "Apparel", "Outerwear", 36, 20, 2020, "StyleWorks"),
    ]

    dim_product = pd.DataFrame(
        products,
        columns=[
            "Product_ID", "Product_Name", "Category", "Subcategory",
            "Base_Unit_Price_USD", "Unit_Cost_USD", "Launch_Year", "Supplier"
        ],
    )

    provinces = {
        "Gauteng": ("Inland", ["Johannesburg", "Pretoria", "Soweto", "Midrand"]),
        "Western Cape": ("Coastal", ["Cape Town", "Bellville", "George", "Stellenbosch"]),
        "KwaZulu-Natal": ("Coastal", ["Durban", "Pietermaritzburg", "Umhlanga", "Pinetown"]),
        "Eastern Cape": ("Coastal", ["Gqeberha", "East London", "Mthatha"]),
        "Free State": ("Inland", ["Bloemfontein", "Welkom", "Sasolburg"]),
        "Mpumalanga": ("Inland", ["Mbombela", "Emalahleni", "Middelburg"]),
        "Limpopo": ("Inland", ["Polokwane", "Tzaneen", "Thohoyandou"]),
        "North West": ("Inland", ["Rustenburg", "Mahikeng", "Klerksdorp"]),
        "Northern Cape": ("Inland", ["Kimberley", "Upington"]),
    }

    first_names = [
        "Rumbidzai", "Tendai", "Thabo", "Lerato", "Amina", "Sipho", "Zanele",
        "Nokuthula", "Mpho", "Chipo", "Farai", "Blessing", "Kabelo", "Tariro",
        "Nomsa", "Brian", "Precious", "Sibusiso", "Nandi", "Kudzai"
    ]
    last_names = [
        "Moyo", "Ndlovu", "Maseko", "Dube", "Patel", "Khumalo", "Mahlangu",
        "Sibanda", "Naidoo", "Williams", "Chuma", "Mthembu", "Mabena",
        "Gumede", "Mokoena", "Nkosi", "Mathebula"
    ]

    segments = ["Consumer", "Corporate", "Small Business"]
    segment_weights = [0.50, 0.25, 0.25]

    province_names = list(provinces.keys())
    province_weights = [0.32, 0.17, 0.15, 0.07, 0.06, 0.08, 0.06, 0.05, 0.04]

    customer_since_dates = pd.date_range("2020-01-01", "2024-12-31", freq="D")
    customer_rows = []

    for i in range(1, NUMBER_OF_CUSTOMERS + 1):
        province = choose_weighted(province_names, province_weights)
        region_group, cities = provinces[province]
        customer_rows.append([
            f"C{i:04d}",
            f"{random.choice(first_names)} {random.choice(last_names)}",
            choose_weighted(segments, segment_weights),
            province,
            region_group,
            random.choice(cities),
            random.choice(customer_since_dates).strftime("%Y-%m-%d"),
        ])

    dim_customer = pd.DataFrame(
        customer_rows,
        columns=[
            "Customer_ID", "Customer_Name", "Segment", "Province",
            "Region_Group", "City", "Customer_Since"
        ],
    )

    dim_date = make_date_dimension(START_DATE, END_DATE)

    channels = ["Online", "Retail Store", "Corporate Account", "Call Centre"]
    channel_weights = [0.42, 0.32, 0.18, 0.08]

    payment_methods = ["Card", "EFT", "Cash", "Mobile Money"]
    payment_weights = [0.48, 0.22, 0.18, 0.12]

    ship_modes = ["Standard", "Express", "Collection", "Same Day"]
    ship_weights = [0.55, 0.22, 0.18, 0.05]

    fact_rows = []
    all_dates = pd.date_range(START_DATE, END_DATE, freq="D")

    for i in range(1, NUMBER_OF_ORDERS + 1):
        order_id = f"ORD{100000 + i}"

        order_date = random.choice(all_dates)
        if random.random() < 0.22:
            seasonal_month = random.choice([6, 7, 11, 12])
            possible_dates = [d for d in all_dates if d.month == seasonal_month]
            order_date = random.choice(possible_dates)

        delivery_days = int(np.random.choice(
            [1, 2, 3, 4, 5, 6, 7, 10],
            p=[0.08, 0.20, 0.25, 0.18, 0.12, 0.08, 0.06, 0.03]
        ))
        ship_date = order_date + timedelta(days=delivery_days)

        customer = dim_customer.sample(n=1, random_state=random.randint(1, 999999)).iloc[0]
        product = dim_product.sample(n=1, random_state=random.randint(1, 999999)).iloc[0]

        if product["Category"] in ["Technology", "Furniture"]:
            quantity = int(np.random.choice([1, 2, 3, 4], p=[0.55, 0.28, 0.12, 0.05]))
        elif product["Category"] == "Office Supplies":
            quantity = int(np.random.choice([1, 2, 3, 4, 5, 10], p=[0.20, 0.25, 0.20, 0.15, 0.10, 0.10]))
        else:
            quantity = int(np.random.choice([1, 2, 3, 4, 5], p=[0.34, 0.28, 0.18, 0.12, 0.08]))

        unit_price = clean_currency(max(product["Base_Unit_Price_USD"] * np.random.normal(loc=1.0, scale=0.06), 1))

        if customer["Segment"] == "Corporate" or quantity >= 5:
            discount = float(np.random.choice([0.00, 0.05, 0.10, 0.15, 0.20], p=[0.35, 0.25, 0.22, 0.13, 0.05]))
        else:
            discount = float(np.random.choice([0.00, 0.05, 0.10, 0.15, 0.20], p=[0.55, 0.24, 0.14, 0.05, 0.02]))

        unit_cost = clean_currency(max(product["Unit_Cost_USD"] * np.random.normal(loc=1.0, scale=0.04), 1))
        gross_sales = clean_currency(quantity * unit_price)
        discount_amount = clean_currency(gross_sales * discount)
        net_sales = clean_currency(gross_sales - discount_amount)
        total_cost = clean_currency(quantity * unit_cost)
        profit = clean_currency(net_sales - total_cost)
        profit_margin = round(profit / net_sales, 4) if net_sales else 0
        return_status = "Returned" if random.random() < 0.08 else "Not Returned"

        fact_rows.append([
            order_id,
            order_date.strftime("%Y-%m-%d"),
            ship_date.strftime("%Y-%m-%d"),
            customer["Customer_ID"],
            customer["Customer_Name"],
            customer["Segment"],
            product["Product_ID"],
            product["Product_Name"],
            product["Category"],
            product["Subcategory"],
            customer["Province"],
            customer["Region_Group"],
            customer["City"],
            choose_weighted(channels, channel_weights),
            choose_weighted(payment_methods, payment_weights),
            choose_weighted(ship_modes, ship_weights),
            quantity,
            unit_price,
            discount,
            gross_sales,
            discount_amount,
            net_sales,
            unit_cost,
            total_cost,
            profit,
            profit_margin,
            delivery_days,
            return_status,
        ])

    fact_sales = pd.DataFrame(
        fact_rows,
        columns=[
            "Order_ID", "Order_Date", "Ship_Date", "Customer_ID", "Customer_Name",
            "Segment", "Product_ID", "Product_Name", "Category", "Subcategory",
            "Province", "Region_Group", "City", "Channel", "Payment_Method",
            "Ship_Mode", "Quantity", "Unit_Price_USD", "Discount",
            "Gross_Sales_USD", "Discount_Amount_USD", "Net_Sales_USD",
            "Unit_Cost_USD", "Total_Cost_USD", "Profit_USD", "Profit_Margin",
            "Delivery_Days", "Return_Status"
        ],
    )

    returned_orders = fact_sales[fact_sales["Return_Status"] == "Returned"].copy()
    return_reasons = [
        "Damaged item", "Wrong item ordered", "Late delivery",
        "Customer changed mind", "Product not as expected"
    ]

    returns_rows = []
    for idx, row in returned_orders.reset_index(drop=True).iterrows():
        return_date = pd.to_datetime(row["Ship_Date"]) + timedelta(days=random.randint(1, 21))
        refund_amount = clean_currency(row["Net_Sales_USD"] * np.random.uniform(0.50, 1.00))
        returns_rows.append([
            f"R{idx + 1:05d}",
            row["Order_ID"],
            return_date.strftime("%Y-%m-%d"),
            random.choice(return_reasons),
            refund_amount,
            row["Product_ID"],
            row["Customer_ID"],
        ])

    returns = pd.DataFrame(
        returns_rows,
        columns=["Return_ID", "Order_ID", "Return_Date", "Reason", "Refund_Amount_USD", "Product_ID", "Customer_ID"],
    )

    fact_sales["YearMonth"] = pd.to_datetime(fact_sales["Order_Date"]).dt.strftime("%Y-%m")
    monthly_category_region = fact_sales.groupby(["YearMonth", "Category", "Region_Group"], as_index=False).agg(
        Net_Sales_USD=("Net_Sales_USD", "sum"),
        Profit_USD=("Profit_USD", "sum")
    )

    targets_rows = []
    for _, row in monthly_category_region.iterrows():
        year, month_no = row["YearMonth"].split("-")
        targets_rows.append([
            row["YearMonth"],
            int(year),
            int(month_no),
            row["Category"],
            row["Region_Group"],
            clean_currency(row["Net_Sales_USD"] * np.random.uniform(0.95, 1.18)),
            clean_currency(row["Profit_USD"] * np.random.uniform(0.95, 1.20)),
        ])

    sales_targets = pd.DataFrame(
        targets_rows,
        columns=["YearMonth", "Year", "Month_No", "Category", "Region_Group", "Sales_Target_USD", "Profit_Target_USD"],
    )

    monthly_summary = fact_sales.groupby("YearMonth", as_index=False).agg(
        Net_Sales_USD=("Net_Sales_USD", "sum"),
        Profit_USD=("Profit_USD", "sum"),
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Returns=("Return_Status", lambda s: (s == "Returned").sum()),
    )
    monthly_summary["Profit_Margin"] = (monthly_summary["Profit_USD"] / monthly_summary["Net_Sales_USD"]).round(4)

    category_summary = fact_sales.groupby("Category", as_index=False).agg(
        Net_Sales_USD=("Net_Sales_USD", "sum"),
        Profit_USD=("Profit_USD", "sum"),
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Returns=("Return_Status", lambda s: (s == "Returned").sum()),
    ).sort_values("Net_Sales_USD", ascending=False)
    category_summary["Profit_Margin"] = (category_summary["Profit_USD"] / category_summary["Net_Sales_USD"]).round(4)

    province_summary = fact_sales.groupby("Province", as_index=False).agg(
        Net_Sales_USD=("Net_Sales_USD", "sum"),
        Profit_USD=("Profit_USD", "sum"),
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum"),
    ).sort_values("Net_Sales_USD", ascending=False)
    province_summary["Profit_Margin"] = (province_summary["Profit_USD"] / province_summary["Net_Sales_USD"]).round(4)

    channel_summary = fact_sales.groupby("Channel", as_index=False).agg(
        Net_Sales_USD=("Net_Sales_USD", "sum"),
        Profit_USD=("Profit_USD", "sum"),
        Orders=("Order_ID", "nunique"),
    ).sort_values("Net_Sales_USD", ascending=False)
    channel_summary["Profit_Margin"] = (channel_summary["Profit_USD"] / channel_summary["Net_Sales_USD"]).round(4)

    segment_summary = fact_sales.groupby("Segment", as_index=False).agg(
        Net_Sales_USD=("Net_Sales_USD", "sum"),
        Profit_USD=("Profit_USD", "sum"),
        Orders=("Order_ID", "nunique"),
    ).sort_values("Net_Sales_USD", ascending=False)
    segment_summary["Profit_Margin"] = (segment_summary["Profit_USD"] / segment_summary["Net_Sales_USD"]).round(4)

    fact_sales = fact_sales.drop(columns=["YearMonth"])

    return {
        "Fact_Sales": fact_sales,
        "Dim_Product": dim_product,
        "Dim_Customer": dim_customer,
        "Dim_Date": dim_date,
        "Sales_Targets": sales_targets,
        "Returns": returns,
        "Monthly_Summary": monthly_summary,
        "Category_Summary": category_summary,
        "Province_Summary": province_summary,
        "Channel_Summary": channel_summary,
        "Segment_Summary": segment_summary,
    }


def export_outputs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_dataset()

    for name, df in tables.items():
        df.to_csv(DATA_DIR / f"{name}.csv", index=False)

    fact_sales = tables["Fact_Sales"]
    print("Synthetic USD retail sales dataset generated successfully.")
    print(f"Output folder: {OUTPUT_ROOT.resolve()}")
    print(f"Fact rows: {len(fact_sales):,}")
    print(f"Total net sales USD: ${fact_sales['Net_Sales_USD'].sum():,.2f}")
    print(f"Total profit USD: ${fact_sales['Profit_USD'].sum():,.2f}")


if __name__ == "__main__":
    export_outputs()
