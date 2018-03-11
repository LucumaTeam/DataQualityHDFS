import abc

class TestOperation(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def assert_operation(self,left_side,rigth_side):
        pass