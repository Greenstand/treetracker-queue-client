import psycopg
from psycopg.rows import dict_row
import json


# publish a message to message table
async def publish(connection_str: str, channel: str, data: dict):

    try:
        con = await psycopg.AsyncConnection.connect(connection_str)
    except:
        print("Connection error! Make sure CONNECTION_URL variable is set.")
        return
    try:
        # used to get row in dict form with column name as key
        cur = con.cursor(row_factory=dict_row)

        # build the publish sql string
        sql = """INSERT into queue.message(channel, data) values (%s, %s) RETURNING *"""
        values = (channel, json.dumps(data))

        await cur.execute(sql, values)

        # fetch inserted row
        row = await cur.fetchone()
        id = None
        if row:
            id = row["id"]

        # commit changes to table
        await con.commit()

        print(f"publish success! message id: {id}")
    except:
        print("publish error!")
        return
    return row
