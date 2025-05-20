

def clean_sql(query: str) -> str:
    """Limpia marcas de formato Markdown en la consulta SQL."""
    query = query.strip()
    if query.startswith("```sql"):
        query = query.replace("```sql", "").replace("```", "").strip()
    elif query.startswith("```"):
        query = query.replace("```", "").strip()
    return query

def is_valid_sql(query: str) -> tuple[bool, str]:
    cleaned_query = clean_sql(query)
    print(f"Cleaned SQL Query: {cleaned_query}")
    return cleaned_query.lower().startswith("select"), cleaned_query
