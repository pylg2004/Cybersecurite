import random
import string

def generer_mdp_simple(longueur=8):
    caracteres = string.ascii_letters
    return ''.join(random.choice(caracteres) for _ in range(longueur))

if __name__ == "__main__":
    print(generer_mdp_simple())
    
