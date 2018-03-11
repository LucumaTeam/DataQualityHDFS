from Metrics import Metric

class MetricColumn(Metric):
    _result = 0

    def __init__(self,column,data_type):
        self._column = column
        self._date_type = data_type

    def evaluate(self,value,metric_context):
        pass

    def get_metric_result(self):
        pass