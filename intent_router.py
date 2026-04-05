def detect_intent(user_question: str) -> str:
    question = user_question.lower()

    if any(word in question for word in ["total amount", "total products sold", "total quantity", "how many products sold"]):
        return "total_products_sold"

    if any(word in question for word in ["most selling", "top selling", "best selling"]):
        return "top_selling_product"

    if any(word in question for word in ["top 5 products", "top five products", "top products"]):
        return "top_5_products"

    if any(word in question for word in ["total revenue", "total sales amount", "overall revenue"]):
        return "total_revenue"

    if any(word in question for word in ["highest revenue", "most revenue", "product generated highest revenue"]):
        return "highest_revenue_product"

    if any(word in question for word in ["average order value", "avg order value", "mean order value"]):
        return "average_order_value"

    return "metadata_query"
