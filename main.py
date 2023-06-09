import cherrypy
import pymysql
import os
import os.path
import datetime
import utilisateur
from mako.lookup import TemplateLookup
from utilisateur import get_boxeurs,display_boxeur, add_boxeur, update_boxeur, delete_boxeur, get_combats, add_combat, update_combat, delete_combat, display_juges, add_juge, update_juge, delete_juge, add_score, display_scores, get_juges, delete_score, add_score_to_db, fetch_scores, update_score_to_db  # ces fonctions doivent être définies dans boxingapp.py






db = "Boxe"
user = "root"
password = ""

conn = pymysql.connect(host='localhost',
                        user=user,
                        password=password,
                        db=db,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)


# Configure Mako
mylookup = TemplateLookup(directories=['res/templates'], input_encoding='utf-8', module_directory='tmp/mako_modules')

# Configure CherryPy





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
    
    def get_combats(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Combats")
            combats = cursor.fetchall()
        return combats
    
    def delete_combat(self, combat_id):
        try:
            combat_id = int(combat_id)
        except ValueError:
            return "Erreur : L'ID du combat doit être un entier."

        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM Combats WHERE id = %s", (combat_id,))
            self.conn.commit()

        return "Le combat a été supprimé avec succès!"
    
    def get_juges(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Juge")
        return cursor.fetchall()
    



    # Reste de votre code...




    @cherrypy.expose
    def index(self):
        mytemplate = mylookup.get_template("index.html")
        return mytemplate.render()

    @cherrypy.expose
    def display_boxeur(self):
        boxeurs = self.get_boxeurs()
        mytemplate = mylookup.get_template("display_boxeur.html")
        return mytemplate.render(boxeurs=boxeurs) 

    @cherrypy.expose
    def add_boxeur(self, nom=None, prenom=None, categorie_choice=None):
        conn = pymysql.connect(host='localhost',
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        error_message = None
        success_message = None

        if cherrypy.request.method == 'POST':
            if not all([nom, prenom, categorie_choice]):
                error_message = "Tous les champs doivent être remplis."
            else:
                try:
                    add_boxeur(nom, prenom, categorie_choice, conn)
                    success_message = "Le boxeur a été ajouté avec succès!"
                    nom = prenom = categorie_choice = None
                except Exception as e:
                    error_message = str(e)

        boxeurs = utilisateur.get_boxeurs(conn)  # Utiliser la fonction de l'utilisateur.py

        mytemplate = mylookup.get_template("add_boxeur.html")
        return mytemplate.render(error_message=error_message, success_message=success_message, nom=nom, prenom=prenom, categorie_choice=categorie_choice, boxeurs=boxeurs)





    @cherrypy.expose
    def update_boxeur(self, id=None, nom=None, prenom=None, categorie_choice=None):
        error_message = None
        conn = pymysql.connect(host='localhost',
                            user=user,
                            password=password,
                            db=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        
        if cherrypy.request.method == 'POST':
            boxeurs = utilisateur.get_boxeurs(conn)  # Utiliser la fonction de l'utilisateur.py

            if not all([id, nom, prenom, categorie_choice]):
                error_message =  "Tous les champs doivent être remplis."
            
            categorie_choice = int(categorie_choice)
            categories = ['légers', 'mi-moyen', 'mi-lourds', 'lourds']
            categorie = categories[categorie_choice - 1]
            message = update_boxeur(id, nom, prenom, categorie, conn)
            
            mytemplate = mylookup.get_template("update_boxeur.html")
            return mytemplate.render(message=message, id=id, nom=nom, prenom=prenom, categorie_choice=categorie_choice, error_message=error_message, boxeurs=boxeurs)
        
        elif cherrypy.request.method == 'GET':
            boxeurs = utilisateur.get_boxeurs(conn)  # Définir la variable boxeurs pour la requête GET
            
            mytemplate = mylookup.get_template("update_boxeur.html")
            return mytemplate.render(boxeurs=boxeurs)

        

       




    @cherrypy.expose
    def delete_boxeur(self, id=None):
        conn = pymysql.connect(host='localhost',
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

        boxeurs = utilisateur.get_boxeurs(conn)

        if cherrypy.request.method == 'POST':
            if id is None or id.strip() == '':
                message = "Veuillez entrer l'ID du boxeur."
                typ = "warning"
            else:
                try:
                    id = int(id)
                    message, typ = delete_boxeur(conn, id)
                except ValueError:
                    message = "ID invalide. Veuillez entrer un nombre entier."
                    typ = "danger"
                except Exception as e:
                    message = f"Une erreur inattendue s'est produite. Veuillez réessayer. Erreur : {e}"
                    typ = "danger"
            mytemplate = mylookup.get_template("delete_boxeur.html")
            return mytemplate.render(message=message, type=typ, boxeurs=boxeurs)
        elif cherrypy.request.method == 'GET':
            mytemplate = mylookup.get_template("delete_boxeur.html")
            return mytemplate.render(boxeurs=boxeurs, message=None, type=None)





    @cherrypy.expose    
    def display_combats(self):
        conn = pymysql.connect(host='localhost',
                            user=user,
                            password=password,
                            db=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        mytemplate = mylookup.get_template("display_combats.html")
        return mytemplate.render(combats=get_combats(conn))  # we are using get_combats now



    
    
    @cherrypy.expose
    def add_combats(self):
        conn = pymysql.connect(host='localhost',
                            user=user,
                            password=password,
                            db=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        boxers = get_boxeurs(conn)  # Modification ici
        message_error = ""
        result = ""
        mytemplate = mylookup.get_template("add_combats.html")
        return mytemplate.render(message="Veuillez remplir tous les champs.", type="info", boxers=boxers,message_error= message_error, result= result)


    @cherrypy.expose
    def add_combat_done(self, date=None, boxeur1_id=None, boxeur2_id=None, lieu_choice=None, result_choice=None,
                        winner_id=None):
        if date and boxeur1_id and boxeur2_id and lieu_choice and result_choice and winner_id:
            try:
                boxeur1_id = int(boxeur1_id)
                boxeur2_id = int(boxeur2_id)
                lieu_choice = int(lieu_choice)
                result_choice = int(result_choice)
                winner_id = int(winner_id)
                message_error = ""
            except ValueError:
                message_error = "Erreur : L'ID des boxeurs, le choix du lieu, le choix du résultat et l'ID du gagnant doivent être des entiers."

            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
                message_error = ""
            except ValueError:
                message_error = "Erreur : La date doit être au format AAAA-MM-JJ."

            if not (result_choice == 1 or result_choice == 2):
                message_error = "Erreur : Veuillez choisir 1 pour KO ou 2 pour Points."

            win_method = 'KO' if result_choice == 1 else 'Points'

            result = self.add_combat(self.conn, date, boxeur1_id, boxeur2_id, lieu_choice, win_method, winner_id)
        else:
            message_error = "Erreur : Tous les champs sont requis."
            result = ""

        boxers = get_boxeurs(conn)
        mytemplate = mylookup.get_template("add_combats.html")
        return mytemplate.render(message="Veuillez remplir tous les champs.", type="info", boxers=boxers,message_error=message_error, result=result)











    @cherrypy.expose
    def update_combat(self):
        mytemplate = mylookup.get_template("update_combat.html")
        combats = get_combats(self.conn)
        return mytemplate.render(message=None, type=None, combats=combats)

    @cherrypy.expose
    def update_combat_done(self, id_combat, date=None, categorie=None, lieu=None):
        if not id_combat:
            return "Erreur : L'ID du combat doit être renseigné !"

        try:
            id_combat = int(id_combat)
        except ValueError:
            return "Erreur : L'ID du combat doit être un entier."

        try:
            message = update_combat(self.conn, id_combat, date, categorie, lieu)
            typ = "success"
        except Exception as e:
            message = str(e)
            typ = "danger"

        mytemplate = mylookup.get_template("update_combat.html")
        combats = get_combats(self.conn)
        return mytemplate.render(message=message, type=typ, combats=combats)


    

    @cherrypy.expose
    def delete_combat(self, combat_id=None):
        combats = get_combats(conn)

        if cherrypy.request.method == 'POST':
            if combat_id is None or combat_id.strip() == '':
                message = "Veuillez entrer l'ID du combat."
                typ = "warning"
            else:
                try:
                    combat_id = int(combat_id)
                    success, message = delete_combat(conn, combat_id)
                    if success:
                        typ = "success"
                    else:
                        typ = "danger"
                except ValueError:
                    message = "ID invalide. Veuillez entrer un nombre entier."
                    typ = "danger"
                except Exception as e:
                    message = f"Une erreur inattendue s'est produite. Veuillez réessayer. Erreur : {e}"
                    typ = "danger"

            mytemplate = mylookup.get_template("delete_combat.html")
            return mytemplate.render(message=message, type=typ, combats=combats)
        else:
            mytemplate = mylookup.get_template("delete_combat.html")
            return mytemplate.render(combats=combats, message=None, type=None)





















    @cherrypy.expose
    def display_juges(self):
        conn = pymysql.connect(host='localhost',
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        juges = display_juges(conn)
        print("Juges sent to template:", juges)  # add this line
        mytemplate = mylookup.get_template("display_juges.html")
        return mytemplate.render(juges=juges)




    @cherrypy.expose
    def add_juge(self, nom=None, prenom=None):
        conn = pymysql.connect(host='localhost',
                            user=user,
                            password=password,
                            db=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        error_message = None
        success_message = None

        if cherrypy.request.method == 'POST':
            if not all([nom, prenom]):
                error_message = "Tous les champs doivent être remplis."
            else:
                try:
                    add_juge(nom, prenom, conn)
                    success_message = "Le juge a été ajouté avec succès!"
                    nom = prenom = None
                except Exception as e:
                    error_message = str(e)

        juges = display_juges(conn)  # Utiliser la fonction display_juges

        mytemplate = mylookup.get_template("add_juge.html")
        return mytemplate.render(error_message=error_message, success_message=success_message, nom=nom, prenom=prenom, juges=juges)


    @cherrypy.expose
    def add_juge_done(self, nom=None, prenom=None):
        if nom and prenom:
            conn = pymysql.connect(host='localhost',
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
            
            try:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO Juge (nom, prenom) VALUES (%s, %s)", (nom, prenom))
                    conn.commit()
                message = f"Le juge {prenom} {nom} a été ajouté."
                typ = "success"
            except Exception as e:
                message = f"Erreur lors de l'ajout du juge: {e}"
                typ = "danger"
            
            juges = get_juges(conn)
            conn.close()
        else:
            message = "All fields must be filled!"
            typ = "warning"
            juges = []

        mytemplate = mylookup.get_template("add_juge.html")
        return mytemplate.render(message=message, type=typ, juges=juges)






    

    

    @cherrypy.expose
    def update_juge(self):
        conn = pymysql.connect(host='localhost',
                            user=user,
                            password=password,
                            db=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        juges = get_juges(conn)
        mytemplate = mylookup.get_template("update_juge.html")
        return mytemplate.render(juges=juges)

    # Handler for update_juge_done
    @cherrypy.expose
    def update_juge_done(self, id_juge=None, nom=None, prenom=None):
        if id_juge:
            id_juge = int(id_juge)  # Ensure id_juge is an int
            conn = pymysql.connect(host='localhost',
                                    user=user,
                                    password=password,
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
            try:
                update_juge(conn, id_juge, nom, prenom)
                message = "Update successful!"
                typ = "success"
            except Exception as e:
                message = str(e)
                typ = "danger"
        else:
            message = "The juge ID must be filled!"
            typ = "warning"
        
        juges = display_juges(conn)  # Récupérer la liste des juges
        mytemplate = mylookup.get_template("update_juge.html")    
        return mytemplate.render(message=message, type=typ, juges=juges)  # Passer la liste des juges au rendu du modèle




    @cherrypy.expose
    def delete_juge(self):
        conn = pymysql.connect(host='localhost',
                            user=user,
                            password=password,
                            db=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        juges = get_juges(conn)  # Récupérer la liste des juges depuis la base de données
        mytemplate = mylookup.get_template("delete_juge.html")
        return mytemplate.render(juges=juges, message="", type="info")



    @cherrypy.expose
    def delete_juge_done(self, juge_id=None):
        if juge_id:
            juge_id = int(juge_id)  # ensure juge_id is an int
            conn = pymysql.connect(host='localhost',
                                user=user,
                                password=password,
                                db=db,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
            try:
                affected_rows = delete_juge(conn, juge_id)
                if affected_rows > 0:
                    message = "Deletion successful!"
                    typ = "success"
                else:
                    message = f"Erreur : Aucun juge trouvé avec l'ID {juge_id}."
                    typ = "danger"
            except ValueError as e:
                message = str(e)
                typ = "danger"
        else:
            message = "Please fill in the juge ID field."
            typ = "warning"

        # Récupérer la liste des juges
        juges = get_juges(conn)

        mytemplate = mylookup.get_template("delete_juge.html")    
        return mytemplate.render(message=message, type=typ, juges=juges)






    @cherrypy.expose
    def add_score(self, combat_id=None, juge_id=None, round_number=None, score_boxer1=None, score_boxer2=None):
        scores = []
        if all([combat_id, juge_id, round_number, score_boxer1, score_boxer2]):
            try:
                combat_id = int(combat_id)
                juge_id = int(juge_id)
                round_number = int(round_number)
                score_boxer1 = int(score_boxer1)
                score_boxer2 = int(score_boxer2)
            except ValueError:
                return "Invalid input."
            conn = self.make_conn()
            try:
                add_score_to_db(conn, combat_id, juge_id, round_number, score_boxer1, score_boxer2)
                scores = self.fetch_scores(combat_id)
                message = "Insertion successful!"
                typ = "success"
            except Exception as e:
                message = str(e)
                typ = "danger"
            conn.close()
        else:
            message = "All fields must be filled!"
            typ = "warning"
        mytemplate = mylookup.get_template("add_score.html")
        return mytemplate.render(scores=scores, message=message, type=typ)
    
    @cherrypy.expose
    def add_score_done(self, juge_id=None, combat_id=None, round_number=None, score_boxer1=None, score_boxer2=None):
        if not all([juge_id, combat_id,  round_number, score_boxer1, score_boxer2]):
            return "Tous les champs doivent être remplis !"

        try:
            combat_id = int(combat_id)
            juge_id = int(juge_id)
            round_number = int(round_number)
            score_boxer1 = int(score_boxer1)
            score_boxer2 = int(score_boxer2)
        except ValueError:
            return "Valeur invalide. Veuillez entrer des nombres entiers."

        scores = []  # Initialiser la variable scores avec une liste vide

        try :

            conn = self.make_conn()
            add_score_to_db(conn, juge_id, combat_id,  round_number, score_boxer1, score_boxer2)
            scores = self.fetch_scores(combat_id)
            message = "Le score a été ajouté avec succès !"
            typ = "success"
        except Exception as e:
            message = f"Erreur lors de l'ajout du score : {e}"
            typ = "danger"
        finally:
            conn.close()
        mytemplate = mylookup.get_template("add_score.html")
        return mytemplate.render(scores=scores, message=message, type=typ)




    @cherrypy.expose
    def fetch_scores(self, combat_id):
        conn = self.make_conn()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM `score` WHERE `combat_id`=%s"
            cursor.execute(sql, (combat_id,))
            result = cursor.fetchall()
        conn.close()
        return result if result else []  # Renvoyer une liste vide si aucun score n'est trouvé



    @cherrypy.expose
    def show_add_score_form(self, combat_id):
        mytemplate = mylookup.get_template("add_score.html")
        scores = self.fetch_scores(combat_id)
        return mytemplate.render(scores=scores, message="Please fill in all fields", type="info")


    @cherrypy.expose
    def display_scores(self, combat_id=None):
        conn = self.make_conn()
        scores = self.fetch_scores(combat_id)  # Ne passez que l'argument `combat_id`
        conn.close()
        mytemplate = mylookup.get_template("display_scores.html")
        return mytemplate.render(scores=scores)





    @cherrypy.expose
    def update_scores(self, id_score=None, combat_id=None, juge_id=None, round_number=None, score_boxer1=None, score_boxer2=None):
        conn = self.make_conn()
        update_score_to_db(conn, id_score, combat_id, juge_id, round_number, score_boxer1, score_boxer2)
        message = "Update successful!"
        typ = "success"
        conn.close()
        mytemplate = mylookup.get_template("update_scores.html")
        return mytemplate.render(message=message, type=typ)




    @cherrypy.expose
    def delete_scores(self, id=None):
        if id is not None:
            conn = self.make_conn()
            try:
                with conn.cursor() as cursor:
                    sql = "DELETE FROM `score` WHERE `id_score`=%s"
                    cursor.execute(sql, (id,))
                    conn.commit()
                message = "Score deleted successfully!"
                typ = "success"
            except Exception as e:
                message = str(e)
                typ = "danger"
        else:
            message = "No id provided!"
            typ = "warning"
        mytemplate = mylookup.get_template("delete_scores.html")
        return mytemplate.render(message=message, type=typ)


    def make_conn(self):
        return pymysql.connect(host='localhost',
                            user=user,
                            password=password,
                            db=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    
    
    




    # Define similar functions for add_fight, add_fight_done, delete_fight

if __name__ == '__main__':
    rootPath = os.path.abspath(os.getcwd())
    print(f"The root of the site is:\n\t{rootPath}\n\tcontains : {os.listdir()}")
    cherrypy.quickstart(TBAWebsite(), '/', 'config.txt')
