import sys
import os

from pyspark.sql import SparkSession

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# --- environment (use correct upper-case names and raw strings) ---
os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-21"
os.environ["SPARK_HOME"] = r"C:\Users\chris\Downloads\C downloads\spark-3.5.7-bin-hadoop3"
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# add spark bin to PATH so Spark can find its scripts (optional but helpful)
os.environ["PATH"] = os.path.join(os.environ["SPARK_HOME"], "bin") + ";" + os.environ.get("PATH", "")

# --- create SparkSession properly (case-sensitive) ---
spark = SparkSession.builder \
    .appName("local-pyspark") \
    .master("local[*]") \
    .getOrCreate()

# --- schema and data (StructType, not StringType([...])) ---
schema = StructType([
    StructField("Name", StringType(), True),
    StructField("Age", IntegerType(), True)
])

data = [("Alice", 25), ("Bob", 30)]

df = spark.createDataFrame(data, schema)
df.printSchema()
df.show()

spark.stop()
