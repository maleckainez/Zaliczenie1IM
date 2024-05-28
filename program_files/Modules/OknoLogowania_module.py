class OknoLogowania(QWidget):  # Wszystkie komendy okna logowania
    def __init__(self):
        super().__init__()
        uic.loadUi("program_files/ui_files/form.ui", self)  # Ładuje UI przygotowane w Qt i formatowane w CSS
        #self.setGeometry(300, 300, 700, 600)
        self.build.setText(f"Build: {wersja}")  # Wyświetla numer wersji na dole okna
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Wyłączenie górna paska w oknie systemowym
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Przeźroczyste tło okna systemowego
        self.pushButton.clicked.connect(self.logowanie_z_baza_danych)  # Przycisk zalogowania pozwala się zalogować
        self.login_z_okna.returnPressed.connect(
            self.logowanie_z_baza_danych)  # Wciśnięcie ENTER w oknie logowania pozwala się zalogować
        self.haslo.returnPressed.connect(
            self.logowanie_z_baza_danych)  # Wciśnięcie ENTER w oknie hasła pozwala się zalogować
        self.zamknij.clicked.connect(self.Zamknij)  # Wciśnięcie czerwonego kółeczka zamyka aplikację

    def logowanie_z_baza_danych(self):
        wprowadzony_login = self.login_z_okna.text()
        wprowadzony_login = wprowadzony_login.lower()
        wprowadzone_haslo = self.haslo.text()
        wprowadzone_haslo_hash = hashlib.sha256(wprowadzone_haslo.encode()).hexdigest()
        # Logowanie użytkownika z bazą danych
        with sqlite3.connect('program_files/databases/baza_danych_userow.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE login=?", (wprowadzony_login,))
            uzytkownik = cursor.fetchone()

            if uzytkownik is not None:
                uzytkownik_id, uzytkownik_login, imie, nazwisko, haslo_hash, uprawnienia = uzytkownik
                if uzytkownik_login == wprowadzony_login and haslo_hash == wprowadzone_haslo_hash:
                    global dostep, dane_usera
                    dane_usera = f"{imie} {nazwisko}"
                    dostep = uprawnienia_lista[1] if uprawnienia == "admin" else uprawnienia_lista[0]
                    self.przejdz_dalej()
                    return dane_usera, dostep
                else:
                    self.blad_logowania.setText("Hasło lub login zostały wpisane niepoprawnie")
            else:
                self.blad_logowania.setText("Brak użytkownika o podanym loginie")

    def przejdz_dalej(self):
        self.main_window = OknoGlowne()
        self.main_window.show()
        self.close()
    def Zamknij(self):  # Definiuje sposób zamknięcia okna - wywołuje je kliknięcie przycisku zamknij
        self.close()  # Zamyka okno
