import re

def evaluer_force_mot_de_passe(mot_de_passe):
    score = 0
    if not mot_de_passe:
        return 0

    longueur = len(mot_de_passe)
    if longueur >= 12:
        score += 40
    elif longueur >= 8:
        score += 20

    if re.search(r"[a-z]", mot_de_passe): score += 10
    if re.search(r"[A-Z]", mot_de_passe): score += 10
    if re.search(r"\d", mot_de_passe): score += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", mot_de_passe): score += 10

    suites = ["123", "abc", "azerty", "qwerty", "password", "admin"]
    if any(s in mot_de_passe.lower() for s in suites):
        score -= 30

    if re.search(r"(.)\1\1", mot_de_passe):
        score -= 20

    return max(0, min(100, score))

if __name__ == "__main__":
    mots = ["#%?gmail", "MdpSecurise@!", "Analyse_2026_Complex"]
    for m in mots:
        print(f"{m} : {evaluer_force_mot_de_passe(m)}/100")