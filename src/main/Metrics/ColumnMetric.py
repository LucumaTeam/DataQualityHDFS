from Metrics import Metric

class ColumnMetric(Metric):
    _result = 0
    _

    def __init__(self,column,data_type):
        self._column = column
        self._date_type = data_type

    def evaluate(self):
        pass