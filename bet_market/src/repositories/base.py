from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @classmethod
    @abstractmethod
    def get_all(cls):
        pass

    @classmethod
    @abstractmethod
    def get_by_id(cls, id):
        pass

    @classmethod
    @abstractmethod
    def create(cls, data):
        pass
