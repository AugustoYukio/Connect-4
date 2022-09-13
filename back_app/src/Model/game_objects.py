from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List
from back_app.src.Interfaces.game_pieces import IPosition, ISlot, IStatusPosition, IGrid, IPlayerCheker, IBoard, IRow, \
    IColumn

THE_PRINCIPAL_NUMBER = 4


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
        return f"Position <x={self.__x}, y={self.__y}>, StatusPosition <status={self.status}>"

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status=StatusPosition.FULL):
        self.__status = status

    def value(self):
        return self.__position_value


@dataclass
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
        self.player_cheker: IPlayerCheker | None = None

    def position(self):
        return self.position.value()

    def __repr__(self):
        __repr = f'Slot: {self.position:}'
        if self.position.status == StatusPosition.FULL:
            __repr += f", {self.player_cheker:}"
        return __repr

    def occupy_with_player_piece(self, player_cheker: IPlayerCheker):
        try:
            self.player_cheker = player_cheker
            self.position.status = StatusPosition.FULL
        except Exception as err:
            print(f'ERRO.: {err}')
            return False
        return True


@dataclass()
class Row(IRow):
    number: int


@dataclass()
class Column(IColumn):
    number: int


class Grid(IGrid):
    COLUMNS, ROWS = 7, 6

    def __init__(self):
        super(Grid, self).__init__()
        self.slots = self.__make_grid()

    def __repr__(self):
        full_representation = []
        count = 10
        cell = "{" + f':^{count}' + "}"
        for n, rows in enumerate(reversed(self.slots), 0):
            index_row = self.ROWS - n - 1
            space = r'{:^3}'.format(index_row)
            base_f = f"{space}|{f'{cell}|' * self.COLUMNS}"
            # print(f"{index_row} -> {[slot for slot in rows]}")
            full_representation.append(base_f.format(*[
                slot.position.status if slot.position.status == StatusPosition.EMPTY else f'Player {slot.player_cheker.number}'
                for slot in rows]))
        space = ' ' * 3
        base_f = f"{space}|{f'{cell}|' * self.COLUMNS}"
        full_representation.append(base_f.format(*[str(slot) for slot in range(self.COLUMNS)]))
        return '\n'.join(full_representation)

    def __make_grid(self) -> List[List[ISlot]]:
        return [[Slot(Position(row, col)) for col in range(self.COLUMNS)] for row in range(self.ROWS)]

    def __get_slots_by_diagonal(self, position: IPosition) -> List[ISlot] | None:
        BOTTOM_END_OF_ROWS, BOTTOM_END_OF_COLUMNS = 0, 0

        inferior_x, inferior_y = position.value()

        if inferior_y >= inferior_x:
            inferior_y -= inferior_x
            inferior_x = BOTTOM_END_OF_ROWS
        else:
            inferior_x -= inferior_y
            inferior_y = BOTTOM_END_OF_COLUMNS

        superior_x, superior_y = position.value()

        if (self.ROWS - 1 - superior_x) <= (self.COLUMNS - 1 - superior_y):
            # limitação em X
            max_mov = self.ROWS - 1 - superior_x
            superior_y += max_mov
            superior_x += max_mov
        else:
            max_mov = self.COLUMNS - 1 - superior_y
            superior_y += max_mov
            superior_x += max_mov

        if (superior_x + 1 - inferior_x) < THE_PRINCIPAL_NUMBER or (superior_y + 1 - inferior_y) < THE_PRINCIPAL_NUMBER:
            """Caso a diagonal formada não tenha ao menos 4 slots"""
            return None

        print(f'Limite Superior: {(superior_x, superior_y,)}')
        print(f'Posição Inserida: {(position.value())}')
        print(f'Limite Inferior: {(inferior_x, inferior_y,)}')
        print(grid_game)

        # print(list(range(inferior_x, superior_x + 1)))
        # print(list(range(inferior_y, superior_y + 1)))
        # list(zip(range(inferior_x, superior_x + 1), range(inferior_y, superior_y + 1)))
        #         [self.slots[p_x][p_y].player_cheker for p_x, p_y in
        #          zip(range(inferior_x, superior_x + 1), range(inferior_y, superior_y + 1)) if
        #          self.slots[p_x][p_y].position.status == StatusPosition.FULL]
        rows_for_diagonal = zip(range(inferior_x, superior_x + 1), range(inferior_y, superior_y + 1))
        return [self.slots[p_x][p_y] for p_x, p_y in rows_for_diagonal]

    def __get_slots_by_horizontal(self, row: Row):
        return self.slots[row.number]

    def __get_slots_by_vertical(self, column: Column):
        return [row[column.number] for row in self.slots]

    def __get_free_slot_by_column(self, column: Column) -> ISlot | None:
        for slot in self.__get_slots_by_vertical(column):
            if slot.position.status == StatusPosition.EMPTY:
                return slot
        return None

    def __put_checker_in_slot(self, player_cheker: IPlayerCheker, column: Column) -> IPosition | None:
        slot = self.__get_free_slot_by_column(column)
        if not slot:
            return slot
        success = slot.occupy_with_player_piece(player_cheker)
        return slot.position if success else None


@dataclass(repr=False)
class Score(object):
    __first_player_points = 0
    __second_player_points = 0

    def switch_player_for_new_game(self):
        self.__first_player_points, self.__second_player_points = self.__second_player_points, self.__first_player_points

    def __repr__(self):
        return f"Score <First_Player={self.__first_player_points}, Second_Player={self.__second_player_points}>"

    def add_victory(self, player='first_player'):
        if player == 'first_player':
            self.__first_player_points += 1
        else:
            self.__second_player_points += 1


class Board(IBoard):
    score = Score()

    @property
    def background(self):
        return ''


def is_connected_for_4(rows: List[ISlot]):
    # TODO: Tornar função agnóstica em relação ao jopgador

    CONDITION_TO_VICTORY = THE_PRINCIPAL_NUMBER * 'p1'
    N = len(rows)

    # A loop to slide pat[] one by one
    for i in range(N - M + 1):

        # For current index i,
        # check for pattern match
        for j in range(M):
            if s2[i + j] != s1[j]:
                break

        if j + 1 == M:
            return i

    return -1


# Driver Code
if __name__ == "__main__":
    # s1 = "for"
    # s2 = "geeksforgeeks"
    # res = isSubstring(s1, s2)
    # if res == -1:
    #     print("Not present")
    # else:
    #     print("Present at index " + str(res))

    # pos = Position(0, 0)
    # print(pos)
    # slot = Slot(pos)
    # print(slot)
    grid_game = Grid()
    print(grid_game)
    pc = PlayerCheker('1')
    row = Row(3)
    column = Column(4)
    #     [grid_game.__put_checker_in_slot(pc, column) for n in range(4)]
    #     p = grid_game.__put_checker_in_slot(pc, column)
    #     diagonal = grid_game.__get_slots_by_diagonal(p)
    #
    #     grid_game.__get_slots_by_horizontal(Row(p.value()[0]))

    print(grid_game)
