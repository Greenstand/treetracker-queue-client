import psycopg


# subscribe client to a channel
async def subscribe(connection_str: str, channel: str):

    try:
        con = psycopg.connect(connection_str, autocommit=True)
    except:
        print("Connection error! Make sure CONNECTION_URL variable is set.")
        return
    try:
        con.execute(f"LISTEN {channel}")
        gen = con.notifies()
        return gen
    except Exception as e:
        print(f"subscribe error: {e}")
        return
