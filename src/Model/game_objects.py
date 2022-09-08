from enum import Enum

from src.Interfaces.game_pieces import IPosition, ISlot, IStatusPosition, IGrid, IPlayerCheker


class StatusPosition(IStatusPosition, Enum):
    @classmethod
    def _missing_(cls, value):
        return cls.EMPTY


class Position(IPosition):

    def __init__(self, x: int, y: int):
        super(Position, self).__init__()
        self.__x = x
        self.__y = y
        self.__status = StatusPosition.EMPTY
        self.__position_value = (self.__x, self.__y)

    def __repr__(self):
        return f"Position <x={self.__x}, y={self.__y}>, StatusPosition <status={self.get_status()}>"

    def set_status(self):
        self.__status = StatusPosition.FULL

    def get_status(self):
        return self.__status

    def value(self):
        return self.__position_value


class PlayerCheker(IPlayerCheker):
    def __init__(self, number: str):
        super(PlayerCheker, self).__init__()
        self.__number = number

    @property
    def number(self):
        return str(self.__number)

    def __repr__(self):
        return f"PlayerCheker: <number={self.number}>"

class Slot(ISlot):
    def __init__(self, position: IPosition):
        super(Slot, self).__init__()
        self.position = position
        self.player_cheker: IPlayerCheker

    def position(self):
        return self.position.value()

    def __repr__(self):
        __repr = f'Slot: {self.position:}'
        if self.position.get_status() == StatusPosition.FULL:
            __repr += f", {self.player_cheker:}"
        return __repr

    def occupy_with_player_piece(self, player_cheker: IPlayerCheker):
        self.player_cheker = player_cheker
        self.position.set_status()


class Grid(IGrid):

    def __init__(self):
        super(Grid, self).__init__()
        self.slots = self.make_grid()

    def make_grid(self):
        return [Slot(Position(row, col)) for col in range(self.COLUMNS) for row in range(self.ROWS)]

    COLUMNS = 7
    ROWS = 6


if __name__ == '__main__':
    pos = Position(0, 1)
    print(pos)
    slot = Slot(pos)
    print(slot)
    grid_game = Grid()
    print(grid_game)
