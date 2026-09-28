# Price Intelligence System

An automated price monitoring and analysis system built with Python and PostgreSQL.

The project collects headphone product data from multiple Iranian online retailers, stores current and historical prices, and applies SQL-based analytical models to identify price changes, trends, and anomalies.

## Overview

The system follows this pipeline:

Scraping → Validation & Deduplication → Database Upsert → Price History → SQL Analysis → Enriched Intelligence View

The project was designed as a practical data engineering and analytics project, combining web scraping, relational database design, automated data collection, and statistical analysis.

## Features

- Scrapes headphone products from multiple online retailers
- Validates scraped product data
- Removes duplicate products before database insertion
- Maintains a centralized product table
- Updates existing products instead of creating duplicates
- Records price history only when a product's price changes
- Calculates historical price statistics
- Detects price trends
- Detects anomalous price observations
- Distinguishes new anomalies from consecutive duplicate anomalies
- Combines analytical results into an enriched intelligence view
- Runs automatically through Windows Task Scheduler
- Uses environment variables for database credentials

## Data Sources

The system currently collects data from three retailers:

- Digikala
- IranHeadphone
- Technolife

Each source requires a different extraction strategy:

- **Digikala** — JSON API response
- **IranHeadphone** — HTML parsing with BeautifulSoup
- **Technolife** — POST request to a GraphQL-style endpoint

The scraped data is normalized into a common structure before being inserted into PostgreSQL.

## Project Structure

```text
Price_Detect/
│
├── Intelligence/
│   ├── ...
│   └── ...
│
├── Views/
│   ├── ...
│   └── ...
│
├── .env
├── .gitignore
├── requirements.txt
├── run.bat
│
├── main.py
├── dbase.py
├── query.py
│
├── Digiscrape.py
├── Irhscrape.py
└── Technoscrape.py 
```

## Main Components
###  main.py

The main entry point of the application, It:

1. Runs the three scrapers
2. Collects validated product data
3. Sends the data to the database layer
4. Updates product information
5. Records price changes in price history

###  Digiscrape.py

Handles product extraction from Digikala.
Responsibilities include:

1. API requests
2. Product extraction
3. Availability transformation
4. Data validation
5. Duplicate removal

###  Irhscrape.py

Handles product extraction from IranHeadphone.
Responsibilities include:

1. HTML requests
2. BeautifulSoup parsing
3. Product and price extraction
4. Availability detection
5. Data validation
6. Duplicate removal

###  Technoscrape.py

Handles product extraction from Technolife.
Responsibilities include:

1. POST requests
2. JSON response parsing
3. Price selection
4. Availability conversion
5. Product URL generation
6. Data validation
7. Duplicate removal

### dbase.py

Contains the database execution layer.
It:

1. Loads database credentials from .env
2. Establishes PostgreSQL connections
3. Inserts or updates products
4. Records price history
5. Handles database exceptions and logging

### query.py

Contains SQL statements used by the Python database layer.
These include:

- Product upsert queries
- Price-history insertion logic

The price-history query only creates a new history record when the current price differs from the most recently recorded price.

### Intelligence

Contains the SQL queries developed during the analytical modeling stage.
These queries were used to develop and test the analytical logic before converting the final versions into database views.

### Views

Contains the final SQL view definitions used by the system.
The analytical views include:

- price_status
- anomaly_stat
- price_intel
- price_intel_rep

### run.bat

A portable Windows launcher for the application:
```bat
@echo off
cd /d "%~dp0"
py main.py
```
The launcher determines its working directory from its own location rather than relying on a hardcoded project path.


## Database Design

The database is built around product information and historical observations.
The main entities include:

- stores
- products
- price_history

Analytical results are generated from the historical price data rather than being manually maintained.

### Products

The products table stores the current state of each product.
Important attributes include:

- Product ID
- Store ID
- Product name
- Current price
- Availability
- Product URL

Products are uniquely identified per store and product URL.

### Price History

The price_history table stores historical price observations.
A new observation is inserted only when the product's price differs from its most recent recorded price.
This prevents the history table from being filled with identical consecutive observations.

### Price Intelligence

The analytical layer consists of several stages.

#### 1. Price Status

The price-status analysis calculates:

- Current price
- Previous price
- Price change
- Percentage change
- Historical average
- Historical maximum
- Historical minimum

This provides a snapshot of the product's current position relative to its historical price data.

#### 2. Trend Detection

The trend model uses the latest observations for each product.
The process includes:

- Ordering price observations chronologically
- Selecting a rolling window of the latest observations
- Calculating a rolling median
- Calculating an ordinary least-squares regression slope
- Normalizing the slope against the rolling median
- Establishing product-specific percentile boundaries
- Classifying the latest trend

**Trend classifications** include:

- Strongly Upward
- Upward
- Stable
- Downward
- Strongly Downward

The model currently uses _observation order_ as the independent variable for trend regression.
This means that the model assumes observations are reasonably regular over time. Because of this, irregular scraping intervals can affect trend interpretation.
The anomaly model, in contrast, explicitly uses _elapsed time_ between observations.

#### 3. Anomaly Detection

The anomaly model uses _elapsed time between observations_ and a regression-based residual approach.

The process includes:

- Calculating elapsed time between observations
- Fitting a regression model
- Calculating predicted prices
- Calculating residuals
- Calculating the interquartile range (IQR)
- Creating lower and upper anomaly boundaries
- Classifying observations

An **observation can be classified** as:

- Normal
- Anomalous
- Undetermined

##### The system also distinguishes between:

- New Anomaly
- Duplicate

A consecutive anomalous observation is therefore not treated as a completely new anomaly.

#### 4. Enriched Intelligence View

The price_intel view combines the analytical outputs into a single dataset.
It brings together:

- Current price
- Price change
- Price change percentage
- Historical statistics
- Normalized trend slope
- Trend direction
- Anomaly status
- Anomaly duplication status

The price_intel_rep view additionally joins store information to provide a more report-oriented dataset.

### Automation

The system can run automatically using Windows Task Scheduler.
The scheduled task has been tested successfully with the current project structure.

### Logging

The application uses Python's built-in logging module.
The main execution flow reports events such as:

- Task start and completion
- Store being processed
- HTTP requests
- Number of collected products
- Number of valid products
- Database connection status
- Database update completion
- Request and database failures

This allows automated executions to be monitored without adding an external logging framework.


### Installation
Requirements:
- Python 3.x
- PostgreSQL
- Internet connection for retailer data collection

#### Python Dependencies

The project uses:
- requests
- beautifulsoup4
- lxml
- psycopg2-binary
- python-dotenv

Python standard-library modules such as _logging, re, os,_ and _pathlib_ do not need to be installed separately.

### Configuration

Database credentials are stored in a local .env file.
Do not commit the .env file to version control.

The repository's .gitignore excludes it:
1. .env
2. .idea/
3. __pycache__/

### Running the Project

After configuring PostgreSQL and the .env file: py main.py
Or run: run.bat
For automated execution, configure Windows Task Scheduler to launch run.bat.

### Limitations
#### Data Source Changes

- The project depends on the structure and availability of external retailer APIs and web pages.

- Changes to those sources may require modifications to the corresponding scraper.

#### Trend Sampling

- The current trend model uses observation order rather than elapsed time.
Therefore, the interpretation of a trend is more reliable when observations are collected at reasonably regular intervals.


#### Scraping Scope

- The current implementation collects a defined subset of products from each retailer rather than attempting to crawl an entire retailer catalog.

#### Database Dependency

- The application requires a configured PostgreSQL database containing the expected schema and analytical views.

### Future Improvements

Potential future improvements include:

- Making trend regression explicitly time-aware
- Expanding retailer and product coverage
- Adding more historical observations
- Improving scraper resilience to source-structure changes
- Adding automated tests
- Adding a reporting/dashboard layer
- Containerizing the application
- Improving deployment portability
- Adding more sophisticated price-change and anomaly models

### Technologies
- Python
- PostgreSQL
- Requests
- BeautifulSoup
- lxml
- psycopg2
- python-dotenv
- SQL
- Windows Task Scheduler