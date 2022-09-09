import requests
from requests.models import PreparedRequest
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, ArrayType
from pyspark.sql import Row
from secrets import base_url, bearer_token
from datetime import datetime, timedelta


class DataLoader:

    vehicles = []

    df = None

    def __init__(self, spark, vehicles, schema): 
        self.vehicles = vehicles
        self.schema = schema   
        self.df = spark.createDataFrame(
            self.generateRows(self.getHeaders(), self.getBody())
            )

    def getHeaders(self):
        return  {
        'content-type': "application/json",
         #Would place Bearer Token Authorisation here for security purposes
         "Authorization": bearer_token
        }  
    def getBody(self):
        return json.dumps({})  

    def executeRestApi(verb, url, headers, body):

        res = None
    
        try:
            if verb == 'get':
                res = requests.get(url, data=body, headers=headers)
            else:
                pass
        except Exception as e:
            return e
        
        if res != None and res.status_code == 200:
            return json.loads(res.text)['Results']
        return None

    def getURL(carReg, today, base_url):

        start_date = today - timedelta(days=1)
        start_date = datetime(start_date.year, start_date.month, start_date.day,0,0,0)
        end_date = datetime(start_date.year, start_date.month, start_date.day,23,59,59)

        params = {
        "start_timestamp"= start_date.strftime("%Y-%m-%d %H:%M:%S"),
        "end_timestamp" = end_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        vehicle_url = base_url + "/{" + f'{carReg}' + "}"
        req = PreparedRequest()
        req.prepare_url(vehicle_url, params)

        return req.url

    def generateRows(self, headers, body):

        rows = []
        RequestRow = Row("verb", "url", "headers", "body")

        today = datetime.now()

        for vehicle in vehicles:
            url = self.getURL(vehicle, today)
            temp = RequestRow("get",url, headers, body)
            rows.append(temp)

        return rows

    def getResponses(self):

        executeAPI = udf(self.executeRestApi, self.schema)

        return self.df.withColumn("result", executeAPIcol(("verb"), col("url"), col("headers"), col("body")))

