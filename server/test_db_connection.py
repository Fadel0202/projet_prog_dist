from sqlalchemy import create_engine
from sqlalchemy.sql import text

# Créer le moteur SQLAlchemy avec l'URI de la base de données
engine = create_engine('postgresql://postgresadmin:Samb2001@postgres:5432/students')

# Tester la connexion en exécutant une requête simple
try:
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        print(result.fetchone())
        print("Connexion réussie à la base de données PostgreSQL.")
except Exception as e:
    print("Erreur lors de la connexion à la base de données PostgreSQL :", e)

