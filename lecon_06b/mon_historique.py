# ============================================================
# Leçon 06b — Calculatrice graphique
# mon_historique.py — LA MÉMOIRE DE LA CALCULATRICE
# ============================================================
# OBJECTIF : Faire retenir à la calculatrice tous les calculs déjà
#            faits, pour les réafficher dans le panneau de droite.
#            Puis traduire les erreurs de Python en messages
#            compréhensibles.
#
#            Tout se fait avec une LISTE et un DICTIONNAIRE —
#            exactement ce que tu as vu à la leçon 05.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# ============================================================
# EXEMPLE (ne pas modifier)
# ============================================================
# Un historique est une liste. Chaque calcul est un dictionnaire
# à deux clés, rangé dans cette liste :

exemple = [
    {"expression": "12+3", "resultat": "15"},
    {"expression": "2↑↑4", "resultat": "65536"},
]

# Pour lire dedans (ce fichier est importé par la calculatrice,
# alors on ne fait pas de print ici — mais essaie-les dans la console) :
#
#   exemple[0]["expression"]   →  "12+3"
#   exemple[1]["resultat"]     →  "65536"
#   len(exemple)               →  2


# ============================================================
# TON TOUR — l'historique
# ============================================================

# TODO 1 : noter(historique, expression, resultat)
#           Ajoute un nouveau calcul à la fin de la liste historique.
#           Le calcul doit avoir la même forme que dans l'exemple :
#           deux clés, "expression" et "resultat".
#           La fonction ne renvoie rien — elle modifie la liste.

def noter(historique, expression, resultat):
    pass


# TODO 2 : dernier(historique)
#           Renvoie le dernier calcul de la liste.
#           Si la liste est vide, renvoie None — sinon le programme
#           plantera au tout premier démarrage.

def dernier(historique):
    pass


# TODO 3 : du_plus_recent(historique)
#           Renvoie la liste des calculs du plus récent au plus ancien.
#           L'historique original ne doit PAS être modifié : le panneau
#           d'affichage et la calculatrice se partagent la même liste.

def du_plus_recent(historique):
    pass


# ============================================================
# TON TOUR — les messages d'erreur
# ============================================================
# Quand un calcul est impossible, Python lève une erreur qui porte
# un nom : "ZeroDivisionError" quand on divise par zéro, "ValueError"
# quand une expression n'a pas de sens.
#
# Un dictionnaire est parfait pour traduire ces noms en français.

# TODO 4 : MESSAGES
#           Crée un dictionnaire qui associe au moins ces deux noms
#           d'erreur à un message clair pour quelqu'un qui ne connaît
#           pas Python :
#             "ZeroDivisionError"  →  un message sur la division par zéro
#             "ValueError"         →  un message sur le calcul impossible
#           Commence chaque message par ❌ pour qu'il se voie à l'écran.

MESSAGES = {}


# TODO 5 : message_pour(nom_erreur)
#           Renvoie le message qui correspond au nom d'erreur.
#           Si le nom n'est pas dans le dictionnaire, renvoie quand même
#           un message par défaut — la calculatrice ne doit jamais
#           afficher un écran vide.

def message_pour(nom_erreur):
    pass


if __name__ == "__main__":
    from tests import tester_historique
    tester_historique()
