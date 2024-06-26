#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2024 Matéis Rgb & Maxence Rgn.

import pygame
import sys

# Configuration de la fenêtre
TAILLE_CASE = 50
COULEURS = {
    "red": (255, 0, 0),
    "magenta": (255, 0, 255),
    "pink": (255, 192, 203),
    "yellow": (255, 255, 0),
    "lightorange": (255, 200, 0),
    "darkorange": (255, 140, 0),
    "maroon": (128, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "lightblue": (173, 216, 230)
}

class Piece:
    """Classe représentant une pièce du jeu."""
    def __init__(self, nom, couleur, identifiant, forme):
        """
        Initialise une pièce avec les attributs donnés.

        Args:
            nom (str): Le nom de la pièce.
            couleur (str): La couleur de la pièce.
            identifiant (int): L'identifiant de la pièce.
            forme (list): La forme de la pièce représentée par une liste de listes.
        """
        self.nom = nom
        self.couleur = couleur
        self.identifiant = identifiant
        self.forme = forme
        self._rang = None

    def definir_rang(self):
        """Définit le rang de la pièce en fonction de sa forme."""
        cpt = sum(row.count(1) for row in self.forme)
        self._rang = cpt

    def remplacer_id(self):
        """Remplace les cellules de la forme de la pièce par son identifiant."""
        self.forme = [[self.identifiant if cell == 1 else cell for cell in row] for row in self.forme]

    def rotation_90_degres(self):
        """Effectue une rotation de 90 degrés de la forme de la pièce."""
        self.forme = [list(row) for row in zip(*self.forme[::-1])]

    def symetrie(self):
        """Effectue une symétrie de la forme de la pièce."""
        self.forme = [row[::-1] for row in self.forme]

    def generer_transformations(self):
        """
        Génère toutes les transformations possibles de la pièce.

        Returns:
            list: Liste des différentes formes obtenues après transformation.
        """
        transformations = set()
        for _ in range(4):
            self.rotation_90_degres()
            forme_tuple = tuple(tuple(row) for row in self.forme)
            transformations.add(forme_tuple)
            self.symetrie()
            forme_tuple_sym = tuple(tuple(row) for row in self.forme)
            transformations.add(forme_tuple_sym)
            self.symetrie()
        return [list(list(row) for row in forme) for forme in transformations]

class BoiteDePieces:
    """Classe représentant une boîte de pièces."""
    def __init__(self):
        """Initialise une boîte de pièces avec un dictionnaire vide de pièces et un classement vide."""
        self.pieces = {}
        self._classement = {}

    def ajouter_piece(self, piece):
        """
        Ajoute une pièce à la boîte de pièces et met à jour le classement.

        Args:
            piece (Piece): La pièce à ajouter.
        """
        self.pieces[piece.nom] = piece
        piece.definir_rang()
        self.definir_classement()

    def supprimer_piece(self, piece):
        """
        Supprime une pièce de la boîte de pièces et met à jour le classement.

        Args:
            piece (Piece): La pièce à supprimer.
        """
        if piece.nom in self.pieces:
            del self.pieces[piece.nom]
            self.definir_classement()

    def definir_classement(self):
        """Définit le classement des pièces en fonction de leur rang."""
        self._classement = {}
        for piece in self.pieces.values():
            rang = piece._rang
            if rang not in self._classement:
                self._classement[rang] = []
            self._classement[rang].append(piece)
        self._classement = dict(sorted(self._classement.items(), reverse=True))

    def afficher(self):
        """Affiche les pièces présentes dans la boîte."""
        print(self.pieces)

class AireDeJeu:
    """Classe représentant l'aire de jeu."""
    def __init__(self, N):
        """
        Initialise l'aire de jeu avec une taille donnée.

        Args:
            N (int): La taille de l'aire de jeu.
        """
        self.N = N
        self.matrice = [[0 for _ in range(N)] for _ in range(5)]

    def afficher(self):
        """Affiche la matrice représentant l'aire de jeu."""
        for row in self.matrice:
            print(row)

    def peut_placer(self, piece, start_i, start_j):
        """
        Vérifie si une pièce peut être placée à une certaine position sur l'aire de jeu.

        Args:
            piece (Piece): La pièce à placer.
            start_i (int): L'indice de ligne de départ.
            start_j (int): L'indice de colonne de départ.

        Returns:
            bool: True si la pièce peut être placée, False sinon.
        """
        lignes_piece = len(piece.forme)
        colonnes_piece = len(piece.forme[0])

        if start_i + lignes_piece > len(self.matrice) or start_j + colonnes_piece > len(self.matrice[0]):
            return False

        for i in range(lignes_piece):
            for j in range(colonnes_piece):
                if piece.forme[i][j] != 0 and self.matrice[start_i + i][start_j + j] != 0:
                    return False

        return True

    def placer(self, piece, position):
        """
        Place une pièce à une certaine position sur l'aire de jeu.

        Args:
            piece (Piece): La pièce à placer.
            position (tuple): La position de départ de la pièce (ligne, colonne).
        """
        x, y = len(piece.forme), len(piece.forme[0])
        ligne, colonne = position

        for i in range(x):
            for j in range(y):
                if piece.forme[i][j] != 0:
                    self.matrice[ligne + i][colonne + j] = piece.identifiant

    def supprimer(self, piece, position):
        """
        Supprime une pièce de l'aire de jeu à une certaine position.

        Args:
            piece (Piece): La pièce à supprimer.
            position (tuple): La position de la pièce à supprimer (ligne, colonne).
        """
        x, y = len(piece.forme[0])
        ligne, colonne = position

        for i in range(x):
            for j in range(y):
                if piece.forme[i][j] != 0:
                    self.matrice[ligne + i][colonne + j] = 0

    def recherche(self, boite):
        """
        Recherche une solution en plaçant les pièces de la boîte sur l'aire de jeu.

        Args:
            boite (BoiteDePieces): La boîte de pièces contenant les pièces à placer.

        Returns:
            bool: True si une solution est trouvée, False sinon.
        """
        pieces = [piece for rang in boite._classement.values() for piece in rang]
        return self.recherche_recursive(pieces, 0)

    def recherche_recursive(self, pieces, index):
        """
        Recherche récursive d'une solution en plaçant les pièces sur l'aire de jeu.

        Args:
            pieces (list): Liste des pièces à placer.
            index (int): Indice de la pièce actuelle dans la liste des pièces.

        Returns:
            bool: True si une solution est trouvée, False sinon.
        """
        if index == len(pieces):
            return True

        piece = pieces[index]
        transformations = piece.generer_transformations()

        for forme in transformations:
            piece.forme = forme
            for i in range(len(self.matrice)):
                for j in range(len(self.matrice[0])):
                    if self.peut_placer(piece, i, j):
                        self.placer(piece, (i, j))
                        if self.recherche_recursive(pieces, index + 1):
                            return True
                        self.supprimer(piece, (i, j))

        return False

    def afficher_aire(self, boite):
        """
        Affiche l'aire de jeu avec les pièces placées en utilisant Pygame.

        Args:
            boite (BoiteDePieces): La boîte de pièces contenant les pièces placées.
        """
        pygame.init()
        fenetre = pygame.display.set_mode((len(self.matrice) * TAILLE_CASE, self.N * TAILLE_CASE))
        pygame.display.set_caption("Aire de Jeu")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            fenetre.fill((30, 30, 30))

            for i in range(len(self.matrice)):
                for j in range(len(self.matrice[0])):
                    couleur = (50, 50, 50)
                    for piece in boite.pieces.values():
                        if self.matrice[i][j] == piece.identifiant:
                            couleur = COULEURS[piece.couleur]
                    pygame.draw.rect(fenetre, couleur, (i * TAILLE_CASE, j * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 0)
                    pygame.draw.rect(fenetre, (255, 255, 255), (i * TAILLE_CASE, j * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)

            pygame.display.flip()

def main():
    # Définir les pièces
    pieces = [
        Piece("A", "red", 1, [[1, 1, 1], [0, 1, 0]]),
        Piece("B", "blue", 2, [[1, 1], [1, 1]]),
        Piece("C", "green", 3, [[1, 1, 1, 1]]),
        Piece("D", "yellow", 4, [[1, 1], [1, 0]]),
        Piece("E", "magenta", 5, [[1, 1, 1], [1, 0, 0]]),
        Piece("F", "pink", 6, [[1, 0], [1, 1], [0, 1]]),
        Piece("G", "lightorange", 7, [[1, 1], [0, 1], [0, 1]]),
        Piece("H", "darkorange", 8, [[1, 1, 1, 1, 1]]),
        Piece("I", "maroon", 9, [[1], [1], [1]]),
        Piece("J", "lightblue", 10, [[1, 1, 1], [1, 1, 0]])
    ]

    # Initialiser la boîte de pièces
    boite = BoiteDePieces()
    for piece in pieces:
        boite.ajouter_piece(piece)
    boite.definir_classement()

    # Initialiser l'aire de jeu
    plateau = AireDeJeu(10)
    if plateau.recherche(boite):
        plateau.afficher()
    else:
        print("Aucune solution trouvée.")

    # Afficher l'aire de jeu avec Pygame
    plateau.afficher_aire(boite)

if __name__ == "__main__":
    main()