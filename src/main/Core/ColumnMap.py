class ColumnMap:

    def __init__(self,name,schema_map,metric_map):
        self._name = name
        self._schema_map = schema_map
        self.metric_map = metric_map
