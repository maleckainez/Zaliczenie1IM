def zapisz_rekord_rejestr(self):
    data = datetime.now().strftime("%d/%m/%Y")
    dodajacy = dane_usera
    rodzajDokumentu = self.rodzajDokumentu.currentText()
    nrwewn = self.nrwewn.text()
    nadawca = self.nadawca.text()
    odbiorca = self.odbiorca.text()
    tytul = self.tytul.text()
    uwagi = self.uwagi.toPlainText()
    indywidualny_numer = self.indywidualny_numer
    print(f"{data}, {rodzajDokumentu}, {nrwewn}, {nadawca}, {odbiorca}, {tytul}, {uwagi}, {indywidualny_numer}")
    try:
        connection = sqlite3.connect('program_files/databases/baza_danych_userow.db')
        cursor = connection.cursor()
        rejestr_query = "INSERT INTO rejestr (data, dodajacy, rodzaj_dokumentu, nr_wewnetrzny, nadawca_dokumentu, odbiorca_dokumentu, tytul_pisma, krotki_opis, kod_katalogowy) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        cursor.execute(rejestr_query,
                       (data, dodajacy, rodzajDokumentu, nrwewn, nadawca, odbiorca, tytul, uwagi, indywidualny_numer))
        connection.commit()
        connection.close()
        print("Datos rejestrados")
        self.popup("Udało się!", "Dokument pomyślnie został dodany do rejestru!")
    except Exception as e:
        print(e)
        self.popup("Wystąpił błąd!", f"{e}")
        connection.close()