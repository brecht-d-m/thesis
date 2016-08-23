import com.typesafe.config.{ConfigException, Config}
import org.apache.spark.sql.SQLContext
import spark.jobserver.{SparkJobValid, SparkJobValidation, SparkSqlJob}

object LDFSparkSearchJob extends SparkSqlJob {

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

    // Limit
    var (limitValue, limitAvailable) = parseConfigString("limit", config)

    // Offset
    var (offsetValue, offsetAvailable) = parseConfigString("offset", config)

    if(limitAvailable && !offsetAvailable) {
        offsetValue = "0"
        offsetAvailable = true
    }

    // SQL statement creation
    val sqlString = "SELECT * FROM " + table_name
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
      if(limitAvailable && offsetAvailable) {
        var totalLimit = offsetValue.toInt + limitValue.toInt
        var df = sql.sql(sqlString + " WHERE " + sqlSuffixString + " LIMIT " + totalLimit);
        //var df_offset = sql.sql(sqlString + " WHERE " + sqlSuffixString + " LIMIT " + offsetValue.toInt);
        var sqlRowCollection = df.collect();
        var tempResult = sqlRowCollection.slice(offsetValue.toInt, offsetValue.toInt + limitValue.toInt);
 
        //var tempResult = df.except(df_offset).collect(); 
        return tempResult
      } else {
        sql.sql(sqlString + " WHERE " + sqlSuffixString).collect()
      }
    } else {
      if(limitAvailable && offsetAvailable) {
        var totalLimit = offsetValue.toInt + limitValue.toInt
        var df = sql.sql(sqlString + " LIMIT " + totalLimit);
        //var df_offset = sql.sql(sqlString + " LIMIT " + offsetValue.toInt);
        var sqlRowCollection = df.collect();
        var tempResult = sqlRowCollection.slice(offsetValue.toInt, offsetValue.toInt + limitValue.toInt);
 
        //var tempResult = df.except(df_offset).collect(); 
        return tempResult
      } else {
        sql.sql(sqlString).collect()
      }
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
