import random
import string
from collections import Counter

def generer_mdp_chiffres(longueur=10):
    chiffres = random.choices(string.digits, k=2)
    reste = random.choices(string.ascii_letters + string.digits, k=longueur - 2)
    mdp_liste = chiffres + reste
    random.shuffle(mdp_liste)
    return ''.join(mdp_liste)

def analyser_mots_de_passe(nombre=1000):
    mdps = [generer_mdp_chiffres(random.randint(8, 12)) for _ in range(nombre)]
    
    # 1. Fréquence des caractères
    tous_caracteres = "".join(mdps)
    frequence = Counter(tous_caracteres)
    
    # 2. Longueur moyenne
    longueur_moyenne = sum(len(m) for m in mdps) / nombre
    
    # 3. Diversité
    uniques = len(set(mdps))
    diversite = (uniques / nombre) * 100

    print(f"--- Analyse sur {nombre} mots de passe ---")
    print(f"Longueur moyenne : {longueur_moyenne:.2f}")
    print(f"Diversité des combinaisons : {diversite:.2f}% d'uniques")
    print(f"Top 5 caractères les plus fréquents : {frequence.most_common(5)}")

if __name__ == "__main__":
    analyser_mots_de_passe()