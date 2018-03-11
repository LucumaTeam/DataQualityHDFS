import abc

class TestRepresentation(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_value(self, metric_result):
        pass