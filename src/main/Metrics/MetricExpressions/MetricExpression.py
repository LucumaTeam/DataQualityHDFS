import abc
from Metrics import Metric

class MetricExpression(Metric, metaclass=abc.ABCMeta):

    def __init__(self, metric):
        self._metric = metric

    @abc.abstractmethod
    def evaluate(self):
        pass