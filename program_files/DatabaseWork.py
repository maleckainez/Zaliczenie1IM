'''class PoczątkowaBazaDanych():
    with sqlite3.connect("program_files/databases/baza_danych_userow.db") as connection:
        cursor = connection.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                imie TEXT NOT NULL,
                nazwisko TEXT NOT NULL,
                haslo_hash TEXT NOT NULL,
                uprawnienia TEXT NOT NULL
            );
            """
        haslo_hash_poczatek = "admin"
        haslo_hash_poczatek = hashlib.sha256(haslo_hash_poczatek.encode()).hexdigest()
        cursor.execute(create_table_query)

        connection.commit() '''