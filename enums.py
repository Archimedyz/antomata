from enum import Enum, StrEnum, IntEnum, auto

class Direction4(IntEnum):
    UP=0
    RIGHT=1
    DOWN=2
    LEFT=3

class Mode(Enum):
    RUNNING = auto(),
    STEP_THRU = auto(),
    CONFIG = auto()

class GridColor(StrEnum):
    LIGHT="white"
    DARK="gray16"
