import psycopg, asyncio, os
from psycopg.rows import dict_row
from datetime import datetime


# this function fetches messages from the message table
async def fetch(
    connection_str: str,
    channel: str,
    start_date: str,
    end_date=datetime.today().strftime("%Y-%m-%d"),
    **kwargs,
):
    try:
        con = await psycopg.AsyncConnection.connect(connection_str)
    except:
        print("Connection error! Make sure CONNECTION_URL variable is set.")
        return
    try:
        # used to get row in dict form with column name as key
        cur = con.cursor(row_factory=dict_row)

        # build the filter sql string
        # this filter looks through the data column to find rows that fit the key-value pairs
        filter_sql = ""
        for key, value in kwargs.items():
            filter_sql += f' and m."data" @> \'{{"{key}":"{value}"}}\''

        # this builds the total sql string that fetches the messages
        sql = f"SELECT * FROM queue.message m WHERE m.channel = '{channel}' and m.created_at >= '{start_date}' and m.created_at < '{end_date}'"
        await cur.execute(sql)

        rows = await cur.fetchall()

        await cur.close()
    except:
        print("fetch error!")

    return rows
