import sqlite3
import random
import sys
import time
import json

def create_connection(database_name):
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(database_name)
        print("Connected to the database.")
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

def insertCardData(conn, cardId, cardStatus, pin, isTwoStepAuth,isBanned):
    insert_data_query = '''
    INSERT INTO card (cardId, cardStatus, pin, isTwoStepAuth, isBanned)
    VALUES (?, ?, ?, ?, ?);
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(insert_data_query, (cardId, cardStatus, pin, isTwoStepAuth, isBanned))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def main ():
    database_path = "./gateway.db"
    conn = create_connection(database_path)
    filePath = str(sys.argv[1])
    data_container = []

    # RESET DATABASE
    # if(True):
    #     conn.cursor().execute(f"DELETE FROM card")
    #     conn.commit()

    totalCardData = conn.cursor().execute(f"SELECT COUNT(*) FROM card").fetchone()[0]
    print(f"Total card data before operation {totalCardData}")

    print("Preapre dataset, loading all dataset")
    file = open(f'{filePath}')
    jsonData = json.load(file)
    file.close()     

    print("Inserting data")
    start_time = time.time()
    for data in jsonData:
        insertCardData(conn, data["cardNumber"], "REGISTER", data["hashPin"], False, False)
    end_time = time.time()

    itteration = len(jsonData)
    elapsed_time = end_time - start_time
    inserts_per_second = itteration / elapsed_time
    totalCardData = conn.cursor().execute(f"SELECT COUNT(*) FROM card").fetchone()[0]

    print(f"Total inserts: {itteration}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Inserts per second: {inserts_per_second:.2f}")
    print(f"Total card data after operation: {totalCardData}")

    conn.close()

if __name__ == "__main__":
    main()