import os
import sys
import pyspark
from pyspark.sql import HiveContext,SQLContext,Row
from pyspark.context import SparkContext

spark = pyspark.sql.SparkSession.builder.appName('test').getOrCreate()

spark.range(10).collect()