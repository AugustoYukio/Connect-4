from abc import ABC, abstractmethod, ABCMeta
from typing import Type, List


class IStatusPosition(object):
    EMPTY = 'EMPTY'
    FULL = 'FULL'


class IPosition(ABC):
    __x: int = 0
    __y: int = 0
    __status: IStatusPosition = IStatusPosition.EMPTY
    __position_value = (__x, __y)

    @property
    @abstractmethod
    def status(self):
        ...

    @status.setter
    @abstractmethod
    def status(self, status: IStatusPosition):
        ...

    @abstractmethod
    def value(self):
        ...


class IBoard(ABC):
    ...


class IPlayerCheker(ABC):
    __number: str

    @property
    @abstractmethod
    def number(self):
        ...


class ISlot(ABC):
    position: IPosition
    player_cheker: IPlayerCheker

    @abstractmethod
    def position(self):
        ...

    @abstractmethod
    def occupy_with_player_piece(self, player_cheker: IPlayerCheker):
        ...

    # @abstractmethod
    # def set_position(self, value):
    #     raise NotImplementedError


class IGridPart(ABC):
    number: int


class IColumn(IGridPart):
    ...


class IRow(IGridPart):
    ...


class IGrid(ABC):
    COLUMNS: int
    ROWS: int
    slots: List[List[ISlot]]

    @abstractmethod
    def __make_grid(self):
        ...


class IBoard(ABC):
    name: str
    background: str
    grid: IGrid

    @property
    @abstractmethod
    def background(self):
        ...

    @background.setter
    @abstractmethod
    def background(self, value):
        ...


if __name__ == '__main__':
    print('asdasd')
