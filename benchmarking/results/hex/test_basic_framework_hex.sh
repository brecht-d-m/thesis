#! /bin/sh

# File structure:
# map:
# -> test_basic_framework_hex.sh
# -> map watdiv
# -> map Client.js

QUERIES_PATHNAME=watdiv/watdiv/bin/Release/gen_queries/*.txt
QUERIES_PATHNAME_100k=watdiv/watdiv/bin/Release/datasets/100k/gen_queries/*.txt
QUERIES_PATHNAME_500k=watdiv/watdiv/bin/Release/datasets/500k/gen_queries/*.txt
QUERIES_PATHNAME_1M=watdiv/watdiv/bin/Release/datasets/1M/gen_queries/*.txt
QUERIES_PATHNAME_5M=watdiv/watdiv/bin/Release/datasets/5M/gen_queries/*.txt
QUERIES_PATHNAME_10M=watdiv/watdiv/bin/Release/datasets/10M/gen_queries/*.txt

spark=true
spark_100k=false
spark_500k=false
spark_1M=true
spark_5M=false
spark_10M=false

# SPARK QUERIES
if $spark; then
        if $spark_100k; then
                if [ -f output_time_spark_100k.log ]; then
                         mv output_time_spark_100k.log output_time_spark_100k.log.old
                fi

                for f in $QUERIES_PATHNAME_100k
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://curry-n1.elis.ugent.be:8000/hex_demo $f | grep "Time " ; } 2>> output_time_spark_100k.log
			sleep 10
                done
        fi

	if $spark_500k; then
                if [ -f output_time_spark_500k.log ]; then
                         mv output_time_spark_500k.log output_time_spark_500k.log.old
                fi

                for f in $QUERIES_PATHNAME_500k
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://curry-n1.elis.ugent.be:8000/hex_demo $f | grep "Time " ; } 2>> output_time_spark_500k.log
                        sleep 20
                done
        fi

        if $spark_1M; then
                if [ -f output_time_spark_1M_hex.log ]; then
                         mv output_time_spark_1M_hex.log output_time_spark_1M_hex.log.old
                fi

                for f in $QUERIES_PATHNAME_1M
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://curry-n1.elis.ugent.be:8000/hex_demo $f | grep "Time " ; } 2>> output_time_spark_1M_hex.log
			sleep 10
                done
        fi

        if $spark_10M; then
                if [ -f output_time_spark_10M.log ]; then
                	mv output_time_spark_10M.log output_time_spark_10M.log.old
                fi

                for f in $QUERIES_PATHNAME_10M
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://curry-n1.elis.ugent.be:8000/hex_demo $f | grep "Time " ; } 2>> output_time_spark_10M.log
                        sleep 20
                done
        fi
fi
