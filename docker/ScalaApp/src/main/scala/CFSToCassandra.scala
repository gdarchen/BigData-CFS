import scala.io.Source
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import com.datastax.spark.connector._
import com.datastax.driver.core.utils.UUIDs
import java.util.UUID

object CFSToCassandra {
    case class Tweets(id:UUID,tweet:String)
    case class Dictionnary(word:String,valence:Int,strength:String)
    case class Ground_Truth(tweet:String,ground_truth_valence:Int)
    def main(args: Array[String]) {
	val conf = new SparkConf().setAppName("Simple Application")
	val sc = new SparkContext(conf)
	val file1 = Source.fromFile(args(0)).getLines.toArray
        file1.foreach(line =>
        sc.textFile(line).map(x=>x.split("\n")).map(x=>Tweets(UUIDs.timeBased(),x(0))).saveToCassandra("test","tweets"))
	val file2=args(1)
        sc.textFile(file2).map(x=>x.split("\t")).map(x=>Dictionnary(x(2),x(5).toInt,x(0))).saveToCassandra("test","dict")
	val file3=args(2)
        sc.textFile(file3).map(x=>x.split("\t")).map(x=>Ground_Truth(x(0),x(1).toInt)).saveToCassandra("test","ground_truth")
	sc.stop()
   }
}



