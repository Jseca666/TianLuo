from abc import ABC, abstractmethod

from .export_models import ExportedTaskModel


class BaseTaskExporter(ABC):
    @abstractmethod
    def export(self) -> ExportedTaskModel:
        raise NotImplementedError
