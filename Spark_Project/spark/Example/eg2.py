import sys
import os
os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-21"
os.environ["SPARK_HOME"] = "D:\Revature-Training\Spark_Project\spark\.venv\Lib\site-packages\pyspark"
os.environ["HADOOP_HOME"]= "C:\hadoop"
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Local PySpark").getOrCreate()

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

myschema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

df = spark.read.option("multiline","true").json("../data/file1.json", schema=myschema)

df.cache()

df_cleaned = df.filter("name is not null and age is not null")
df_cleaned.show()

df.show()
df.printSchema()

df.createOrReplaceTempView("people")
spark.sql("select * from people where age > 25").show()

# ⭐ FIX: overwrite mode
df.write.mode("overwrite").json("../data/out1.json")