import abc

class Granularity(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_granularity(self):
        pass