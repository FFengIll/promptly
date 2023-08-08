from abc import abstractmethod, ABC

from promptly.model.profile import Snapshot

class BaseCaseManager(ABC):
    pass

class BaseProfileManager(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def reload(self):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def get(self, key):
        pass

  