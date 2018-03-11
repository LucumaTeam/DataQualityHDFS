class Interface:

    def __init__(self,granularities,tables):
        self._granularity = granularities
        self._table= tables

    @property
    def granularities(self):
        return self._granularities

    @property
    def tables(self):
        return self._tables

