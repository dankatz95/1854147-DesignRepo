import requests
import json
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import Row
import time
from datetime import datetime
import pyspark
from pyspark.sql import SparkSession

from ingest import DataLoader



#Filtering functions
udf_getDate = udf(lambda x : x['Date'])
udf_getLat = udf(lambda x : x['Latitude'])
udf_getLng = udf(lambda x : x['Longitude'])
udf_getSpeed = udf(lambda x : x['Speed'])
udf_getCarReg = udf(lambda x : x["Registration"])
  

#returns list of vehicles from fleet
def getVehicles():
    return []


def getFilteredDF(df):
    final_df = df.withColumn("Date", udf_getDate(df.col)).withColumn("Latitude", udf_getLat(df.col))\
        .withColumn("Longitude", udf_getLng(df.col))\
        .withColumn("Speed", udf_getSpeed(df.col))\
        .withColumn("CarRegistration", udf_getCarReg(df.col))
    final_df = final_df.drop("col")
    final_df = final_df.withColumn("New Date", to_timestamp(final_df.Date))
    final_df = final_df.drop("Date").withColumnRenamed("New Date", "Date").select("Date", "Latitude", "Longitude", "Speed", "CarRegistration")
    final_df = final_df.withColumn("Latitude", final_df.Latitude.cast("double"))\
        .withColumn("Longitude", final_df.Longitude.cast("double"))\
        .withColumn("Speed", final_df.Speed.cast("integer"))
    final_df = final_df.withColumn("Processed", lit(0)).dropna()
    final_df = final_df.withColumnRenamed("Speed", "Velocity")
    final_df = final_df.withColumn("Year", year(final_df.Date)).withColumn("Month", month(final_df.Date)).withColumn("Day", dayofmonth(final_df.Date))

    return final_df



def main():

    spark = SparkSession.builder.appName().getOrCreate()

    vehicles = getVehicles()

    #Example Schema obtained from CarTrack Fleet API
    schema = ArrayType(
        StructType([
            StructField("Registration")
            StructField("Events"),
            StructField("Vision Events"),
            StructField("Date"),
            StructField("Latitude"),
            StructField("Longitude"),
            StructField("Speed"),
            StructField("Road Speed"),
            StructField("Odometer"),
            StructField("Linear G"),
            StructField("Lateral G"),
            StructField("Location"),
            StructField("Geofences")
        ])
    )

    DL = DataLoader(spark, vehicles, schema)

    request_df = DL.getResponses()

    new_df = request_df.select(explode(request_df.result))

    final_df = getFilteredDF(new_df)


    final_df.write.option("header", True).option("schema", True).partitionBy("Processed","Year", "Month", "Day")\
        .mode("append").csv("/FileStore/output/dataset.csv", header=True)


if __name__ == '__main__':
    main()