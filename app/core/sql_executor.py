

import psycopg2

def execute_sql(db_config: dict, query: str):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def fetch_sql(db_config, query: str):
    import psycopg2
    import pandas as pd

    conn = psycopg2.connect(**db_config)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df