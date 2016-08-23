1. Start the server monitors  (process attached to session)

    sudo bash monitor_servers [PID1 [PID2 [...]]

  This will create a folder `/srv/evaluation_bloom/monitor_[current_time]` with one logfile per PID, e.g. 1111.csv. Remember, when logging an ldf-server, you have to specify the PIDs for all workers, not the master process.
  The interval is default 500ms. Currently, this can be changed by editing the `monitor_servers` script by replacing `./monitor $pid` with `./monitor $pid [delay in ms]`.


2. Edit and start the evaluation script (process attached to session):

    sudo bash evaluation 2> error.log

  This will create a folder `/srv/evaluation_bloom/output_[current_time]` with one CSV results-file per test. Currently 250 queries should be run on watdiv100M. Failing queries log their error within error.log and the CSV results-file.
  In its original state it tests the original, optimized and amq client in combination with the original server, Bloom server and GCS server.
  The CSV output is generated to stdout by the script `run-tests-ext` and can be used for a single test run. It reads a query file line by line and produces the following values:

      file,id,timeFirst(ms),timeHalf(ms),time(ms),resultCount,requestCount,timeOut,cpu(%),memory(MB),error
