"""
Unit tests for finance analytics module
"""

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src/main/python'))

from finance_analytics import create_spark_session, analyze_transactions, analyze_stock_prices


@pytest.fixture(scope="session")
def spark():
    """
    Create a Spark session for testing
    """
    spark = SparkSession.builder \
        .appName("FinanceAnalyticsTests") \
        .master("local[2]") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
    yield spark
    spark.stop()


@pytest.fixture
def sample_transaction_data(spark):
    """
    Create sample transaction data for testing
    """
    schema = StructType([
        StructField("date", StringType(), True),
        StructField("category", StringType(), True),
        StructField("description", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("account", StringType(), True)
    ])
    
    data = [
        ("2024-01-01", "Groceries", "Supermarket", 100.0, "Checking"),
        ("2024-01-02", "Groceries", "Store", 50.0, "Checking"),
        ("2024-01-03", "Dining", "Restaurant", 75.0, "Credit Card"),
        ("2024-01-04", "Dining", "Cafe", 25.0, "Credit Card"),
    ]
    
    return spark.createDataFrame(data, schema)


@pytest.fixture
def sample_stock_data(spark):
    """
    Create sample stock data for testing
    """
    schema = StructType([
        StructField("date", StringType(), True),
        StructField("symbol", StringType(), True),
        StructField("open", DoubleType(), True),
        StructField("high", DoubleType(), True),
        StructField("low", DoubleType(), True),
        StructField("close", DoubleType(), True),
        StructField("volume", DoubleType(), True)
    ])
    
    data = [
        ("2024-01-01", "AAPL", 180.0, 185.0, 179.0, 184.0, 50000000.0),
        ("2024-01-02", "AAPL", 184.0, 188.0, 183.0, 187.0, 52000000.0),
        ("2024-01-01", "GOOGL", 140.0, 145.0, 139.0, 144.0, 28000000.0),
        ("2024-01-02", "GOOGL", 144.0, 148.0, 143.0, 147.0, 30000000.0),
    ]
    
    return spark.createDataFrame(data, schema)


def test_create_spark_session():
    """
    Test Spark session creation
    """
    spark = create_spark_session("TestApp")
    assert spark is not None
    assert spark.sparkContext.appName == "TestApp"
    spark.stop()


def test_transaction_analysis(spark, sample_transaction_data, tmp_path):
    """
    Test transaction analysis functionality
    """
    # Write sample data to temporary CSV
    output_path = str(tmp_path / "transactions.csv")
    sample_transaction_data.coalesce(1).write.csv(output_path, header=True, mode="overwrite")
    
    # Find the actual CSV file (it will be in a partition directory)
    import glob
    csv_files = glob.glob(f"{output_path}/*.csv")
    assert len(csv_files) > 0, "No CSV file generated"
    
    # Analyze transactions
    result = analyze_transactions(spark, csv_files[0])
    
    # Verify results
    assert result is not None
    assert result.count() == 2  # Two categories: Groceries and Dining
    
    # Check that categories are present
    categories = [row.category for row in result.collect()]
    assert "Groceries" in categories
    assert "Dining" in categories


def test_stock_analysis(spark, sample_stock_data, tmp_path):
    """
    Test stock price analysis functionality
    """
    # Write sample data to temporary CSV
    output_path = str(tmp_path / "stocks.csv")
    sample_stock_data.coalesce(1).write.csv(output_path, header=True, mode="overwrite")
    
    # Find the actual CSV file
    import glob
    csv_files = glob.glob(f"{output_path}/*.csv")
    assert len(csv_files) > 0, "No CSV file generated"
    
    # Analyze stocks
    result = analyze_stock_prices(spark, csv_files[0])
    
    # Verify results
    assert result is not None
    assert result.count() == 2  # Two symbols: AAPL and GOOGL
    
    # Check that symbols are present
    symbols = [row.symbol for row in result.collect()]
    assert "AAPL" in symbols
    assert "GOOGL" in symbols
