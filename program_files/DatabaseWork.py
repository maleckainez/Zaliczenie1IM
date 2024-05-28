import sqlite3
import hashlib
with sqlite3.connect("../program_files/databases/testowe.db") as connection:
    cursor = connection.cursor()

    create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                imie TEXT  NOT NULL,
                nazwisko TEXT NOT NULL,
                haslo_hash TEXT NOT NULL,
                uprawnienia TEXT NOT NULL );
            """
    cursor.execute(create_table_query)
    login="admin"
    imie="admin"
    nazwisko="admin"
    haslo="admin"
    haslo_hash = hashlib.sha256(haslo.encode()).hexdigest()
    uprawnienia ="admin"
    add_user_query = "INSERT INTO users (login, imie, nazwisko, haslo_hash, uprawnienia) VALUES (?, ?, ?, ?, ?);"
    cursor.execute(add_user_query,(login, imie, nazwisko, haslo_hash, uprawnienia))


    create_table_query = """
        CREATE TABLE IF NOT EXISTS rejestr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rodzaj_dokumentu TEXT NOT NULL,
            nr_wewnetrzny TEXT UNIQUE NOT NULL,
            nadawca_dokumentu TEXT NOT NULL,
            odbiorca_dokumentu TEXT NOT NULL,
            tytul_pisma TEXT NOT NULL,
            krotki_opis TEXT,
            kod_katalogowy TEXT UNIQUE NOT NULL );
        """
    cursor.execute(create_table_query)

    connection.commit()

