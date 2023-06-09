import pymysql
import csv
import getpass

# Initialisation d'un dictionnaire vide pour stocker les paramètres de connexion

db = input("Nom de la base de donnée: ")
user = input("Nom d'utilisateur: ")
password = getpass.getpass("Mot de passe: ")

conn = pymysql.connect(host='localhost',
                       user=user,
                       password=password,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

cursor = conn.cursor()
cursor.execute(f"DROP DATABASE IF EXISTS {db}")
conn.commit()

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS " + db)
conn.commit()

print("Base de données créée !\n")

conn = pymysql.connect(host='localhost',
                       user=user,
                       password=password,
                       db=db,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

print("Connexion à la base de données réussie !\n")
cursor = conn.cursor()

def create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS Boxeurs (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(255), prenom VARCHAR(255), categorie VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Combats (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, boxeur1_id INT, boxeur2_id INT, categorie VARCHAR(255), lieu VARCHAR(255), points1 INT, points2 INT, winner_id INT, win_method VARCHAR(255), FOREIGN KEY (boxeur1_id) REFERENCES Boxeurs(id), FOREIGN KEY (boxeur2_id) REFERENCES Boxeurs(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Juge (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(255), prenom VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Score (id_score INT AUTO_INCREMENT PRIMARY KEY, juge_id INT, combat_id INT, round_number INT, score_boxer1 INT, score_boxer2 INT, FOREIGN KEY (juge_id) REFERENCES Juge(id), FOREIGN KEY (combat_id) REFERENCES Combats(id))")
    conn.commit()




create_tables()

def insert_csv_data():

    # Boxeurs
    with open('boxeurs.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("INSERT INTO Boxeurs (nom, prenom, categorie) VALUES (%s, %s, %s)", (row['nom'], row['prenom'], row['categorie']))

    # Combats
    with open('combats.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("INSERT INTO Combats (date, boxeur1_id, boxeur2_id, categorie, lieu, points1, points2, winner_id, win_method) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['date'], row['boxeur1_id'], row['boxeur2_id'], row['categorie'], row['lieu'], row['points1'], row['points2'], row['winner_id'], row['win_method']))

    conn.commit()

    # Juge
    with open('juge.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("INSERT INTO Juge (nom, prenom) VALUES (%s, %s)", (row['nom'], row['prenom']))

    conn.commit()

    #score
    with open('score.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("INSERT INTO Score (juge_id, combat_id, score_boxer1, score_boxer2) VALUES (%s, %s, %s, %s)", (row['juge_id'], row['combat_id'], row['score_boxer1'], row['score_boxer2']))

    conn.commit()

insert_csv_data()
conn.close()

print("Données insérées avec succès !\n")

print("Base de données prête à être utilisée !\n")

print("Pour lancer l'interface WEB, exécutez le fichier main.py\n")
