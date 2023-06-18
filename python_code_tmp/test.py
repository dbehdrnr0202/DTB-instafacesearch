#import findspark
#findspark.init()

import pyspark
#import tensorflow as tf
#from tensorflow.keras.models import Sequential
from tensorflow import keras
from sparkdl import DeepImageFeaturizer
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.ml.image import ImageSchema
#from sparkdl import readImages
from keras.applications import InceptionV3
from pyspark.ml import Pipeline
from pyspark.sql.functions import lit
import os

SUBMIT_ARGS="--packages databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11 --master spark://nn1:7077 pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS

if __name__=="__main__":
    spark = SparkSession.builder.appName('sparkdl_test').getOrCreate()
    '''
    spark = SparkSession.builder
            #.config('spark.jars.packages', 'databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11')
            .appName('sparkdl_test')
            .getOrCreate()
    
    
    conf = SparkConf()
    conf.set("spark.jars", 'databricks:spark-deep-learning:1.5.0-spark2.4-s_2.11.jar').setMaster("spark://nn1:7077")
    conf.setAppName("ml")
    '''

    print("conf=================================================================================================")
    #sc = SparkContext(conf)
    print("sc=================================================================================================")

    image_dir = "/home/test/project/JENNIE/"
    jennie_image = spark.read.format("image").load(image_dir).withColumn("label", lit(1))
    featurizer = DeepImageFeaturizer(inputCol="image", outputCol="features", modelName="InceptionV3")
    print("done")
