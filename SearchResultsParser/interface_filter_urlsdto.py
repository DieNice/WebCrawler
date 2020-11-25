from abc import ABC, abstractmethod

from .urlsdto import UrlsDTO


class InterfaceFilterUrlsDTO(ABC):
    @abstractmethod
    def filtering(self, data: UrlsDTO) -> UrlsDTO:
        pass
