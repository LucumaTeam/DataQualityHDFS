import abc

class Source(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def Load(self):
        pass

