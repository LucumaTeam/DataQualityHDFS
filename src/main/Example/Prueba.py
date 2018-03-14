import os
import sys
import pyspark
from pyspark.sql import HiveContext,SQLContext,Row
from pyspark.context import SparkContext


print(os.path.join("c:/", "tv_audience.csv"))

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

print("hola")
rdd = sc.textFile("c:/tv_audience.csv").map(lambda line: line.split(","))

x = ['channel_id', 'slot','week','genre_id','duration','subgenre_id','user_id','program_id','event_id']


Person = Row(x)#Row('channel_id', 'slot','week','genre_id','duration','subgenre_id','user_id','program_id','event_id')
person = rdd.map(lambda r: Person(*r))
df2 = sqlContext.createDataFrame(rdd,x)
df2.collect()
print(df2.take(1))
