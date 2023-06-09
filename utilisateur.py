import sys
import re
import pymysql


db = "Boxe"
user = "root"
password = ""

conn = pymysql.connect(host='localhost',
                        user=user,
                        password=password,
                        db=db,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)


def is_name_valid(name):
    return name[0].isupper() and name[1:].islower() and name.isalpha()


def get_boxeurs(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Boxeurs")
        boxeurs = cursor.fetchall()
        return boxeurs

class TBAWebsite(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    user=user,
                                    password=password,
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)


    def add_combat(self, conn, date, boxeur1_id, boxeur2_id, lieu_choice, win_method, winner_id):
        # Vérification de l'existence et de la catégorie des boxeurs
        with conn.cursor() as cursor:
            cursor.execute("SELECT categorie FROM Boxeurs WHERE id = %s", (boxeur1_id,))
            result = cursor.fetchone()
            if result is None:
                return f"Erreur : Aucun boxeur trouvé avec l'ID {boxeur1_id}."
            boxeur1_categorie = result["categorie"]

            cursor.execute("SELECT categorie FROM Boxeurs WHERE id = %s", (boxeur2_id,))
            result = cursor.fetchone()
            if result is None:
                return f"Erreur : Aucun boxeur trouvé avec l'ID {boxeur2_id}."
            boxeur2_categorie = result["categorie"]

        if boxeur1_categorie != boxeur2_categorie:
            return "Erreur : Les boxeurs ne sont pas de la même catégorie. Veuillez choisir deux boxeurs de la même catégorie."

        if winner_id != boxeur1_id and winner_id != boxeur2_id:
            return "Erreur : L'ID du boxeur gagnant n'est pas valide."

        categorie = boxeur1_categorie
        lieux = ['Paris', 'Lyon', 'Marseille', 'Grenoble', 'Lille', 'Saint Etienne']
        if not 1 <= lieu_choice <= 6:
            return "Erreur : Veuillez choisir un numéro entre 1 et 6."
        lieu = lieux[lieu_choice - 1]

        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Combats (date, boxeur1_id, boxeur2_id, categorie, lieu, winner_id, win_method) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                               (date, boxeur1_id, boxeur2_id, categorie, lieu, winner_id, win_method))
                conn.commit()
        except Exception as e:
            return f"Erreur lors de l'ajout du combat : {e}"

        return "Le combat a été ajouté avec succès!"

    def __del__(self):
        self.conn.close()

    def get_boxeurs(self):
        conn = pymysql.connect(host='localhost', user=user, password=password, db=db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Boxeurs")
        boxeurs = cursor.fetchall()
        conn.close()
        return boxeurs



class TBAWebsite(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    user=user,
                                    password=password,
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
    def __del__(self):
        self.conn.close()









def display_boxeur(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Boxeurs")
        boxeurs = cursor.fetchall()
        boxeur_list = []
        for boxeur in boxeurs:
            boxeur_list.append(f"{boxeur['id']} - {boxeur['nom']} {boxeur['prenom']} - Catégorie: {boxeur['categorie']}")
        return boxeur_list


def add_boxeur(nom, prenom, categorie_choice, conn):
    if nom and prenom and categorie_choice:
        if not nom[0].isupper() or not prenom[0].isupper() or len(nom) > 60 or len(prenom) > 60:
            raise ValueError("Les noms et prénoms doivent commencer par une majuscule et ne doivent pas dépasser 60 caractères.")
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Boxeurs (nom, prenom, categorie) VALUES (%s, %s, %s)", (nom, prenom, categorie_choice))
            conn.commit()











def update_boxeur(id_boxeur, new_nom=None, new_prenom=None, new_categorie=None, conn=None):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Boxeurs WHERE id=%s", (id_boxeur,))
    boxeur = cursor.fetchone()

    if boxeur:
        if new_nom:
            boxeur['nom'] = new_nom
        if new_prenom:
            boxeur['prenom'] = new_prenom
        if new_categorie:
            boxeur['categorie'] = new_categorie

        cursor.execute("UPDATE Boxeurs SET nom=%s, prenom=%s, categorie=%s WHERE id=%s",
                        (boxeur['nom'], boxeur['prenom'], boxeur['categorie'], id_boxeur))
        conn.commit()
        return "Boxeur mis à jour avec succès."
    else:
        return "Aucun boxeur trouvé avec cet ID."


# Le reste du code de add_combat() se trouve ci-dessous

def delete_boxeur(conn, boxeur_id):
    try:
        with conn.cursor() as cursor:
            # Vérifier si le boxeur existe avant de le supprimer
            cursor.execute("SELECT * FROM Boxeurs WHERE id = %s", (boxeur_id,))
            boxeur = cursor.fetchone()
            if not boxeur:
                raise ValueError("Aucun boxeur ne correspond à cet ID.")

            # Supprimer le boxeur
            cursor.execute("DELETE FROM Boxeurs WHERE id = %s", (boxeur_id,))
            conn.commit()

        return ("Boxeur supprimé avec succès.", "success")
    except ValueError as e:
        return (str(e), "danger")
    except Exception as e:
        return (f"Une erreur s'est produite lors de la suppression du boxeur. Veuillez réessayer. Erreur : {e}", "danger")





def get_combats(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT Combats.id AS combat_id, Combats.date AS combat_date, Boxeurs.nom AS boxeur1, Combats.points1, Boxeurs_1.nom AS boxeur2, Combats.points2, Combats.winner_id, Combats.win_method FROM Combats JOIN Boxeurs ON Combats.boxeur1_id = Boxeurs.id JOIN Boxeurs AS Boxeurs_1 ON Combats.boxeur2_id = Boxeurs_1.id")
        combats = cursor.fetchall()

    # Vérification et formatage des valeurs des points
    for combat in combats:
        points1 = combat['points1']
        points2 = combat['points2']
        if points1 is not None and points2 is not None:
            combat['points1'] = int(points1)
            combat['points2'] = int(points2)

    return combats









def add_combat(conn, date, boxeur1_id, boxeur2_id, lieu_choice, result_choice, winner_id):
    # Vérification de l'existence et de la catégorie des boxeurs
    with conn.cursor() as cursor:
        cursor.execute("SELECT categorie FROM Boxeurs WHERE id = %s", (boxeur1_id,))
        result = cursor.fetchone()












def update_combat(conn, id_combat, date=None, categorie=None, lieu=None):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Combats WHERE id=%s", (id_combat,))
    combat = cursor.fetchone()

    if not combat:
        return "Erreur : Aucun combat trouvé avec cet ID."

    if date and not re.match('^\d{4}-\d{2}-\d{2}$', date):
        return "Erreur : Veuillez entrer une date valide sous la forme AAAA-MM-JJ."

    if date:
        combat['date'] = date
    if categorie:
        combat['categorie'] = categorie
    if lieu:
        combat['lieu'] = lieu

    cursor.execute("UPDATE Combats SET date=%s, categorie=%s, lieu=%s WHERE id=%s", (combat['date'], combat['categorie'], combat['lieu'], id_combat))
    conn.commit()
    return "Combat mis à jour avec succès."






# ...
# Les autres fonctions restent inchangées




def delete_combat(conn, combat_id):
    try:
        combat_id = int(combat_id)
    except ValueError:
        return False, "ID invalide. Veuillez entrer un nombre entier."

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Combats WHERE id = %s", (combat_id,))
        combat = cursor.fetchone()

        if not combat:
            return False, "Aucun combat trouvé avec cet ID."

        cursor.execute("DELETE FROM Combats WHERE id = %s", (combat_id,))
        conn.commit()

    return True, "Le combat a été supprimé avec succès !"








def get_juges(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Juge")
    return cursor.fetchall()


def get_juges_byID(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT nom FROM Juge WHERE id = %s", (id))
    return cursor.fetchone()




def display_juges(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Juge")
        juges = cursor.fetchall()
    return juges





def add_juge(conn, nom, prenom):
    if not is_name_valid(nom) or len(nom) > 60:
        return "Erreur : Le nom doit commencer par une majuscule, ne contenir que des lettres et avoir une longueur maximale de 60 caractères."

    if not is_name_valid(prenom) or len(prenom) > 60:
        return "Erreur : Le prénom doit commencer par une majuscule, ne contenir que des lettres et avoir une longueur maximale de 60 caractères."

    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Juge (nom, prenom) VALUES (%s, %s)", (nom, prenom))
            conn.commit()
        return f"Le juge {prenom} {nom} a été ajouté."
    except Exception as e:
        return f"Erreur lors de l'ajout du juge: {e}"






def update_juge(conn, juge_id, nom, prenom):
    if not isinstance(juge_id, int):
        return "Erreur : L'ID du juge doit être un nombre entier."

    if not (nom and is_name_valid(nom) and len(nom) <= 60):
        return "Erreur : Le nom doit commencer par une majuscule, ne contenir que des lettres, avoir une longueur maximale de 60 caractères et ne peut pas être vide."

    if not (prenom and is_name_valid(prenom) and len(prenom) <= 60):
        return "Erreur : Le prénom doit commencer par une majuscule, ne contenir que des lettres, avoir une longueur maximale de 60 caractères et ne peut pas être vide."

    query = "UPDATE Juge SET "
    params = []

    if nom:
        query += "nom = %s, "
        params.append(nom)
    if prenom:
        query += "prenom = %s, "
        params.append(prenom)

    query = query.rstrip(", ") + " WHERE id = %s"
    params.append(juge_id)

    with conn.cursor() as cursor:
        cursor.execute(query, params)
        conn.commit()

    return "Le juge a été modifié."




def delete_juge(conn, juge_id):
    if not isinstance(juge_id, int):
        raise ValueError("Erreur : L'ID du juge doit être un nombre entier.")

    try:
        with conn.cursor() as cursor:
            affected_rows = cursor.execute("DELETE FROM Juge WHERE id = %s", (juge_id,))
            conn.commit()

        if affected_rows > 0:
            return affected_rows
        else:
            return -1  # Aucun juge trouvé avec l'ID donné
    except Exception as e:
        raise ValueError(f"Erreur : Une erreur inattendue s'est produite. {e}")




def display_scores(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Scores")
        scores = cursor.fetchall()
    return scores


def add_score(conn, id_score, juge_id, score_boxer1, score_boxer2, points_ou_ko, ko_boxeur_id):
    if not isinstance(id_score, int):
        return "Erreur : L'ID du round doit être un nombre entier."

    if not isinstance(juge_id, int):
        return "Erreur : L'ID du juge doit être un nombre entier."

    if not (isinstance(score_boxer1, int) and score_boxer1 >= 0):
        return "Erreur : Les points du boxeur 1 doivent être un nombre entier positif."

    if not (isinstance(score_boxer2, int) and score_boxer2 >= 0):
        return "Erreur : Les points du boxeur 2 doivent être un nombre entier positif."

    if not isinstance(points_ou_ko, bool):
        return "Erreur : Le champ points_ou_ko doit être un booléen."

    if not (isinstance(ko_boxeur_id, int) and ko_boxeur_id >= 0):
        return "Erreur : L'ID du boxeur KO doit être un nombre entier positif."

    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Score (id_score, juge_id, score_boxer1, score_boxer2, points_ou_ko, ko_boxeur_id) VALUES (%s, %s, %s, %s, %s, %s)", (id_score, juge_id, score_boxer1, score_boxer2, points_ou_ko, ko_boxeur_id))
            conn.commit()
        return f"Le score du round {id_score} a été ajouté."
    except Exception as e:
        return f"Erreur lors de l'ajout du score : {e}"

def add_score_to_db(conn, juge_id, combat_id, round_number, score_boxer1, score_boxer2):
    with conn.cursor() as cursor:
        sql = "INSERT INTO score (juge_id, combat_id, round_number, score_boxer1, score_boxer2) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (juge_id, combat_id, round_number, score_boxer1, score_boxer2))
        conn.commit()


def fetch_scores(self, combat_id):
    conn = self.make_conn()
    with conn.cursor() as cursor:
        sql = "SELECT * FROM `score` WHERE `combat_id`=%s"
        cursor.execute(sql, (combat_id,))
        result = cursor.fetchall()
        print(result)  # Instructions de débogage
    conn.close()
    return result






def update_score_to_db(conn, id_score, juge_id, combat_id, round_number, score_boxer1, score_boxer2):
    with conn.cursor() as cursor:
        sql = "UPDATE score SET score_boxer1=%s, score_boxer2=%s, juge_id=%s , combat_id=%s , round_number=%s Where id_score=%s"
        cursor.execute(sql, (score_boxer1, score_boxer2, juge_id, combat_id, round_number, id_score))
        conn.commit()



def delete_score(conn, id_combat, id_juge):
    if not isinstance(id_combat, int):
        return "Erreur : L'ID du combat doit être un nombre entier."

    if not isinstance(id_juge, int):
        return "Erreur : L'ID du juge doit être un nombre entier."

    try:
        with conn.cursor() as cursor:
            affected_rows = cursor.execute("DELETE FROM Scores WHERE id_combat = %s AND id_juge = %s", (id_combat, id_juge))
            conn.commit()

            if affected_rows > 0:
                return f"Le score du combat {id_combat} a été supprimé."
            else:
                return f"Erreur : Aucun score trouvé avec l'ID du combat {id_combat} et l'ID du juge {id_juge}."
    except Exception as e:
        return f"Erreur : Une erreur inattendue s'est produite. {e}"


def add_round(conn, combat_id, round_number, duration):
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Rounds (combat_id, round_number, duration) VALUES (%s, %s, %s)",
                            (combat_id, round_number, duration))
            conn.commit()
    except Exception as e:
        return f"Erreur lors de l'ajout du round : {e}"

    return "Le round a été ajouté avec succès!"
