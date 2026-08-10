# ============================================================
# calculator.py — le "cerveau" de la calculatrice
# ============================================================
# Ce fichier est FOURNI. Tu n'as pas à le modifier.
#
# Il sait lire une expression écrite avec les boutons
# (ex. "12+3×4", "√16", "5!", "2↑↑4", "3ⁿ√8", "X²+1")
# et la calculer avec mpmath — donc avec autant de décimales
# que tu veux, et des nombres géants.
#
# Ce que tu dois retenir pour ton projet :
#
#   calc = Calculator()
#   calc.add("7")            -> ajoute un symbole à l'expression
#   calc.rappeler()          -> réinsère le dernier résultat (Ans)
#   calc.get_historique()    -> [{"expression": "12+3", "resultat": "15"}, …]
#   calc.effacer_historique()
#   calc.inserer("15")       -> colle un ancien résultat dans l'expression
#   calc.signe()             -> change le signe du nombre en cours (±)
#   calc.basculer_mode()     -> bascule l'affichage NORM ⇄ SCI
#   calc.point_permis()      -> False si le nombre a déjà un point
#   calc.retour()            -> efface le dernier symbole
#   calc.clear()             -> efface tout
#   calc.get_display()       -> le texte à afficher à l'écran
#   calc.get_info()          -> une petite info (nb de chiffres) ou ""
#   calc.contient_x()        -> True si l'expression contient X
#   calc.solve()             -> calcule, et peut LEVER une erreur :
#                                 ZeroDivisionError (division par zéro)
#                                 ValueError        (expression invalide)
#   calc.evaluer_pour(3)     -> calcule l'expression avec X = 3
#   calc.set_precision(50)   -> 50 décimales
# ============================================================

import mpmath
from mpmath import mp, mpf

# Les deux modules écrits par toi. Le moteur les appelle :
# sans eux, la calculatrice ne sait rien calculer ni rien retenir.
import mes_operations as ops
import mon_historique as hist


class Calculator:

    # --- Les symboles que la calculatrice comprend -------------
    # (les plus longs en premier : "↑↑" doit être testé avant "↑")
    SYMBOLES = ("↑↑", "ⁿ√", "+", "-", "×", "÷", "^", "√",
                "!", "²", "(", ")", "π", "X")

    INFIXES = ("+", "-", "×", "÷", "^", "↑↑", "ⁿ√")   # entre deux nombres
    PREFIXES = ("√", "neg")                            # devant un nombre
    #  "neg" n'est pas une touche : c'est le "-" d'un nombre négatif,
    #  reconnu tout seul par tokenize (ex. -5² = -25, mais 2^-3 = 0.125)
    POSTFIXES = ("!", "²")                             # après un nombre
    CONSTANTES = ("π", "X")                            # valeurs toutes faites
    CHIFFRES = "0123456789."                           # (pas isdigit : '²'.isdigit() est True !)

    # --- Garde-fous : au-delà, on refuse au lieu de figer ------
    # (ceux de la puissance et de la tétration sont dans mes_operations.py)
    EXPOSANT_MAX = mpf(10) ** 15
    CHIFFRES_ENTIER_MAX = 40   # au-delà : notation scientifique

    HISTORIQUE_MAX = 25

    def __init__(self, precision=30):
        self.expression = ""
        self.repetition = ""          # la dernière opération, pour re-faire "="
        self.valeur = None            # le dernier résultat, en nombre
        self.vient_de_calculer = False
        self.mode = "NORM"            # "NORM" ou "SCI"
        self.historique = []          # liste de {"expression": …, "resultat": …}
        self.set_precision(precision)

    # ==========================================================
    # Saisie
    # ==========================================================

    def set_precision(self, decimales):
        mp.dps = int(decimales)

    def basculer_mode(self):
        """NORM ⇄ SCI — et ré-affiche tout de suite le dernier résultat."""
        self.mode = "SCI" if self.mode == "NORM" else "NORM"

        if self.vient_de_calculer and self.valeur is not None:
            self.expression = self.formater(self.valeur)

        return self.mode

    def add(self, txt):
        # Comme sur une vraie calculatrice : après un résultat,
        # taper un chiffre recommence, mais taper un opérateur continue.
        if self.vient_de_calculer:

            if txt in self.INFIXES or txt in self.POSTFIXES:
                self.vient_de_calculer = False
            else:
                self.clear()

        self.expression += txt

    def inserer(self, texte):
        """Colle un résultat déjà calculé dans l'expression en cours."""
        if self.vient_de_calculer:
            self.clear()

        self.expression += texte

    def rappeler(self):
        """Ans — réinsère le dernier résultat, pris dans l'historique."""
        calcul = hist.dernier(self.historique)

        if not calcul:
            return

        self.inserer(calcul["resultat"])

    # ==========================================================
    # Historique — une liste de dictionnaires
    # ==========================================================

    def noter(self, expression, resultat):
        hist.noter(self.historique, expression, resultat)

        while len(self.historique) > self.HISTORIQUE_MAX:
            self.historique.pop(0)

    def get_historique(self):
        """Du plus récent au plus ancien."""
        return hist.du_plus_recent(self.historique) or []

    def dernier_calcul(self):
        return hist.dernier(self.historique)

    def effacer_historique(self):
        self.historique = []

    def retour(self):
        for symbole in self.SYMBOLES:
            if self.expression.endswith(symbole):
                self.expression = self.expression[:-len(symbole)]
                return

        self.expression = self.expression[:-1]

    def clear(self):
        self.expression = ""
        self.vient_de_calculer = False

    def signe(self):
        """Change le signe du nombre en cours de saisie — mantisse comprise."""
        nombre = self.dernier_nombre()

        if nombre == "":
            return

        debut = len(self.expression) - len(nombre)

        if self.expression[debut - 1:debut] == "-":
            self.expression = self.expression[:debut - 1] + nombre
        else:
            self.expression = self.expression[:debut] + "-" + nombre

    def dernier_nombre(self):
        """Le nombre en cours de saisie à la fin de l'expression.

        Renvoie le nombre COMPLET, exposant compris : dans "5+2.5e+18"
        c'est "2.5e+18", pas "18" — sinon ± changerait le signe de
        l'exposant au lieu de celui du nombre.
        """
        i = 0
        debut = None

        while i < len(self.expression):

            if self.expression[i] in self.CHIFFRES:
                debut = i
                i += len(self.lire_nombre(i))

            else:
                debut = None
                i += 1

        return "" if debut is None else self.expression[debut:]

    def point_permis(self):
        """Un nombre n'a qu'un seul point — et pas de point dans l'exposant."""
        nombre = self.dernier_nombre()

        return "." not in nombre and "e" not in nombre.lower()

    def contient_x(self):
        return "X" in self.expression

    # ==========================================================
    # Affichage
    # ==========================================================

    def get_display(self):
        return self.expression if self.expression else "0"

    def get_info(self):
        """Sous l'écran : combien de chiffres a le résultat, quand c'est gros.

        Inutile en mode SCI : l'exposant est déjà à l'écran, le compte
        de chiffres n'est que « exposant + 1 ».
        """
        if self.mode == "SCI":
            return ""

        if not self.vient_de_calculer or self.valeur is None or self.valeur == 0:
            return ""

        chiffres = self.exposant(self.valeur) + 1

        if chiffres > 15:
            return f"≈ {chiffres:,} chiffres".replace(",", " ")

        return ""

    def formater(self, valeur):
        """3.0 s'affiche 3, 3.5 reste 3.5, et 2^65536 passe en 2.0e+19728."""
        valeur = self.reel(valeur)

        if mpmath.isnan(valeur) or mpmath.isinf(valeur):
            raise ValueError("Nombre trop grand")

        if self.mode == "SCI":
            return self.scientifique(valeur)

        if abs(valeur) < mpf(10) ** self.CHIFFRES_ENTIER_MAX and valeur == int(valeur):
            return str(int(valeur))

        return mp.nstr(valeur, mp.dps, strip_zeros=True)

    def scientifique(self, valeur):
        """Toujours sous la forme  m.mmm e+xx  — un seul chiffre avant le point."""
        if valeur == 0:
            return "0"

        exposant = self.exposant(valeur)
        mantisse = valeur / mpf(10) ** exposant

        # l'arrondi peut donner 10.0 au lieu de 1.0 — on rattrape
        if abs(mantisse) >= 10:
            mantisse /= 10
            exposant += 1

        signe = "+" if exposant >= 0 else "-"

        return f"{mp.nstr(mantisse, mp.dps, strip_zeros=True)}e{signe}{abs(exposant)}"

    def exposant(self, valeur):
        """La puissance de 10 : 4500 -> 3, parce que 4500 = 4.5 × 10³."""
        return int(mpmath.floor(mpmath.log10(abs(valeur))))

    # ==========================================================
    # Calcul
    # ==========================================================

    def solve(self):
        """Calcule l'expression et la remplace par le résultat."""

        # Ré-appuyer sur "=" refait la dernière opération (comme une TI).
        if self.vient_de_calculer and self.repetition:
            self.expression += self.repetition

        if self.contient_x():
            raise ValueError("X : utilise le bouton Graphique")

        calcul = self.expression

        tokens = self.tokenize()
        self.verifier(tokens)

        self.repetition = self.extraire_repetition(tokens)

        self.valeur = self.evaluer(tokens)
        self.expression = self.formater(self.valeur)
        self.vient_de_calculer = True

        self.noter(calcul, self.expression)

        return self.get_display()

    def evaluer_pour(self, x):
        """Calcule l'expression en remplaçant X par une valeur (pour le graphique)."""
        tokens = self.tokenize()
        self.verifier(tokens)

        return self.evaluer(tokens, mpf(x))

    def extraire_repetition(self, tokens):
        """La fin '×4' de '12+3×4' — ce que '=' refera si on ré-appuie."""
        if len(tokens) >= 2 and tokens[-2] in self.INFIXES and self.est_nombre(tokens[-1]):
            return tokens[-2] + self.formater(tokens[-1])

        return ""

    # ==========================================================
    # Étape 1 — découper le texte en morceaux (tokens)
    # ==========================================================

    def tokenize(self):
        tokens = []
        i = 0

        while i < len(self.expression):
            c = self.expression[i]

            # un "-" là où on attend une valeur est un signe, pas une soustraction
            if c == "-" and self.attend_valeur(tokens):
                tokens.append("neg")
                i += 1
                continue

            if c in self.CHIFFRES:
                texte = self.lire_nombre(i)
                tokens.append(self.en_nombre(texte))
                i += len(texte)
                continue

            symbole = self.lire_symbole(i)

            if symbole is None:
                raise ValueError("Symbole inconnu")

            tokens.append(symbole)
            i += len(symbole)

        return self.multiplications_implicites(tokens)

    def lire_nombre(self, depart):
        """Lit 12, 3.5, et aussi la notation scientifique 2.5e+18."""
        i = depart

        while i < len(self.expression) and self.expression[i] in self.CHIFFRES:
            i += 1

        fin_mantisse = i

        if i < len(self.expression) and self.expression[i] in "eE":
            i += 1

            if i < len(self.expression) and self.expression[i] in "+-":
                i += 1

            if i < len(self.expression) and self.expression[i].isascii() \
                    and self.expression[i].isdigit():

                while i < len(self.expression) and self.expression[i].isascii() \
                        and self.expression[i].isdigit():
                    i += 1
            else:
                i = fin_mantisse      # un "e" tout seul : on l'ignore ici

        return self.expression[depart:i]

    def lire_symbole(self, i):
        for symbole in self.SYMBOLES:
            if self.expression.startswith(symbole, i):
                return symbole

        return None

    def attend_valeur(self, tokens):
        """Vrai si, à cet endroit, la calculatrice attend un nombre."""
        return (not tokens) or tokens[-1] in self.INFIXES \
            or tokens[-1] in self.PREFIXES or tokens[-1] == "("

    def en_nombre(self, texte):
        try:
            return mpf(texte)
        except (ValueError, TypeError):
            raise ValueError("Nombre invalide")

    def multiplications_implicites(self, tokens):
        """2π, 3X, 2(1+1) et 2√9 valent 2×π, 3×X, 2×(1+1), 2×√9."""
        resultat = []

        for token in tokens:

            if resultat and self.termine_valeur(resultat[-1]) and self.commence_valeur(token):
                resultat.append("×")

            resultat.append(token)

        return resultat

    def termine_valeur(self, token):
        return self.est_nombre(token) or token in self.CONSTANTES \
            or token in self.POSTFIXES or token == ")"

    def commence_valeur(self, token):
        return self.est_nombre(token) or token in self.CONSTANTES \
            or token in self.PREFIXES or token == "("

    def est_nombre(self, token):
        return not isinstance(token, str)

    # ==========================================================
    # Étape 2 — vérifier que l'expression a du sens
    # ==========================================================

    def verifier(self, tokens):
        if not tokens:
            raise ValueError("Expression vide")

        attend_valeur = True
        profondeur = 0

        for token in tokens:

            if attend_valeur:

                if self.est_nombre(token) or token in self.CONSTANTES:
                    attend_valeur = False

                elif token in self.PREFIXES:
                    pass

                elif token == "(":
                    profondeur += 1

                else:
                    raise ValueError("Expression invalide")

            else:

                if token in self.INFIXES:
                    attend_valeur = True

                elif token in self.POSTFIXES:
                    pass

                elif token == ")":
                    profondeur -= 1

                    if profondeur < 0:
                        raise ValueError("Parenthèse en trop")

                else:
                    raise ValueError("Expression invalide")

        if attend_valeur:
            raise ValueError("Expression incomplète")

        if profondeur > 0:
            raise ValueError("Parenthèse pas fermée")

    # ==========================================================
    # Étape 3 — calculer, dans le bon ordre de priorité
    # ==========================================================

    def evaluer(self, tokens, x=None):
        tokens = [self.valeur_de(t, x) for t in tokens]

        return self.reduire(self.parentheses(tokens))

    def valeur_de(self, token, x):
        if token == "π":
            return +mp.pi

        if token == "X":
            if x is None:
                raise ValueError("X : utilise le bouton Graphique")
            return x

        return token

    def parentheses(self, tokens):
        """Calcule les parenthèses les plus intérieures d'abord."""
        while "(" in tokens:
            fin = tokens.index(")")
            debut = max(i for i in range(fin) if tokens[i] == "(")

            tokens[debut:fin + 1] = [self.reduire(tokens[debut + 1:fin])]

        return tokens

    def reduire(self, tokens):
        """Applique les priorités, de la plus forte à la plus faible."""
        if not tokens:
            raise ValueError("Parenthèse vide")

        tokens = self.postfixes(tokens)
        tokens = self.racines(tokens)
        tokens = self.puissances(tokens)
        tokens = self.negations(tokens)
        tokens = self.multiply_divide(tokens)

        return self.add_subtract(tokens)

    def postfixes(self, tokens):
        """5! et 7² — collés à droite du nombre."""
        i = 0

        while i < len(tokens):

            if tokens[i] == "!":
                tokens[i - 1:i + 1] = [self.factorielle(tokens[i - 1])]

            elif tokens[i] == "²":
                tokens[i - 1:i + 1] = [self.puissance(tokens[i - 1], mpf(2))]

            else:
                i += 1

        return tokens

    def racines(self, tokens):
        """√9 — collé à gauche du nombre, donc on lit de droite à gauche."""
        i = len(tokens) - 1

        while i >= 0:

            if tokens[i] == "√":
                self.resoudre_neg(tokens, i + 1)
                tokens[i:i + 2] = [self.racine(tokens[i + 1], mpf(2))]

            i -= 1

        return tokens

    def puissances(self, tokens):
        """^, ↑↑ et ⁿ√ — de droite à gauche : 2^3^2 = 2^9."""
        i = len(tokens) - 1

        while i >= 0:

            if tokens[i] in ("^", "↑↑", "ⁿ√"):

                # le signe de l'exposant appartient à l'exposant : 2^-3 = 0.125
                self.resoudre_neg(tokens, i + 1)

                if tokens[i] == "^":
                    resultat = self.puissance(tokens[i - 1], tokens[i + 1])

                elif tokens[i] == "↑↑":
                    resultat = self.tetration(tokens[i - 1], tokens[i + 1])

                else:
                    resultat = self.racine(tokens[i + 1], tokens[i - 1])

                tokens[i - 1:i + 2] = [resultat]

            i -= 1

        return tokens

    def negations(self, tokens):
        """-2² vaut -4 : le moins passe APRÈS la puissance, comme en maths."""
        i = len(tokens) - 1

        while i >= 0:

            if tokens[i] == "neg":
                self.resoudre_neg(tokens, i)

            i -= 1

        return tokens

    def resoudre_neg(self, tokens, i):
        """Applique les 'neg' empilés à partir de la position i, du plus interne."""
        fin = i

        while fin < len(tokens) and tokens[fin] == "neg":
            fin += 1

        while fin > i:
            fin -= 1
            tokens[fin:fin + 2] = [-tokens[fin + 1]]

    def multiply_divide(self, tokens):
        i = 0

        while i < len(tokens):

            if tokens[i] == "×":
                tokens[i - 1:i + 2] = [tokens[i - 1] * tokens[i + 1]]
                i -= 1

            elif tokens[i] == "÷":
                tokens[i - 1:i + 2] = [tokens[i - 1] / tokens[i + 1]]
                i -= 1

            else:
                i += 1

        return tokens

    def add_subtract(self, tokens):
        resultat = tokens[0]
        i = 1

        while i < len(tokens):

            operateur = tokens[i]
            nombre = tokens[i + 1]

            if operateur == "+":
                resultat += nombre

            elif operateur == "-":
                resultat -= nombre

            i += 2

        return resultat

    # ==========================================================
    # Les opérations elles-mêmes (avec leurs garde-fous)
    # ==========================================================

    # Ces quatre-là ne calculent rien elles-mêmes : elles vérifient ce
    # qui doit l'être, puis passent le travail à mes_operations.py.

    def puissance(self, base, exposant):
        return self.resultat_de(ops.puissance(base, exposant))

    def racine(self, nombre, indice):
        if indice == 0:
            raise ValueError("Racine d'indice 0")

        if nombre < 0:
            raise ValueError("Racine d'un nombre négatif")

        if indice == 2:
            return self.resultat_de(ops.racine_carree(nombre))

        if indice != int(indice):
            return self.puissance(nombre, mpf(1) / indice)

        return self.resultat_de(ops.racine_nieme(nombre, indice))

    def factorielle(self, nombre):
        if nombre < 0:
            raise ValueError("Factorielle d'un nombre négatif")

        if nombre > self.EXPOSANT_MAX:
            raise ValueError("Factorielle trop grande")

        return self.resultat_de(ops.factorielle(nombre))

    def tetration(self, base, hauteur):
        return self.resultat_de(ops.tetration(base, hauteur))

    def resultat_de(self, valeur):
        """Vérifie ce que mes_operations.py vient de renvoyer."""
        if valeur is None:
            raise ValueError("Opération pas encore écrite")

        return self.reel(valeur)

    def reel(self, valeur):
        """mpmath peut renvoyer un nombre imaginaire — on refuse poliment."""
        if isinstance(valeur, mpmath.mpc):

            if valeur.imag == 0:
                return valeur.real

            raise ValueError("Résultat imaginaire")

        return valeur
