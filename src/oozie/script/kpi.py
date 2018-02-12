import pyspark
from pyspark.context import SparkContext
from pyspark.sql import HiveContext,SQLContext,Row
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import lit

channel_id = 'channel_id'
duration = 'duration'
week = 'week'
slot = 'slot'
program_id = 'program_id'
kpi_id ='kpi_id'
value ='value'
table_preparation = 'tv_audience_preparation.tv_audience'
table_kpi = 'tv_audience_kpi.kpi_by_ch_pr_we_sl'

sc = SparkContext.getOrCreate()

hivec = HiveContext(sc)
sql = SQLContext(sc)
hivec.setConf("hive.exec.dynamic.partition", "true") 
hivec.setConf("hive.exec.dynamic.partition.mode", "nonstrict")

preparation = hivec.sql("select * from "+table_preparation)
kpi = preparation.groupBy(week,slot,channel_id,program_id)\
    .sum(duration)\
    .withColumnRenamed("SUM(duration)", value)\
    .withColumn(kpi_id,lit(1))\
    .select(channel_id,program_id,kpi_id,value,week,slot)
kpi.write.partitionBy(week,slot).insertInto(table_kpi,"overwrite")
