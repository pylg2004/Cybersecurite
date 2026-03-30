import random
import string

def generer_mdp_chiffres(longueur=10):
    chiffres = random.choices(string.digits, k=2)
    reste = random.choices(string.ascii_letters + string.digits, k=longueur - 2)
    
    mdp_liste = chiffres + reste
    random.shuffle(mdp_liste)
    
    return ''.join(mdp_liste)

if __name__ == "__main__":
    print(generer_mdp_chiffres())