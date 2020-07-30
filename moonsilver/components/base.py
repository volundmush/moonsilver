from dataclasses import dataclass


@dataclass
class BaseComponent:
    app = None
    component_key = None

    dirty: bool = False

    def export(self):
        pass
