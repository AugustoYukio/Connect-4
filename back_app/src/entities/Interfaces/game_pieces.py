from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Type


class IStatusPosition(Enum):
    pass
    # def _generate_next_value_(name, start, count, last_values):
    # return name


class IGridPart(ABC):
    number: int


class IColumn(IGridPart):
    ...


class IRow(IGridPart):
    ...


class IPosition(ABC):
    __x: int
    __y: int

    __status: IStatusPosition
    __position_value: tuple

    @property
    @abstractmethod
    def status(self):
        ...

    @status.setter
    @abstractmethod
    def status(self, status: Type[IStatusPosition]):
        ...

    @abstractmethod
    def value(self):
        ...

    @abstractmethod
    def column(self) -> Type[IColumn]:
        ...

    @abstractmethod
    def row(self) -> Type[IRow]:
        ...


class IPlayerChecker(ABC):
    __number: str

    @property
    @abstractmethod
    def number(self):
        ...


class ISlot(ABC):
    position: IPosition
    player_cheker: Type[IPlayerChecker]

    @abstractmethod
    def position(self):
        ...

    @abstractmethod
    def occupy_with_player_piece(self, player_cheker: Type[IPlayerChecker]):
        ...

    # @abstractmethod
    # def set_position(self, value):
    #     raise NotImplementedError


class IScore(ABC):
    _first_player_points = 0
    _second_player_points = 0

    @abstractmethod
    def add_victory(self) -> None:
        ...


class IGrid(ABC):
    COLUMNS: int
    ROWS: int
    slots: List[List[ISlot]]

    @abstractmethod
    def _make_grid(self) -> List[List[ISlot]]:
        ...


class IPlayer(ABC):
    number: int


class IBoard(ABC):
    score: Type[IScore]
    grid: Type[IGrid]


class IStatusGame(Enum):
    ...


class IGame(ABC):
    status = IStatusGame
    board: IBoard
    player_1: IPlayer
    player_2: IPlayer | None
    player_in_turn: IPlayer | None
