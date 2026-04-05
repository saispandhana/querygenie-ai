import pandas as pd
from difflib import get_close_matches

VALUE_SYNONYM_MAP = {
    "softdrinks": "soft drinks",
    "soft drink": "soft drinks",
    "soft drinks": "soft drinks",
    "soda": "soft drinks",
    "cold drink": "soft drinks",
    "cold drinks": "soft drinks",
    "juice": "juices",
    "juices": "juices",
    "water bottle": "water",
    "plain water": "water"
}

COLUMN_SYNONYM_MAP = {
    "people": "customer_id",
    "person": "customer_id",
    "customer": "customer_id",
    "customers": "customer_id",
    "user": "customer_id",
    "users": "customer_id",

    "region": "region",
    "area": "region",
    "location": "region",
    "zone": "region",

    "brand": "product",
    "item": "product",
    "product": "product",
    "products": "product",

    "discount": "discount",
    "discounted": "discount",
    "discount given": "discount",

    "quantity": "quantity",
    "count": "quantity",

    "revenue": "total_price",
    "sales": "total_price",
    "amount": "total_price",
    "price": "price"
}


def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def apply_value_synonym(value):
    return VALUE_SYNONYM_MAP.get(normalize_text(value), normalize_text(value))


def apply_column_synonym(value):
    return COLUMN_SYNONYM_MAP.get(normalize_text(value), normalize_text(value))


def get_best_fuzzy_match(user_value, actual_values, synonym_func=None):
    user_val = normalize_text(user_value)

    if synonym_func:
        user_val = synonym_func(user_val)

    normalized_map = {normalize_text(v): v for v in actual_values if pd.notna(v)}

    if user_val in normalized_map:
        return normalized_map[user_val]

    matches = get_close_matches(user_val, list(normalized_map.keys()), n=1, cutoff=0.6)
    if matches:
        return normalized_map[matches[0]]

    return user_value


def resolve_column_name(user_column, df_columns):
    if not user_column:
        return None

    df_map = {normalize_text(col): col for col in df_columns}
    mapped = apply_column_synonym(user_column)

    if mapped in df_map:
        return df_map[mapped]

    matches = get_close_matches(mapped, list(df_map.keys()), n=1, cutoff=0.6)
    if matches:
        return df_map[matches[0]]

    return user_column


def apply_filters(df, filters):
    result = df.copy()

    for f in filters:
        col = resolve_column_name(f["column"], result.columns)
        val = f["value"]
        op = f["operator"]

        if col not in result.columns:
            continue

        if op in ["equals", "contains"]:
            values = result[col].dropna().unique()
            best_match = get_best_fuzzy_match(val, values, apply_value_synonym)

            if op == "equals":
                result = result[
                    result[col].astype(str).str.strip().str.lower()
                    == str(best_match).strip().lower()
                ]

            elif op == "contains":
                result = result[
                    result[col].astype(str).str.strip().str.lower().str.contains(
                        normalize_text(val), na=False
                    )
                ]

        elif op == "greater_than":
            result = result[pd.to_numeric(result[col], errors="coerce") > float(val)]

        elif op == "less_than":
            result = result[pd.to_numeric(result[col], errors="coerce") < float(val)]

    return result


def format_selected_columns(row, return_columns):
    output = []
    for col in return_columns:
        output.append(f"{col}: {row[col]}")
    return "\n".join(output)


def execute_query_plan(df, plan):
    action = plan.get("action")
    filters = plan.get("filters", [])
    target_column = resolve_column_name(plan.get("target_column"), df.columns)
    group_by = resolve_column_name(plan.get("group_by"), df.columns)
    raw_return_columns = plan.get("return_columns", [])
    n = plan.get("n", 5)
    sort_order = plan.get("sort_order", "desc")

    return_columns = []
    for col in raw_return_columns:
        resolved = resolve_column_name(col, df.columns)
        if resolved in df.columns:
            return_columns.append(resolved)

    df = apply_filters(df, filters)

    if df.empty:
        return "No matching data found."

    if action == "count":
        return f"Answer: {len(df)}"

    if action == "count_unique":
        if target_column in df.columns:
            return f"Answer: {df[target_column].nunique()}"
        return "Column not found."

    if action == "sum":
        if target_column in df.columns:
            total = pd.to_numeric(df[target_column], errors="coerce").sum()
            return f"Answer: {total}"
        return "Column not found."

    if action == "average":
        if target_column in df.columns:
            avg = pd.to_numeric(df[target_column], errors="coerce").mean()
            return f"Answer: {avg}"
        return "Column not found."

    if action == "groupby_count":
        if group_by in df.columns:
            grouped = df.groupby(group_by).size().sort_values(ascending=False)
            return grouped.to_string()
        return "Group-by column not found."

    if action == "groupby_sum":
        if group_by in df.columns and target_column in df.columns:
            grouped = df.groupby(group_by)[target_column].sum().sort_values(ascending=False)
            return grouped.to_string()
        return "Required columns not found."

    if action == "groupby_average":
        if group_by in df.columns and target_column in df.columns:
            grouped = df.groupby(group_by)[target_column].mean().sort_values(ascending=False)
            return grouped.to_string()
        return "Required columns not found."

    if action == "max_row":
        if target_column in df.columns:
            series = pd.to_numeric(df[target_column], errors="coerce")
            idx = series.idxmax()
            row = df.loc[idx]
            if return_columns:
                return format_selected_columns(row, return_columns)
            return row.to_string()
        return "Target column not found."

    if action == "min_row":
        if target_column in df.columns:
            series = pd.to_numeric(df[target_column], errors="coerce")
            idx = series.idxmin()
            row = df.loc[idx]
            if return_columns:
                return format_selected_columns(row, return_columns)
            return row.to_string()
        return "Target column not found."

    if action == "top_n":
        if target_column in df.columns:
            ascending = sort_order == "asc"
            temp_df = df.copy()
            temp_df[target_column] = pd.to_numeric(temp_df[target_column], errors="coerce")
            temp_df = temp_df.sort_values(by=target_column, ascending=ascending).head(int(n))

            if return_columns:
                cols = [col for col in return_columns if col in temp_df.columns]
                return temp_df[cols].to_string(index=False)

            return temp_df.to_string(index=False)
        return "Target column not found."

    if action == "distinct_values":
        if target_column in df.columns:
            values = df[target_column].dropna().astype(str).unique().tolist()
            return "\n".join(values[:50])
        return "Target column not found."

    if action == "filter":
        if return_columns:
            cols = [col for col in return_columns if col in df.columns]
            if cols:
                return df[cols].head(10).to_string(index=False)
        return df.head(10).to_string(index=False)

    return "Unsupported action."
