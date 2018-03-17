
import os
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import HiveContext,SQLContext,Row
from pyspark.sql.types import IntegerType



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
from dataqualityhdfs.source.sourcebbdd.sourcehive import SourceHIVE
from dataqualityhdfs.test.test import Test
from dataqualityhdfs.test.testoperations.testoperationmayor import TestOperationMayor
from dataqualityhdfs.test.testoperations.testoperationminor import TestOperationMinor
from dataqualityhdfs.test.testrepresentations.testrepresentationpercentage import TestRepresentationPercentage
from dataqualityhdfs.test.testservice import TestService

TableLanding = 'tv_audience_landing.tv_audience'
TablePreparation= 'tv_audience_preparation.tv_audience'

sc = SparkContext.getOrCreate()

hivec = HiveContext(sc)
sql = SQLContext(sc)

landing_time = hivec.sql("select time from "+TableLanding+ " group by time order by time desc")

if landing_time.count() > 0:
    
    landing_time_to_Check = landing_time.first().time

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

    source = SourceHIVE("select * from "+TableLanding +" where time="+str(landing_time_to_Check))

    #source = SourceCSV("/tfm/tv-audience/landing/tv_audience/time=1518980865/","tv_audience.csv",',',False, ['channel_id', 'slot','week','genre_id','duration','subgenre_id','user_id','program_id','event_id'])

    table = Table(granularity,columns,None,[test_column_metric],source,None)

    interface = Interface([granularity],[table])

    metric_service = MetricService()
    test_service = TestService()

    metric_service.evaluate_metrics(interface)
    test_service.assert_tests(interface)

    print(test_column_metric.test_result)

