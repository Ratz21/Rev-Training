from pyspark.sql import SparkSession

import sys
import os
os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-21"
os.environ["SPARK_HOME"] = "D:\Revature-Training\Spark_Project\spark\.venv\Lib\site-packages\pyspark"
os.environ["HADOOP_HOME"]= "C:\hadoop"
os.environ['PYSPARK_PYTHON'] = sys.executable

os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder \
    .appName("Local PySpark") \
    .getOrCreate()

#Get SparkContext
sc = spark.sparkContext

# numbers = [1,2,3,4,5]
# rdd = sc.parallelize(numbers)
# print("Original RDD: ", rdd.collect())
#
# #Transformations
# doubled = rdd.map(lambda x: x * 2)
# print('type : ', type(doubled))
# print("Doubled: ", doubled.collect())
#
# even_num= rdd.filter(lambda x: x%2==0)
# print('type : ', type(even_num))
# print("Even num: ", even_num.collect())
#
# total = rdd.reduce(lambda x, y: x + y)
# print('type : ', type(total))
# print("Total Sum: ", total)



#rdd transformation sc is spark context object created above

data = [("a",1), ("b", 2),("c",3)] # we can also reverse this 1,a 2,b
pairRDD = sc.parallelize(data)
print('Original:', pairRDD.collect())

sumByKey = pairRDD.reduceByKey(lambda x,y: x+y) #if the key is the same it will start adding
print(sumByKey.collect())

sumByKey = pairRDD.reduceByKey(lambda x, y: x+y)
print('Reduced:' ,sumByKey.collect())

#lazy evaluation action -> triggers collect reduced count and transformation -> map filter flatmap
