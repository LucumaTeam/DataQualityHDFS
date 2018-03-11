import abc

class Metric(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def evaluate(self,value,metric_context):
        pass

    @abc.abstractmethod
    def get_metric_result(self):
        pass
