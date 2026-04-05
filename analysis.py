import os
import pandas as pd


def load_first_csv():
    for file_name in os.listdir():
        if file_name.endswith(".csv"):
            return pd.read_csv(file_name)
    return None


def get_total_products_sold(df):
    if "Quantity" in df.columns:
        total_qty = df["Quantity"].sum()
        return f"Total amount of products sold is {total_qty}"
    return "Quantity column not found."


def get_top_selling_product(df):
    if "Product" in df.columns and "Quantity" in df.columns:
        result = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
        return f"Top selling product is {result.index[0]} with quantity {result.iloc[0]}"
    return "Required columns Product and Quantity not found."


def get_top_5_products(df):
    if "Product" in df.columns and "Quantity" in df.columns:
        result = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(5)
        lines = [f"{idx}: {val}" for idx, val in result.items()]
        return "Top 5 products by quantity sold:\n" + "\n".join(lines)
    return "Required columns Product and Quantity not found."


def get_total_revenue(df):
    if "Total_Price" in df.columns:
        total_revenue = df["Total_Price"].sum()
        return f"Total revenue is {total_revenue}"
    return "Total_Price column not found."


def get_highest_revenue_product(df):
    if "Product" in df.columns and "Total_Price" in df.columns:
        result = df.groupby("Product")["Total_Price"].sum().sort_values(ascending=False)
        return f"Highest revenue product is {result.index[0]} with revenue {result.iloc[0]}"
    return "Required columns Product and Total_Price not found."


def get_average_order_value(df):
    if "Total_Price" in df.columns:
        avg_value = df["Total_Price"].mean()
        return f"Average order value is {avg_value:.2f}"
    return "Total_Price column not found."
