# ========== CLASSE JOUEUR ==========
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.pv = 30
        self.pv_max = 30
        self.atk = 5
        self.niv = 1
        self.xp = 0
        self.pieces_or = 100
        self.inventaire = {"Potion": 2, "Épée": 1}
        self.zone = "village"
        self.quetes = []

# ========== DONNÉES CORRIGÉES ==========
def get_pnj_dialogues(nom):
    return {
        "Barman": [
            f"Salut {nom}! Bienvenue à la taverne. Que puis-je faire pour toi?",
            "Une bière coûte 5 pièces. Ou peut-être une quête?",
            "Les loups rôdent près de la forêt ces temps-ci..."
        ],
        "Thalion": [
            f"Salut {nom}! Je suis le forgeron du village.",
            "Tu veux une nouvelle arme? J'ai besoin de minerai...",
            f"Le Barman t'a envoyé, {nom}? Tu as mes bières?"
        ],
        "Aldric": [
            f"Bienvenue {nom}. Veyloria a besoin de héros comme toi!",
            "Les monstres deviennent plus nombreux...",
            f"Le Capitaine Arthus cherche des volontaires, {nom}."
        ]
    }

pnjs = {
    "Barman": {
        "dialogues": [],
        "quetes": [
            {
                "titre": "Livrer des bières",
                "description": "Apporte 3 bières au forgeron.",
                "recompense": {"pieces_or": 20, "objet": "Chope en argent"}
            }
        ]
    },
    "Thalion": {
        "dialogues": [],
        "quetes": [
            {
                "titre": "Trouver du minerai",
                "description": "Rapport 5 minerais des montagnes.",
                "recompense": {"pieces_or": 50, "objet": "Épée en mithril"}
            }
        ]
    },
    "Aldric": {
        "dialogues": [],
        "quetes": [
            {
                "titre": "Patrouille nocturne",
                "description": "Patrouille avec les gardes 3 nuits.",
                "recompense": {"pieces_or": 100, "objet": "Médaillon"}
            }
        ]
    }
}

zones = {
    "village": {
        "description": "Cœur de Veyloria avec taverne, forge et mairie.",
        "pnjs": ["Barman", "Thalion", "Aldric"],
        "actions": ["PNJ", "Taverne", "Forge", "Mairie", "Forêt"]
    },
    "foret": {
        "description": "Forêt mystérieuse pleine de dangers.",
        "monstres": [{"nom": "Loup", "pv": 15, "atk": 5},
                    {"nom": "Dryade", "pv": 20, "atk": 4}]
    }
}

# ========== FONCTIONS CORRIGÉES ==========
def clear():
    print("\n" * 30)

def combat(joueur, monstre):
    print(f"\n⚔️ {monstre['nom']} (PV: {monstre['pv']}, ATK: {monstre['atk']})")

    while monstre["pv"] > 0 and joueur.pv > 0:
        print(f"\nPV: {joueur.pv}/{joueur.pv_max} | ATK: {joueur.atk}")
        print(f"PV {monstre['nom']}: {monstre['pv']}")
        action = input("1) Attaquer | 2) Fuir → ")

        if action == "1":
            degats = max(1, joueur.atk - random.randint(0, 2))
            monstre["pv"] -= degats
            print(f"Tu infliges {degats} dégâts!")
        else:
            if random.random() < 0.7:
                print("Tu t'échappes!")
                return True
            else:
                print("Échec de fuite!")

        if monstre["pv"] > 0:
            degats = max(1, monstre["atk"] - 2)
            joueur.pv -= degats
            print(f"{monstre['nom']} t'inflige {degats} dégâts!")

    if joueur.pv <= 0:
        print("\n💀 Tu es mort...")
        return False
    else:
        recompense_or = random.randint(5, 15)
        print(f"\n🎉 Victoire! +{recompense_or} pièces d'or")
        joueur.pieces_or += recompense_or
        return True

def parler_pnj(joueur, pnj):
    # On génère les dialogues avec le nom du joueur
    pnjs[pnj]["dialogues"] = get_pnj_dialogues(joueur.nom)[pnj]
    print(f"\n{pnj}: {random.choice(pnjs[pnj]['dialogues'])}")

    if "quetes" in pnjs[pnj] and pnjs[pnj]["quetes"]:
        print("\n1) Demander une quête")
        if input("→ ") == "1":
            quete = pnjs[pnj]["quetes"][0]
            joueur.quetes.append(quete)
            print(f"\nQuête: {quete['titre']}")
            print(f"Description: {quete['description']}")
            print(f"Récompense: {quete['recompense']}")

def explorer_foret(joueur):
    print(f"\n🌳 Forêt de Sylvaris 🌳")
    print("Les arbres murmurent... attention aux créatures!")

    if random.random() < 0.7:
        monstre = random.choice(zones["foret"]["monstres"])
        combat(joueur, monstre)

    print("\n1) Explorer encore | 2) Retour")
    return input("→ ") == "1"

def village(joueur):
    # Initialise les dialogues avec le nom du joueur
    for pnj in pnjs:
        pnjs[pnj]["dialogues"] = get_pnj_dialogues(joueur.nom)[pnj]

    while True:
        clear()
        print(f"\n🏰 VILLAGE DE VEYLORIA 🏰")
        print(zones["village"]["description"])

        print("\nQue faire?")
        for i, action in enumerate(zones["village"]["actions"], 1):
            print(f"{i}) {action}")

        print(f"{len(zones['village']['actions']) + 1}) Quitter")

        choix = input("\n→ ")

        if choix == "1":  # Parler à un PNJ
            print("\nPNJ disponibles:")
            for i, pnj in enumerate(zones["village"]["pnjs"], 1):
                print(f"{i}) {pnj}")
            pnj_choix = input("\n→ ")
            try:
                parler_pnj(joueur, zones["village"]["pnjs"][int(pnj_choix)-1])
            except:
                pass

        elif choix == "2":  # Taverne
            print("\n🍺 TAVERNE DU SANGLIER 🍺")
            parler_pnj(joueur, "Barman")

        elif choix == "3":  # Forge
            print("\n⚒️ FORGE DE THALION ⚒️")
            parler_pnj(joueur, "Thalion")

        elif choix == "4":  # Mairie
            print("\n🏛️ MAIRIE 🏛️")
            parler_pnj(joueur, "Aldric")

        elif choix == "5":  # Forêt
            while explorer_foret(joueur):
                pass

        else:
            break

def boucle_jeu(joueur):
    while True:
        clear()
        print(f"\n--- {joueur.nom} ---")
        print(f"PV: {joueur.pv}/{joueur.pv_max} | ATK: {joueur.atk} | Niv: {joueur.niv} | Or: {joueur.pieces_or}")
        print(f"Quêtes: {len(joueur.quetes)}")

        print("\n1) Aller au village")
        print("2) Quitter")

        if input("→ ") == "1":
            village(joueur)

def menu_principal():
    while True:
        clear()
        print("🏰 VEYLORIA 🏰")
        print("\n1) Nouveau jeu")
        print("2) Quitter")

        if input("→ ") == "1":
            nom = input("\nNom: ")
            joueur = Joueur(nom)
            boucle_jeu(joueur)
        else:
            break

# ========== LANCEMENT ==========
if __name__ == "__main__":
    import random
    menu_principal()
