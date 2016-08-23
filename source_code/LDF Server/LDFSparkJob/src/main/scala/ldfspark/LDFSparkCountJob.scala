import com.typesafe.config.{ConfigException, Config}
import org.apache.spark.sql.SQLContext
import spark.jobserver.{SparkJobValid, SparkJobValidation, SparkSqlJob}

object LDFSparkCountJob extends SparkSqlJob {

  var table_name = "triple_table"

  override def runJob(sql: SQLContext, config: Config): Any = {
    var subjectValue = ""
    var subjectAvailable = true

    try {
      subjectValue = config.getString("subject")
      subjectAvailable = !subjectValue.equals("")
    } catch {
      case e: ConfigException.Missing => subjectAvailable = false
    }

    var predicateValue = ""
    var predicateAvailable = true

    try {
      predicateValue = config.getString("predicate")
      predicateAvailable = !predicateValue.equals("")
    } catch {
      case e: ConfigException.Missing => predicateAvailable = false
    }

    var objectValue = ""
    var objectAvailable = true

    try {
      objectValue = config.getString("object")
      objectAvailable = !objectValue.equals("")
    } catch {
      case e: ConfigException.Missing => objectAvailable = false
    }

    // SQL statement creation
    val sqlString = "SELECT count(*) FROM " + table_name
    var appended = false
    var sqlSuffixString = ""

    if(subjectAvailable) {
      sqlSuffixString += createSelectStatement("subjectTripleObject", subjectValue, appended)
      appended = true
    }

    if(predicateAvailable) {
      sqlSuffixString += createSelectStatement("predicateTripleObject", predicateValue, appended)
      appended = true
    }

    if(objectAvailable) {
      sqlSuffixString += createSelectStatement("objectTripleObject", objectValue, appended)
      appended = true
    }

    if(appended) {
      sql.sql(sqlString + " WHERE " + sqlSuffixString).collect()
    } else {
      sql.sql(sqlString).collect()
    }
  }

  override def validate(sql: SQLContext, config: Config): SparkJobValidation = SparkJobValid

  def createSelectStatement(column: String, searchValue: String, appended: Boolean): String = {
    (if(appended) "AND " else "") + column + " = \"" + searchValue + "\" "
  }

  def parseConfigString(configString: String, config: Config): (String, Boolean) = {
    var value = ""
    var available = true

    try {
      value = config.getString(configString)
      available = !value.equals("")
    } catch {
      case e: ConfigException.Missing => available = false
    }

    return (value, available)
  }
}
