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
hdfs_location=args.h
from PIL import Image, ImageDraw
#from tensorflow.python.keras.applications.resnet50 import ResNet50
from pyspark.sql import SparkSession
from pyspark.ml.image import ImageSchema
import pyspark
from pyspark.sql.functions import lit
spark = SparkSession.builder \
    .appName('test_load_model') \
    .master(args.s) \
    .config('spark.executor.instances', args.i) \
    .config('spark.sql.execution.arrow.pyspark.enabled', True) \
    .config('spark.executor.core', '2') \
    .config('spark.executor.memory', args.m) \
    .config('spark.ui.showConsoleProgress',True) \
    .getOrCreate()
sc = spark.sparkContext
sc
testDF = ImageSchema.readImages(hdfs_location+"/test/").withColumn("label", lit(0))

from sparkdl.image import imageIO as imageIO
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from pyspark.ml import Pipeline, PipelineModel
from sparkdl import DeepImageFeaturizer
from pyspark.sql.functions import regexp_replace
#load from hdfs 
#models in hdfs://HDFS_SITE/train/lr
lr_test = LogisticRegressionModel.load(hdfs_location+'/train/lr/')
featurizer_test = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")

p_lr_test = PipelineModel(stages=[featurizer_test, lr_test])
tested_lr_test = p_lr_test.transform(testDF)

evaluator_lr_test = MulticlassClassificationEvaluator(metricName="accuracy")
#print("accuracy", str(tested_lr_test.select("prediction", "label").show()))
#df = tested_lr_test.withColumn('prediction', when(tested_lr_test.prediction=='0', "JENNIE").when(tested_lr_test.prediction='1', "JISOO").when(tested_lr_test.prediction=='2', "LISA").when(tested_lr_test.prediction=='3', "ROSE").otherwise(tested_lr_test.prediction))
#tested_lr_test.withColumn('image', regexp_replace('image', 'hdfs://localhost:9000/test/', ''))
df1 = tested_lr_test.filter(tested_lr_test.prediction=='0.0')
df2 = tested_lr_test.filter(tested_lr_test.prediction=='1.0')
df3 = tested_lr_test.filter(tested_lr_test.prediction=='2.0')
df4 = tested_lr_test.filter(tested_lr_test.prediction=='3.0')

df1 = df1.withColumn('prediction', regexp_replace('prediction', '0.0', 'JENNIE'))
df2 = df2.withColumn('prediction', regexp_replace('prediction', '1.0', 'JISOO'))
df3 = df3.withColumn('prediction', regexp_replace('prediction', '2.0', 'LISA'))
df4 = df4.withColumn('prediction', regexp_replace('prediction', '3.0', 'ROSE'))
print('JENNIE Prediction')
df1.select('image', 'prediction').show()
print('JISOO Prediction')
df2.select('image', 'prediction').show()
print('LISA Prediction')
df3.select('image', 'prediction').show()
print('ROSE Prediction')
df4.select('image', 'prediction').show()
