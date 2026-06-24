from dataclasses import dataclass

from model.state import State


@dataclass
class Arco:
    id1: State
    id2: State
    peso: int