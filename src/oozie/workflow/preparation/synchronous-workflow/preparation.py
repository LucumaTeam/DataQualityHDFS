import pyspark
from pyspark.context import SparkContext
from pyspark.sql import HiveContext,SQLContext,Row
from pyspark.sql.types import IntegerType

channel_id = 'channel_id'
genre_id = 'genre_id'
subgenre_id = 'subgenre_id'
duration = 'duration'
week = 'week'
slot = 'slot'
time = 'time'
user_id = 'user_id'
program_id = 'program_id'
event_id = 'event_id'
TableLanding = 'tv_audience_landing.tv_audience'
TablePreparation= 'tv_audience_preparation.tv_audience'

sc = SparkContext.getOrCreate()

hivec = HiveContext(sc)
sql = SQLContext(sc)
hivec.setConf("hive.exec.dynamic.partition", "true") 
hivec.setConf("hive.exec.dynamic.partition.mode", "nonstrict")

#property1 = 1518366457
#property2 = 1518394387

landing_time = hivec.sql("select time from "+TableLanding+ " group by time order by time desc")

if landing_time.count() > 0:
    landing_time_to_Check = landing_time.first().time
    landing_time_import = hivec.sql("select * from "+TableLanding +" where time="+str(landing_time_to_Check))
    landing_time_import = landing_time_import\
    .withColumn(channel_id, landing_time_import[channel_id].cast(IntegerType()))\
    .withColumn(genre_id, landing_time_import[genre_id].cast(IntegerType()))\
    .withColumn(subgenre_id, landing_time_import[subgenre_id].cast(IntegerType()))\
    .withColumn(duration, landing_time_import[duration].cast(IntegerType()))\
    .withColumn(week, landing_time_import[week].cast(IntegerType()))\
    .withColumn(slot, landing_time_import[slot].cast(IntegerType()))\
    .drop(time)\
    .select(channel_id,genre_id,subgenre_id,user_id,program_id,event_id,duration,week,slot).cache()
    preparation = hivec.sql("select tva.* from "+ TablePreparation +" tva join(select week,slot from "+TableLanding +" where time = "+ str(landing_time_to_Check) +" GROUP BY week,slot) tvp ON tvp.week = tva.week and tvp.slot = tva.slot")
    preparationAppend = preparation.join(landing_time_import,(preparation[week] == landing_time_import[week]) &\
                 (preparation[slot] == landing_time_import[slot]) &\
                 (preparation[channel_id] == landing_time_import[channel_id]) &\
                 (preparation[genre_id] == landing_time_import[genre_id]) &\
                 (preparation[subgenre_id] == landing_time_import[subgenre_id]) &\
                 (preparation[user_id] == landing_time_import[user_id]) &\
                 (preparation[program_id] == landing_time_import[program_id]) &\
                 (preparation[event_id] == landing_time_import[event_id]),"left_outer")\
                .where(landing_time_import[channel_id].isNull())\
                .select(preparation[channel_id],preparation[genre_id],preparation[subgenre_id],preparation[user_id],preparation[program_id],preparation[event_id],preparation[duration],preparation[week],preparation[slot])
    landing_time_insert = landing_time_import.unionAll(preparationAppend)
    landing_time_insert.write.partitionBy(week,slot).insertInto(TablePreparation,"overwrite")