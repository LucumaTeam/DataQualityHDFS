class Test:

    def __init__(self,threshold,test_representation,test_operation,metric):
        self._threshold = threshold
        self._test_representation = test_representation
        self._test_operation = test_operation
        self._metric = metric

    @property
    def test_representation(self):
        return self._test_representation

    @property
    def test_operation(self):
        return self._test_operation

    @property
    def threshold(self):
        return self._threshold

    @property
    def metric(self):
        return self._threshold

    def assert_test(self):
        pass


