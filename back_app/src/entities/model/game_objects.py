from __future__ import annotations

import secrets
from random import randint
from dataclasses import dataclass
from enum import Enum
from typing import List, Type, Tuple
from ..Interfaces.game_pieces import (
    IPosition, ISlot, IGrid, IPlayerChecker, IBoard, IRow, IColumn, IScore, IPlayer, IGame, IStatusGame,
    IStatusPosition)


THE_PRINCIPAL_NUMBER = 4


class StatusPosition(IStatusPosition, Enum):
    EMPTY = 'EMPTY'
    FULL = 'FULL'


#   class StatusPosition(IStatusPosition):

#   @classmethod
#   def __missing__(cls, key):
#   return super().EMPTY


class Position(IPosition):

    def __init__(self, x: int, y: int) -> Type[IPosition]:
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

    @property
    def row(self):
        return Row(self.__x)

    @property
    def column(self) -> IColumn:
        return Column(self.__y)

    @property
    def value(self):
        return self.__position_value


@dataclass
class PlayerChecker(IPlayerChecker):
    def __init__(self, number: str):
        super(PlayerChecker, self).__init__()
        self.__number = number

    @property
    def number(self):
        return str(self.__number)

    def __repr__(self):
        return f"PlayerChecker: <number={self.number}>"


class Slot(ISlot):
    player_checker: Type[IPlayerChecker] = None

    def __init__(self, position: Type[IPosition]):
        super(Slot, self).__init__()
        self.position = position

    def position(self):
        return self.position.value

    def __repr__(self):
        __repr = f'Slot: {self.position:}'
        if self.position.status == StatusPosition.FULL:
            __repr += f", {self.player_checker:}"
        return __repr

    def occupy_with_player_piece(self, player_checker: Type[IPlayerChecker]):
        self.player_checker = player_checker
        self.position.status = StatusPosition.FULL


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
        self.slots = self._make_grid()

    def __repr__(self):
        full_representation = []
        count = 10
        cell = "{" + f':^{count}' + "}"
        for n, rows in enumerate(reversed(self.slots), 0):
            index_row = self.ROWS - n - 1
            space = r'{:^3}'.format(index_row)
            base_f = f"{space}|{f'{cell}|' * self.COLUMNS}"
            # print(f"{index_row} -> {[slot for slot in rows]}")
            full_representation.append(
                base_f.format(
                    *[
                        slot.position.status.value if slot.position.status == StatusPosition.EMPTY
                        else f'Player {slot.player_checker._id_}' for slot in rows
                    ]
                )
            )
        space = ' ' * 3
        base_f = f"{space}|{f'{cell}|' * self.COLUMNS}"
        full_representation.append(base_f.format(*[str(slot) for slot in range(self.COLUMNS)]))
        return '\n'.join(full_representation)

    def _make_grid(self) -> List[List[ISlot]]:
        return [[Slot(Position(row, col)) for col in range(self.COLUMNS)] for row in range(self.ROWS)]

    def __get_slots_by_diagonal_1(self, position: Type[IPosition]) -> List[ISlot] | None:
        """Inferior esquerdo para superior direito."""
        BOTTOM_END_OF_ROWS, BOTTOM_END_OF_COLUMNS = 0, 0

        inferior_x, inferior_y = position.value

        if inferior_y >= inferior_x:
            inferior_y -= inferior_x
            inferior_x = BOTTOM_END_OF_ROWS
        else:
            inferior_x -= inferior_y
            inferior_y = BOTTOM_END_OF_COLUMNS

        superior_x, superior_y = position.value

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

        # print(f'Limite Superior: {(superior_x, superior_y,)}')
        # print(f'Posição Inserida: {(position.value)}')
        # print(f'Limite Inferior: {(inferior_x, inferior_y,)}')
        # print(grid_game)

        # print(list(range(inferior_x, superior_x + 1)))
        # print(list(range(inferior_y, superior_y + 1)))
        # list(zip(range(inferior_x, superior_x + 1), range(inferior_y, superior_y + 1)))
        #         [self.slots[p_x][p_y].player_checker for p_x, p_y in
        #          zip(range(inferior_x, superior_x + 1), range(inferior_y, superior_y + 1)) if
        #          self.slots[p_x][p_y].position.status == StatusPosition.FULL]
        rows_for_diagonal = zip(range(inferior_x, superior_x + 1), range(inferior_y, superior_y + 1))
        return [self.slots[p_x][p_y] for p_x, p_y in rows_for_diagonal]

    def __get_slots_by_horizontal(self, row: Row):
        return self.slots[row.number]

    def __get_slots_by_vertical(self, column: Type[IColumn]):
        return [row[column.number] for row in self.slots]

    def get_all_directions_slots(self, position: Type[IPosition]) -> List[List[ISlot]]:
        # print(position)
        results = [func(parameter) for (func, parameter) in zip(
            (self.__get_slots_by_diagonal_1, self.__get_slots_by_vertical, self.__get_slots_by_horizontal),
            (position, position.column, position.row))
                   ]

        return results

    def __get_free_slot_by_column(self, column: Type[IColumn]) -> ISlot | None:
        for slot in self.__get_slots_by_vertical(column):
            if slot.position.status == StatusPosition.EMPTY:
                return slot
        return None

    def put_checker_in_slot(self, player_checker: Type[IPlayerChecker], column: Type[IColumn]) -> IPosition | None:
        slot = self.__get_free_slot_by_column(column)
        if not slot:
            return slot
        slot.occupy_with_player_piece(player_checker)
        return slot.position


@dataclass(repr=False)
class Score(IScore):
    def switch_player_for_new_game(self):
        self._first_player_points, self._second_player_points = self._second_player_points, self._first_player_points

    def __repr__(self):
        return f"Score <First_Player={self._first_player_points}, Second_Player={self._second_player_points}>"

    def add_victory(self, player='first_player'):
        if player == 'first_player':
            self._first_player_points += 1
        else:
            self._second_player_points += 1


class Board(IBoard):
    grid = Grid()
    checker_on_turn: IPlayerChecker
    last_position_valid_mov: Type[IPosition]

    def insert_in_column(self, column: Type[IColumn]):
        self.last_position_valid_mov = self.grid.put_checker_in_slot(self.checker_on_turn, column)

    def check_winner_condition(self):
        all_directions_slots = self.grid.get_all_directions_slots(self.last_position_valid_mov)
        return all_directions_slots

    def set_player_checker_for_turn(self, player_checker: Type[IPlayerChecker]):
        self.checker_on_turn = player_checker


@dataclass
class Player(IPlayer):
    _id_: str

    def __repr__(self):
        return f'Player <ID: {self._id_}>'


class StatusGame(IStatusGame, Enum):
    RUNNING = 'RUNNING'
    WAITING = 'WAITING'
    STOPPED = 'STOPPED'


def __is_connected_for_4(rows: List[ISlot]) -> Tuple[bool, List[Type[ISlot]]]:
    # TODO: Tornar função agnóstica em relação ao jogador

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


@dataclass
class Game(IGame):
    __player_2 = None
    __movements = 0
    __player_in_turn: Type[IPlayer]

    def __init__(self, player_1: Type[IPlayer]):
        self.__player_1 = player_1
        self.__board = Board()
        self.__status_game = StatusGame('STOPPED')
        self.__score = Score()

    def __random_order_for_first_game(self):
        self.__player_in_turn = [self.__player_1, self.__player_2][randint(0, 1)]

    def second_player_initialize(self, player_id: str):
        self.__player_2 = Player(player_id)
        self.__random_order_for_first_game()
        # self.status_game = StatusGame.RUNNING

    def move(self, column_number: int):
        self.__board.set_player_checker_for_turn(self.__player_in_turn)
        self.__board.do_movement(Column(column_number))

    def __status_init_game(self) -> bool:
        if self.__player_2 is None:
            self.__status_game = StatusGame.WAITING
            return False
        return True

    def start(self):
        if self.__status_init_game():
            self.__status_game = StatusGame.RUNNING
            self.__random_order_for_first_game()
        else:
            self.__status_game = StatusGame.WAITING

    def __new_game(self):
        if not self.__status_init_game():
            self.__status_game = StatusGame.STOPPED
        else:
            ...

    def get_current_player(self):
        return self.__player_in_turn

    def set_player_for_current_turn(self, player: Type[IPlayer]):
        self.__player_in_turn = player


@dataclass
class GameRoom:
    game: Type[IGame]

    def __init__(self, player_id: str):
        self.game = Game(Player(player_id))

    def start_new_game(self, player_id: str):
        self.game.second_player_initialize(player_id)

    def do_movement(self, move):
        self.game.move(move)


# Driver Code
if __name__ == "__main__":
    game_room = GameRoom(secrets.token_urlsafe(5))
    game_room.start_new_game(secrets.token_urlsafe(5))
    game_room.do_movement(4)
    # grid = Grid()
    # grid.put_checker_in_slot(Player(2), Column(3))
    # print(grid)
    # p1 = Player(secrets.token_urlsafe(5))
    # game = Game(p1)

    # game.second_player_initialize(secrets.token_urlsafe(5))
    # game.start()
    # game.set_player_for_current_turn()
    # game.move(3)
