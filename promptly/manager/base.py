from abc import abstractmethod, ABC


class BaseProfileManager(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def list_profile(self):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def push_history(self, item: History):
        pass