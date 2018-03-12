import abc

class MetricResult(metaclass=abc.ABCMeta):


    def __init__(self,count):
        self._count = count

    @property
    def count(self):
        return self._count