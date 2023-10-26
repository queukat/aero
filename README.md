# Cannabis Data Fetcher and PostgreSQL Storage

This Python script is designed to fetch data about cannabis strains, cannabinoids, and related information from the Random Data API. It then stores this data in a PostgreSQL database. The script can be used to periodically update the database with new data from the API.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Configuration](#configuration)
  - [Running the Script](#running-the-script)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- PostgreSQL database server installed and running
- Necessary Python packages installed (you can install them using `pip install -r requirements.txt`)

## Getting Started

### Configuration

1. Open the script file `cannabis_data_fetcher.py`.
2. Modify the database configuration variables according to your PostgreSQL setup:
   - `DB_HOST`: The hostname of your PostgreSQL server.
   - `DB_PORT`: The port number on which PostgreSQL is running (default is 5432).
   - `DB_NAME`: The name of the PostgreSQL database.
   - `DB_USER`: The username for connecting to the database.
   - `DB_PASSWORD`: The password for connecting to the database.
3. Configure the `REQUEST_SIZE` variable to determine how much data to fetch from the API in each request.

### Running the Script

To run the script and fetch data from the API, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the script using the following command:

### To schedule periodic execution of your Python script, you can use cron jobs on your computer or server. Follow these steps:

1. Open the terminal on your computer or server.
2. Enter the following command to edit the list of cron jobs:
```bash
crontab -e
```
3.In the opened cron job editor, add the following line to the end of the file:
```bash
0 */12 * * * /usr/bin/python3 /path/to/your/file.py
```
Here:

0 */12 * * * means that the task will run every 12 hours (twice a day).
/usr/bin/python3 is the path to the Python 3 interpreter on your computer or server. Make sure this path is correct.
/path/to/your/file.py - replace this with the full path to your Python file that you want to run periodically.
Save the file and close the editor.

Now, your Python script will automatically run every 12 hours, as specified in the cron job. Ensure that the path to your file and the Python interpreter are correctly set.

