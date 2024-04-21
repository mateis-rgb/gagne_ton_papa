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


class AireDeJeu:
    def __init__(self, N):
        self.N = N
        self.matrice = np.zeros((5, N), dtype=int)

    def placer_piece(self, piece, forme, position):
        y, x = position
        piece_shape = piece.shapes[forme]
        self.matrice[y:y+piece_shape.shape[0], x:x+piece_shape.shape[1]] += piece_shape * piece.identifier

    def afficher(self):
        print(self.matrice)
