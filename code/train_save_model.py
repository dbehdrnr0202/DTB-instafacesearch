import os
import argparse

SUBMIT_ARGS = "--packages databricks:spark-deep-learning:1.0.0-spark2.3-s_2.11 pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS

parser = argparse.ArgumentParser(description='arguments -i instance_number -m instance_memory -s spark_master -h hdfs_save_location')
parser.add_argument('-i', type=int, default=1)
parser.add_argument('-m', default='4G')
parser.add_argument('-s', default='spark://master:7077')
parser.add_argument('-h', default='hdfs://master:9000')
args = parser.parse_args()

print('build spark session with:\n')
print('\tinstance number: ', args.i)
print('\tinstance memory: ', args.m)
print('\tspark master: ', args.s)
print('\thdfs model save location: ', args.h)
hdfs_location = args.h
from PIL import Image, ImageDraw
#from tensorflow.python.keras.applications.resnet50 import ResNet50
from pyspark.sql import SparkSession
from pyspark.ml.image import ImageSchema
import pyspark
from pyspark.sql.functions import lit
spark = SparkSession.builder \
    .appName("train_save_model") \
    .master(args.s) \
    .config('spark.executor.instances', args.i) \
    .config('spark.sql.execution.arrow.pyspark.enabled', True) \
    .config('spark.executor.core', '2') \
    .config('spark.executor.memory', args.m) \
    .config('spark.ui.showConsoleProgress',True) \
    .getOrCreate()
sc = spark.sparkContext
sc
# hdfs read
jennie_image_df = ImageSchema.readImages(hdfs_location+"/train/JENNIE_2/").withColumn("label", lit(0))
jisoo_image_df = ImageSchema.readImages(hdfs_location+"/train/JISOO_2/").withColumn("label", lit(1))
lisa_image_df = ImageSchema.readImages(hdfs_location+"/train/LISA_2/").withColumn("label", lit(2))
rose_image_df = ImageSchema.readImages(hdfs_location+"/train/ROSE_2/").withColumn("label", lit(3))

'''
local read
jennie_image_df = ImageSchema.readImages("/home/test/project/JENNIE_2/").withColumn("label", lit(0))
jisoo_image_df = ImageSchema.readImages("/home/test/project/JISOO_2/").withColumn("label", lit(1))
lisa_image_df = ImageSchema.readImages("/home/test/project/LISA_2/").withColumn("label", lit(2))
rose_image_df = ImageSchema.readImages("/home/test/project/ROSE_2/").withColumn("label", lit(3))
'''
jennie_train, jennie_test = jennie_image_df.randomSplit([80.00, 20.00], seed = 12)
jisoo_train, jisoo_test = jisoo_image_df.randomSplit([80.00, 20.00], seed = 12)
lisa_train, lisa_test = lisa_image_df.randomSplit([80.00, 20.00], seed = 12)
rose_train, rose_test = rose_image_df.randomSplit([80.00, 20.00], seed = 12)

x1_df = jennie_train.unionAll(jisoo_train)
x2_df = lisa_train.unionAll(rose_train)
train_df = x1_df.unionAll(x2_df)

y1_df = jennie_test.unionAll(jisoo_test)
y2_df = lisa_test.unionAll(rose_test)
test_df = y1_df.unionAll(y2_df)


train_df = train_df.repartition(100)
test_df = test_df.repartition(100)

from sparkdl.image import imageIO as imageIO
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from sparkdl import DeepImageFeaturizer

featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
lr = LogisticRegression(maxIter=20, regParam=0.05, elasticNetParam=0.3, labelCol="label", featuresCol="features")
#pipeline 1: featurizer(fitting model)
#pipeline 2: save model
p = Pipeline(stages=[featurizer, lr])
p_model = p.fit(train_df)

from pyspark.ml.evaluation import MulticlassClassificationEvaluator
tested_df = p_model.transform(test_df)
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print("test set accuracy:"+str(evaluator.evaluate(tested_df.select("prediction", "label"))))

#saving the model
lr_model = p_model
lr_model.stages[1].write().overwrite().save(hdfs_location+"/train/lr")

#df = model.transform(train_images_df)
