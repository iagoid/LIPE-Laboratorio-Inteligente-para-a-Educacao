from dataclasses import dataclass

@dataclass
class Dialog:
    Text: str
    Character_Dir: str
    Italic: bool = False
    Bold: bool = False
