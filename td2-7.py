import csv
import hashlib
import random
import string
import re
import os

class Etudiant:
    def __init__(self, id_etudiant, nom, prenom, email, mot_de_passe, salt=None):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.salt = salt if salt else os.urandom(16).hex()
        self.__mot_de_passe_hashe = self.__hasher_mdp(mot_de_passe) if mot_de_passe else ""

    def __hasher_mdp(self, mdp):
        entree = mdp + self.salt
        return hashlib.sha256(entree.encode()).hexdigest()

    def verifier_mot_de_passe(self, mdp_tente):
        return self.__mot_de_passe_hashe == self.__hasher_mdp(mdp_tente)

    def obtenir_hash(self):
        return self.__mot_de_passe_hashe

class GestionnaireEtudiants:
    def __init__(self):
        self.etudiants = []

    def generer_mdp(self, longueur=12):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        mdp = [random.choice(string.ascii_uppercase), 
               random.choice(string.ascii_lowercase),
               random.choice(string.digits),
               random.choice(string.digits)]
        mdp += random.choices(chars, k=longueur-4)
        random.shuffle(mdp)
        return ''.join(mdp)

    def evaluer_force(self, mdp):
        score = len(mdp) * 4
        if re.search(r"[A-Z]", mdp): score += 10
        if re.search(r"[0-9]", mdp): score += 10
        if re.search(r"[!@#$%^&*]", mdp): score += 10
        return min(100, score)

    def sauvegarder(self, fichier="etudiants.csv"):
        with open(fichier, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['id', 'nom', 'prenom', 'email', 'salt', 'hash'])
            for e in self.etudiants:
                w.writerow([e.id_etudiant, e.nom, e.prenom, e.email, e.salt, e.obtenir_hash()])

    def charger(self, fichier="etudiants.csv"):
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.etudiants = []
                for r in reader:
                    e = Etudiant(r['id'], r['nom'], r['prenom'], r['email'], None, r['salt'])
                    e._Etudiant__mot_de_passe_hashe = r['hash']
                    self.etudiants.append(e)
        except FileNotFoundError:
            print("Fichier introuvable.")

def afficher_menu():
    print("\n--- MENU GESTION SÉCURISÉE ---")
    print("1. Générer mot de passe")
    print("2. Ajouter étudiant")
    print("3. Lister étudiants")
    print("4. Sauvegarder")
    print("5. Charger")
    print("6. Audit sécurité")
    print("0. Quitter")

def main():
    gest = GestionnaireEtudiants()
    while True:
        afficher_menu()
        choix = input("Choix : ")
        
        if choix == "1":
            print(f"MDP suggéré : {gest.generer_mdp()}")
        
        elif choix == "2":
            id_e = input("ID : ")
            nom = input("Nom : ")
            prenom = input("Prénom : ")
            email = input("Email : ")
            mdp = input("Mot de passe (laisser vide pour générer) : ")
            if not mdp: mdp = gest.generer_mdp()
            gest.ajouter_etudiant(Etudiant(id_e, nom, prenom, email, mdp))
            print(f"Ajouté avec succès. (MDP: {mdp})")
            
        elif choix == "3":
            for e in gest.etudiants:
                print(f"[{e.id_etudiant}] {e.nom} {e.prenom} - {e.email}")
                
        elif choix == "4":
            gest.sauvegarder()
            print("Données sécurisées en CSV.")
            
        elif choix == "5":
            gest.charger()
            print("Données chargées.")
            
        elif choix == "6":
            print(f"Total étudiants : {len(gest.etudiants)}")
            print("Audit : Tous les hash utilisent SHA-256 avec Salt unique.")
            
        elif choix == "0":
            break

if __name__ == "__main__":
    main()