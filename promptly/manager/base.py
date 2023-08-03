from abc import abstractmethod, ABC

from promptly.model.profile import History

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
    def list_profile(self):
        pass

    @abstractmethod
    def get_profile(self, key):
        pass

    @abstractmethod
    def push_history(self, item: History):
        pass
