from Metrics import MetricExpression


class NullValueMetricExpression(MetricExpression):
    """
    Add responsibilities to the component.
    """

    def operation(self):
        # ...
        self._component.operation()
        # ...