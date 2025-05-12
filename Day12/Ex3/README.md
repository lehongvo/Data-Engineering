# Exercise 3: dbt Data Mart for Business Analytics

This exercise demonstrates how to build an analytical data mart using dbt (data build tool). This project takes the foundations built in Exercises 1 and 2 and expands them to create a full-featured data mart optimized for business analytics.

## Project Structure

The project follows a multi-layer architecture:

1. **Sources Layer**: Raw data from the e-commerce system
2. **Staging Layer**: Cleaned and standardized data models
3. **Core Layer**: Dimensional model (Star Schema) with facts and dimensions
4. **Mart Layer**: Analytical data models optimized for specific business domains

### Star Schema Design

The project implements a Star Schema for the core layer:

- **Fact tables**: Orders and Order Items
- **Dimension tables**: Customers, Products, and Date

### Data Mart Layers

The data mart is structured around these key analytical areas:

- **Dimensions**: Enhanced business entities with additional attributes
- **Facts**: Aggregated facts at various levels of granularity
- **Metrics**: Pre-calculated KPIs and business metrics

## Key Features

1. **Incremental Loading**: Optimized data loading for large tables
2. **Materialized Views**: Performance optimization for analytics queries
3. **Data Freshness Checks**: Monitoring data pipeline health
4. **Custom Metrics**: Business-specific calculations
5. **Performance Monitoring**: Tracking model build and run times

## Analytical Capabilities

This data mart enables the following analytics:

- **Sales Analysis**: Daily and monthly sales performance
- **Customer Behavior**: Retention, segmentation, and lifetime value
- **Product Performance**: Category analysis and inventory optimization
- **Cohort Analysis**: Customer retention by acquisition cohort

## Directory Structure

```
Ex3/
├── docker-compose.yml       # Docker configuration
├── profiles.yml             # dbt connection profiles
├── run.sh                   # Automation script
├── ecommerce_dbt/           # dbt project
│   ├── dbt_project.yml      # Project configuration
│   ├── packages.yml         # Dependencies
│   ├── models/              # Data models
│   │   ├── sources/         # Source definitions
│   │   ├── staging/         # Staging models
│   │   ├── core/            # Core dimensional models
│   │   └── mart/            # Data mart models
│   │       ├── dimensions/  # Enhanced dimensions
│   │       ├── facts/       # Aggregated facts
│   │       └── metrics/     # Business metrics
│   ├── macros/              # Reusable SQL logic
│   └── tests/               # Data quality tests
├── postgres/                # Database initialization
├── logs/                    # Runtime logs
└── reports/                 # Test reports and documentation
```

## Requirements

- Docker and Docker Compose
- dbt (data build tool) with PostgreSQL adapter
- Python 3.6+

## Getting Started

1. Clone the repository
2. Run the setup script:

```bash
./run.sh
```

3. Access the generated documentation:

```bash
cd ecommerce_dbt && dbt docs serve
```

4. Explore the data mart:

```bash
psql -h localhost -U dbt_user -d dbt_db_ex3 -p 5434
```

## Implementation Details

- **Incremental Models**: Orders and order_items tables use incremental loading
- **Materialized Views**: All mart models are materialized as tables for query performance
- **Data Refresh Policy**: Daily refresh for all fact tables
- **Monitoring**: Runtime logs and model statistics capture in reports/ 