import pyspark
from pyspark.sql.functions import *


def getDays(df):
	daysDF = []

	days= [x.YMD for x in df.withColumn("YMD", date_format(df_clean.Date, "yyyy MM dd")).select("YMD").distinct().sort("YMD").collect()]

	return days 