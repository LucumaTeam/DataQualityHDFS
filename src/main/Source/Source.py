import abc

class Source(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def retrieve_dataset(self):
        pass


