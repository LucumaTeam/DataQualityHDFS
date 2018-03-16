from dataqualityhdfs.metrics.metriccolumn import MetricColumn
from dataqualityhdfs.metrics.metricservice import MetricService
from dataqualityhdfs.core.column import Column
from dataqualityhdfs.core.enum_type import Enum_Type
from dataqualityhdfs.core.granularity.granularitytemporal import GranularityTemporal
from dataqualityhdfs.core.granularity.granularitytimeinterval import GranularityTimeInterval
from dataqualityhdfs.core.interface import Interface
from dataqualityhdfs.core.table import Table
from dataqualityhdfs.metrics.metricexpressions import MetricExpressionNullValue
from dataqualityhdfs.source.sourcefile import SourceCSV
from dataqualityhdfs.test.test import Test
from dataqualityhdfs.test.testoperations.testoperationmayor import TestOperationMayor
from dataqualityhdfs.test.testrepresentations.testrepresentationpercentage import TestRepresentationPercentage
from dataqualityhdfs.test.testservice import TestService

column_metric_program = MetricExpressionNullValue(MetricColumn())

test_column_metric = Test(15,TestRepresentationPercentage(),TestOperationMayor(),column_metric_program)

columns = [Column('channel_id',Enum_Type.STRING,None),
          Column('slot',Enum_Type.STRING,None),
          Column('week',Enum_Type.STRING,None),
          Column('genre_id',Enum_Type.STRING,None),
          Column('duration',Enum_Type.STRING,None),
          Column('subgenre_id',Enum_Type.STRING,None),
          Column('user_id',Enum_Type.STRING,None),
          Column('program_id',Enum_Type.STRING,column_metric_program),
          Column('event_id',Enum_Type.STRING,None)
          ]

granularity = GranularityTemporal(2018,3,0,11,None,None,None,GranularityTimeInterval.DAY)

#source = SourceHIVE('select * from tv_audience_preparation.tv_audience')

source = SourceCSV("c:/","tv_audience.csv",',',False, ['channel_id', 'slot','week','genre_id','duration','subgenre_id','user_id','program_id','event_id'])

table = Table(granularity,columns,None,[test_column_metric],source,None)

interface = Interface([granularity],[table])

metric_service = MetricService()
test_service = TestService()

metric_service.evaluate_metrics(interface)
test_service.assert_tests(interface)

print(test_column_metric.test_result)
