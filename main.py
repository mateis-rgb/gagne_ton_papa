#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2024 Matéis Rgb & Maxence Rgn.

class Piece:
	"""
	Classe représentant une pièce.

	Attributes
	
		nom (str): Le nom de la pièce.
		couleur (str): La couleur de la pièce.
		identifiant (int): L'identifiant de la pièce.
		forme (list[list[int]]): Les différentes forme de la pièce.
		_rang (int): rang de la pièce (taille)
	"""
	def __init__(self, nom, couleur, identifiant, forme):
		self.nom: str = nom
		self.couleur: str = couleur
		self.identifiant: int = identifiant
		self.forme: list[list[int]] = forme
		
		self._rang: int = None

	def definir_rang(self):
		"""
		Méthode pour calculer le rang d'une pièce, en se basant sur sa taille, la taille étant défini par le nombre de case qui sont remplis dans la matrice de la forme.
		"""

		cpt: int = 0

		for row in self.forme:
			for elm in row:
				if elm != 0:
					cpt += 1

		self._rang = cpt


	def remplacer_id(self):
		"""
		Méthode pour remplacer l'identifiant de la pièce.
		"""
		for i in range(len(self.forme)):
			for j in range(len(self.forme[i])):
				if self.forme[i][j] == 1:
					self.forme[i][j] = self.identifiant
		

	def rotation_90_degres(self):
		"""
		Méthode pour effectuer une rotation de 90 degrés de la pièce.
		"""
		# Récupérer les dimensions de la forme de la pièce
		lignes = len(self.forme)  # Nombre de lignes de la forme de pièce
		colonnes = len(self.forme[0])  # Nombre de colonnes de la forme de pièce

		# Créer une nouvelle forme de pièce pour stocker la rotation
		forme_rot = [[0 for _ in range(lignes)] for _ in range(colonnes)]

		# Parcourir la forme de la pièce d'origine
		for i in range(lignes):
			for j in range(colonnes):
				# Effectuer la rotation en déplaçant les éléments de la forme de pièce d'origine
				# vers la nouvelle forme de pièce selon la formule de rotation de 90 degrés dans le sens des aiguilles d'une montre
				forme_rot[j][lignes - 1 - i] = self.forme[i][j]

		# Mettre à jour la forme de pièce de l'objet Piece avec la forme tournée
		self.forme = forme_rot


class BoiteDePieces:
	"""
	Classe représentant une boîte de pièces.

	Attributes:
		pieces (dict[str, Piece]): Un dictionnaire contenant les pièces de la boîte.
		_classement (dict[int, list[Piece]]): Un dictionnaire contenant les pièces de la boîte classé selon leur rang (inversement au rang, les plus petites clées sont les pièces les plus grandes).
	"""
	def __init__(self):
		self.pieces: dict[str, Piece] = {}
		self._classement: dict[str, list[Piece]] = {}


	def ajouter_piece(self, piece: Piece):
		"""
		Méthode pour ajouter une pièce à la boîte.

		Args:
			piece (Piece): La pièce à ajouter.
		"""
		self.pieces[piece.nom] = piece


	def supprimer_piece(self, piece: Piece):
		"""
		Méthode pour supprimer une pièce de la boîte.

		Args:
			piece (Piece): La pièce à supprimer.
		"""
		# Vérifier si la pièce est présente dans la boîte
		if piece.nom in self.pieces:
			# Supprimer la pièce de la boîte
			del self.pieces[piece.nom]
			
			# Actualiser le classement des pièces
			self.definir_classement()


	def definir_classement(self):
		"""
		Méthode pour classer les pièces en fonction de leur rang.
		"""
		# Initialisation du dictionnaire de classement
		self._classement = {}

		# Parcourir les pièces de la boîte
		for nom, piece in self.pieces.items():
			# Vérifier si le rang de la pièce a déjà été défini
			if piece._rang is None:
				piece.definir_rang()

			# Récupérer le rang de la pièce
			rang_piece = piece._rang

			# Utiliser un rang inversé pour classer les pièces de la plus grande à la plus petite
			rang_inverse = -rang_piece

			# Convertir le rang inverse en rang positif
			rang_positif = abs(rang_inverse)

			# Vérifier si le rang positif existe déjà dans le classement
			if rang_positif in self._classement:
				# Ajouter la pièce à la liste correspondante au rang positif
				self._classement[rang_positif].append(piece)
			else:
				# Créer une nouvelle liste pour ce rang positif et y ajouter la pièce
				self._classement[rang_positif] = [piece]

		# Trier le classement en fonction des rangs positifs (clés du dictionnaire)
		self._classement = dict(sorted(self._classement.items(), reverse=True))
	
		for i in range(len(self._classement.items())//2):
			self._classement[rang_positif], self._classement[len(self._classement.items())-rang_positif+1] = self._classement[len(self._classement.items())-rang_positif+1], self._classement[rang_positif]


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

	def recherche(self, boiteDePieces: BoiteDePieces):
		"""
		Méthode pour rechercher une solution au plateau de jeu en plaçant en priorité les pièces les plus grandes (plus petit rang).

		Args:
			boiteDePieces (BoiteDePieces): La boîte de pièces contenant les pièces à placer sur l'aire de jeu.
		"""
		# Parcourir chaque rang de pièces dans la boîte de pièces
		for rang in boiteDePieces._classement.values():
			# Parcourir chaque pièce dans le rang
			for piece in rang:
				# Vérifier si la pièce peut être placée dans l'aire de jeu
				position_possible = self.peut_placer(piece)
				if position_possible is not None:
					# Si une position valide est trouvée, placer la pièce et passer à la suivante
					self.placer(piece, position_possible)
					break
				else:
					# Si la pièce ne peut pas être placée dans sa forme d'origine, essayer de la faire pivoter et réessayer
					for _ in range(3):
						piece.rotation_90_degres()  # Faire pivoter la pièce de 90 degrés
						position_possible = self.peut_placer(piece)
						if position_possible is not None:
							# Si une position valide est trouvée après la rotation, placer la pièce et passer à la suivante
							self.placer(piece, position_possible)
							break

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
		x = len(piece.forme)  # Nombre de lignes de la forme de la pièce
		y = len(piece.forme[0])  # Nombre de colonnes de la forme de la pièce

		# Parcourir la matrice de l'aire de jeu
		for i in range(m - x + 1):
			for j in range(n - y + 1):
				# Vérifier si la forme de la pièce peut être placée à cette position
				peut_placer = True
				for ligne in range(x):
					for colonne in range(y):
						# Vérifier si l'emplacement dans la matrice est libre (vaut 0)
						# et si la forme de la pièce correspond à cette position
						if self.matrice[i + ligne][j + colonne] != 0 and piece.forme[ligne][colonne] == 1:
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
		x = len(piece.forme)  # Nombre de lignes de la forme de la pièce
		y = len(piece.forme[0])  # Nombre de colonnes de la forme de la pièce
		
		# Récupérer les coordonnées de la position où placer la pièce
		ligne, colonne = position
		
		# Parcourir la forme de la pièce
		for i in range(x):
			for j in range(y):
				# Vérifier si la forme de la pièce a une valeur de 1 à cette position
				if piece.forme[i][j] == 1:
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
	# plateau.afficher()
	
	# boite.afficher()

	boite.definir_classement()

	plateau.recherche(boite)


if __name__ == '__main__':
	main()