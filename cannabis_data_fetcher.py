"""
Cannabis Data Fetcher and PostgreSQL Storage

This Python script fetches data from the Random Data API about cannabis strains, cannabinoids, and related information.
It then stores this data in a PostgreSQL database. The script can be used to periodically update the database
with new data from the API.

The script contains the following main functions:

1. `fetch_data_from_api`: Fetches data from the Random Data API and returns it as a list of dictionaries.
2. `store_data_to_postgres`: Stores the fetched data in a structured PostgreSQL table. It creates the table if it
   doesn't exist and adapts the table structure if the API data changes.
3. `adapt_table_structure`: Checks if the table structure matches the data structure and adds columns if necessary.

To use this script, you need to provide the database configuration (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
and configure the REQUEST_SIZE to determine how much data to fetch from the API in each request.

Usage:
1. Configure the database settings and REQUEST_SIZE.
2. Run the script. It will fetch data from the API and display it.
3. The fetched data will be stored in the PostgreSQL database in the specified table.

Note:
- If the table structure changes in the future, you may need to update it manually or use an automated migration tool.
- The script includes basic error handling and logging to help identify and troubleshoot issues.

"""


import requests
import psycopg2
from datetime import datetime
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'aero_de'
DB_USER = 'username'
DB_PASSWORD = 'password'

# Define the request size variable
REQUEST_SIZE = 10

# Define the table name as a global constant for easier modification and access
TABLE_NAME = 'cannabis_data'


# Updated fetch_data_from_api function to use REQUEST_SIZE variable
def fetch_data_from_api():
    """
    Fetch data from the specified API using the REQUEST_SIZE variable.
    """
    url = f'https://random-data-api.com/api/cannabis/random_cannabis?size={REQUEST_SIZE}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(response.json())
        return response.json()
    except requests.RequestException as e:
        logging.error(f'Error fetching data from API: {e}')
        return []


"""
Update the table structure
The new table structure will have columns corresponding to each field in the API data.
"""


def store_data_to_postgres(data):
    # Store fetched data to PostgreSQL database with a structured table.
    try:
        # Connect to the database
        connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = connection.cursor()

        """ 
        Create table if not exists with potential structure update
        If the structure changes in the future, this needs to be updated manually or via an automated migration tool.
        """
        cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                uid VARCHAR(255) UNIQUE,
                strain VARCHAR(255),
                cannabinoid_abbreviation VARCHAR(10),
                cannabinoid VARCHAR(255),
                terpene VARCHAR(255),
                medical_use VARCHAR(255),
                health_benefit VARCHAR(255),
                category VARCHAR(255),
                type VARCHAR(50),
                buzzword VARCHAR(50),
                brand VARCHAR(255),
                fetched_at TIMESTAMP NOT NULL
            )
            '''
        )

        # Adapt the table structure if needed
        adapt_table_structure(data, cursor)

        """ 
        Insert data while avoiding potential data conflicts
        Using ON CONFLICT to handle potential duplication of 'uid'
        """
        now = datetime.now()
        fields = ', '.join(data[0].keys())
        values_placeholders = ', '.join(['%s' for _ in data[0].keys()])
        records = [tuple(item[field] for field in data[0].keys()) + (now,) for item in data]
        insert_query = f'''
                    INSERT INTO {TABLE_NAME} ({fields}, fetched_at)
                    VALUES ({values_placeholders}, %s)
                    ON CONFLICT (uid) DO NOTHING
                '''

        # Optimize insertion using executemany
        cursor.executemany(insert_query, records)

        # Commit changes
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()
        logging.info("Data successfully stored to PostgreSQL.")
    except Exception as e:
        logging.error(f'Error storing data to PostgreSQL: {e}')


def adapt_table_structure(data, cursor):
    """
    Adapts the table structure to match the data structure.

    This function checks if the fields in the data are present as columns in the table.
    If not, it will add the necessary columns.
    """
    # Fetch the current columns in the table
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'cannabis_data'")
    current_columns = [row[0] for row in cursor.fetchall()]

    # Check each field in the data against the current columns
    for field in data[0].keys():
        if field not in current_columns and field != "id":  # We exclude 'id' as it's our primary key
            # Alter table to add a new column of type VARCHAR(255) for simplicity
            # A more advanced implementation might determine the data type based on the actual data
            cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {field} VARCHAR(255)")


# Adding the main block to test the fetch_data_from_api function
if __name__ == "__main__":
    # Fetching data from the API
    fetched_data = fetch_data_from_api()

    # Displaying the fetched data
    print(fetched_data)
