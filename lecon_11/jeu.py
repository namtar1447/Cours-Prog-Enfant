# ============================================================
# Leçon 11 — Les îles et la tombée de la nuit
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Donner une FIN à ton jeu. La nuit tombe, lentement
#            d'abord, puis de plus en plus vite d'île en île.
#            Quand il fait noir, la partie est terminée.
#
#            Pour la repousser : aller vite, et bien atterrir.
#
# TROIS FICHIERS maintenant : jeu.py, terrain.py et themes.py.
#            Ils doivent rester dans le même dossier.
#
# DANS QUEL ORDRE : fais les TODO dans l'ordre, 1, 2, 3, 4, 5.
#            Ils ne sont pas rangés dans l'ordre dans le fichier :
#            pour trouver le TODO 3, fais Ctrl+F et tape « TODO 3 ».
#            Le jeu marche après CHAQUE TODO : teste à chaque fois.
#
# BESOIN D'AIDE : chaque TODO a sa carte « Boîte à outils » dans
#            presentation.html, avec le même numéro.
#
# COMMENT TESTER : Clique sur ▶
#            Puis regarde l'écran et coche la liste « Ça doit faire ça »
#            dans presentation.html.
#
# POUR FERMER : clique le ✕ de la fenêtre, ou appuie sur ÉCHAP
#               (R pour recommencer une partie)
# ============================================================

import pygame

import random

from terrain import hauteur_du_sol, numero_ile, est_eau, CRETE, NIVEAU_EAU
from themes import DRAGONNEAU, melanger

# --- Les réglages du jeu ---
LARGEUR, HAUTEUR = 160, 120
ZOOM_FENETRE = 4
X_DRAGON = 40
MI_HAUTEUR = 6

# --- La chute et la glisse (leçon 09b) ---
GRAVITE = 0.08
GRAVITE_PLONGEON = 0.30
ACCEL_DESCENTE = 0.22
FREIN_MONTEE = 0.28
BONUS_PLONGEON = 2.6
MALUS_PLONGEON = 3.5
FRICTION = 0.997
VX_MIN, VX_MAX = 1.2, 9.0
VITESSE_AILES = 0.15

# --- La caméra (leçon 10) ---
ZOOM_MIN = 0.30
SEUIL_ZOOM = 50
HAUTEUR_ZOOM = 190
SUIVI_SORTIE = 0.07
SUIVI_RETOUR = 0.10
MARGE_SOL = 8
VISEE_BAS = 60
VISEE_HAUT = 26
SUIVI_CAMERA = 0.10

# --- La nuit (NOUVEAU) ---
VITESSE_NUIT = 0.00015           # ce que la nuit gagne à chaque image
FACTEUR_ILE = 0.35               # ... et 35 % de plus par île franchie
BONUS_ATTERRISSAGE = 0.004       # le jour que rend un atterrissage gagnant
DEBUT_ETOILES = 0.6              # à partir de quelle nuit on voit les étoiles

THEME = DRAGONNEAU
NIVEAUX_NUIT = 8                 # en combien d'étapes le dragonneau s'assombrit
COULEUR_HUD    = (255, 255, 255)
COULEUR_PLAQUE = (14, 14, 24)    # derrière le texte, pour qu'il reste lisible


# ============================================================
# --- EXEMPLE (ne pas modifier) ---
# ============================================================
# MÉLANGER deux couleurs, c'est comme mélanger deux peintures.
# On le fait d'abord sur UN seul nombre : 200 le jour, 40 la nuit.

jour, nuit = 200, 40

# 4 cuillères de jour, 0 de nuit  (part_de_nuit = 0.0)
#     tout le 200                          →  200
#
# 3 cuillères de jour, 1 de nuit  (part_de_nuit = 0.25)
#     les trois quarts de 200 = 150
#     un quart de 40          =  10
#     150 + 10                             →  160
#
# 2 cuillères de chaque           (part_de_nuit = 0.5)
#     la moitié de 200 = 100
#     la moitié de 40  =  20
#     100 + 20                             →  120
#
# 1 cuillère de jour, 3 de nuit   (part_de_nuit = 0.75)
#     un quart de 200          =  50
#     les trois quarts de 40   =  30
#     50 + 30                              →   80
#
# 0 cuillère de jour, 4 de nuit   (part_de_nuit = 1.0)
#     tout le 40                           →   40

# Une couleur, c'est TROIS nombres (rouge, vert, bleu) : la fonction
# melanger() de themes.py fait ce calcul sur les trois. Tu n'as pas à
# l'écrire — seulement à t'en servir (TODO 3).


# ============================================================
# Le dessin du dragonneau (déjà écrit pour toi)
# ============================================================

DRAGON_AILE_HAUTE = [
    "......AAAA......",
    ".....AAAAAA.....",
    "....AAAAAAA.....",
    "....AAAAAA.D.D..",
    "......CCCCCCCC..",
    "D....CCCCCCCCC..",
    "DD..CCCCCCCOCCC.",
    ".DDCCCCCCCCCCCCC",
    "..DCCCCCCCCCCC..",
    "...DCCCCCCCC....",
    "....DDDDDD......",
    "................",
]

DRAGON_AILE_BASSE = [
    "................",
    "................",
    "................",
    "......CC...D.D..",
    "......CCCCCCCC..",
    "D....CCCCCCCCC..",
    "DD..CCCCCCCOCCC.",
    ".DDCCCCCCCCCCCCC",
    "..DCCCCAAACCCC..",
    "...DCCAAAAAA....",
    "....DAAAAAA.....",
    ".....AAAA.......",
]


def faire_sprite(motif, part_de_nuit):
    """Dessine le dragonneau à l'heure voulue, avec un CONTOUR d'un pixel.

    Le contour, c'est ce qui le garde visible quel que soit le fond :
    au fil de la journée, le ciel passe par toutes les couleurs, et sans
    contour il finirait par s'y fondre.
    """
    couleurs = {
        "C": melanger(THEME["heros"], THEME["heros_nuit"], part_de_nuit),
        "D": melanger(THEME["aile"], THEME["aile_nuit"], part_de_nuit),
        "A": melanger(THEME["aile"], THEME["aile_nuit"], part_de_nuit),
        "O": melanger(THEME["contour"], THEME["contour_nuit"], part_de_nuit),
    }
    contour = melanger(THEME["contour"], THEME["contour_nuit"], part_de_nuit)

    # une marge d'un pixel tout autour, pour avoir la place du contour
    image = pygame.Surface((18, 14), pygame.SRCALPHA)

    for ligne_y, ligne in enumerate(motif):
        for ligne_x, lettre in enumerate(ligne):
            if lettre not in couleurs:
                continue
            # d'abord le contour : les huit cases autour
            for decale_y in (-1, 0, 1):
                for decale_x in (-1, 0, 1):
                    image.set_at((ligne_x + 1 + decale_x, ligne_y + 1 + decale_y), contour)

    for ligne_y, ligne in enumerate(motif):
        for ligne_x, lettre in enumerate(ligne):
            if lettre in couleurs:
                image.set_at((ligne_x + 1, ligne_y + 1), couleurs[lettre])

    return image


# Les étoiles : tirées au hasard UNE fois, mais toujours les mêmes grâce
# à la graine. Chacune a sa propre luminosité, sinon le ciel a l'air
# quadrillé.
hasard = random.Random(7)
ETOILES = [(hasard.randrange(LARGEUR), hasard.randrange(74),
            hasard.uniform(0.35, 1.0)) for _ in range(44)]


# ============================================================
# Préparation (déjà écrite pour toi)
# ============================================================
pygame.init()
ecran = pygame.display.set_mode((LARGEUR * ZOOM_FENETRE, HAUTEUR * ZOOM_FENETRE))
pygame.display.set_caption("Le Dragonneau")
surf = pygame.Surface((LARGEUR, HAUTEUR))
horloge = pygame.time.Clock()

POLICE = pygame.font.SysFont("consolas", 8)
GROSSE_POLICE = pygame.font.SysFont("consolas", 14, bold=True)


def ecrire(surface, message, x, y, couleur=COULEUR_HUD, police=POLICE):
    """Le texte, avec son ombre : lisible sur un ciel clair comme sur la nuit."""
    surface.blit(police.render(message, False, COULEUR_PLAQUE), (x + 1, y + 1))
    surface.blit(police.render(message, False, couleur), (x, y))


# Le dragonneau est préparé à l'avance dans plusieurs clartés : on ne
# redessine pas 200 pixels à chaque image.
SPRITES = [[faire_sprite(motif, niveau / (NIVEAUX_NUIT - 1))
            for motif in (DRAGON_AILE_HAUTE, DRAGON_AILE_BASSE)]
           for niveau in range(NIVEAUX_NUIT)]


def nouvelle_partie():
    """Remet tout à zéro. Appelé au début, et quand on appuie sur R."""
    depart_y = hauteur_du_sol(0) - MI_HAUTEUR
    return {
        "camera_x": 0.0, "y": depart_y, "vy": 0.0, "vx": 2.0,
        "animation": 0.0, "au_sol_avant": True,
        "zoom": 1.0, "visee": float(VISEE_BAS), "camera_y": depart_y - VISEE_BAS,
        "heure": 0.0, "finie": False, "soleil": 0,
    }


jeu = nouvelle_partie()

en_marche = True
while en_marche:

    # --- 1. ÉCOUTER (déjà écrit) ---------------------------
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_marche = False
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                en_marche = False
            if evenement.key == pygame.K_r:
                jeu = nouvelle_partie()

    touches = pygame.key.get_pressed()
    bouton = touches[pygame.K_SPACE]

    # On sort les valeurs du dictionnaire pour écrire du code lisible.
    camera_x, y, vy, vx = jeu["camera_x"], jeu["y"], jeu["vy"], jeu["vx"]
    zoom, visee, heure = jeu["zoom"], jeu["visee"], jeu["heure"]

    if not jeu["finie"]:

        # --- 2. CALCULER (déjà écrit — leçon 09b) ----------
        if bouton:
            vy += GRAVITE_PLONGEON
        else:
            vy += GRAVITE

        y += vy

        hauteur_ici = hauteur_du_sol(camera_x)
        sol = hauteur_ici - MI_HAUTEUR

        if y >= sol:
            y = sol
            pente = hauteur_du_sol(camera_x + 1) - hauteur_ici

            if not jeu["au_sol_avant"]:
                avant = vx                       # sa vitesse juste avant le choc
                vx = (vx + vy * pente) / (1 + pente * pente)
                vx = max(VX_MIN, min(VX_MAX, vx))

                # (déjà écrit) Ce que le choc lui a fait GAGNER en vitesse.
                # Si le nombre est négatif, c'est qu'il en a PERDU.
                gain = vx - avant
                heure_avant = heure

                # --- TON TOUR ---

                # TODO 5a : Un bel atterrissage rend un peu de jour.
                #           Pourquoi ? Pour récompenser le joueur qui vise bien.
                #
                #           S'il a gagné de la vitesse, fais reculer l'heure.
                #           Écris :
                #
                #               if gain > 0:
                #                   heure -= gain * BONUS_ATTERRISSAGE
                #
                #           ▶ Teste : après un beau plongeon, « + jour ! »
                #             s'affiche en haut à gauche.


                # TODO 5b : Le plancher. L'heure ne descend jamais sous 0.0.
                #           Pourquoi ? 0.0, c'est midi. Plus clair que midi,
                #           ça n'existe pas : les couleurs deviendraient
                #           bizarres.
                #
                #           Si heure est plus petite que 0.0, remets-la à 0.0.
                #           Complète :
                #
                #               if heure < ___:
                #                   heure = ___
                #
                #           ▶ Teste : rien de nouveau à voir, et c'est normal.
                #             Le plancher, c'est comme une ceinture de
                #             sécurité : presque toujours, elle ne sert à
                #             rien. Mais le jour où elle sert…
                #             Vérifie juste que le jeu marche encore.


                # (déjà écrit) Si ton TODO 5 a rendu du jour, on l'affiche.
                if heure < heure_avant:
                    jeu["soleil"] = 45           # pendant 45 images

            vy = pente * vx

            if pente > 0:
                accel = ACCEL_DESCENTE * (BONUS_PLONGEON if bouton else 1.0)
            else:
                accel = FREIN_MONTEE * (MALUS_PLONGEON if bouton else 1.0)

            vx = max(VX_MIN, min(VX_MAX, (vx + pente * accel) * FRICTION))

        jeu["au_sol_avant"] = y >= sol
        camera_x += vx
        jeu["animation"] += VITESSE_AILES

        # --- 3. LA NUIT ------------------------------------

        # (déjà écrit) Sur quelle île est-il ? 0 pour la première.
        ile = numero_ile(camera_x)

        # (déjà écrit) Plus il est loin, plus la nuit va vite :
        #   1re île → 1.00 fois   2e île → 1.35 fois   3e île → 1.70 fois
        fois_plus_vite = 1 + FACTEUR_ILE * ile

        # TODO 1 : Fais tomber la nuit, un tout petit peu à chaque image.
        #          Pourquoi ? Sans ça, la partie ne finit jamais.
        #          Écris :
        #
        #              heure += VITESSE_NUIT
        #
        #          ▶ Teste : la jauge de nuit, en haut à droite, se
        #            remplit tranquillement.


        # TODO 4 : Fais aller la nuit plus vite sur les îles lointaines.
        #          Pourquoi ? Pour que le jeu devienne plus dur à mesure
        #          qu'on avance.
        #          Dans ta ligne du TODO 1, juste au-dessus, multiplie
        #          VITESSE_NUIT par fois_plus_vite. Elle devient :
        #
        #              heure += VITESSE_NUIT * fois_plus_vite
        #
        #          ▶ Teste : après le premier océan, la jauge de nuit se
        #            remplit plus vite qu'avant.

        # TODO 2 : Termine la partie quand il fait nuit noire.
        #          Pourquoi ? C'est la fin du jeu : la nuit t'a rattrapé.
        #          Si heure arrive à 1.0 (ou plus), mets True dans
        #          jeu["finie"]. Complète :
        #
        #              if heure >= ___:
        #                  jeu["finie"] = ___
        #
        #          ▶ Teste : « LA NUIT T'A RATTRAPE » s'affiche et tout
        #            s'arrête. C'est long à attendre (presque 2 minutes) :
        #            pour essayer plus vite, mets VITESSE_NUIT = 0.002 en
        #            haut du fichier… et remets 0.00015 après !


    # --- 4. LA CAMÉRA (déjà écrit — leçon 10) --------------
    hauteur_de_vol = max(0.0, CRETE - y)
    if hauteur_de_vol <= SEUIL_ZOOM:
        part = 0.0
    else:
        part = min(1.0, (hauteur_de_vol - SEUIL_ZOOM) / (HAUTEUR_ZOOM - SEUIL_ZOOM))

    confort = 1.0 - (1.0 - ZOOM_MIN) * part
    if confort < zoom:
        zoom += (confort - zoom) * SUIVI_SORTIE
    else:
        zoom += (confort - zoom) * SUIVI_RETOUR

    visee += (VISEE_BAS + (VISEE_HAUT - VISEE_BAS) * part - visee) * SUIVI_CAMERA

    # Le garde-fou garde toujours du sol à l'écran. Au-dessus de la mer,
    # c'est ELLE qu'il faut garder en vue : elle est bien plus bas que
    # les crêtes, et parfaitement plate — donc la mesure ne tremble pas.
    reference = NIVEAU_EAU if est_eau(camera_x) else CRETE
    plafond = (HAUTEUR - MARGE_SOL - visee) / max(1.0, reference - y)
    zoom = max(0.12, min(1.0, plafond, zoom))
    camera_y = y - visee / zoom

    # On range tout dans le dictionnaire avant de dessiner.
    jeu.update(camera_x=camera_x, y=y, vy=vy, vx=vx,
               zoom=zoom, visee=visee, camera_y=camera_y, heure=heure)

    # --- 5. DESSINER ---------------------------------------

    # TODO 3a : Fais tomber la nuit sur le CIEL.
    #           Pourquoi ? Le ciel, c'est l'horloge du jeu : en le
    #           regardant, le joueur sait combien de temps il lui reste.
    #
    #           Pour l'instant, la ligne couleur_ciel (ci-dessous) prend
    #           toujours la couleur de jour. Change-la pour qu'elle devienne :
    #
    #               couleur_ciel = melanger(THEME["ciel"], THEME["ciel_nuit"], heure)
    #
    #           Pourquoi `heure` ? Parce que heure, c'est justement la
    #           part de nuit : 0.0 au début de la partie, 1.0 à la fin.
    #
    #           ▶ Teste : le ciel fonce petit à petit… mais les collines
    #             restent vertes comme à midi. C'est normal ! → TODO 3b

    # TODO 3b : Fais pareil pour les trois autres lignes.
    #           Même recette : seuls les noms entre guillemets changent.
    #           Attention : couleur_sol va avec "collines" et "collines_nuit".
    #           Boîte à outils : la carte « TODO 3 » de la présentation.
    #
    #           ▶ Teste : tout le paysage s'assombrit en même temps.

    couleur_ciel  = THEME["ciel"]
    couleur_sol   = THEME["collines"]
    couleur_ombre = THEME["ombre"]
    couleur_eau   = THEME["eau"]

    surf.fill(couleur_ciel)

    # (déjà écrit) Les étoiles, quand la nuit est bien avancée.
    if heure > DEBUT_ETOILES:
        force = min(1.0, (heure - DEBUT_ETOILES) / (1.0 - DEBUT_ETOILES))
        for etoile_x, etoile_y, eclat in ETOILES:
            surf.set_at((etoile_x, etoile_y),
                        melanger(couleur_ciel, (255, 255, 255), force * eclat))

    # (déjà écrit) Le décor, colonne par colonne — leçon 10, plus l'eau.
    for colonne in range(LARGEUR):
        monde_x = camera_x + (colonne - X_DRAGON) / zoom
        sy = int((hauteur_du_sol(monde_x) - camera_y) * zoom)
        if sy >= HAUTEUR:
            continue
        if est_eau(monde_x):
            pygame.draw.line(surf, couleur_eau, (colonne, sy), (colonne, HAUTEUR))
        else:
            pygame.draw.line(surf, couleur_sol, (colonne, sy), (colonne, HAUTEUR))
            pygame.draw.line(surf, couleur_ombre, (colonne, sy),
                             (colonne, sy + max(1, int(3 * zoom))))

    # (déjà écrit) Le dragonneau.
    niveau = min(NIVEAUX_NUIT - 1, int(heure * NIVEAUX_NUIT))
    image = SPRITES[niveau][int(jeu["animation"]) % 2]
    if zoom < 0.85:
        image = pygame.transform.scale(image, (max(6, int(18 * zoom)),
                                               max(5, int(14 * zoom))))
    ecran_y = int((y - camera_y) * zoom)
    surf.blit(image, (X_DRAGON - image.get_width() // 2,
                      ecran_y - image.get_height() // 2))

    # --- 6. LE HUD (déjà écrit) ----------------------------
    ecrire(surf, f"{int(camera_x / 10)} m", 3, 2)
    ecrire(surf, f"ile {numero_ile(camera_x) + 1}", 3, 11)

    # « + jour ! » pendant quelques images, après un atterrissage gagnant
    if jeu["soleil"] > 0:
        jeu["soleil"] -= 1
        ecrire(surf, "+ jour !", 3, 20, (255, 214, 102))

    pygame.draw.rect(surf, COULEUR_PLAQUE, (LARGEUR - 30, 2, 28, 15))

    plein = int(24 * (vx - VX_MIN) / (VX_MAX - VX_MIN))
    pygame.draw.rect(surf, COULEUR_HUD, (LARGEUR - 29, 3, 26, 5), 1)
    if plein > 0:
        pygame.draw.rect(surf, THEME["heros"], (LARGEUR - 28, 4, plein, 3))

    # la jauge de nuit : elle se remplit, et c'est le compte à rebours
    pygame.draw.rect(surf, COULEUR_HUD, (LARGEUR - 29, 11, 26, 5), 1)
    nuit_pleine = int(24 * min(1.0, heure))
    if nuit_pleine > 0:
        pygame.draw.rect(surf, (120, 124, 196), (LARGEUR - 28, 12, nuit_pleine, 3))

    if jeu["finie"]:
        ecrire(surf, "LA NUIT", 48, 40, (255, 255, 255), GROSSE_POLICE)
        ecrire(surf, "T'A RATTRAPE", 34, 56, (255, 255, 255), GROSSE_POLICE)
        ecrire(surf, f"{int(camera_x / 10)} m  -  R pour rejouer", 26, 78)

    # --- 7. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, ecran.get_size(), ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
