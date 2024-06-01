import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Przykładowe dane: Każde zadanie ma termin (dni), szacowany czas trwania (godziny) i historyczny czas realizacji (godziny)
data = {
    'deadline': [1, 2, 3, 4, 5, 1, 3, 2, 5, 4],
    'estimated_duration': [2, 1, 4, 3, 2, 3, 1, 4, 2, 3],
    'historical_completion': [2, 1, 4, 3, 2, 3, 1, 4, 2, 3],
    'priority': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1]  # 1 = wysoki, 0 = niski
}

# Konwersja do DataFrame
df = pd.DataFrame(data)

# Cechy i cel
X = df[['deadline', 'estimated_duration', 'historical_completion']]
y = df['priority']

# Podział danych na zbiory treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicjalizacja i trening modelu
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Dokonywanie przewidywań
y_pred = model.predict(X_test)

# Ocena modelu
accuracy = accuracy_score(y_test, y_pred)
print(f"Dokładność: {accuracy * 100:.2f}%")

# Przykład przewidywania
new_task = pd.DataFrame([[2, 2, 3]], columns=['deadline', 'estimated_duration', 'historical_completion'])  # Przykładowe zadanie z terminem 2 dni, szacowanym czasem 2 godziny i historycznym czasem realizacji 3 godziny
predicted_priority = model.predict(new_task)
print(f"Przewidywany priorytet: {'Wysoki' if predicted_priority[0] == 1 else 'Niski'}")
