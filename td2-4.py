import hashlib

class Etudiant:
    def __init__(self, id_etudiant, nom, prenom, email, mot_de_passe):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.__mot_de_passe_hashe = self.__hasher_mdp(mot_de_passe)

    def __hasher_mdp(self, mdp):
        return hashlib.sha256(mdp.encode()).hexdigest()

    def verifier_mot_de_passe(self, mot_de_passe_tente):
        return self.__mot_de_passe_hashe == self.__hasher_mdp(mot_de_passe_tente)

    def changer_mot_de_passe(self, ancien_mdp, nouveau_mdp):
        if self.verifier_mot_de_passe(ancien_mdp):
            self.__mot_de_passe_hashe = self.__hasher_mdp(nouveau_mdp)
            return True
        return False

if __name__ == "__main__":
    
    e = Etudiant(1, "Dupont", "Jean", "jean@ecole.fr", "MdpSecurise123")
    
    print(f"Vérification (correct) : {e.verifier_mot_de_passe('MdpSecurise123')}")
    print(f"Vérification (faux) : {e.verifier_mot_de_passe('mauvais_mdp')}")
    
    succes = e.changer_mot_de_passe("MdpSecurise123", "NouveauCode456")
    print(f"Changement réussi : {succes}")
    print(f"Ancien mot de passe fonctionne encore ? : {e.verifier_mot_de_passe('MdpSecurise123')}")