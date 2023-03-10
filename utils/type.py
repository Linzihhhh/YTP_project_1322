from __future__ import annotations
from enum import Enum, IntEnum, auto
from typing import *

class EmotionType(IntEnum):
    HAPPY = 0
    HUMOROUS = 0
    RELAX = 1
    SORROW = 2
    TRAGIC = 2
    DEPRESS = 2
    HEAVY = 5
    EXCITING = 0
    NERVOUS = 3
    RAGE = 4
    AMBITIOUS = 6

    def __str__(self):
        return self.name

    @classmethod
    def from_classes(cls, num: int) -> EmotionType:
        classes = [0, 0, 1, 2, 2, 2, 5, 0, 3, 4, 6]
        return cls(classes[num - 1])