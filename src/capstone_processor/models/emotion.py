from enum import Enum

class Emotions(Enum):
    ANGRY = "angry"
    DISGUST = "disgust"
    FEAR = "fear"
    HAPPY = "happy"
    SAD = "sad"
    SURPRISE = "surprise"
    NEUTRAL = "neutral"

    @classmethod
    def from_index(cls, index):
        emotions = list(cls)
        if 0 <= index < len(emotions):
            return emotions[index]
        raise ValueError(f"Invalid emotion index: {index}")