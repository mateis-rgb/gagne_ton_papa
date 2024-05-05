from numpy import zeros, array

class Piece:
	def __init__(self, name, color, identifier, shapes):
		self.name: str = name
		self.color: str = color
		self.identifier: int = identifier
		self.shapes: list[list[int]] = shapes

	def replace_id(self):
		pass

	def get(self):
		return {
			"name": self.name, 
			"color": self.color, 
			"identifier": self.identifier, 
			"shapes": self.shapes
		} 
	
	def rotate_90_degrees(self):
		# Récupérer les dimensions de la forme de la pièce
		rows = len(self.shapes)  # Nombre de lignes de la forme de pièce
		cols = len(self.shapes[0])  # Nombre de colonnes de la forme de pièce

		# Créer une nouvelle forme de pièce pour stocker la rotation
		rotated_shape = [[0 for _ in range(rows)] for _ in range(cols)]

		# Parcourir la forme de la pièce d'origine
		for i in range(rows):
			for j in range(cols):
				# Effectuer la rotation en déplaçant les éléments de la forme de pièce d'origine
				# vers la nouvelle forme de pièce selon la formule de rotation de 90 degrés dans le sens des aiguilles d'une montre
				rotated_shape[j][rows - 1 - i] = self.shapes[i][j]

		# Mettre à jour la forme de pièce de l'objet Piece avec la forme tournée
		self.shapes = rotated_shape


class BoiteDePieces:
	def __init__(self):
		self.pieces: dict[str, Piece] = {}

	def ajouter_piece(self, piece: Piece):
		self.pieces[piece.name] = piece.get()

	def afficher(self):
		print(self.pieces)


class AireDeJeu:
	def __init__(self, N: int):
		self.N: int = N
		self.matrice: list[list[int]] = zeros((5, N), dtype=int)


	def afficher(self):
		print(self.matrice)


	def peut_placer(self, piece: Piece) -> list[list[int]]:
		# Initialise une liste vide pour stocker les coordonnées des positions valides
		positions_valides = []

		# Récupérer les dimensions de la matrice de l'aire de jeu
		m = len(self.matrice)  # Nombre de lignes
		n = len(self.matrice[0])  # Nombre de colonnes

		# Récupérer les dimensions de la forme de la pièce
		x = len(piece.shapes)  # Nombre de lignes de la forme de la pièce
		y = len(piece.shapes[0])  # Nombre de colonnes de la forme de la pièce

		# Parcourir la matrice de l'aire de jeu
		for i in range(m - x + 1):
			for j in range(n - y + 1):
				# Vérifier si la forme de la pièce peut être placée à cette position
				can_place = True
				for row in range(x):
					for col in range(y):
						# Vérifier si l'emplacement dans la matrice est libre (vaut 0)
						# et si la forme de la pièce correspond à cette position
						if self.matrice[i + row][j + col] != 0 and piece.shapes[row][col] == 1:
							# Si l'emplacement est occupé dans la matrice et que la forme de la pièce est également
							# occupée à cette position, la pièce ne peut pas être placée ici
							can_place = False
							break
					if not can_place:
						break
				if can_place:
					# Si la forme de la pièce peut être placée à cette position, ajouter les coordonnées à la liste
					positions_valides.append((i, j))
		
		# Retourner la liste des coordonnées des positions valides
		return positions_valides


	def placer(self, piece: Piece, position: list[int]):
		# Récupérer les dimensions de la forme de la pièce
		x = len(piece.shapes)  # Nombre de lignes de la forme de la pièce
		y = len(piece.shapes[0])  # Nombre de colonnes de la forme de la pièce
		
		# Récupérer les coordonnées de la position où placer la pièce
		row, col = position
		
		# Parcourir la forme de la pièce
		for i in range(x):
			for j in range(y):
				# Vérifier si la forme de la pièce a une valeur de 1 à cette position
				if piece.shapes[i][j] == 1:
					# Placer l'identifiant de la pièce à la position correspondante dans la matrice de l'aire de jeu
					self.matrice[row + i][col + j] = piece.identifier


	def supprimer(self, identifier: int):
		# Parcourir la matrice de l'aire de jeu
		for i in range(len(self.matrice)):
			for j in range(len(self.matrice[0])):
				# Si l'élément de la matrice correspond à l'identifiant de la pièce
				if self.matrice[i][j] == identifier:
					# Remplacer l'identifiant par 0 (emplacement vide)
					self.matrice[i][j] = 0


def main() -> None:
	# Définition des pièces
	boite = BoiteDePieces()

	piece1 = Piece("PointRouge", "red", 1, [[1]]) # comment faites vous les . 
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
	piece16 = Piece("SJaune", "yellow", 32768, [[1, 1], [1, 0], [1, 1], [0, 1], [1, 1]])
	piece17 = Piece("SBleuClair", "lightblue", 65536, [[1, 1], [1, 0], [1, 1], [0, 1], [1, 1]]) # comment faites vous le S 
	piece18 = Piece("SViolet", "magenta", 131072, [[1, 1], [1, 0], [1, 1], [0, 1], [1, 1]])

	# Définition des autres pièces...

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