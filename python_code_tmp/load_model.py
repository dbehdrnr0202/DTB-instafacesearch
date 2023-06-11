import os
SUBMIT_ARGS = "--packages databricks:spark-deep-learning:1.0.0-spark2.3-s_2.11 pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS

from PIL import Image, ImageDraw
#from tensorflow.python.keras.applications.resnet50 import ResNet50
from pyspark.sql import SparkSession
from pyspark.ml.image import ImageSchema
import pyspark
from pyspark.sql.functions import lit
spark = SparkSession.builder \
    .appName("dltest") \
    .master("spark://nn1:7077") \
    .config('spark.executor.instances', 2) \
    .config('spark.sql.execution.arrow.pyspark.enabled', True) \
    .config('spark.executor.core', '2') \
    .config('spark.executor.memory', '4G') \
    .config('spark.ui.showConsoleProgress',True) \
    .getOrCreate()
sc = spark.sparkContext
sc
testDF = ImageSchema.readImages("hdfs://localhost:9000/test/").withColumn("label", lit(0))

from sparkdl.image import imageIO as imageIO
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from pyspark.ml import Pipeline, PipelineModel
from sparkdl import DeepImageFeaturizer

lr_test = LogisticRegressionModel.load('./lr')
featurizer_test = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")

p_lr_test = PipelineModel(stages=[featurizer_test, lr_test])
tested_lr_test = p_lr_test.transform(testDF)

evaluator_lr_test = MulticlassClassificationEvaluator(metricName="accuracy")
print("accuracy", str(tested_lr_test.select("prediction", "label").show()))
