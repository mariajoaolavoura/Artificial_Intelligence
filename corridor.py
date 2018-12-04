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
        self.length = len(coordinates) - 2 if len(coordinates) > 1 else 0
        self.cost = len(coordinates) - 1
        self.ends = [coordinates[0], coordinates[-1]]
        self.safe = CORRIDOR_SAFETY.SAFE
        
    def dist_end0(self, coord):
        return len(self.coordinates[:self.coordinates.index(coord)])

    def dist_end1(self, coord):
        return len(self.coordinates[self.coordinates.index(coord)+1:])

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

    def get_coord_next_to_end0(self):
        if len(self.coordinates) > 1:
            return self.coordinates[1]
        else:
            return None

    def get_coord_next_to_end1(self):
        if len(self.coordinates) > 1:
            return self.coordinates[-2]
        else:
            return None

    def get_coord_next_to_end(self, end):
        if end == self.ends[0]:
            return self.get_coord_next_to_end0()
        elif end == self.ends[1]:
            return self.get_coord_next_to_end1()
        else:
            return None

    def get_next_coord_to_the_side_of_crossroad(self, initial, crossroad):
        
        if crossroad == None:
            print('CORRIDOR: crossroad is None')
            return None

        initial_index = None
        for i in range(len(self.coordinates)):
            if initial == self.coordinates[i]:
                initial_index = i
                break
        
        if initial_index == None or initial == crossroad:
            if initial_index == None:
                print('CORRIDOR: initial index not found')
            else:
                print('CORRIDOR: pacman is in the crossroad is trying to go to the side of')
            return None

        if crossroad == self.ends[0]:
            return self.coordinates[initial_index-1]
        elif crossroad == self.ends[1]:
            return self.coordinates[initial_index+1]
        else:
            print('CORRIDOR: crossroad is wrong')
            return None

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return self.__str__()