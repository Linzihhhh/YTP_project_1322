from __future__ import annotations
from enum import Enum, IntEnum, auto
from typing import *

class EmotionType(IntEnum):
    
    HIGH_AROUSAL_HIGH_VALENCE = 0
    LOW_AROUSAL_HIGH_VALENCE = 1
    LOW_AROUSAL_LOW_VALENCE = 2
    HIGH_AROUSAL_LOW_VALENCE = 3

    def __str__(self) -> str:

        match self.value:
            case 0:
                return "Happy"
            case 1:
                return "Calm"
            case 2:
                return "Sad"
            case 3:
                return "Angry"
            case _:
                raise Exception("Emotion Type not found!")

    @classmethod
    def from_name(cls, name) -> EmotionType:

        match name:
            case "Happy":
                return cls.HIGH_AROUSAL_HIGH_VALENCE
            case "Calm":
                return cls.LOW_AROUSAL_HIGH_VALENCE
            case "Sad":
                return cls.LOW_AROUSAL_LOW_VALENCE
            case "Angry":
                return cls.HIGH_AROUSAL_LOW_VALENCE
            case _:
                raise Exception("Emotion Type not found!")