import asyncio
from publish import publish

# Example usage (assuming you have a PostgreSQL connection pool):
async def main():
    dsn = "dbname=xxxxx user=xxxxxx password=xxxxxx host=localhost"
    await publish(dsn, 'my_channel', '{"message": "Hello, world!"}')

asyncio.run(main())

