import sqlite3
import random
import bcrypt
import sys
import time

def generate_random_hex(length):
    # Generate a random hex string of the specified length
    hex_characters = "0123456789abcdef"
    hex_string = ''.join(random.choice(hex_characters) for _ in range(length))
    return hex_string

def generate_random_pin(length):
    # Generate a random PIN number of the specified length
    pin_digits = "0123456789"
    pin = ''.join(random.choice(pin_digits) for _ in range(length))
    return (pin)

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
    itteration = int(sys.argv[1])
    data_container = []

    # RESET DATABASE
    if(False):
        conn.cursor().execute(f"DELETE FROM card")
        conn.commit()

    totalCardData = conn.cursor().execute(f"SELECT COUNT(*) FROM card").fetchone()[0]
    print(f"Total card data before operation {totalCardData}")

    print("Preapre dataset")
    for i in range(0, itteration):
        cardId = generate_random_hex(14)
        cardPin = bcrypt.hashpw(generate_random_pin(6).encode("utf-8"), bcrypt.gensalt(10))
        payload = {
            "cardId":cardId, "cardStatus":"REGISTER", "pin":cardPin.decode("utf-8"), "isTwoStepAuth":False, "isBanned":False
        }
        data_container.append(payload)
        print(f"\rGenerating data number {i + 1} of {itteration}", end='', flush=True)
    print()    
    print("Success genrating data")    

    print("Inserting data")
    start_time = time.time()
    for data in data_container:
        insertCardData(conn, data["cardId"], data["cardStatus"], data["pin"], data["isTwoStepAuth"], data["isBanned"])
    end_time = time.time()

    elapsed_time = end_time - start_time
    inserts_per_second = itteration / elapsed_time

    print(f"Total inserts: {itteration}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Inserts per second: {inserts_per_second:.2f}")
    totalCardData = conn.cursor().execute(f"SELECT COUNT(*) FROM card").fetchone()[0]
    print(f"Total card data after operation: {totalCardData}")

    conn.close()

if __name__ == "__main__":
    main()