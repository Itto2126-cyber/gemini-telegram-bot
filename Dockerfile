# Usa un'immagine Python leggera
FROM python:3.9-slim

# Imposta la cartella di lavoro all'interno del container
WORKDIR /code

# Copia il file delle dipendenze e installale
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice del bot
COPY . .

# Comando per avviare il bot quando il servizio parte
CMD ["python", "bot.py"]