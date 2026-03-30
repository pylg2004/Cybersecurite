import csv
import hashlib
import random
import string
import re
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class Etudiant:
    def __init__(self, id_etudiant, nom, prenom, email, mot_de_passe, salt=None):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.salt = salt if salt else os.urandom(16).hex()
        self.__mot_de_passe_hashe = self.__hasher_mdp(mot_de_passe) if mot_de_passe else ""

    def __hasher_mdp(self, mdp):
        return hashlib.sha256((mdp + self.salt).encode()).hexdigest()

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
               random.choice(string.punctuation)]
        mdp += random.choices(chars, k=longueur-4)
        random.shuffle(mdp)
        return ''.join(mdp)

    def evaluer_force(self, mdp):
        score = len(mdp) * 4
        if re.search(r"[A-Z]", mdp): score += 10
        if re.search(r"[0-9]", mdp): score += 10
        if re.search(r"[!@#$%^&*]", mdp): score += 10
        return min(100, score)

    def ajouter_etudiant(self, etudiant):
        self.etudiants.append(etudiant)

    def sauvegarder_csv(self, fichier="etudiants.csv"):
        with open(fichier, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['id', 'nom', 'prenom', 'email', 'salt', 'hash'])
            for e in self.etudiants:
                w.writerow([e.id_etudiant, e.nom, e.prenom, e.email, e.salt, e.obtenir_hash()])

    def charger_csv(self, fichier="etudiants.csv"):
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.etudiants = []
                for r in reader:
                    e = Etudiant(r['id'], r['nom'], r['prenom'], r['email'], None, r['salt'])
                    e._Etudiant__mot_de_passe_hashe = r['hash']
                    self.etudiants.append(e)
        except FileNotFoundError:
            pass

    def generer_rapport_pdf(self, nom_fichier="rapport_securite.pdf"):
        c = canvas.Canvas(nom_fichier, pagesize=A4)
        y = 800
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, y, "Rapport de Sécurité - Liste des Étudiants")
        y -= 30
        c.setFont("Helvetica", 10)
        for e in self.etudiants:
            if y < 50:
                c.showPage()
                y = 800
            c.drawString(100, y, f"ID: {e.id_etudiant} | {e.nom} {e.prenom} | Email: {e.email}")
            y -= 20
        c.save()

def afficher_menu():
    print("\n1. Generer MDP\n2. Ajouter Etudiant\n3. Lister\n4. Sauvegarder CSV\n5. Charger CSV\n6. Export PDF\n0. Quitter")

def main():
    gest = GestionnaireEtudiants()
    while True:
        afficher_menu()
        choix = input("Choix : ")
        if choix == "1":
            print(f"MDP: {gest.generer_mdp()}")
        elif choix == "2":
            id_e = input("ID: ")
            n = input("Nom: ")
            p = input("Prenom: ")
            em = input("Email: ")
            mdp = input("MDP (vide pour auto): ")
            if not mdp: mdp = gest.generer_mdp()
            gest.ajouter_etudiant(Etudiant(id_e, n, p, em, mdp))
        elif choix == "3":
            for e in gest.etudiants:
                print(f"{e.id_etudiant} - {e.nom} {e.prenom}")
        elif choix == "4":
            gest.sauvegarder_csv()
        elif choix == "5":
            gest.charger_csv()
        elif choix == "6":
            gest.generer_rapport_pdf()
        elif choix == "0":
            break

if __name__ == "__main__":
    main()