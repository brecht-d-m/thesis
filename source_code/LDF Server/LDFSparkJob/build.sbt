name := "LDFSpark"

version := "1.0"

scalaVersion := "2.10.4"

resolvers += "Job Server Bintray" at "https://dl.bintray.com/spark-jobserver/maven"

libraryDependencies ++= Seq(
  "spark.jobserver" %% "job-server" % "0.6.0" % "provided",
  "spark.jobserver" %% "job-server-api" % "0.6.0" % "provided",
  "spark.jobserver" %% "job-server-extras" % "0.6.0" % "provided",
  "org.apache.spark" % "spark-sql_2.10" % "1.5.1"
)


