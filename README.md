# Treetracker queue Python client for PostgreSQL

This Python project provides asynchronous pub-sub (publish-subscribe) functionality using PostgreSQL as a message broker, leveraging `aiopg` for asynchronous PostgreSQL connections and `psycopg2` for handling PostgreSQL notifications.

## Features

- **Subscribe**: Listen to PostgreSQL channels for incoming notifications.
- **Publish**: Send messages to a PostgreSQL queue and notify subscribers.

## Requirements

Make sure you have the following installed:

- **Python 3.7+**
- **PostgreSQL 9.0+**
- **aiopg**: Asynchronous PostgreSQL driver for Python.
- **psycopg2**: PostgreSQL database adapter for Python.

Install the required Python packages using `pip`:

```bash
pip install aiopg psycopg2
```

## Database Setup

Before using the client, set up the necessary PostgreSQL table for the queue:

```sql
CREATE SCHEMA queue; -- creates a schema called queue
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- helps us generate uuids
CREATE TABLE queue.message (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  channel text,
  data json,
  created_at timestamptz,
  updated_at timestamptz
); -- creates a table with columns id, channel, data, created_at & updated_at
ALTER TABLE queue.message ALTER COLUMN created_at SET DEFAULT now();
ALTER TABLE queue.message ALTER COLUMN updated_at SET DEFAULT now();
-- above two lines make created_at and updated_at columns to be autopopulated

CREATE OR REPLACE FUNCTION queue.new_message_notify() RETURNS TRIGGER AS $$
        DECLARE
        BEGIN
            PERFORM pg_notify(cast(NEW.channel as text), row_to_json(new)::text);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

CREATE TRIGGER new_insert_trigger BEFORE INSERT ON queue.message
            FOR EACH ROW EXECUTE PROCEDURE queue.new_message_notify();
```

## Usage

### 1. Subscribing to a Channel

To subscribe to a PostgreSQL channel, you can use the `subscribe` method of the `Client` class. It continuously listens for notifications on the given channel.

```python
import asyncio
import aiopg
from client import Client 

dsn = 'dbname=test user=postgres password=yourpassword host=localhost'

async def run_subscriber():
    async with aiopg.connect(dsn) as conn:
        await Client.subscribe(conn, 'my_channel')

# Run the subscriber
asyncio.run(run_subscriber())
```

### 2. Publishing to a Channel

To publish a message to a PostgreSQL channel, use the `publish` method. It inserts a message into the `queue.message` table and notifies listeners.

```python
import asyncio
from client import Client

dsn = 'dbname=test user=postgres password=yourpassword host=localhost'

async def run_publisher():
    await Client.publish(dsn, 'my_channel', 'Hello, PostgreSQL!')

# Run the publisher
asyncio.run(run_publisher())
```

### Example Output

- When you publish a message, you’ll see:

  ```
  Postgres message dispatch success: (1, 'my_channel', 'Hello, PostgreSQL!')
  ```

- When you subscribe to a channel, you’ll receive:

  ```
  Receive <- Hello, PostgreSQL!
  ```

## Methods

### `subscribe(conn, channel: str)`
Listens for notifications on a PostgreSQL channel.

- **Parameters**:
  - `conn`: The `aiopg.Connection` object.
  - `channel`: The PostgreSQL channel name.

- **Returns**: Prints out the messages received from the channel.

### `publish(dsn: str, channel: str, data: str)`
Publishes a message to a PostgreSQL channel by inserting data into the `queue.message` table.

- **Parameters**:
  - `dsn`: The PostgreSQL connection string.
  - `channel`: The PostgreSQL channel to notify.
  - `data`: The message to be published.

- **Returns**: Inserts a row into the `queue.message` table and notifies the channel subscribers.

## Error Handling

- The code catches and handles common PostgreSQL errors during subscription and publishing.
- It also ensures that listeners receive a 'finish' message, signaling the end of notifications.

## License

This project is open-source and available under the MIT License.