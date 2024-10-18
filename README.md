# Treetracker queue client for Python

## Steps to run the publish/subscribe tests

## First activate virtual environment:
.\venv\Scripts\activate

## Second postgres DB connection url into .env file as follows:
CONNECTION_URL="connection string goes here"

## Third install the required packages by running:
pip install -r ./requirements.txt

## Fourth run the end to end test:
pytest .\tests\test_message.py

## Finally deactivate to get out of the virtual env:
.\venv\Scripts\deactivate
