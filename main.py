from numpy import zeros, array

class Piece:
    def __init__(self, name, color, identifier, shapes):
        self.name: str = name
        self.color: str = color
        self.identifier: str = identifier
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

    def placer_piece(self, piece: Piece, forme: list[list[int]], position: tuple[int, int]):
        y, x = position
        piece_shape = piece.shapes[forme]
        self.matrice[y:y+piece_shape.shape[0], x:x+piece_shape.shape[1]] += piece_shape * piece.identifier # à revoir

    def afficher(self):
        print(self.matrice)

    def peut_placer():
        pass

    def placer():
        pass

    def supprimer():
        pass

def main() -> None:
    # Définition des pièces
    boite = BoiteDePieces()

    piece1 = Piece("PointRouge", "red", 1, [1])
    piece2 = Piece("PointViolet", "magenta", 2, [1])
    piece3 = Piece("CRose", "pink", 4, [[1, 1], [1, 0], [1, 1]])
    # Définition des autres pièces...

    boite.ajouter_piece(piece1)
    boite.ajouter_piece(piece2)
    boite.ajouter_piece(piece3)

    plateau = AireDeJeu(4)
    plateau.afficher()

    boite.afficher()

if __name__ == '__main__':
    main()