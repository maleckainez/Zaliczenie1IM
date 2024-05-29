import sqlite3
import hashlib
with sqlite3.connect("/Users/inezmalecka/Desktop/Studiowanie/Zaliczenie1IM/program_files/databases/baza_danych_userow.db") as connection:
    cursor = connection.cursor()
    drop_table = "DROP TABLE IF EXISTS rejestr "
    cursor.execute(drop_table)
    connection.commit()
#
#
#    create_table_query = """
#            CREATE TABLE IF NOT EXISTS users (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                login TEXT UNIQUE NOT NULL,
#                imie TEXT  NOT NULL,
#                nazwisko TEXT NOT NULL,
#                haslo_hash TEXT NOT NULL,
#                uprawnienia TEXT NOT NULL );
#            """
#    cursor.execute(create_table_query)
#    login="admin"
#   imie="admin"
#    nazwisko="admin"
#    haslo="admin"
#    haslo_hash = hashlib.sha256(haslo.encode()).hexdigest()
#    uprawnienia ="admin"
#    add_user_query = "INSERT INTO users (login, imie, nazwisko, haslo_hash, uprawnienia) VALUES (?, ?, ?, ?, ?);"
#    cursor.execute(add_user_query,(login, imie, nazwisko, haslo_hash, uprawnienia))


    create_table_query = """
        CREATE TABLE IF NOT EXISTS rejestr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            dodajacy TEXT NOT NULL,
            rodzaj_dokumentu TEXT NOT NULL,
            nr_wewnetrzny TEXT,
            nadawca_dokumentu TEXT NOT NULL,
            odbiorca_dokumentu TEXT NOT NULL,
            tytul_pisma TEXT NOT NULL,
            krotki_opis TEXT,
            kod_katalogowy TEXT UNIQUE NOT NULL );
        """
    cursor.execute(create_table_query)

    connection.commit()

#def dodawanierejestru():
#    rodzajDokumentu = self.rodzajDokumentu.text()
#    nrwewn = self.nrwewn.text()
#    nadawca = self.nadawca.text()
#    odbiorca = self.odbiorca.text()
#    tytul = self.tytul.text()
#    uwagi = self.uwagi.text()
#    indywidualny_numer = self.indywidualny_numer
#    with sqlite3.connect('program_files/databases/baza_danych_userow.db') as connection:
#        cursor = connection.cursor()
#        rejestr_query = "INSERT INTO rejestr (rodzaj_dokumentu, nr_wewnetrzny, nadawca_dokumentu, odbiorca_dokumentu, tytul_pisma, krotki_opis, kod_katalogowy) VALUES (?, ?, ?, ?, ?, ?, ?);"
#        cursor.execute(rejestr_query, (rodzajDokumentu, nrwewn, nadawca, odbiorca, tytul, uwagi, indywidualny_numer))
