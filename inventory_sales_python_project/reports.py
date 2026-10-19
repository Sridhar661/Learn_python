"""Console report formatting."""


def print_inventory(products: list[dict]) -> None:
    if not products:
        print("No matching products found.")
        return

    print("\nID | SKU | Product | Price | Quantity | Alert at")
    print("-" * 68)
    for product in products:
        print(
            f"{product['id']} | {product['sku']} | {product['name']} | "
            f"{product['price']:.2f} | {product['quantity']} | "
            f"{product['low_stock_threshold']}"
        )


def print_sales_report(summary: dict) -> None:
    print("\n===== SALES REPORT =====")
    print(f"Number of sales: {summary['sale_count']}")
    print(f"Units sold: {summary['units_sold']}")
    print(f"Total revenue: {summary['revenue']:.2f}")

    if summary["sales"]:
        print("\nSale ID | Product | Qty | Unit price | Total")
        print("-" * 58)
        for sale in summary["sales"]:
            print(
                f"{sale['id']} | {sale['product_name']} | "
                f"{sale['quantity']} | {sale['unit_price']:.2f} | "
                f"{sale['total']:.2f}"
            )
