# Dockerfile

# Verwende ein schlankes Python 3.9 Image als Basis
FROM python:3.11-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt-Datei
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere alle restlichen Dateien deines Projekts in das Arbeitsverzeichnis
COPY . .

# Definiere den Befehl, der beim Start des Containers ausgeführt wird
CMD ["python3", "bot.py"]