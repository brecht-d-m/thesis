import com.typesafe.config.{ConfigException, Config}
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.Row
import spark.jobserver.{SparkJobValid, SparkJobValidation, SparkSqlJob}

object LDFSparkCountJobIndexTable extends SparkSqlJob {

  var table_name = "triple_table"

  val prefixesArray: Array[String] =
   Array(
        "<http://xmlns.com/foaf/0.1/",
        "<http://xmlns.com/foaf/",
        "<http://localhost/vocabulary/bench/",
        "<http://www.w3.org/2001/XMLSchema#",
        "<http://purl.org/dc/elements/1.1/",
        "<http://purl.org/dc/terms/",
        "<http://purl.org/dc/dcmitype/",
        "<http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "<http://www.w3.org/2000/01/rdf-schema#",
        "<http://swrc.ontoware.org/ontology#",
        "<http://purl.org/rss/1.0/",
        "<http://www.w3.org/2002/07/owl#",
        "<http://localhost/persons/",
        "<http://example.org/",
        "<http://v.org/",
        "<http://rdfs.org/sioc/ns#>",
        "<http://rdfs.org/sioc/type#>",
        "<http://dbpedia.org/resource/",
        "<http://dbpedia.org/ontology/",
        "<http://dbpedia.org/property/",
        "<http://www.ins.cwi.nl/sib/vocabulary/>",
        "<http://www.ins.cwi.nl/sib/person/>",
        "<http://www.ins.cwi.nl/sib/user/>",
        "<http://www.ins.cwi.nl/sib/forum/>",
        "<http://www.ins.cwi.nl/sib/friendship/>",
        "<http://www.ins.cwi.nl/sib/group/>",
        "<http://www.ins.cwi.nl/sib/group/membership/>",
        "<http://www.ins.cwi.nl/sib/post/>",
        "<http://www.ins.cwi.nl/sib/post/comment/>",
        "<http://www.ins.cwi.nl/sib/photoalbum/photo/>",
        "<http://www.ins.cwi.nl/sib/photoalbum/>",
        "<http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#",
        "<http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
        "<http://www.w3.org/2002/07/owl#",
        "<http://db.uwaterloo.ca/~galuc/wsdbm/",
        "<http://schema.org/",
        "<http://purl.org/stuff/rev#",
        "<http://purl.org/ontology/mo/",
        "<http://purl.org/goodrelations/",
        "<http://www.geonames.org/ontology#",
        "<http://ogp.me/ns#"
  )

  def getIndex(triple: String): (Int, String) = {
    if(isURI(triple)) {
        for (i <- prefixesArray.indices) {
            if(triple.startsWith(prefixesArray(i))) {
                return ((i+1), triple.substring(prefixesArray(i).length,triple.length-1))
            }
        }

        return (0, triple)
    } else {
        return (0, triple)
    }
  }

  def isURI(input: String): Boolean = {
    if (input.startsWith("<") && input.endsWith(">")) {
      return true
    } else {
      return false
    }
  }

  override def runJob(sql: SQLContext, config: Config): Any = {
    var subjectValue = ""
    var subjectValueIndex = 0
    var subjectAvailable = true

    try {
      var subjectString = config.getString("subject") 
      subjectAvailable = !subjectString.equals("")
      
      if(subjectAvailable) {
        var subjectTuple = getIndex(subjectString)

        subjectValue = subjectTuple._2
        subjectValueIndex = subjectTuple._1
      }
    } catch {
      case e: ConfigException.Missing => subjectAvailable = false
    }

    var predicateValue = ""
    var predicateValueIndex = 0
    var predicateAvailable = true

    try {
      var predicateString = config.getString("predicate")
      predicateAvailable = !predicateString.equals("")

      if(predicateAvailable) {
        var predicateTuple = getIndex(predicateString)

        predicateValue = predicateTuple._2
        predicateValueIndex = predicateTuple._1
      }
    } catch {
      case e: ConfigException.Missing => predicateAvailable = false
    }

    var objectValue = ""
    var objectValueIndex = 0
    var objectAvailable = true

    try {
      var objectString = config.getString("object")
      objectAvailable = !objectString.equals("")

      if(objectAvailable) { 
        var objectTuple = getIndex(objectString)

        objectValue = objectTuple._2
        objectValueIndex = objectTuple._1
      }
    } catch {
      case e: ConfigException.Missing => objectAvailable = false
    }

    // SQL statement creation
    val sqlString = "SELECT count(*) FROM " + table_name
    var appended = false
    var sqlSuffixString = ""

    if(subjectAvailable) {
        sqlSuffixString += createSelectStatementIndex("subjectTripleObjectIndex", subjectValueIndex, appended)
        appended = true
    }
    if(predicateAvailable) {
        sqlSuffixString += createSelectStatementIndex("predicateTripleObjectIndex", predicateValueIndex, appended)
        appended = true
    }
    if(objectAvailable) {
        sqlSuffixString += createSelectStatementIndex("objectTripleObjectIndex", objectValueIndex, appended)
        appended = true
    }


    if(subjectAvailable) {      
      sqlSuffixString += createSelectStatement("subjectTripleObject", subjectValue, appended)
    }
    if(predicateAvailable) {
      sqlSuffixString += createSelectStatement("predicateTripleObject", predicateValue, appended)
    }
    if(objectAvailable) {
      sqlSuffixString += createSelectStatement("objectTripleObject", objectValue, appended)
    }

    if(appended) {
      sql.sql(sqlString + " WHERE " + sqlSuffixString).collect();
    } else {
      sql.sql(sqlString).collect()
    }
  }

  override def validate(sql: SQLContext, config: Config): SparkJobValidation = SparkJobValid

  def createSelectStatement(column: String, searchValue: String, appended: Boolean): String = {
    (if(appended) "AND " else "") + column + " = \"" + searchValue + "\" "
  }

  def createSelectStatementIndex(column: String, searchValue: Int, appended: Boolean): String = {
    (if(appended) "AND " else "") + column + " = " + searchValue + " "
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
