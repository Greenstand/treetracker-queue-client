# Treetracker queue client for Python

## Follow the steps below to run the publish/subscribe tests

## Create virtual environment:
py -m venv venv

## Activate virtual environment:
.\venv\Scripts\activate

## Add postgres DB connection url into .env file as follows:
CONNECTION_URL="connection string goes here"

## Install the required packages by running:
pip install -r ./requirements.txt

## Run the end to end test:
pytest .\tests\test_message.py

## Finally deactivate to get out of the virtual env:
.\venv\Scripts\deactivate
