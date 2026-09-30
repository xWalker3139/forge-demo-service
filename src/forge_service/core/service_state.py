from dataclasses import dataclass


@dataclass(slots=True)
class ServiceState:
    _ready: bool = False

    @property
    def ready(self) -> bool:
        return self._ready

    def mark_ready(self) -> None:
        self._ready = True

    def mark_not_ready(self) -> None:
        self._ready = False
