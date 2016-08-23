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

impala=true

spark=false
spark_100k=false
spark_500k=false
spark_1M=true
spark_5M=false
spark_10M=false

hdt=false
hdt_100k=true
hdt_500k=true
hdt_1M=true
hdt_5M=true
hdt_10M=true

# SPARK QUERIES
if $spark; then
        if $spark_100k; then
                if [ -f output_time_spark_100k.log ]; then
                         mv output_time_spark_100k.log output_time_spark_100k.log.old
                fi

                for f in $QUERIES_PATHNAME_100k
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/spark_test_index_table $f | grep "Time " ; } 2>> output_time_spark_100k.log
			sleep 20
                done
        fi

	if $spark_500k; then
                if [ -f output_time_spark_500k.log ]; then
                         mv output_time_spark_500k.log output_time_spark_500k.log.old
                fi

                for f in $QUERIES_PATHNAME_500k
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/spark_test_index_table_sorted $f | grep "Time " ; } 2>> output_time_spark_its_500k.log
                        sleep 20
                done
        fi

        if $spark_1M; then
                if [ -f output_time_spark_its_1M.log ]; then
                         mv output_time_spark_its_1M.log output_time_spark_its_1M.log.old
                fi

                for f in $QUERIES_PATHNAME_1M
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/spark_test_index_table_sorted $f | grep "Time " ; } 2>> output_time_spark_its_1M.log
			sleep 20
                done
        fi

        if $spark_10M; then
                if [ -f output_time_spark_it_10M.log ]; then
                	mv output_time_spark_it_10M.log output_time_spark_it_10M.log.old
                fi

                for f in $QUERIES_PATHNAME_10M
                do
                        echo $f
                        { /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/spark_test_index_table $f | grep "Time " ; } 2>> output_time_spark_it_10M.log
                        sleep 20
                done
        fi
fi

# HDT QUERIES
if $hdt; then
	if $hdt_100k; then
		if [ -f output_time_hdt_100k.log ]; then
			 mv output_time_hdt_100k.log output_time_hdt_100k.log.old
		fi

		for f in $QUERIES_PATHNAME_100k
		do
			echo $f
			{ /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/hdt_test_100k $f | grep "Time " ; } 2>> output_time_hdt_100k.log
		done
	fi

    if $hdt_500k; then
		if [ -f output_time_hdt_500k.log ]; then
			 mv output_time_hdt_500k.log output_time_hdt_500k.log.old
		fi

		for f in $QUERIES_PATHNAME_500k
		do
			echo $f
			{ /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/hdt_test_500k $f | grep "Time " ; } 2>> output_time_hdt_500k.log
		done
	fi
	
	if $hdt_1M; then
		if [ -f output_time_hdt_1M.log ]; then
	                 mv output_time_hdt_1M.log output_time_hdt_1M.log.old
	        fi
	
		for f in $QUERIES_PATHNAME_1M
		do
			echo $f
			{ /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/hdt_test_1M $f | grep "Time " ; } 2>> output_time_hdt_1M.log
		done
	fi

    if $hdt_5M; then
		if [ -f output_time_hdt_5M.log ]; then
	                 mv output_time_hdt_5M.log output_time_hdt_5M.log.old
	        fi
	
		for f in $QUERIES_PATHNAME_5M
		do
			echo $f
			{ /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/hdt_test_5M $f | grep "Time " ; } 2>> output_time_hdt_5M.log
		done
	fi
	
	if $hdt_10M; then
		if [ -f output_time_hdt_10M.log ]; then
	                mv output_time_hdt_10M.log output_time_hdt_10M.log.old
	        fi
	
		for f in $QUERIES_PATHNAME_10M
		do
			echo $f
			{ /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/hdt_test_10M $f | grep "Time " ; } 2>> output_time_hdt_10M.log
		done
	fi
fi

if $impala; then
	rm output_time_impala_it.500k.new.log

	# IMPALA QUERIES
	for f in $QUERIES_PATHNAME_500k
	do
        echo $f
		{ /usr/bin/time -f "$f, %E" Client.js/bin/ldf-client http://localhost:8000/impala_index_table_test $f | grep "Time " ; } 2>> output_time_impala_it.500k.new.log
		sleep 10
	done
fi
