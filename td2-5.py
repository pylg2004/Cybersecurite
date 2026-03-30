import csv
import hashlib
import random
import string

class Etudiant:
    def __init__(self, id_etudiant, nom, prenom, email, mot_de_passe):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.__mot_de_passe_hashe = self.__hasher_mdp(mot_de_passe) if mot_de_passe else ""

    def __hasher_mdp(self, mdp):
        return hashlib.sha256(mdp.encode()).hexdigest()

    def verifier_mot_de_passe(self, mdp_tente):
        return self.__mot_de_passe_hashe == self.__hasher_mdp(mdp_tente)

    def changer_mot_de_passe(self, ancien_mdp, nouveau_mdp):
        if self.verifier_mot_de_passe(ancien_mdp):
            self.__mot_de_passe_hashe = self.__hasher_mdp(nouveau_mdp)
            return True
        return False

class GestionnaireEtudiants:
    def __init__(self):
        self.etudiants = []

    def generer_mdp_automatique(self, longueur=10):
        chiffres = random.choices(string.digits, k=2)
        lettres = random.choices(string.ascii_letters, k=longueur - 2)
        mdp_liste = chiffres + lettres
        random.shuffle(mdp_liste)
        return ''.join(mdp_liste)

    def ajouter_etudiant(self, etudiant):
        self.etudiants.append(etudiant)

    def sauvegarder_csv(self, nom_fichier):
        with open(nom_fichier, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nom', 'prenom', 'email', 'hash_mdp'])
            for e in self.etudiants:
                writer.writerow([e.id_etudiant, e.nom, e.prenom, e.email, e._Etudiant__mot_de_passe_hashe])

    def charger_csv(self, nom_fichier):
        self.etudiants = []
        try:
            with open(nom_fichier, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    e = Etudiant(row['id'], row['nom'], row['prenom'], row['email'], None)
                    e._Etudiant__mot_de_passe_hashe = row['hash_mdp']
                    self.etudiants.append(e)
        except FileNotFoundError:
            print(f"Erreur : Le fichier {nom_fichier} n'existe pas.")

    def trouver_etudiant_par_email(self, email):
        for e in self.etudiants:
            if e.email == email:
                return e
        return None

if __name__ == "__main__":
    gestion = GestionnaireEtudiants()

    # 1. Création d'un étudiant avec mot de passe généré
    mdp_genere = gestion.generer_mdp_automatique(12)
    nouvel_etudiant = Etudiant("1", "Doe", "Alice", "alice@example.com", mdp_genere)
    gestion.ajouter_etudiant(nouvel_etudiant)
    print(f"Étudiant créé. MDP généré : {mdp_genere}")

    # 2. Sauvegarde et rechargement
    gestion.sauvegarder_csv("base_etudiants.csv")
    gestion.charger_csv("base_etudiants.csv")

    # 3. Test de connexion
    test_email = "alice@example.com"
    cible = gestion.trouver_etudiant_par_email(test_email)
    
    if cible:
        est_valide = cible.verifier_mot_de_passe(mdp_genere)
        print(f"Connexion pour {test_email} : {'Réussie' if est_valide else 'Échec'}")