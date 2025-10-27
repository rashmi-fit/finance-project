"""
Finance Data Processing with Apache Spark
Main application entry point
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, count, round as spark_round
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
import sys


def create_spark_session(app_name="FinanceAnalytics"):
    """
    Create and configure Spark session
    
    Args:
        app_name: Name of the Spark application
        
    Returns:
        SparkSession: Configured Spark session
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.warehouse.dir", "spark-warehouse") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark


def analyze_transactions(spark, input_path):
    """
    Analyze financial transactions
    
    Args:
        spark: SparkSession
        input_path: Path to transaction data
        
    Returns:
        DataFrame: Analysis results
    """
    # Read transaction data
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    
    print("=" * 80)
    print("Transaction Data Schema:")
    print("=" * 80)
    df.printSchema()
    
    print("\n" + "=" * 80)
    print("Sample Transactions:")
    print("=" * 80)
    df.show(10, truncate=False)
    
    # Perform analysis
    print("\n" + "=" * 80)
    print("Transaction Analysis by Category:")
    print("=" * 80)
    
    category_analysis = df.groupBy("category") \
        .agg(
            count("*").alias("transaction_count"),
            spark_round(sum("amount"), 2).alias("total_amount"),
            spark_round(avg("amount"), 2).alias("avg_amount")
        ) \
        .orderBy(col("total_amount").desc())
    
    category_analysis.show(truncate=False)
    
    return category_analysis


def analyze_stock_prices(spark, input_path):
    """
    Analyze stock price data
    
    Args:
        spark: SparkSession
        input_path: Path to stock price data
        
    Returns:
        DataFrame: Stock analysis results
    """
    # Read stock data
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    
    print("\n" + "=" * 80)
    print("Stock Price Data Schema:")
    print("=" * 80)
    df.printSchema()
    
    print("\n" + "=" * 80)
    print("Sample Stock Prices:")
    print("=" * 80)
    df.show(10, truncate=False)
    
    # Calculate price changes
    print("\n" + "=" * 80)
    print("Stock Price Summary:")
    print("=" * 80)
    
    stock_summary = df.groupBy("symbol") \
        .agg(
            count("*").alias("trading_days"),
            spark_round(avg("close"), 2).alias("avg_close"),
            spark_round(avg("volume"), 0).alias("avg_volume")
        ) \
        .orderBy(col("symbol"))
    
    stock_summary.show(truncate=False)
    
    return stock_summary


def main():
    """
    Main application logic
    """
    print("Starting Finance Analytics Spark Application")
    print("=" * 80)
    
    # Create Spark session
    spark = create_spark_session()
    
    try:
        # Analyze transactions if data exists
        transaction_path = "data/sample_transactions.csv"
        print(f"\nAnalyzing transactions from: {transaction_path}")
        analyze_transactions(spark, transaction_path)
        
        # Analyze stock prices if data exists
        stock_path = "data/sample_stocks.csv"
        print(f"\nAnalyzing stock prices from: {stock_path}")
        analyze_stock_prices(spark, stock_path)
        
        print("\n" + "=" * 80)
        print("Analysis Complete!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}", file=sys.stderr)
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
