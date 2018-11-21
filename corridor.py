from game_consts import CORRIDOR_SAFETY

class Corridor():
    """Represents an uninterrupted path of adjacente coordinates with a
    crossroad at each end

    Args:
        coordinates: list of coordinates of the Corridor

    Attr:
        coordinates: list of coordinates of the Corridor
        length: length of coordinates without crossroad ends

    """
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.length = len(coordinates) - 2 if len(coordinates)>1 else 0
        self.ends = (coordinates[0], coordinates[len(coordinates)-1])
        self.safe = CORRIDOR_SAFETY.SAFE
        
    def dist_end0(self, coord):
        return len(self.coordinates[0:coord])

    def dist_end1(self, coord):
        return len(self.coordinates[coord:self.length])

    def dist_end(self, coord, end):
        if end == self.ends[0]:
            return self.dist_end0(coord)
        return self.dist_end1(coord)

    def closest_end(self, coord):
        return self.dist_end0(coord) \
            if self.dist_end0(coord) <= self.dist_end1(coord) \
            else self.dist_end1(coord)

    def sub_corridors(self, coord):
        index = self.coordinates.index(coord)
        return Corridor(self.coordinates[:index+1]), Corridor(self.coordinates[index:])

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return self.__str__()