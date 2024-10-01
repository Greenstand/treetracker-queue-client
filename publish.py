import aiopg

async def publish(dsn, channel: str, data: str):
    """
    Publish a message to the PostgreSQL queue by inserting data into the table.

    Args:
        dsn (str): The PostgreSQL database connection string.
        channel (str): The channel where the message is to be dispatched.
        data (str): The data to be inserted into the queue.
    """
    # SQL query to insert data into the queue.message table
    query = "INSERT INTO queue.message(channel, data) VALUES (%s, %s) RETURNING *"
    values = (channel, data)

    async with aiopg.connect(dsn) as conn:
        async with conn.cursor() as cur:
            try:
                # Execute the SQL query with the provided values
                await cur.execute(query, values)
                
                # Fetch and print the result from the database
                result = await cur.fetchone()
                print(f"Postgres message dispatch success: {result}")
            except Exception as error:
                    print(f"Error Occurred -> {error}")
                
            finally:
                # This is often useful to let listeners know that no more messages will be sent.
                await cur.execute(f"NOTIFY {channel}, 'finish'")