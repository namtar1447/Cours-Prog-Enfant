# ============================================================
# interface.py — la fenêtre de la calculatrice
# ============================================================
# Ce fichier est FOURNI. Tu n'as pas à le modifier.
#
# Il s'occupe uniquement de l'apparence : la grille de boutons,
# l'écran, le panneau d'historique et la fenêtre du graphique.
# Tout le calcul est dans calculator.py, qui appelle TES modules
# mes_operations.py et mon_historique.py.
#
# Pour lancer la calculatrice : ouvre projet.py et clique sur ▶
# ============================================================

import tkinter as tk
import customtkinter as ctk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import calculator as c
import mon_historique as hist

calc = c.Calculator()

BG = "#1e1e2e"
SURFACE = "#2a2a3e"
TEXTE = "#cdd6f4"
MUTED = "#6c7086"
ACCENT = "#8d7bf8"
ACCENT2 = "#f7a26a"
VERT = "#a6e3a1"
ERREUR = "#f38ba8"

VIOLET = {"fg_color": "#5a3ec5", "border_color": ACCENT}
ORANGE = {"fg_color": "#c46f37", "border_color": ACCENT2}
BLEU = {"fg_color": "#3e5ac5", "border_color": "#7ba7f8"}
VERT_BTN = {"fg_color": "#73af6e", "border_color": VERT}
GRIS = {"fg_color": "#3a3a4e", "border_color": MUTED}


# ============================================================
# Construction des boutons
# ============================================================

def ajouterBtn(fenetre, texte, commande, row, column, columnspan=1, rowspan=1,
               couleurs=VIOLET, taille=20):
    btn = ctk.CTkButton(fenetre, text=texte, command=commande, border_width=2,
                        font=("Courier New", taille, "bold"), **couleurs)
    btn.grid(row=row, column=column, padx=5, pady=5,
             columnspan=columnspan, rowspan=rowspan, sticky="nsew")
    return btn


# ============================================================
# Affichage
# ============================================================

def tailleEcran(texte):
    """Plus le résultat est long, plus la police rapetisse — jusqu'à un plancher."""
    if len(texte) <= 18:
        return 30

    if len(texte) <= 40:
        return 23

    if len(texte) <= 90:
        return 18

    return 15


def afficher(texte, couleur=ACCENT2):
    resultat.set(texte)

    ecran.configure(state="normal", text_color=couleur,
                    font=("Courier New", tailleEcran(texte)))
    ecran.delete("1.0", "end")
    ecran.insert("1.0", texte)
    ecran.tag_add("droite", "1.0", "end")
    ecran.tag_config("droite", justify="right")
    ecran.see("end")
    ecran.configure(state="disabled")


def rafraichir():
    afficher(calc.get_display())
    info.set(calc.get_info())
    majBoutonAction()


def majBoutonAction():
    """Le gros bouton devient 📊 dès qu'il y a un X — car = n'a plus de sens."""
    if calc.contient_x():
        btn_action.configure(text="📊", command=graphique, **VERT_BTN)
    else:
        btn_action.configure(text="=", command=egale, **VIOLET)


# ============================================================
# Les touches
# ============================================================

def taper(symbole):
    calc.add(symbole)
    rafraichir()


def period():
    if calc.point_permis():
        taper(".")


def egale():
    try:
        afficher(calc.solve())
        info.set(calc.get_info())
        majBoutonAction()
        majHistorique()

    except (ZeroDivisionError, ValueError) as erreur:
        afficher(texteErreur(erreur), ERREUR)


def texteErreur(erreur):
    """Le dictionnaire MESSAGES donne le message principal ;
    le détail Python le précise, quand il y en a un."""
    message = hist.message_pour(type(erreur).__name__) or "❌ Erreur"
    detail = str(erreur)

    if detail:
        return f"{message} — {detail}"

    return message


def retour():
    calc.retour()
    rafraichir()


def signe():
    calc.signe()
    rafraichir()


def rappeler():
    calc.rappeler()
    rafraichir()


def clear():
    calc.clear()
    rafraichir()


def changerPrecision(choix):
    calc.set_precision(choix)
    rafraichir()


def basculerMode():
    mode = calc.basculer_mode()
    btn_mode.configure(text=mode)
    rafraichir()


# ============================================================
# Le clavier de l'ordinateur
# ============================================================
# Chaque touche fait exactement la même chose que le bouton.

TOUCHES = {
    "+": "+", "-": "-", "*": "×", "/": "÷",
    "(": "(", ")": ")", "^": "^", "!": "!", "²": "²",
}

NOMS = {
    "asciicircum": "^",   # la touche ^ des claviers anglais
    "Multi_key": "^",     # la même touche, « morte », sur clavier canadien-français
}


def toucheClavier(evenement):
    caractere = evenement.char
    nom = evenement.keysym

    if caractere in "0123456789" and caractere != "":
        taper(caractere)

    elif caractere in TOUCHES:
        taper(TOUCHES[caractere])

    elif nom in NOMS:
        taper(NOMS[nom])

    elif caractere in (".", ","):
        period()

    elif nom in ("x", "X"):
        taper("X")

    elif nom in ("Return", "KP_Enter", "equal"):
        btn_action.invoke()

    elif nom == "BackSpace":
        retour()

    elif nom in ("Escape", "Delete"):
        clear()


# ============================================================
# Le graphique — trace y = f(X)
# ============================================================

def graphique():
    if not calc.contient_x():
        return

    expression = calc.expression
    fenetre_graph = ctk.CTkToplevel(fg_color=BG)
    fenetre_graph.title(f"Graphique — y = {expression}")
    fenetre_graph.geometry("640x560")
    fenetre_graph.grid_columnconfigure(1, weight=1)
    fenetre_graph.grid_rowconfigure(1, weight=1)

    barre = ctk.CTkFrame(fenetre_graph, fg_color=SURFACE)
    barre.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")

    ctk.CTkLabel(barre, text="X de", text_color=TEXTE).pack(side="left", padx=(10, 4), pady=8)
    champ_min = ctk.CTkEntry(barre, width=60)
    champ_min.insert(0, "-10")
    champ_min.pack(side="left", padx=4, pady=8)

    ctk.CTkLabel(barre, text="à", text_color=TEXTE).pack(side="left", padx=4)
    champ_max = ctk.CTkEntry(barre, width=60)
    champ_max.insert(0, "10")
    champ_max.pack(side="left", padx=4, pady=8)

    message = ctk.CTkLabel(barre, text="", text_color=MUTED, font=("Segoe UI", 12))
    message.pack(side="left", padx=12)

    figure = Figure(figsize=(6, 4.4), dpi=100, facecolor=BG)
    ax = figure.add_subplot(facecolor=SURFACE)
    canvas = FigureCanvasTkAgg(figure, master=fenetre_graph)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=3,
                                padx=10, pady=10, sticky="nsew")

    def tracer():
        try:
            x_min = float(champ_min.get())
            x_max = float(champ_max.get())
        except ValueError:
            message.configure(text="Bornes invalides", text_color=ERREUR)
            return

        if x_min >= x_max:
            message.configure(text="X de … à … : le premier doit être plus petit", text_color=ERREUR)
            return

        xs = np.linspace(x_min, x_max, 400)
        ys = []
        sautes = 0
        pourquoi = ""

        for valeur in xs:
            try:
                ys.append(float(calc.evaluer_pour(valeur)))
            except (ValueError, ZeroDivisionError, OverflowError, TypeError) as erreur:
                ys.append(np.nan)
                sautes += 1
                pourquoi = pourquoi or texteErreur(erreur)

        ys = np.array(ys, dtype=float)

        if np.all(np.isnan(ys)):
            message.configure(text=f"Aucun point traçable — {pourquoi}", text_color=ERREUR)
            return

        ax.clear()
        ax.set_facecolor(SURFACE)
        ax.plot(xs, ys, color=ACCENT2, linewidth=2)
        ax.set_title(f"y = {expression}", color=TEXTE)
        ax.grid(True, color=MUTED, alpha=.3)
        ax.axhline(0, color=MUTED, linewidth=1)
        ax.axvline(0, color=MUTED, linewidth=1)
        ax.tick_params(colors=TEXTE)

        for bord in ax.spines.values():
            bord.set_color(MUTED)

        cadrer(ax, ys)
        canvas.draw()

        if sautes:
            message.configure(text=f"{sautes} point(s) impossible(s) — ignorés", text_color=MUTED)
        else:
            message.configure(text="", text_color=MUTED)

    ctk.CTkButton(barre, text="Retracer", command=lambda: tracer(), width=90,
                  border_width=2, **VIOLET).pack(side="right", padx=10, pady=8)

    tracer()
    fenetre_graph.lift()
    fenetre_graph.focus()


def cadrer(ax, ys):
    """Évite qu'un seul pic écrase toute la courbe (ex. 1÷X près de 0)."""
    finis = ys[np.isfinite(ys)]

    if finis.size == 0:
        return

    bas, haut = np.percentile(finis, 2), np.percentile(finis, 98)

    if bas == haut:
        bas, haut = bas - 1, haut + 1

    marge = (haut - bas) * .15
    ax.set_ylim(bas - marge, haut + marge)


# ============================================================
# L'historique — une liste de dictionnaires affichée à droite
# ============================================================

def majHistorique():
    for ligne in liste_historique.winfo_children():
        ligne.destroy()

    entrees = calc.get_historique()

    if not entrees:
        ctk.CTkLabel(liste_historique, text="(vide)", text_color=MUTED,
                     font=("Segoe UI", 13)).pack(pady=10)
        return

    for entree in entrees:
        ctk.CTkButton(liste_historique,
                      text=f"{abreger(entree['expression'])}\n= {abreger(entree['resultat'])}",
                      command=lambda r=entree["resultat"]: reprendre(r),
                      anchor="e", height=44, font=("Courier New", 13),
                      fg_color=SURFACE, hover_color="#3a3a5e",
                      text_color=TEXTE).pack(fill="x", padx=4, pady=3)


def abreger(texte, maximum=26):
    return texte if len(texte) <= maximum else texte[:maximum - 1] + "…"


def reprendre(resultat):
    """Cliquer une ligne d'historique colle son résultat dans le calcul en cours."""
    calc.inserer(resultat)
    rafraichir()


def viderHistorique():
    calc.effacer_historique()
    majHistorique()


# ============================================================
# La fenêtre
# ============================================================

def main():
    fenetre = ctk.CTk(fg_color=BG)
    fenetre.title("Calculatrice graphique")
    fenetre.geometry("880x800")
    fenetre.grid_columnconfigure(0, weight=1)
    fenetre.grid_rowconfigure(0, weight=1)
    fenetre.protocol("WM_DELETE_WINDOW", fenetre.destroy)

    global liste_historique

    clavier = ctk.CTkFrame(fenetre, fg_color=BG)
    clavier.grid(row=0, column=0, sticky="nsew")
    clavier.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    clavier.grid_rowconfigure((3, 4, 5, 6, 7, 8), weight=1)

    panneau = ctk.CTkFrame(fenetre, fg_color=SURFACE, width=250)
    panneau.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=12)
    panneau.grid_propagate(False)
    panneau.grid_rowconfigure(1, weight=1)

    ctk.CTkLabel(panneau, text="Historique", text_color=TEXTE,
                 font=("Segoe UI", 16, "bold")).grid(row=0, column=0, pady=(10, 4))

    liste_historique = ctk.CTkScrollableFrame(panneau, fg_color=BG, width=210)
    liste_historique.grid(row=1, column=0, padx=8, sticky="nsew")

    ctk.CTkButton(panneau, text="Vider", command=viderHistorique, height=32,
                  border_width=2, font=("Courier New", 14), **ORANGE
                  ).grid(row=2, column=0, padx=8, pady=10, sticky="ew")

    global resultat, info, ecran, btn_action, btn_mode
    resultat = tk.StringVar(value=calc.get_display())
    info = tk.StringVar(value="")

    # ---- écran : plusieurs lignes, il enroule et défile si c'est très long ----
    ecran = ctk.CTkTextbox(clavier, height=110, wrap="char", fg_color=SURFACE,
                           text_color=ACCENT2, font=("Courier New", 30),
                           activate_scrollbars=True)
    ecran.grid(row=0, column=0, columnspan=5, padx=10, pady=(12, 0), sticky="ew")

    ctk.CTkLabel(clavier, textvariable=info, text_color=MUTED, anchor="e",
                 font=("Courier New", 15)).grid(row=1, column=0, columnspan=5,
                                                padx=10, pady=(0, 6), sticky="ew")

    # ---- précision, mode d'affichage, effacement ----
    ctk.CTkLabel(clavier, text="Décimales", text_color=MUTED, anchor="w",
                 font=("Segoe UI", 15)).grid(row=2, column=0, padx=(12, 0), sticky="w")

    menu = ctk.CTkOptionMenu(clavier, values=["15", "30", "50", "100", "500"],
                             command=changerPrecision, width=90,
                             fg_color=SURFACE, button_color="#5a3ec5",
                             font=("Courier New", 15))
    menu.set("30")
    menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    btn_mode = ajouterBtn(clavier, calc.mode, basculerMode, 2, 2, couleurs=GRIS, taille=15)
    ajouterBtn(clavier, "⌫", retour, 2, 3, couleurs=ORANGE)
    ajouterBtn(clavier, "C", clear, 2, 4, couleurs=ORANGE)

    # ---- fonctions ----
    ajouterBtn(clavier, "x²", lambda: taper("²"), 3, 0, couleurs=BLEU)
    ajouterBtn(clavier, "^", lambda: taper("^"), 3, 1, couleurs=BLEU)
    ajouterBtn(clavier, "√", lambda: taper("√"), 3, 2, couleurs=BLEU)
    ajouterBtn(clavier, "ⁿ√", lambda: taper("ⁿ√"), 3, 3, couleurs=BLEU)
    ajouterBtn(clavier, "↑↑", lambda: taper("↑↑"), 3, 4, couleurs=BLEU)

    ajouterBtn(clavier, "n!", lambda: taper("!"), 4, 0, couleurs=BLEU)
    ajouterBtn(clavier, "π", lambda: taper("π"), 4, 1, couleurs=BLEU)
    ajouterBtn(clavier, "(", lambda: taper("("), 4, 2, couleurs=BLEU)
    ajouterBtn(clavier, ")", lambda: taper(")"), 4, 3, couleurs=BLEU)
    ajouterBtn(clavier, "±", signe, 4, 4, couleurs=BLEU)

    # ---- pavé numérique ----
    ajouterBtn(clavier, "7", lambda: taper("7"), 5, 0)
    ajouterBtn(clavier, "8", lambda: taper("8"), 5, 1)
    ajouterBtn(clavier, "9", lambda: taper("9"), 5, 2)
    ajouterBtn(clavier, "÷", lambda: taper("÷"), 5, 3, couleurs=ORANGE)
    ajouterBtn(clavier, "EE", lambda: taper("e"), 5, 4, couleurs=BLEU, taille=17)

    ajouterBtn(clavier, "4", lambda: taper("4"), 6, 0)
    ajouterBtn(clavier, "5", lambda: taper("5"), 6, 1)
    ajouterBtn(clavier, "6", lambda: taper("6"), 6, 2)
    ajouterBtn(clavier, "×", lambda: taper("×"), 6, 3, couleurs=ORANGE)
    ajouterBtn(clavier, "Ans", rappeler, 6, 4, couleurs=BLEU, taille=16)

    ajouterBtn(clavier, "1", lambda: taper("1"), 7, 0)
    ajouterBtn(clavier, "2", lambda: taper("2"), 7, 1)
    ajouterBtn(clavier, "3", lambda: taper("3"), 7, 2)
    ajouterBtn(clavier, "-", lambda: taper("-"), 7, 3, couleurs=ORANGE)

    # ce bouton change tout seul : "=" normalement, "📊" dès qu'il y a un X
    btn_action = ajouterBtn(clavier, "=", egale, 7, 4, rowspan=2, couleurs=VIOLET, taille=26)

    ajouterBtn(clavier, "X", lambda: taper("X"), 8, 0, couleurs=VERT_BTN)
    ajouterBtn(clavier, "0", lambda: taper("0"), 8, 1)
    ajouterBtn(clavier, ".", period, 8, 2)
    ajouterBtn(clavier, "+", lambda: taper("+"), 8, 3, couleurs=ORANGE)

    fenetre.bind("<Key>", toucheClavier)

    rafraichir()
    majHistorique()
    fenetre.mainloop()


if __name__ == "__main__":
    main()
