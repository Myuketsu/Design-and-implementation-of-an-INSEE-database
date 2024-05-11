# BDA_project

Bonjour et bienvenue sur notre DashBoard.

Vous y retrouverez toutes les réponses aux questions posées sur moodle.
Pour profiter pleinement des outils mis à disposition, on vous invite à respecter les étapes d'initialisation qui suivent.
Assurez-vous d'ouvrir le projet à sa racine.

### Configuration des versions des bibliothèques

Pour commencer, 
exécutez le fichier : requirements.txt

### Configuration de la base de données

Pour faire fonctionner le code avec votre propre base de données, suivez les étapes suivantes :

1. Ouvrez le fichier `config.toml`.

2. Recherchez la section  `[database]` dans le fichier (tout en haut du fichier). Vous y trouverez les paramètres de connexion à la base de données.

3. Modifiez les valeurs suivantes en fonction de vos propres paramètres de base de données :
- `dbname`: remplacez `'BDA'` par le nom de votre base de données.
- `user`: remplacez `'vscode'` par votre nom d'utilisateur de base de données.
- `password`: remplacez `'SQL_BDA'` par votre mot de passe de base de données.
- `host`: si votre base de données est hébergée sur un serveur distant, remplacez `'localhost'` par l'adresse IP ou le nom de domaine de votre serveur.
- `port`: si votre base de données utilise un port différent du port par défaut `5432`, modifiez cette valeur en conséquence.

Assurez-vous d'enregistrer les modifications apportées au fichier `config.toml` une fois que vous avez terminé.

### Initialisation de la base de données

Exécutez le fichier : db_initialization.py

Le temps d'exécution peut varier selon votre machine. Sur les nôtres, les données s'importent entre 50 secondes et 1 min 30 en moyenne.

### Lancement de l'application web

Exécutez le fichier : app.py

### Quelques détails du code pour vous y retrouver

Toutes les requêtes pour créer la base de données complètes sont classées dans le dossier "sql". 
Vous y trouverez : create_tables.sql, alter_tables.sql.
Si vous devez ou voulez effacer l'entièreté de la base de données, il vous suffit d'exécuter le fichier db_killer.py.
Cela exécutera le fichier drop_tables.sql

### Concernant les fihiers .toml

Ces fichiers contiennent toutes les informations concernant la structure de nos requêtes et celle de notre base de données.

### Les questions

Les fichiers nous permettant de répondre aux questions posées ont des noms assez évidents pour vous retrouver.
Par exemple la question :

"Vues : sauf à avoir des requêtes récurrentes et fréquentes, il est de bon usage d'éviter de stocker des informations calculables. Créer deux vues (cf commande CREATE OR REPLACE VIEW) qui donnent la population des départements et des régions pour les différentes années ainsi que les indicateurs existants."

Les fichiers permettant de répondre à cette question sont donc : create_views.toml et views.py.

### Conclusion

L'application a été conçue en suivant le modèle MVC (Modèle View Controller) garantissant une bonne expérience utilisateur.
Nous avons réalisé notre base de données en 3eme forme normale ; vous trouverez son schéma sur moodle et sur PGAdmin où vous pouvez le générer.