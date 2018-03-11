class Table:

    def __init__(self,granularity,columns,metric,source):
        self._granularity = granularity
        self._columns = columns
        self._metric = metric
        self._source = source

    @property
    def granularity(self):
        return self._granularity

    @property
    def columns(self):
        return self._columns

    @property
    def metric(self):
        return self._metric

    @property
    def dataset(self):
        return self._dataset

    @property
    def source(self):
        return self._source


