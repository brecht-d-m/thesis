from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.types import *

sc = SparkContext()
sqlContext = SQLContext(sc)

triples_input_file="watdiv.500k.out.csv"
triples = sc.textFile(triples_input_file)

triples_splitted = triples.map(lambda t: t.split(","))
triples_header   = triples_splitted.first()
triples_data     = triples_splitted.filter(lambda t: t != triples_header)

fields = [StructField(field_name, StringType(), True) for field_name in triples_header]
schema = StructType(fields)

triples_df = sqlContext.createDataFrame(triples_data, schema)
triples_df.write.mode("overwrite").save("triples_property_parquet_file.parquet", format="parquet")
