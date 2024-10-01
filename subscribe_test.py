import asyncio
from subscribe import subscribe
import aiopg

# Example usage (assuming you have a PostgreSQL connection pool):
async def main():
    #provide a postgres data source here
    dsn = "dbname=xxxxx user=xxxxx password=xxxxx host=localhost"
    async with aiopg.connect(dsn) as conn:
        result = await subscribe(conn, 'my_channel') # change 'my_channel' to the channel you want to use
        print(f"Received notification: {result}")

asyncio.run(main())
