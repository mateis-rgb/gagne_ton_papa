#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2024 Matéis Rgb & Maxence Rgn.

class Piece:
	"""
	Classe représentant une pièce.

	Attributes:
		nom (str): Le nom de la pièce.
		couleur (str): La couleur de la pièce.
		identifiant (int): L'identifiant de la pièce.
		formes (list[list[int]]): Les différentes formes de la pièce.
		_rang (int): rang de la pièce (taille)
	"""
	def __init__(self, nom, couleur, identifiant, formes):
		self.nom: str = nom
		self.couleur: str = couleur
		self.identifiant: int = identifiant
		self.formes: list[list[int]] = formes
		
		self._rang: int = None

	def definir_rang(self):
		"""
		Méthode pour calculer le rang d'une pièce, en se basant sur sa taille.
		"""
		pass

	def remplacer_id(self):
		"""
		Méthode pour remplacer l'identifiant de la pièce.
		"""
		pass

	def obtenir(self):
		"""
		Méthode pour obtenir les informations de la pièce.

		Returns:
			dict: Un dictionnaire contenant les informations de la pièce.
		"""
		return {
			"nom": self.nom, 
			"couleur": self.couleur, 
			"identifiant": self.identifiant, 
			"formes": self.formes
		} 

	def rotation_90_degres(self):
		"""
		Méthode pour effectuer une rotation de 90 degrés de la pièce.
		"""
		# Récupérer les dimensions de la forme de la pièce
		lignes = len(self.formes)  # Nombre de lignes de la forme de pièce
		colonnes = len(self.formes[0])  # Nombre de colonnes de la forme de pièce

		# Créer une nouvelle forme de pièce pour stocker la rotation
		forme_rot = [[0 for _ in range(lignes)] for _ in range(colonnes)]

		# Parcourir la forme de la pièce d'origine
		for i in range(lignes):
			for j in range(colonnes):
				# Effectuer la rotation en déplaçant les éléments de la forme de pièce d'origine
				# vers la nouvelle forme de pièce selon la formule de rotation de 90 degrés dans le sens des aiguilles d'une montre
				forme_rot[j][lignes - 1 - i] = self.formes[i][j]

		# Mettre à jour la forme de pièce de l'objet Piece avec la forme tournée
		self.formes = forme_rot


class BoiteDePieces:
	"""
	Classe représentant une boîte de pièces.

	Attributes:
		pieces (dict[str, Piece]): Un dictionnaire contenant les pièces de la boîte.
	"""
	def __init__(self):
		self.pieces: dict[str, Piece] = {}

	def ajouter_piece(self, piece: Piece):
		"""
		Méthode pour ajouter une pièce à la boîte.

		Args:
			piece (Piece): La pièce à ajouter.
		"""
		self.pieces[piece.nom] = piece.obtenir()

	def supprimer_piece(self, piece: Piece):
		"""
		Méthode pour supprimer une pièce de la boîte.
		"""
		pass

	def classement(self):
		"""
		Méthode pour classer les pièces en fonction de leur rang.
		"""
		pass

	def afficher(self):
		"""
		Méthode pour afficher les pièces de la boîte.
		"""
		print(self.pieces)


class AireDeJeu:
	"""
	Classe représentant une aire de jeu.

	Attributes:
		N (int): La taille de l'aire de jeu.
		matrice (list[list[int]]): La matrice représentant l'aire de jeu.
	"""
	def __init__(self, N: int):
		self.N: int = N
		self.matrice: list[list[int]] = [[0 for k in range(N)] for _ in range(5)]

	def afficher(self):
		"""
		Méthode pour afficher la matrice de l'aire de jeu.
		"""
		print(self.matrice)

	def recherche(self):
		"""
		Méthode pour rechercher une solution au plateau de jeu, en essayant de placer en priorité les pièces les plus grande (plus petit rank)
		"""
		pass

	def peut_placer(self, piece: Piece) -> list[list[int]]:
		"""
		Méthode pour vérifier si une pièce peut être placée dans l'aire de jeu.

		Args:
			piece (Piece): La pièce à placer.

		Returns:
			list[list[int]]: Une liste de coordonnées des positions valides.
		"""
		# Initialise une liste vide pour stocker les coordonnées des positions valides
		positions_valides = []

		# Récupérer les dimensions de la matrice de l'aire de jeu
		m = len(self.matrice)  # Nombre de lignes
		n = len(self.matrice[0])  # Nombre de colonnes

		# Récupérer les dimensions de la forme de la pièce
		x = len(piece.formes)  # Nombre de lignes de la forme de la pièce
		y = len(piece.formes[0])  # Nombre de colonnes de la forme de la pièce

		# Parcourir la matrice de l'aire de jeu
		for i in range(m - x + 1):
			for j in range(n - y + 1):
				# Vérifier si la forme de la pièce peut être placée à cette position
				peut_placer = True
				for ligne in range(x):
					for colonne in range(y):
						# Vérifier si l'emplacement dans la matrice est libre (vaut 0)
						# et si la forme de la pièce correspond à cette position
						if self.matrice[i + ligne][j + colonne] != 0 and piece.formes[ligne][colonne] == 1:
							# Si l'emplacement est occupé dans la matrice et que la forme de la pièce est également
							# occupée à cette position, la pièce ne peut pas être placée ici
							peut_placer = False
							break

					if not peut_placer:
						break

				if peut_placer:
					# Si la forme de la pièce peut être placée à cette position, ajouter les coordonnées à la liste
					positions_valides.append((i, j))
		
		# Retourner la liste des coordonnées des positions valides
		return positions_valides

	def placer(self, piece: Piece, position: list[int]):
		"""
		Méthode pour placer une pièce dans l'aire de jeu.

		Args:
			piece (Piece): La pièce à placer.
			position (list[int]): Les coordonnées de la position où placer la pièce.
		"""
		# Récupérer les dimensions de la forme de la pièce
		x = len(piece.formes)  # Nombre de lignes de la forme de la pièce
		y = len(piece.formes[0])  # Nombre de colonnes de la forme de la pièce
		
		# Récupérer les coordonnées de la position où placer la pièce
		ligne, colonne = position
		
		# Parcourir la forme de la pièce
		for i in range(x):
			for j in range(y):
				# Vérifier si la forme de la pièce a une valeur de 1 à cette position
				if piece.formes[i][j] == 1:
					# Placer l'identifiant de la pièce à la position correspondante dans la matrice de l'aire de jeu
					self.matrice[ligne + i][colonne + j] = piece.identifiant

	def supprimer(self, identifiant: int):
		"""
		Méthode pour supprimer une pièce de l'aire de jeu.

		Args:
			identifiant (int): L'identifiant de la pièce à supprimer.
		"""
		# Parcourir la matrice de l'aire de jeu
		for i in range(len(self.matrice)):
			for j in range(len(self.matrice[0])):
				# Si l'élément de la matrice correspond à l'identifiant de la pièce
				if self.matrice[i][j] == identifiant:
					# Remplacer l'identifiant par 0 (emplacement vide)
					self.matrice[i][j] = 0


def main() -> None:
	boite = BoiteDePieces()

	# Définition des pièces
	piece1 = Piece("PointRouge", "red", 1, [[1]])
	piece2 = Piece("PointRouge", "red", 2, [[1]])
	piece3 = Piece("PointViolet", "magenta", 4, [[1]])
	piece4 = Piece("BRose", "pink", 8, [[1,0], [1, 1], [1, 1]])
	piece5 = Piece("CJaune", "yellow", 16, [[1, 1], [1, 0], [1, 1]])
	piece6 = Piece("IOrangeClair", "lightorange", 32, [[1], [1]])
	piece7 = Piece("IOrangeClair", "lightorange", 64, [[1], [1]])
	piece8 = Piece("IOrangeFonce", "darkorange", 128, [[1], [1]])
	piece9 = Piece("IRose", "pink", 256,[[1], [1]])
	piece10 = Piece("LMarron", "maroon", 512, [[1, 0], [1, 0], [1, 1]])
	piece11 = Piece("LVert", "green", 1024, [[1, 0], [1, 0], [1, 1]])
	piece12 = Piece("LBleu", "blue", 2048, [[1, 0], [1, 0], [1, 1]])
	piece13 = Piece("LOrangeFonce", "darkorange", 4096, [[1, 0], [1, 0], [1, 1]])
	piece14 = Piece("TMarron", "maroon", 8192, [[1, 1, 1], [0, 1, 0]])
	piece15 = Piece("TBleuClair", "lightblue", 16384, [[1, 1, 1]])
	piece16 = Piece("SJaune", "yellow", 32768, [[0, 1, 1], [1, 1, 0]])
	piece17 = Piece("SBleuClair", "lightblue", 65536, [[0, 1, 1], [1, 1, 0]])
	piece18 = Piece("SViolet", "magenta", 131072, [[0, 1, 1], [1, 1, 0]])

	# Ajout des pièces dans la boite
	boite.ajouter_piece(piece1)
	boite.ajouter_piece(piece2)
	boite.ajouter_piece(piece3)
	boite.ajouter_piece(piece4)
	boite.ajouter_piece(piece5)
	boite.ajouter_piece(piece6)
	boite.ajouter_piece(piece7)
	boite.ajouter_piece(piece8)
	boite.ajouter_piece(piece9)
	boite.ajouter_piece(piece10)
	boite.ajouter_piece(piece11)
	boite.ajouter_piece(piece12)
	boite.ajouter_piece(piece13)
	boite.ajouter_piece(piece14)
	boite.ajouter_piece(piece15)
	boite.ajouter_piece(piece16)
	boite.ajouter_piece(piece17)
	boite.ajouter_piece(piece18)

	plateau = AireDeJeu(4)
	plateau.afficher()
	
	boite.afficher()

if __name__ == '__main__':
	main()