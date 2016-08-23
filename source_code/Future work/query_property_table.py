from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *

sc = SparkContext()
sqlContext = SQLContext(sc)

property_table = sqlContext.read.load("triples_property_parquet_file.parquet")
property_table.registerTempTable("property_table")

triples_count = sqlContext.sql("SELECT COUNT(*) FROM property_table")

print_results=True
print_time=True
write_to_csv=True

print()
print("=== NUMBER OF TRIPLES ===")
print(triples_count.collect())
print()

import timeit

execution_times=[]

def execute_query(query_string, query_tag):
    start_time = timeit.default_timer()
    # Querying
    triples=sqlContext.sql(query_string)
    elapsed = timeit.default_timer()-start_time
    
    if(print_time):
        print(query_tag + "," + str(elapsed))

    if(print_results):
        print()
        print("=== TRIPLES ===")
        print(triples.collect())
        print()

    if(write_to_csv):
        execution_times.append({"query": query_tag, "time": elapsed})

# SPARQL queries translated to SQL using SempalaTranslator with manual editing

# SELECT ?v0 ?v1 ?v3 ?v4 ?v5 ?v6 ?v7 ?v8 ?v9 WHERE {
#     ?v0 <http://purl.org/goodrelations/includes> ?v1 .
#     <http://db.uwaterloo.ca/~galuc/wsdbm/Retailer9> <http://purl.org/goodrelations/offers> ?v0 .
#     ?v0 <http://purl.org/goodrelations/price> ?v3 .
#     ?v0 <http://purl.org/goodrelations/serialNumber> ?v4 .
#     ?v0 <http://purl.org/goodrelations/validFrom> ?v5 .
#     ?v0 <http://purl.org/goodrelations/validThrough> ?v6 .
#     ?v0 <http://schema.org/eligibleQuantity> ?v7 .
#     ?v0 <http://schema.org/eligibleRegion> ?v8 .
#     ?v0 <http://schema.org/priceValidUntil> ?v9 .
# }
query_string_1 = """(SELECT DISTINCT BGP1.v6 AS v6, BGP1.v7 AS v7, BGP1.v8 AS v8, BGP1.v9 AS v9, BGP1.v0 AS v0, BGP1.v1 AS v1, BGP1.v3 AS v3, BGP1.v4 AS v4, BGP1.v5 AS v5 FROM 
    (SELECT  DISTINCT BGP1_0.v6 AS v6, BGP1_0.v7 AS v7, BGP1_0.v8 AS v8, BGP1_0.v9 AS v9, BGP1_0.v0 AS v0, BGP1_0.v1 AS v1, BGP1_0.v3 AS v3, BGP1_0.v4 AS v4, BGP1_0.v5 AS v5 FROM 
        (SELECT  DISTINCT 
            `<http://purl.org/goodrelations/validThrough>` AS v6, 
            `<http://schema.org/eligibleQuantity>` AS v7, 
            `<http://schema.org/eligibleRegion>` AS v8, 
            `<http://schema.org/priceValidUntil>` AS v9, 
            subject AS v0, 
            `<http://purl.org/goodrelations/includes>` AS v1, 
            `<http://purl.org/goodrelations/price>` AS v3, 
            `<http://purl.org/goodrelations/serialNumber>` AS v4, 
            `<http://purl.org/goodrelations/validFrom>` AS v5 
        FROM property_table 
        WHERE 
            subject is not null  
            AND `<http://purl.org/goodrelations/includes>` is not null 
            AND `<http://purl.org/goodrelations/price>` is not null 
            AND `<http://purl.org/goodrelations/serialNumber>` is not null 
            AND `<http://purl.org/goodrelations/validFrom>` is not null 
            AND `<http://purl.org/goodrelations/validThrough>` is not null 
            AND `<http://schema.org/eligibleQuantity>` is not null 
            AND `<http://schema.org/eligibleRegion>` is not null 
            AND `<http://schema.org/priceValidUntil>` is not null
        ) BGP1_0 JOIN 
        (SELECT  DISTINCT 
            `<http://purl.org/goodrelations/offers>` AS v0 
        FROM property_table 
        WHERE 
            subject = \"<http://db.uwaterloo.ca/~galuc/wsdbm/Retailer9>\" 
            AND `<http://purl.org/goodrelations/offers>` is not null
        ) BGP1_1 
        ON(BGP1_0.v0=BGP1_1.v0)
    ) BGP1) """

# SELECT ?v0 ?v1 ?v3 WHERE {
#     ?v0 <http://purl.org/dc/terms/Location> ?v1 .
#     ?v0 <http://schema.org/nationality> <http://db.uwaterloo.ca/~galuc/wsdbm/Country9> .
#     ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/gender> ?v3 .
#     ?v0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://db.uwaterloo.ca/~galuc/wsdbm/Role2> .
# }
query_string_2 = """(SELECT  DISTINCT BGP1_0.v0 AS v0, BGP1_0.v1 AS v1, BGP1_0.v3 AS v3 FROM 
    (SELECT  DISTINCT 
        subject AS v0, 
        `<http://purl.org/dc/terms/Location>` AS v1, 
        `<http://db.uwaterloo.ca/~galuc/wsdbm/gender>` AS v3 
    FROM property_table 
    WHERE 
        subject is not null  
        AND `<http://purl.org/dc/terms/Location>` is not null 
        AND `<http://schema.org/nationality>` is not null 
        AND `<http://schema.org/nationality>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/Country9>\" 
        AND `<http://db.uwaterloo.ca/~galuc/wsdbm/gender>` is not null 
        AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` is not null
        AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/Role2>\"
    ) BGP1_0)"""

# SELECT ?v0 ?v2 ?v3 ?v4 WHERE {
#     ?v0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://db.uwaterloo.ca/~galuc/wsdbm/ProductCategory7> .
#     ?v0 <http://schema.org/caption> ?v2 .
#     ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre> ?v3 .
#     ?v0 <http://schema.org/publisher> ?v4 .
# }
query_string_3 = """(SELECT  DISTINCT BGP1_0.v0 AS v0, BGP1_0.v2 AS v2, BGP1_0.v3 AS v3, BGP1_0.v4 AS v4 FROM 
    (SELECT  DISTINCT 
        subject AS v0, 
        `<http://schema.org/caption>` AS v2, 
        `<http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre>` AS v3 , 
        `<http://schema.org/publisher>` AS v4 
    FROM property_table 
    WHERE 
        subject is not null  
        AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` is not null 
        AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/ProductCategory7>\" 
        AND `<http://schema.org/caption>` is not null 
        AND `<http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre>` is not null 
        AND `<http://schema.org/publisher>` is not null
    ) BGP1_0)"""

# SELECT ?v0 ?v2 ?v3 WHERE {
#    ?v0 <http://xmlns.com/foaf/age> <http://db.uwaterloo.ca/~galuc/wsdbm/AgeGroup5> .
#     ?v0 <http://xmlns.com/foaf/familyName> ?v2 .
#     ?v3 <http://purl.org/ontology/mo/artist> ?v0 .
#     ?v0 <http://schema.org/nationality> <http://db.uwaterloo.ca/~galuc/wsdbm/Country1> .
# }
query_string_4 = """(SELECT  DISTINCT BGP1.v0 AS v0, BGP1.v2 AS v2, BGP1.v3 AS v3 FROM 
    (SELECT DISTINCT BGP1_1.v0 AS v0, BGP1_0.v2 AS v2, BGP1_1.v3 AS v3 FROM 
        (SELECT  DISTINCT 
            `<http://purl.org/ontology/mo/artist>` AS v0, 
            subject AS v3 
        FROM property_table 
        WHERE 
            subject is not null  
            AND `<http://purl.org/ontology/mo/artist>` is not null
        ) BGP1_1 JOIN 
        (SELECT DISTINCT 
            subject AS v0, 
            `<http://xmlns.com/foaf/familyName>` AS v2 
        FROM property_table 
        WHERE 
            subject is not null  
            AND `<http://xmlns.com/foaf/age>` is not null 
            AND `<http://xmlns.com/foaf/age>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/AgeGroup5>\" 
            AND `<http://xmlns.com/foaf/familyName>` is not null 
            AND `<http://schema.org/nationality>` is not null 
            AND `<http://schema.org/nationality>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/Country1>\"
        ) BGP1_0 
        ON(BGP1_1.v0=BGP1_0.v0)
    ) BGP1)"""

# SELECT ?v0 ?v2 ?v3 WHERE {
#     ?v0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://db.uwaterloo.ca/~galuc/wsdbm/ProductCategory3> .
#     ?v0 <http://schema.org/description> ?v2 .
#     ?v0 <http://schema.org/keywords> ?v3 .
#     ?v0 <http://schema.org/language> <http://db.uwaterloo.ca/~galuc/wsdbm/Language0> .
# }
query_string_5 = """(SELECT  DISTINCT BGP1_0.v0 AS v0, BGP1_0.v2 AS v2, BGP1_0.v3 AS v3 FROM 
    (SELECT  DISTINCT 
        subject AS v0, 
        `<http://schema.org/description>` AS v2, 
        `<http://schema.org/keywords>` AS v3 
    FROM property_table
    WHERE 
        subject is not null  
        AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` is not null 
        AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/ProductCategory3>\" 
        AND `<http://schema.org/description>` is not null 
        AND `<http://schema.org/keywords>` is not null 
        AND `<http://schema.org/language>` is not null 
        AND `<http://schema.org/language>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/Language0>\"
    ) BGP1_0)"""

# SELECT ?v0 ?v1 ?v2 WHERE {
#     ?v0 <http://purl.org/ontology/mo/conductor> ?v1 .
#     ?v0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?v2 .
#     ?v0 <http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre> <http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre71> .
# }
query_string_6 = """(SELECT  DISTINCT BGP1_0.v0 AS v0, BGP1_0.v1 AS v1, BGP1_0.v2 AS v2 FROM 
    (SELECT  DISTINCT 
        subject AS v0, 
        `<http://purl.org/ontology/mo/conductor>` AS v1,
        `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` AS v2 
    FROM property_table
    WHERE 
        subject is not null  
        AND `<http://purl.org/ontology/mo/conductor>` is not null 
        AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` is not null 
        AND `<http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre>` is not null 
        AND `<http://db.uwaterloo.ca/~galuc/wsdbm/hasGenre>` = \"<http://db.uwaterloo.ca/~galuc/wsdbm/SubGenre71>\"
    ) BGP1_0)"""

# SELECT ?v0 ?v1 ?v2 WHERE {
#     ?v0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?v1 .
#     ?v0 <http://schema.org/text> ?v2 .
#     <http://db.uwaterloo.ca/~galuc/wsdbm/User945> <http://db.uwaterloo.ca/~galuc/wsdbm/likes> ?v0 .
# }
query_string_7 = """(SELECT DISTINCT BGP1.v0 AS v0 , BGP1.v1 AS v1 , BGP1.v2 AS v2 FROM 
    (SELECT DISTINCT BGP1_0.v0 AS v0 , BGP1_0.v1 AS v1 , BGP1_0.v2 AS v2 FROM 
        (SELECT DISTINCT 
            subject AS v0, 
            `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` AS v1, 
            `<http://schema.org/text>` AS v2 
        FROM property_table 
        WHERE 
            subject is not null  
            AND `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>` is not null 
            AND `<http://schema.org/text>` is not null
        ) BGP1_0 JOIN 
        (SELECT  DISTINCT 
            `<http://db.uwaterloo.ca/~galuc/wsdbm/likes>` AS v0 
        FROM property_table 
        WHERE 
            subject = \"<http://db.uwaterloo.ca/~galuc/wsdbm/User945>\" 
            AND `<http://db.uwaterloo.ca/~galuc/wsdbm/likes>` is not null
        ) BGP1_1 
        ON (BGP1_0.v0 = BGP1_1.v0)
     ) BGP1)"""

# Execute queries
execute_query(query_string_1, "S1") 
execute_query(query_string_2, "S2") 
execute_query(query_string_3, "S3") 
execute_query(query_string_4, "S4") 
execute_query(query_string_5, "S5") 
execute_query(query_string_6, "S6") 
execute_query(query_string_7, "S7") 

if(write_to_csv):
    import csv
    
    with open('property_table_test_times_500k.csv', 'w') as csvfile:
        fieldnames = ['query', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
            
        for line in execution_times:
            writer.writerow(line)
