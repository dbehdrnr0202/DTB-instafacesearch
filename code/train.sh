#!/bin/bash
param_instance=""
param_memory=""
param_spark=""
param_hdfs=""
empty_str=""
while [ -n "$1" ]
do
    case "$1" in
        -i) $param_instance=$2
            shift;;
        -m) $param_memory=$2
            shift;;
        -s) $param_spark=$2
            shift;;
        -h) $param_hdfs=$2
            shift;;
        *) ;;
    esac
    shift
done

if [ ${#param_instance} == 0 ]
then
    param_i=2
fi
if [ ${#param_memory} == 0 ]
then
    param_m='4G'
fi
if [ ${#param_spark} == 0 ]
then
    param_s='spark://mater:7077'
fi
if [ ${#param_hdfs} == 0 ]
then
    param_h='hdfs://master:9000'
fi


hdfs dfs -put ./img_crop/* /train/
python train_save_model.py -i $param_i -m $param_m -s $param_s -h $param_h