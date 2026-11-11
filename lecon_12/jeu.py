# ============================================================
# Leçon 12 — Un vrai jeu : le menu, la fin, et quatre thèmes
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Ton jeu devient un VRAI jeu : on le lance, on arrive sur
#            un menu, on choisit un thème, on joue, on voit son score…
#            et on recommence. Quatre thèmes à débloquer en battant
#            ton record.
#
# CINQ FICHIERS maintenant. Ils doivent rester dans le même dossier.
#            jeu.py      ← le tien : c'est le seul que tu modifies
#            partie.py   ← ton jeu des leçons 07 à 11, rangé en fonctions
#            ecrans.py   ← le dessin du menu et de l'écran de fin
#            terrain.py  ← les îles
#            themes.py   ← les quatre thèmes
#
# DANS QUEL ORDRE : fais les TODO dans l'ordre, 1, 2, 3, 4, 5.
#            Pour trouver le TODO 3, fais Ctrl+F et tape « TODO 3 ».
#            Le jeu marche après CHAQUE TODO : teste à chaque fois.
#
# BESOIN D'AIDE : chaque TODO a sa carte « Boîte à outils » dans
#            presentation.html, avec le même numéro.
#
# COMMENT TESTER : Clique sur ▶
#            Puis regarde l'écran et coche la liste « Ça doit faire ça »
#            dans presentation.html.
#
# LES TOUCHES : ← et → au menu, ESPACE pour jouer (et plonger)
#               N : triche ! la nuit tombe d'un coup (pour tester)
#               ÉCHAP ou le ✕ de la fenêtre : quitter
# ============================================================

import pygame

from themes import THEMES
from partie import nouvelle_partie, avancer, dessiner_partie, distance
from ecrans import dessiner_menu, dessiner_fin, lire_record, sauver_record

# --- Les réglages ---
LARGEUR, HAUTEUR = 160, 120
ZOOM_FENETRE = 4
GRAVITE = 0.06                   # la gravité normale (jusqu'au TODO 5a)


# ============================================================
# --- EXEMPLE (ne pas modifier) ---
# ============================================================
# Un ÉTAT, c'est une variable qui dit OÙ ON EN EST.
# Exemple : un feu de circulation.

feu = "rouge"

# Le reste du programme REGARDE l'état pour savoir quoi faire :
if feu == "rouge":
    action = "on attend"
elif feu == "vert":
    action = "on avance"

# Et pour changer d'état, on change juste la variable :
feu = "vert"

# Ton jeu fait pareil, avec la variable `ecran` :
#   "menu"    → on choisit un thème
#   "partie"  → on joue
#   "fin"     → la nuit t'a rattrapé


# ============================================================
# Préparation (déjà écrite pour toi)
# ============================================================
pygame.init()
fenetre = pygame.display.set_mode((LARGEUR * ZOOM_FENETRE, HAUTEUR * ZOOM_FENETRE))
pygame.display.set_caption("Le Dragonneau")
surf = pygame.Surface((LARGEUR, HAUTEUR))
horloge = pygame.time.Clock()

ecran = "menu"                   # on commence toujours par le menu
choix = 0                        # le numéro du thème choisi dans THEMES
theme = THEMES[0]                # le thème de la partie en cours
record = lire_record()           # ta meilleure distance, gardée dans record.txt
jeu = nouvelle_partie()


en_marche = True
while en_marche:

    # --- 1. ÉCOUTER LES TOUCHES ----------------------------
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_marche = False
        if evenement.type != pygame.KEYDOWN:
            continue                         # on ne s'occupe que des touches
        if evenement.key == pygame.K_ESCAPE:
            en_marche = False

        if ecran == "menu":
            # (déjà écrit) ← et → changent de thème. Après le dernier, on
            # revient au premier : c'est le % de la leçon 09.
            if evenement.key == pygame.K_RIGHT:
                choix = (choix + 1) % len(THEMES)
            if evenement.key == pygame.K_LEFT:
                choix = (choix - 1) % len(THEMES)

            # (déjà écrit) Le record qu'il faut avoir pour jouer ce thème.
            prix = THEMES[choix]["distance"]

            # --- TON TOUR ---

            # TODO 1 : ESPACE lance la partie.
            #          Pourquoi ? Le menu attend que le joueur soit prêt.
            #
            #          Écris ces quatre lignes, et complète la dernière :
            #          quel écran faut-il montrer, maintenant ?
            #
            #              if evenement.key == pygame.K_SPACE:
            #                  theme = THEMES[choix]
            #                  jeu = nouvelle_partie()
            #                  ecran = ___
            #
            #          ▶ Teste : ESPACE au menu, et la partie commence.
            #            (Elle ne finit jamais : c'est le TODO 2.)


            # TODO 5b : Un thème verrouillé ne se lance pas.
            #           Pourquoi ? Sinon, débloquer ne sert à rien !
            #
            #           Change la première ligne de ton TODO 1, pour qu'elle
            #           devienne :
            #
            #               if evenement.key == pygame.K_SPACE and record >= prix:
            #
            #           ▶ Teste : au menu, un thème VERROUILLE ne démarre plus.

        elif ecran == "partie":
            # (déjà écrit) La touche de triche, pour tester sans attendre :
            # la nuit tombe presque d'un coup.
            if evenement.key == pygame.K_n:
                jeu["heure"] = 0.97

        elif ecran == "fin" and jeu["attente"] > 45:
            # (déjà écrit) On attend 45 images avant d'écouter ESPACE :
            # sinon, un joueur qui tapait sur ESPACE sauterait l'écran de
            # fin sans le voir.

            # TODO 3 : ESPACE ramène au menu.
            #          Pourquoi ? Pour rejouer, ou choisir un autre thème.
            #
            #          C'est comme le TODO 1, en plus court. Complète :
            #
            #              if evenement.key == ___:
            #                  ecran = ___
            #
            #          ▶ Teste : après la fin, ESPACE te ramène au menu.

            pass                 # (ce pass ne fait rien : tu peux le laisser)


    # --- 2. AVANCER ----------------------------------------
    if ecran == "partie":
        bouton = pygame.key.get_pressed()[pygame.K_SPACE]

        # TODO 5a : C'est le THÈME qui choisit la gravité.
        #           Pourquoi ? Sur la Lune, on doit planer plus longtemps !
        #
        #           Dans la ligne ci-dessous, remplace GRAVITE par la
        #           gravité du thème. Elle devient :
        #
        #               avancer(jeu, bouton, theme["gravite"])
        #
        #           ▶ Teste : choisis le thème Lune. Le dragonneau
        #             retombe plus lentement.
        avancer(jeu, bouton, GRAVITE)

        # TODO 2 : À la nuit noire, montre l'écran de fin.
        #          Pourquoi ? C'est la fin de la partie.
        #
        #          Complète :
        #
        #              if jeu["heure"] >= 1.0:
        #                  ecran = ___
        #
        #          ▶ Teste : appuie sur N pendant la partie. La nuit
        #            tombe, et l'écran de fin s'affiche.


    elif ecran == "fin":
        jeu["attente"] += 1                   # (déjà écrit) on compte les images

        # TODO 4 : Le record.
        #          Pourquoi ? Pour savoir quelle est ta meilleure partie.
        #          Et c'est le record qui débloque les thèmes !
        #
        #          Si cette partie est allée plus loin que le record, elle
        #          devient le nouveau record. Écris :
        #
        #              if distance(jeu) > record:
        #                  record = distance(jeu)
        #
        #          ▶ Teste : à la fin, « NOUVEAU RECORD ! » s'affiche. Au
        #            menu, ton record est écrit en bas de l'écran.


    # --- 3. DESSINER (déjà écrit) --------------------------
    # Chaque écran a son dessin.
    if ecran == "menu":
        dessiner_menu(surf, choix, record)
    elif ecran == "partie":
        dessiner_partie(surf, jeu, theme)
    elif ecran == "fin":
        dessiner_partie(surf, jeu, theme)     # la partie figée, derrière
        dessiner_fin(surf, jeu, record)

    # --- 4. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, fenetre.get_size(), fenetre)
    pygame.display.flip()
    horloge.tick(60)

sauver_record(record)                    # (déjà écrit) pour la prochaine fois
pygame.quit()
