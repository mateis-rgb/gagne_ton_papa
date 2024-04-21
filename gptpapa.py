import numpy as np

class Piece:
    def __init__(self, name, color, identifier, shapes):
        self.name = name
        self.color = color
        self.identifier = identifier
        self.shapes = shapes

class BoiteDePieces:
    def __init__(self):
        self.pieces = []

    def ajouter_piece(self, piece):
        self.pieces.append(piece)

# Définition des pièces
boite = BoiteDePieces()

piece1 = Piece("PointRouge", "red", 1, [np.array([[1]])])
piece2 = Piece("PointViolet", "magenta", 2, [np.array([[1, 1], [1, 0]]), np.array([[1, 1], [0, 1]])])
piece3 = Piece("BRose", "pink", 4, [np.array([[1, 0], [1, 1]]), np.array([[1, 1], [1, 0]])])
# Définition des autres pièces...

boite.ajouter_piece(piece1)
boite.ajouter_piece(piece2)
boite.ajouter_piece(piece3)
# Ajouter les autres pièces...

class AireDeJeu:
    def __init__(self, N):
        self.N = N
        self.matrice = np.zeros((5, N), dtype=int)

    def placer_piece(self, piece, forme, position):
        y, x = position
        piece_shape = piece.shapes[forme]
        self.matrice[y:y+piece_shape.shape[0], x:x+piece_shape.shape[1]] += piece_shape * piece.identifier

    def retirer_piece(self, piece, forme, position):
        y, x = position
        piece_shape = piece.shapes[forme]
        self.matrice[y:y+piece_shape.shape[0], x:x+piece_shape.shape[1]] -= piece_shape * piece.identifier

    def est_case_valide(self, position, piece, forme):
        y, x = position
        piece_shape = piece.shapes[forme]
        if y + piece_shape.shape[0] > 5 or x + piece_shape.shape[1] > self.N:
            return False
        sub_matrix = self.matrice[y:y+piece_shape.shape[0], x:x+piece_shape.shape[1]]
        return np.all((sub_matrix == 0) | (sub_matrix == piece.identifier))

    def afficher(self):
        print(self.matrice)

def trouver_solutions(boite_pieces, aire_de_jeu, pieces_placees=[]):
    if len(pieces_placees) == len(boite_pieces.pieces):
        aire_de_jeu.afficher()
        print("Solution trouvée!\n")
        return 1

    nombre_solutions = 0

    for piece in boite_pieces.pieces:
        if piece not in pieces_placees:
            for forme_index, forme in enumerate(piece.shapes):
                for y in range(aire_de_jeu.matrice.shape[0]):
                    for x in range(aire_de_jeu.matrice.shape[1]):
                        if aire_de_jeu.est_case_valide((y, x), piece, forme_index):
                            aire_de_jeu.placer_piece(piece, forme_index, (y, x))
                            pieces_placees.append(piece)
                            nombre_solutions += trouver_solutions(boite_pieces, aire_de_jeu, pieces_placees)
                            pieces_placees.pop()
                            aire_de_jeu.retirer_piece(piece, forme_index, (y, x))

    return nombre_solutions

# Test de l'algorithme
aire = AireDeJeu(4)
print("Nombre de solutions trouvées:", trouver_solutions(boite, aire))
