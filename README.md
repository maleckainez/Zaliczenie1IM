# Projekt Python - INEZ MAŁECKA

> Niniejszy projekt został wykonany na zaliczenie pierwszego semestru studiów niestacjonarnych na kierunku INFORMATYKA na Uniwersytecie DSW, przez studentkę Inez Małecka o numerze indeksu 52738

## Spis Treści
* [Informacje Ogólne](#informacje-ogólne)
* [Zastosowane Technologie](#zastosowane-technologie)
* [Funkcjonalności Programu](#funkcjonalności-programu)
* [Wymagania, Instalacja](#wymagania-instalacja)
* [Uruchomienie](#uruchomienie)
* [Inspiracje, Autorstwo](#inspiracje-autorstwo)
* [Kontakt](#kontakt)

<a name="informacje-ogólne"></a>
## Informacje Ogólne
Powyższy program powstał jako odpowiedź na istniejące zapotrzebowanie na efektywny, tani i godny zaufania system katalogowania dokumentów przychodzących oraz wychodzących z małych i średnich przedsiębiorstw. W związku z doświadczeniem w pracy jako Asystenka Projektanta w firmie Projektowo-Konsultingowej, znając problemy oraz często pojawiające nieścisłości związane z dużą ilością pism i dokumentacji wpływających oraz wychodzących z firmy, niniejszy program został przystosowany do prostego katalogowania dokumentów.

Powyższy program jest projektem na zaliczenie przedmiotu "Programowanie w języku Python", jednakże planowane jest go wdrożenie w życiu zawodowym, rozwijanie funkcjonalości oraz debugowanie ew. zaistniejących problemów.

<a name="zastosowane-technologie"></a>
## Zastosowane Technologie

1. Język programowania - Python 3.12
2. Framework - PyQt6
3. Bazy danych - SQLite3

Program ten korzysta z wielu bibliotek zawartych w [wymagania systemowe](#Wymagania-Instalacja). Głównym językiem programowania jaki zastosowano w tym projekcie jest python 3.12 mający wiele modułów które znalazły zastosowanie w kodzie źródłowym programu.

Z racji wykorzystania SQLite do stworzenia oraz zarządzania bazami danych, nie ma potrzeby przeprowadzania instalacji dodatkowego środowiska.

<a name="funkcjonalności-programu"></a>
## Funkcjonalności Programu

Projekt oferuje następujące funkcje:

1. **Katalogowanie dokumentów:** Program w kolejnej aktualizacji umożliwi dodawanie, edycję i usuwanie raportów dotyczących dokumentów przychodzącyych oraz wychodzących, przypisując im odpowiednie kategorie i tagi.

2. **Wyszukiwanie:** Program w kolejnej aktualizacji umożliwi szybkie wyszukanie dokumentów na podstawie różnych kryteriów, takich jak tytuł, data, kategoria, itp.

3. **Statystyki:** Program w kolejnej aktualizacji generować będzie statystyki na temat ilości dokumentów w poszczególnych kategoriach, co ułatwii analizę i zarządzanie.

4. **Zarządzanie użytkownikami:** Program umożliwia dodanie poprzez panel aministratora użytkowników, usuwanie ich, zmianę loginu oraz hasła. Nie dopuszcza on powtarzających się loginów oraz loginów zawierających duże litery. Hasła dodane poprzez panel administratora są automatycznie zabezpieczone poprzez algorytm hashujący.

5. **Interaktywny formularz:** Program umożliwia zebranie wszystkich istotnych informacji dot. rejestrowanego dokumentu w jednym formularzu, każdorazowo generując mu unikalny kod katalogowy oraz kod kreskowy, który można wydrukować na drukarce do etykiet podłączonej do komputera. 

<a name="wymagania-instalacja"></a>
## Wymagania-Instalacja

### Wymagania Systemowe

Aby korzystać z programu, wymagane są następujące zależności:

- Python 3.12
- Biblioteka code128 v0.3
- Biblioteka peewee v3.17.0
- Biblioteka pillow v10.2.0
- Biblioteka PyQt6 v.6.6.1
- Biblioteka python-barcode v0.15.1


### Instalacja

1. Sklonuj repozytorium na swój lokalny komputer lub rozpakuj archiwum .rar:

    ```bash
    # Jeśli pobierasz z GitHub
    git clone https://github.com/maleckainez/Zaliczenie1IM.git
    ```

2. Przejdź do katalogu projektu:

    ```bash
    # Jeśli pobierasz z GitHub
    cd <lokalizacja folderu>/Zaliczenie1IM-main
    # Jeśli plik został wypakowany z archiwum .rar
    cd <lokalizacja folderu>/Zaliczenie1IM
    ```

3. Nie musisz instalować zależności, instalują się one przy rozruchu programu!

<a name="uruchomienie"></a>
## Uruchomienie

Aby uruchomić program, wykonaj poniższe kroki:

1. Otwórz terminal w katalogu projektu.

2. Uruchom program za pomocą komendy:

    ```bash
    python3.12 run_OfficeHelper.py
    ```

3. jeżeli biblioteki nie zainstalowały się automatycznie, zrób to za pomocą komendy:
   
   ```bash
    python3.12 -m pip install -r requirements.txt
    ```

<a name="inspiracje-autorstwo"></a>
## Inspiracje, Autorstwo

Program był inspirowany codziennymi potrzebami związanymi z zarządzaniem dokumentacją w małych i średnich przedsiębiorstwach. 

Planowane aktualizacje wynikają ze zgłoszonego zapotrzebowania przez współpracowników autorki, którzy w trakcie wywiadu zwrócili uwagę na na potrzebę wprowadzenia w firmie systemu podobnego do "Slack", lecz bardziej czytelnego i skrojonego dla użytkowników nie dających sobie rady z technologią.

&copy; Inez Małecka

<a name="kontakt"></a>
## Kontakt

Jeśli masz pytania, sugestie lub chcesz zgłosić błędy, skontaktuj się ze mną:

- Email: [maleckainez@gmail.com](mailto:maleckainez@gmail.com)
- LinkedIn: [https://www.linkedin.com/in/inez-małecka/](https://www.linkedin.com/in/inez-małecka-828408226/)
- GitHub: [github.com/maleckainez](https://github.com/maleckainez)
