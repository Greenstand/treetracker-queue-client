import pytest, asyncio, sys, os, json
from dotenv import load_dotenv

load_dotenv()

rootpath = os.path.join(os.getcwd(), "pg-queue")
sys.path.append(rootpath)

from fetch import fetch

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# test message fetch function
@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_async_fetch():

    # fetch message
    result = await fetch(
        connection_str=os.environ.get("CONNECTION_URL"),
        channel="sports",
        start_date="2024-09-06",
        end_date="2024-09-07",
        game="NFL",
    )
    subset = {"channel": "sports", "data": {"game": "NFL"}}
    assert subset.items() <= result[0].items()
