from Core import Column
from Core import Table
from Core import Interface
from Core.Granularity import GranularityTemporal
from Core.Granularity import GranularityTimeInterval
from Core.Enum_Type import Enum_Type
from Metrics import MetricColumn
from Metrics.MetricExpressions import MetricExpressionNullValue
from Test import Test
from Test.TestOperations import TestOperationMayor
from Test.TestRepresentations import TestRepresentationPercentage
from Test.TestService import TestService
from Source.SourceBBDD import SourceHIVE
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

source = SourceHIVE("select * from TablePreparation")

table = Table(granularity,columns,None,[test_column_metric],source,None)

interface = Interface([granularity],[Table(granularity,columns,None,None,None)])

metric_service = MetricService()
test_service = TestService()

metric_service.evaluate_metrics(interface)
test_service.assert_tests(interface)
