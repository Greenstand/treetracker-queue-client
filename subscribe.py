import psycopg2

async def subscribe(conn, channel: str):
    """
    Listen for notifications on a PostgreSQL channel.

    Args:
        conn (aiopg.Connection): The aiopg connection.
        channel (str): The PostgreSQL channel to listen to.
    """
    async with conn.cursor() as cur:
        await cur.execute(f"LISTEN {channel}")
        
        # Continuously listen for notifications
        while True:
            try:
                # Wait and get the next notification message
                msg = await conn.notifies.get()
            except psycopg2.Error as ex:
                print("ERROR: ", ex)
                return
            
            if msg.payload == "finish":
                return
            else:
                print(f"Receive <- {msg.payload}")

