import os
import time
import sys  # Umożliwia pobranie danych z systemu
import random  # Umożliwia generowanie losowych liczb dla kodów katalogowych
from datetime import datetime  # Umożliwia pobranie daty z systemu-katalogowanie wejść do rejestru
import hashlib  # Import umożliwiający hashowanie haseł
import sqlite3  # Import umożliwiający integrację baz danych w sqlite
# Poniżej, import elementów framework'u PyQt:
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintEngine, QPrintPreviewDialog
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMessageBox
import code128
import io
from PIL import Image, ImageDraw, ImageFont
from PyQt6.QtGui import QPixmap, QPainter, QImage

# Poniżej, wszystkie potrzebne publiczne dane:
wersja = "0.7.120 private"
nazwa_firmy_global = "PRI Kępno ZUP-K"
uprawnienia_lista = ["Użytkownik", "Administrator"]
dostep = ""
uprawnienia_administratora = False

def sprawdz_dostep_dekorator(sprawdzanie_dostepu):
    def wrapper(*args, **kwargs):
        if dostep == uprawnienia_lista[1]:
            uprawnienia_administratora = True
            print(f"Dekorator: {uprawnienia_administratora}")
            return sprawdzanie_dostepu(*args, uprawnienia_administratora, **kwargs)
        else:
            uprawnienia_administratora = False
            print(f"Dekorator: {uprawnienia_administratora}")
            return sprawdzanie_dostepu(*args, uprawnienia_administratora, **kwargs)
    return wrapper
def Generowanie_numeru():
    unikatowy_id = ''.join(random.choices('0123456789', k=10))
    dzisiejsza_data = datetime.now().strftime("%d%m%Y")
    KodKatalogowy_formularz = f"{unikatowy_id}-{dzisiejsza_data}"
    return KodKatalogowy_formularz
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
class OknoGlowne(QWidget):  # Definiuje wszystkie komenty głównego ekranu aplikacji
    def __init__(self):
        super().__init__()
        uic.loadUi("program_files/ui_files/mainwindow.ui", self)  # Ładuje UI przygotowane w Qt i formatowane w CSS
        self.przycisk_dodawania()
        self.dodaj_user.clicked.connect(self.otworz_panel_admina)
        self.zalogowano.setText(
            f"Zalogowano: {dane_usera}\nUprawnienia użytkownika: {dostep}")  # Do loginu przypisane są dane osobowe i
        # uprawnienie, wyświetla to w odpowiednim miejscu
        self.build.setText(
            f"Copyright Inez Malecka\n Build: {wersja}")  # Do informacji o właścicielu praw autorskich do tej
        # aplikacji, dodaje informację o obecnej jej wersji
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Wyłączenie górna paska w oknie systemowym
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Przeźroczyste tło okna systemowego
        self.zamknij.clicked.connect(self.zamknij_okno)  # Wciśnięcie czerwonego kółeczka zamyka aplikację
        self.wyloguj.clicked.connect(self.wyloguj_sie)  # Wciśnięcie przycisku przenosi go do okna logowania
        self.formularz.clicked.connect(self.otworz_formularz)  # Wciśnięcie przycisku formularz, pozwala go otworzyć
        self.odswierz_rejestr()



    @sprawdz_dostep_dekorator
    def przycisk_dodawania(self, uprawnienia_administratora):
        print(f"zadziałała cz0, uprawnienia {uprawnienia_administratora}")
        if uprawnienia_administratora:
            self.dodaj_user.setVisible(True)
            self.dodaj_user.setEnabled(True)
            self.tlo_dodaj_user.setVisible(True)
            print(f"uprawnienia administratora {uprawnienia_administratora}")
        else:
            self.dodaj_user.setVisible(False)
            self.dodaj_user.setEnabled(False)
            self.tlo_dodaj_user.setVisible(False)
    def otworz_panel_admina(self):
            self.panel_admina_otwieranie = Okno_Panel_Administracyjny()
            self.panel_admina_otwieranie.exec()

    def otworz_formularz(self):  # Definiuje sposób otwarcia formularza
        self.formularz_dokumentu = FormularzDokumentu()
        self.formularz_dokumentu.exec()
    def zamknij_okno(self):  # Definiuje sposób zamknięcia okna
        self.close()
    def wyloguj_sie(self):  # Definiuje sposób wylogowania się
        self.main_window = OknoLogowania()
        self.main_window.show()
        self.close()

    def odswierz_rejestr(self):
        with sqlite3.connect("program_files/databases/baza_danych_userow.db") as connection:
            cursor = connection.cursor()
            self.widok_rejestru.clear()
            cursor.execute(
                "SELECT dodajacy, rodzaj_dokumentu, nr_wewnetrzny, nadawca_dokumentu, odbiorca_dokumentu, tytul_pisma, krotki_opis, kod_katalogowy FROM rejestr")
            daneRejestru = cursor.fetchall()
            print("Polaczono")

        # Ustawienie liczby wierszy i kolumn
        self.widok_rejestru.setRowCount(len(daneRejestru))
        self.widok_rejestru.setColumnCount(8)
        self.widok_rejestru.verticalHeader().setVisible(True)
        print("Ustawiono wiersze i kolumny")

        # Ustawienie nagłówków kolumn
        self.widok_rejestru.setHorizontalHeaderLabels(
            ["Dodajacy", "Rodzaj", "Nr Wewn", "Nadawca", "Odbiorca", "Tytuł", "Opis", "Kod"])
        print("Ustawiono tytuly")
        # Ustawienie właściwości tabeli
        self.widok_rejestru.setShowGrid(True)  # Usunięcie linii siatki
        self.widok_rejestru.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)  # Zaznaczanie całych wierszy

        # Wypełnienie tabeli danymi
        for row_idx, entry in enumerate(daneRejestru):
            for col_idx, value in enumerate(entry):
                item = QTableWidgetItem(str(value))
                self.widok_rejestru.setItem(row_idx, col_idx, item)
                print("uzupelniono")


class FormularzDokumentu(QtWidgets.QDialog):  # Definiuje wszyskie komendy w formularzu
    def __init__(self):
        super().__init__()
        uic.loadUi("program_files/ui_files/formularz_dokumentu.ui", self)  # Ładuje UI przygotowane w Qt i formatowane w CSS
        self.indywidualny_numer = Generowanie_numeru()
        self.generuj_kod_kreskowy()
        self.wczytaj_obrazek_kodu()
        self.kod_katalogowy.setText(
            f"{self.indywidualny_numer}")  # Wygenerowany, idywidualny kod katalogowy zostaje wyświetlony
        self.zamknij.clicked.connect(self.zamknij_okno)  # Definiuje zamknięcie okna po naciśnięciu przycisku
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Again, chowa pasek
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Again, chowa tło
        self.drukuj.clicked.connect(self.wydrukuj_kod)  # Wykorzystując odpowiednią bibliotekę frameworku, umożliwia wydrukowanie kodu
        self.zatwierdz.clicked.connect(self.zapisz_rekord_rejestr) # Po kliknęciu w "zapisz" dane zapisywane sa w database
    def wydrukuj_kod(self):
        self.okno_drukowania_kodu = self.aplikacja_drukujaca()
    class aplikacja_drukujaca(QWidget):
        def __init__(self):
            super().__init__()
            self.printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            self.otworz_kod_kreskowy()
        def otworz_kod_kreskowy(self):
            nazwa_pliku = "program_files/databases/temp_files/kod_kreskowy.png"  # Zawsze drukujemy ten plik
            self.image = QPixmap(nazwa_pliku)
            self.dialog_drukowania()
        def dialog_drukowania(self):
            dialog = QPrintDialog(self.printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.operacja_drukowania()
        def operacja_drukowania(self):
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image.toImage())
    def generuj_kod_kreskowy(self):
        wartosc_kodu_kreskowego = self.indywidualny_numer
        wartosc_dpi = 400
        # tworzenie obrazka kodu kreskowego
        obrazek_kodu_kreskowego = code128.image(wartosc_kodu_kreskowego, height=100)
        # Tworzenie pustej podstawki na tekst i kod
        margines_gora_dol = 70
        pragines_prawa_lewa = 10
        nowe_h = obrazek_kodu_kreskowego.height + (2 * margines_gora_dol)
        nowa_szer = obrazek_kodu_kreskowego.width + (2 * pragines_prawa_lewa)
        nowy_obrazek = Image.new('RGB', (nowa_szer, nowe_h), (255, 255, 255))
        draw = ImageDraw.Draw(nowy_obrazek)
        #Definiowanie rozmiaru tekstu
        rozmiar_H1 = 20
        rozmiar_H2 = 20
        rozmiar_H3 = 16
        rozmiar_H4 = 21
        font_H1 = ImageFont.truetype("program_files/fonts/DejaVuSans-Bold.ttf", rozmiar_H1)
        font_H2 = ImageFont.truetype("program_files/fonts/Ubuntu-Th.ttf", rozmiar_H2)
        font_H3 = ImageFont.truetype("program_files/fonts/Ubuntu-Th.ttf", rozmiar_H3)
        font_H4 = ImageFont.truetype("program_files/fonts/arial.ttf", rozmiar_H4)
        nazwa_firmy_na_kodzie = nazwa_firmy_global
        data_utworzenia = datetime.now().strftime("%d/%m/%Y")
        pracownik_tworzacy = f"Wygenerowano przez użytkownika {dane_usera}"
        wycentruj_wartosc_kodu_kreskowego = (nowy_obrazek.width / 2) - len(wartosc_kodu_kreskowego) * 6.5
        # Stwórz tekst na obrazie
        draw.text((pragines_prawa_lewa, 0), nazwa_firmy_na_kodzie, fill=(0, 0, 0), font=font_H1)
        draw.text((pragines_prawa_lewa, rozmiar_H1), data_utworzenia, fill=(0, 0, 0), font=font_H2)
        draw.text((pragines_prawa_lewa + 2, (rozmiar_H1 + rozmiar_H2 + 5)), pracownik_tworzacy, fill=(0, 0, 0), font=font_H3)
        draw.text((wycentruj_wartosc_kodu_kreskowego, (nowe_h - rozmiar_H4 - 15)), wartosc_kodu_kreskowego, fill=(0, 0, 0), font=font_H1)
        # wklej kod kreskowy na nowy obraz z tekstem
        nowy_obrazek.paste(obrazek_kodu_kreskowego, (0, 80))
        print(wartosc_kodu_kreskowego)
        # save in file
        nowy_obrazek.save('program_files/databases/kod_kreskowy.png', 'PNG', dpi=(wartosc_dpi, wartosc_dpi))
    def wczytaj_obrazek_kodu(self):
        kodzik_kreskowy = QPixmap('program_files/databases/kod_kreskowy.png')
        # Sprawdzenie czy obraz został wczytany poprawnie
        if not kodzik_kreskowy.isNull():
            self.kod_kreskowy.setPixmap(kodzik_kreskowy)  # Ustawienie obrazu w etykiecie
            self.kod_kreskowy.setScaledContents(True)  # Dopuszczenie skalowania zawartości etykiety
        self.show()
    def zamknij_okno(self):  # Again, definiuje zamknięcie okna
        self.close()
        os.remove('program_files/databases/kod_kreskowy.png')
    def zapisz_rekord_rejestr(self):
        dodajacy = dane_usera
        rodzajDokumentu = self.rodzajDokumentu.currentText()
        nrwewn = self.nrwewn.text()
        nadawca = self.nadawca.text()
        odbiorca = self.odbiorca.text()
        tytul = self.tytul.text()
        uwagi = self.uwagi.toPlainText()
        indywidualny_numer = self.indywidualny_numer
        print(f"{rodzajDokumentu}, {nrwewn}, {nadawca}, {odbiorca}, {tytul}, {uwagi}, {indywidualny_numer}")
        try:
            connection = sqlite3.connect('program_files/databases/baza_danych_userow.db')
            cursor = connection.cursor()
            rejestr_query = "INSERT INTO rejestr ( dodajacy, rodzaj_dokumentu, nr_wewnetrzny, nadawca_dokumentu, odbiorca_dokumentu, tytul_pisma, krotki_opis, kod_katalogowy) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
            cursor.execute(rejestr_query, (dodajacy, rodzajDokumentu, nrwewn, nadawca, odbiorca, tytul, uwagi, indywidualny_numer))
            connection.commit()
            connection.close()
            print("Datos rejestrados")
            popup = QMessageBox()
            popup.setWindowTitle("Pomyślnie dodano!")
            popup.setText("Pomyślnie dodano dokument do Rejestru")
            popup.exec()
        except Exception as e:
            print(e)
            connection.close()
class Okno_Panel_Administracyjny(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("program_files/ui_files/zarzadzaj_uzytkownikami.ui", self)
        self.connection = sqlite3.connect('program_files/databases/baza_danych_userow.db')
        self.cursor = self.connection.cursor()
        self.odswiez_liste_istniejacych()
        self.panel_administratora_button_dodaj_uzytkownika.clicked.connect(self.dodaj_nowego_usera)
        # Wczytanie danych z bazy danych i wyświetlenie ich w tabeli
        self.panel_administratora_button_usun_usera.clicked.connect(self.usun_uzytkownika_z_bazy)
        self.panel_administratora_button_zmien_login_usera.clicked.connect(self.zmien_login_ist_usera)
        self.panel_administratora_button_zmien_haslo_usera.clicked.connect(self.zmien_haslo_istniejacego_usera)

    def odswiez_liste_istniejacych(self):
        with sqlite3.connect("program_files/databases/baza_danych_userow.db") as connection:
            cursor = connection.cursor()
            self.panel_administratora_show_users.clear()
            self.cursor.execute("SELECT login, imie, nazwisko, haslo_hash, uprawnienia FROM users")
            istniejacy_uzytkownicy = self.cursor.fetchall()

        # Ustawienie liczby wierszy i kolumn
            self.panel_administratora_show_users.setRowCount(len(istniejacy_uzytkownicy))
            self.panel_administratora_show_users.setColumnCount(5)
            self.panel_administratora_show_users.verticalHeader().setVisible(False)

        # Ustawienie nagłówków kolumn
            self.panel_administratora_show_users.setHorizontalHeaderLabels(
            ["Login", "Imię", "Nazwisko", "Haslo", "Uprawnienia"])

        # Ustawienie właściwości tabeli
            self.panel_administratora_show_users.setShowGrid(False)  # Usunięcie linii siatki
            self.panel_administratora_show_users.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Zaznaczanie całych wierszy

        # Wypełnienie tabeli danymi
            for row_idx, uzytkownik in enumerate(istniejacy_uzytkownicy):
                for col_idx, value in enumerate(uzytkownik):
                    item = QTableWidgetItem(str(value))
                    self.panel_administratora_show_users.setItem(row_idx, col_idx, item)

    def dodaj_nowego_usera(self):
        # Pobranie danych z pól tekstowych
        nowy_user_imie = self.panel_administratora_input_imie.text()
        nowy_user_nazwisko = self.panel_administratora_input_nazwisko.text()
        nowy_user_login = self.panel_administratora_input_login.text()
        nowy_user_login = nowy_user_login.lower()
        nowy_user_haslo = self.panel_administratora_input_haslo.text()
        nowy_user_haslo_hash = hashlib.sha256(nowy_user_haslo.encode()).hexdigest()
        nowy_user_uprawnienia = self.panel_administratora_wybierz_uprawnienia.currentText()
        if nowy_user_imie and nowy_user_nazwisko and nowy_user_login and nowy_user_haslo:
            if nowy_user_uprawnienia.strip() in ["admin", "user"]:
                print(nowy_user_uprawnienia.strip())
                try:
                    if nowy_user_uprawnienia == uprawnienia_lista[1]:
                        nowy_user_uprawnienia == "admin"
                    elif nowy_user_uprawnienia == uprawnienia_lista[0]:
                        nowy_user_uprawnienia == "user"

                except Exception as e:
                    print(f"Błąd {e}")
                # Dodanie nowego użytkownika
                self.dodaj_nowego_usera_czynnosc(nowy_user_login, nowy_user_imie, nowy_user_nazwisko,
                                          nowy_user_haslo_hash, nowy_user_uprawnienia)
                self.panel_administratora_button_dodaj_uzytkownika.setEnabled(False)
            else:
                self.panel_administratora_label_dodano_uzytkownika.setText("Wybierz uprawnienia!")
        else:
            self.panel_administratora_label_dodano_uzytkownika.setText("Pola nie mogą być puste!")
    def dodaj_nowego_usera_czynnosc(self, nowy_user_login, nowy_user_imie, nowy_user_nazwisko, nowy_user_haslo_hash, nowy_user_uprawnienia):
        try:
            connection = sqlite3.connect("program_files/databases/baza_danych_userow.db")
            cursor = connection.cursor()
            add_user_query = "INSERT INTO users (login, imie, nazwisko, haslo_hash, uprawnienia) VALUES (?, ?, ?, ?, ?);"
            cursor.execute(add_user_query, (nowy_user_login, nowy_user_imie, nowy_user_nazwisko, nowy_user_haslo_hash, nowy_user_uprawnienia))
            connection.commit()
            self.panel_administratora_label_dodano_uzytkownika.setText("Do spisu użykowników dodano nowego użytkownika!")
            self.czyszczenie_pola_dodawnia()
        except sqlite3.IntegrityError:
            self.panel_administratora_label_dodano_uzytkownika.setText("Wystąpił błąd, login musi być unikalny!")
            connection.close()
        except sqlite3.OperationalError or IndexError or AttributeError or NameError or TypeError:
            self.panel_administratora_label_dodano_uzytkownika.setText("Wystąpił błąd!")
            connection.close()
        self.odswiez_liste_istniejacych()
        QTimer.singleShot(500, self.wlacz_przycisk_dodawania)
    def wlacz_przycisk_dodawania(self):
            self.panel_administratora_button_dodaj_uzytkownika.setEnabled(True)
    def czyszczenie_pola_dodawnia(self):
        self.panel_administratora_input_imie.clear()
        self.panel_administratora_input_nazwisko.clear()
        self.panel_administratora_input_login.clear()
        self.panel_administratora_input_haslo.clear()
        self.panel_administratora_wybierz_uprawnienia.setCurrentIndex(0)
    def usun_uzytkownika_z_bazy(self):
        wybrane_elementy = self.panel_administratora_show_users.selectedItems()
        if wybrane_elementy:
            wybrany_wiersz = wybrane_elementy[0].row()
            dane_do_usuniecia = [self.panel_administratora_show_users.item(wybrany_wiersz, i).text() for i in range(5)]
            try:
                connection = sqlite3.connect("program_files/databases/baza_danych_userow.db")
                cursor = connection.cursor()
                # Pobranie identyfikatora użytkownika na podstawie wszystkich dostępnych danych
                cursor.execute(
                    "SELECT id FROM users WHERE login = ? AND imie = ? AND nazwisko = ? AND haslo_hash = ? AND uprawnienia = ?",
                    tuple(dane_do_usuniecia))
                row = cursor.fetchone()
                if row:
                    id_uzytkownika = row[0]
                    # Usunięcie użytkownika na podstawie jego identyfikatora
                    cursor.execute("DELETE FROM users WHERE id = ?", (id_uzytkownika,))
                    connection.commit()
            except:
             pass
        self.odswiez_liste_istniejacych()


    def zmien_login_ist_usera(self):
        try:
            wybrany_element = self.panel_administratora_show_users.selectedItems()
            nowy_login_usera = self.panel_administratora_input_zmien_login_usera.text()
            nowy_login_usera = nowy_login_usera.lower()

            if len(wybrany_element) == 0:
                self.panel_administratora_blad_zmien_login_usera.setText("Nie wybrano użytkownika")
                return

            wybrany_wiersz = wybrany_element[0].row()
            wybrany_element = self.panel_administratora_show_users.item(wybrany_wiersz, 0)

            if nowy_login_usera.strip() == "":
                self.panel_administratora_blad_zmien_login_usera.setText("Login nie może być pusty!")
                return

            if wybrany_element is not None:
                login_do_zmiany = wybrany_element.text()
                login_do_zmiany = login_do_zmiany.lower()
                if login_do_zmiany:
                    with sqlite3.connect("program_files/databases/baza_danych_userow.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("SELECT COUNT(*) FROM users WHERE login = ?", (nowy_login_usera,))
                        count = cursor.fetchone()[0]
                        if count > 0:
                            self.panel_administratora_blad_zmien_login_usera.setText("Login musi być unikalny!")
                        else:
                            cursor.execute("UPDATE users SET login = ? WHERE login = ?",
                                           (nowy_login_usera, login_do_zmiany,))
                            connection.commit()
                            self.panel_administratora_blad_zmien_login_usera.setText("Zmieniono login!")
            else:
                self.panel_administratora_blad_zmien_login_usera.setText("Nie wybrano użytkownika")

        except (sqlite3.IntegrityError, sqlite3.OperationalError, IndexError, AttributeError) as e:
            self.panel_administratora_blad_zmien_login_usera.setText("Błąd")
        self.odswiez_liste_istniejacych()

    def zmien_haslo_istniejacego_usera(self):
        try:
            wybrany_element = self.panel_administratora_show_users.selectedItems()
            nowe_haslo_usera = self.panel_administratora_input_zmien_haslo_usera.text()
            nowe_haslo_usera_hash = hashlib.sha256(nowe_haslo_usera.encode()).hexdigest()

            if len(wybrany_element) == 0:
                self.panel_administratora_blad_zmien_haslo_usera.setText("Nie wybrano użytkownika")
                return

            # Sprawdź, czy nowe hasło jest puste
            if not nowe_haslo_usera.strip():
                self.panel_administratora_blad_zmien_haslo_usera.setText("Nowe hasło nie może być puste!")
                return

            wybrany_wiersz = wybrany_element[0].row()
            wybrany_element = self.panel_administratora_show_users.item(wybrany_wiersz, 0)

            if wybrany_element is not None:
                try:
                    wybrany_user = wybrany_element.text()
                    if wybrany_user:
                        with sqlite3.connect("program_files/databases/baza_danych_userow.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("UPDATE users SET haslo_hash = ? WHERE login = ?",
                                           (nowe_haslo_usera_hash, wybrany_user))
                            connection.commit()
                            self.panel_administratora_blad_zmien_haslo_usera.setText("Zmieniono hasło!")
                    else:
                        self.panel_administratora_blad_zmien_haslo_usera.setText("Nie wybrano użytkownika")
                except Exception as e:
                    print("Błąd:", e)
        except Exception as e:
            print("Błąd:", e)
        self.odswiez_liste_istniejacych()

app = QtWidgets.QApplication(sys.argv)
window = OknoLogowania()  # Definiuje że pierwszym otwartym oknem będzie okno logowania
window.show()
app.exec()