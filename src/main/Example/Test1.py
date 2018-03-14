from Core import Column
from Core import Table
from Core import Interface
from Core.Granularity import GranularityTemporal
from Core.Granularity.GranularityTimeInterval import GranularityTimeInterval
from Core.Enum_Type import Enum_Type
from Metrics import MetricColumn
from Metrics.MetricExpressions import MetricExpressionNullValue
from Test import Test
from Test.TestOperations import TestOperationMayor
from Test.TestOperations import TestOperationMinor
from Test.TestRepresentations import TestRepresentationPercentage
from Test.TestService import TestService
from Source.SourceBBDD import SourceHIVE
from Source.SourceFile import SourceCSV
from Metrics import MetricService

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