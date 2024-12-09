from enum import Enum

class Emotions(Enum):
    ANGRY = "angry"
    CONTEMPT = "contempt"
    DISGUST = "disgust"
    FEAR = "fear"
    HAPPY = "happy"
    NEUTRAL = "neutral"
    SAD = "sad"
    SURPRISE = "surprise"

    @classmethod
    def from_index(cls, index):
        emotions = list(cls)
        if 0 <= index < len(emotions):
            return emotions[index]
        raise ValueError(f"Invalid emotion index: {index}")