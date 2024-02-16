"""
Psycopg2 client test and demo module.
"""
# import the connect library for psycopg2
from psycopg2 import connect
# import the error handling libraries for psycopg2
from psycopg2 import OperationalError, IntegrityError

VEHICLES = [
    {
        'vehicle_id': '10-ZFJ-9',
        'type': 'Car',
        'brand': 'Volvo',
        'model': 'V40 T3',
        'odometer': 0
    },
    {
        'vehicle_id': 'LF-xx-xx',
        'type': 'Car',
        'brand': 'MG',
        'model': 'Midget 1500',
        'odometer': 0
    },
    {
        'vehicle_id': 'MS-DV-75',
        'type': 'Motorbike',
        'brand': 'Royal Enfield',
        'model': 'Classic 350',
        'odometer': 0
    }
]

def pg_connect():
    """Connect to Postgres db."""
    connection = None
    try:
        connection = connect(database = "testserver",
                            user = "testserver",
                            host= 'pi4b02',
                            password = "testserver",
                            port = 5432)
    except OperationalError as err:
        print(f"Connection error: {err}")
    return connection


def create_schemas(connection):
    """Create db scheams on first use."""
    # Open a cursor to perform database operations
    cur = connection.cursor()
    # Execute a command: create datacamp_courses table
    cur.execute("""CREATE TABLE vehicle(
                vehicle_id SERIAL PRIMARY KEY,
                vehicle_registration VARCHAR (12) UNIQUE NOT NULL,
                type VARCHAR (10) NOT NULL,
                brand VARCHAR (30) NOT NULL,
                model VARCHAR (30) NOT NULL,
                odometer INTEGER );
                """)
    # Make the changes to the database persistent
    connection.commit()
    # Close cursor and communication with the database
    cur.close()
    connection.close()

def fill_vehicle(connection, vehicles):
    """Fill vehicle table from hash."""
    cursor = connection.cursor()

    # Execute a command: create datacamp_courses table
    for item in vehicles:
        print(f"vehicle: {item}")
        try:
            cursor.execute(f"""INSERT INTO vehicle (
                    vehicle_registration, type, brand, model, odometer)
                VALUES (
                    \'{item['vehicle_id']}\',
                    \'{item['type']}\',
                    \'{item['brand']}\',
                    \'{item['model']}\',
                    {item['odometer']}
                ); """)
            # Make the changes to the database persistent
            connection.commit()
        except IntegrityError as err:
            print(f"Record exists: {err}")
            connection.rollback()
    # Close cursor and communication with the database
    cursor.close()
    connection.close()

if __name__ == "__main__":
    db_connection = pg_connect()
    if not db_connection:
        exit(1)
    # Do a test first
    # create_schemas(db_connection)
    fill_vehicle(db_connection, VEHICLES)
