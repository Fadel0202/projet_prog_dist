import logging
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

os.environ['FLASK_DEBUG'] = 'True'

# créer l'application Flask
app = Flask(__name__)

# Configuration du niveau de journalisation
app.logger.setLevel(logging.DEBUG)  # ou logging.DEBUG pour un niveau plus détaillé

# Configurer un gestionnaire de logs pour enregistrer les logs dans un fichier
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.DEBUG)  # ou logging.DEBUG pour un niveau plus détaillé
app.logger.addHandler(file_handler)


# Activer CORS avec des options spécifiques
CORS(app, resources={r'/*': {'origins': '*'}})


# configurer la base de données SQLite
# Configurer la base de données PostgreSQL avec l'utilisateur fadel
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresadmin:Samb2001@postgres:31798/students'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# créer l'objet SQLAlchemy
db = SQLAlchemy(app)

# créer le modèle Student
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    present = db.Column(db.Boolean, default=False)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/students', methods=['GET', 'POST'])
def get_all_students():
    if request.method == 'GET':
        # Interroger la base de données pour récupérer tous les étudiants
        students = Student.query.all()

        # Convertir les objets Student en un format JSONifiable
        student_list = [{'id': student.id, 'prenom': student.prenom, 'name': student.name, 'present': student.present} for student in students]

        # Retourner la liste des étudiants au format JSON
        return jsonify({'students': student_list})

    elif request.method == 'POST':
        # Récupérer les données du corps de la requête POST
        data = request.get_json()

        # Extraire les informations de l'élève à partir des données
        name = data.get('name')
        prenom = data.get('prenom')
        present = data.get('present', False)  # Par défaut, l'élève est marqué absent s'il n'est pas spécifié

        # Créer un nouvel objet Student avec les informations fournies
        new_student = Student(name=name, prenom=prenom, present=present)

        try:
            # Ajouter le nouvel élève à la base de données
            db.session.add(new_student)
            db.session.commit()
            return jsonify({'message': 'Élève ajouté avec succès'}), 201  # Réponse de succès avec le code HTTP 201 (Created)
        except Exception as e:
            # En cas d'erreur lors de l'ajout de l'élève
            db.session.rollback()  # Annuler les modifications de la session
            return jsonify({'error': str(e)}), 500  # Réponse d'erreur avec le code HTTP 500 (Internal Server Error)

@app.route('/students/<int:id>', methods=['PUT', 'DELETE'])
def update_or_delete_student(id):
    # Récupérer l'élève à mettre à jour ou supprimer depuis la base de données
    student = Student.query.get(id)

    # Vérifier si l'élève existe
    if student is None:
        return jsonify({'error': 'Élève non trouvé'}), 404  # Répondre avec le code HTTP 404 (Not Found) si l'élève n'est pas trouvé

    if request.method == 'PUT':
        # Récupérer les données de la requête
        data = request.get_json()

        # Mettre à jour les attributs de l'élève avec les données de la requête
        if 'name' in data:
            student.name = data['name']
        if 'prenom' in data:
            student.prenom = data['prenom']
        if 'present' in data:
            student.present = data['present']

        # Enregistrer les modifications dans la base de données
        try:
            db.session.commit()
            return jsonify({'message': 'Élève mis à jour avec succès'}), 200  # Répondre avec le code HTTP 200 (OK) si la mise à jour est réussie
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500  # Répondre avec le code HTTP 500 (Internal Server Error) en cas d'erreur lors de la mise à jour

    elif request.method == 'DELETE':
        # Supprimer l'élève de la base de données
        try:
            db.session.delete(student)
            db.session.commit()
            return jsonify({'message': 'Élève supprimé avec succès'}), 200  # Répondre avec le code HTTP 200 (OK) si la suppression est réussie
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500  # Répondre avec le code HTTP 500 (Internal Server Error) en cas d'erreur lors de la suppression



if __name__ == '__main__':
    app.run()
