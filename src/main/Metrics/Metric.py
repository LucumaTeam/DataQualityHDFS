import abc

class Metric(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def evaluate(self):
        pass
