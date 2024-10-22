# Utiliser une image Python officielle avec Python 3.11
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier tout le reste du projet dans le conteneur
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--log-file", "-"]
