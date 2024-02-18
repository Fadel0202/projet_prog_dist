# Utilisation de l'image officielle Python
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install flask-cors Flask flask_sqlalchemy flask_migrate psycopg2  gunicorn

# Exposer le port sur lequel l'application écoute
EXPOSE 8080

# Commande à exécuter lors du démarrage du conteneur
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

