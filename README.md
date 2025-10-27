# Finance Project - Apache Spark Analytics

A financial data analytics project built with Apache Spark for processing and analyzing financial transactions and stock market data.

## Overview

This project demonstrates how to use Apache Spark for financial data analysis, including:
- Transaction data processing and categorization
- Stock price analysis and aggregation
- Scalable data processing for large financial datasets

## Project Structure

```
finance-project/
├── src/
│   ├── main/
│   │   └── python/
│   │       └── finance_analytics.py    # Main Spark application
│   └── test/
│       └── python/
│           └── test_finance_analytics.py # Unit tests
├── data/
│   ├── sample_transactions.csv         # Sample transaction data
│   └── sample_stocks.csv              # Sample stock price data
├── config/
│   └── application.json               # Application configuration
├── notebooks/                         # Jupyter notebooks for analysis
├── requirements.txt                   # Python dependencies
└── README.md                         # This file
```

## Prerequisites

- Python 3.8 or higher
- Java 8 or 11 (required for Spark)
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rashmi-fit/finance-project.git
cd finance-project
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Application

Execute the main Spark analytics application:

```bash
python src/main/python/finance_analytics.py
```

This will:
1. Load sample transaction and stock data
2. Perform aggregation and analysis
3. Display results in the console

### Running Tests

Execute the test suite:

```bash
pytest src/test/python/
```

For verbose output:
```bash
pytest -v src/test/python/
```

## Features

### Transaction Analysis
- Aggregates transactions by category
- Calculates total spending per category
- Computes average transaction amounts
- Provides transaction counts

### Stock Price Analysis
- Analyzes stock price data by symbol
- Calculates average closing prices
- Computes average trading volumes
- Tracks trading day counts

## Sample Data

The project includes sample data files:

- **sample_transactions.csv**: Contains personal finance transactions with categories like Groceries, Dining, Transportation, etc.
- **sample_stocks.csv**: Contains stock price data for major tech companies (AAPL, GOOGL, MSFT, TSLA)

## Configuration

Configuration settings are stored in `config/application.json`:

```json
{
  "spark": {
    "app_name": "FinanceAnalytics",
    "master": "local[*]",
    "log_level": "WARN"
  },
  "data": {
    "transactions_path": "data/sample_transactions.csv",
    "stocks_path": "data/sample_stocks.csv"
  }
}
```

## Extending the Project

### Adding New Data Sources
1. Place your CSV files in the `data/` directory
2. Update the paths in `config/application.json`
3. Modify the analysis functions in `finance_analytics.py`

### Adding New Analysis Functions
1. Create new functions in `finance_analytics.py`
2. Add corresponding unit tests in `test_finance_analytics.py`
3. Call the functions from `main()`

### Working with Large Datasets
For production use with large datasets:
1. Update `spark.master` in config to point to your cluster
2. Adjust partition counts based on data size
3. Consider using Parquet format for better performance
4. Enable data caching for iterative analysis

## Performance Tips

- Use `repartition()` or `coalesce()` to optimize partition counts
- Cache frequently accessed DataFrames with `.cache()`
- Use Parquet format for large datasets
- Leverage Spark's distributed processing for big data

## Troubleshooting

### Java Not Found
If you get a Java error, ensure Java 8 or 11 is installed:
```bash
java -version
```

### Memory Issues
If you encounter memory errors, adjust Spark memory settings:
```python
spark = SparkSession.builder \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, please open an issue on GitHub.