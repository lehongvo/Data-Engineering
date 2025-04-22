# Data Engineering Bootcamp

## Prerequisites
- Experience in programming, specifically in backend development
- Database knowledge is a plus

## Modules & Free Resources

### Week 1: Setup & Fundamentals

#### Environment & Prerequisites
- Refresh your Python, SQL, and Linux command-line skills
  - Python courses on GitHub
  - SQL tutorials on Khan Academy
- Follow the bootcamp instructions in the GitHub repos to set up:
  - Docker
  - Git/GitHub
  - Cloud free-tier (GCP/AWS/Azure)

#### Day 1: Docker and Docker Compose

##### Learning Content
- GCP Setup: Introduction to Google Cloud Platform (GCP) and creating an account
- Docker Setup: Installing Docker on your local machine and understanding Docker basics
- Git/GitHub Setup: Setting up Git and GitHub for version control
- Linux Command Line: Review essential Linux commands for data engineering

##### Exercises
1. Set up a Docker container that runs a simple web application (e.g., a "Hello World" app) and expose it to the internet.
2. Configure a cloud provider (GCP/AWS/Azure) and create a VM instance, ensuring you can SSH into it and deploy Docker containers.

#### Day 2: Python & SQL Fundamentals

##### Learning Content
- Python: Review Python basics, especially data structures, loops, and functions
- SQL: Refresh SQL skills, including SELECT, JOIN, GROUP BY, and WHERE clauses

##### Exercises
1. Write a Python script that reads a CSV file, processes the data (filtering, aggregating), and writes the output to a new CSV.
2. Write SQL queries to answer specific questions from a sample database (e.g., calculate the total revenue, find the top 10 customers, etc.).

#### Day 3: Docker and Docker Compose

##### Learning Content
- Docker: Learn how to create and manage Docker containers
- Docker Compose: Understand how to define multi-container environments
- Hands-on: Deploy PostgreSQL with Docker and interact with it using SQL

##### Exercises
1. Create a Dockerfile for a Python application and set up the required environment inside the container.
2. Build a multi-container environment using Docker Compose that includes a web application and a PostgreSQL database.

#### Day 4: Terraform for Infrastructure as Code

##### Learning Content
- Introduction to Terraform: Learn how Terraform works to manage infrastructure on cloud providers
- Hands-on: Use Terraform to create basic cloud resources (VM, storage, etc.)

##### Exercises
1. Write a Terraform script to create a virtual machine on GCP (or AWS/Azure).
2. Modify the script to provision a cloud storage bucket and set up appropriate access permissions.

#### Day 5: Review and Practice

##### Learning Content
- Review all topics from the week: Docker, Git/GitHub, Python, SQL, and Terraform
- Practice setting up and managing Docker containers, Terraform scripts, and basic SQL queries

##### Exercises
1. Build a Dockerized application with a PostgreSQL backend and deploy it using Terraform on a cloud provider.
2. Write a simple Python script that connects to your PostgreSQL database and performs basic CRUD operations.

### Week 2: Core Concepts

#### Containerization & Infrastructure as Code
- Learn Docker (many free YouTube tutorials exist)
- Basic Terraform (plenty of GitHub repos and free tutorials)

#### Workflow Orchestration & ETL
- Build simple pipelines using Apache Airflow or Prefect
- Free courses on YouTube and blog posts available

#### Day 6: Workflow Orchestration with Kestra

##### Learning Content
- Introduction to Workflow Orchestration: Learn the basics of data lakes and orchestration
- Kestra: Introduction to Kestra, a tool for managing workflows
- Hands-on: Create simple workflows with Kestra to move data between services

##### Exercises
1. Create a simple workflow in Kestra that ingests data from an API and stores it in a CSV file.
2. Add error handling to your Kestra workflow to manage failures.

#### Day 7: Data Warehousing with BigQuery

##### Learning Content
- BigQuery Overview: Learn about data warehouses and the importance of partitioning and clustering
- Hands-on: Create tables in BigQuery and run simple queries to analyze data

##### Exercises
1. Import a sample dataset into BigQuery and explore the dataset using SQL.
2. Use BigQuery's partitioning feature to manage large datasets.

#### Day 8: Batch Processing with Apache Spark

##### Learning Content
- Introduction to Apache Spark: Learn the fundamentals of Spark, including DataFrames and SparkSQL
- Hands-on: Work with DataFrames and perform basic operations

##### Exercises
1. Write a Spark program to load a CSV file, filter data, and perform basic transformations.
2. Save the processed data from Spark to a new CSV file, and then load it into a PostgreSQL database.

#### Day 9: Streaming with Kafka

##### Learning Content
- Introduction to Kafka: Learn Kafka basics, such as producers, consumers, and topics
- Hands-on: Create a simple Kafka producer and consumer to handle streaming data

##### Exercises
1. Set up a Kafka producer and consumer for real-time data streaming.
2. Create a Kafka stream that processes real-time data and performs aggregate operations.

#### Day 10: Review and Practice

##### Learning Content
- Review and practice all tools and concepts covered during the week

##### Exercises
1. Combine Apache Spark with Kafka for stream processing.
2. Create a simple end-to-end pipeline with Kestra, Kafka, and Spark.

### Week 3: Advanced Topics & Capstone

#### Day 11: Real-Time Streaming with Kafka and Flink

##### Learning Content
- Kafka Streams: Learn how to use Kafka Streams for real-time data processing
- Flink Basics: Introduction to Flink for real-time stream processing
- Hands-on: Set up a real-time streaming application

##### Exercises
1. Set up a Kafka producer and consumer with Flink for real-time processing.
2. Implement schema management with Avro for Kafka.

#### Day 12: Data Engineering with dbt

##### Learning Content
- Introduction to dbt: Learn about dbt for transforming and modeling data
- Hands-on: Set up dbt with PostgreSQL and BigQuery

##### Exercises
1. Set up a dbt project with PostgreSQL and create transformation models.
2. Use dbt to test your data transformation models.

#### Day 13: Final Project Setup

##### Learning Content
- Capstone Project Planning: Outline a full data pipeline
- Tools Setup: Set up required tools and services

##### Exercises
1. Define the use case for your final project.
2. Plan and sketch your architecture.

#### Day 14: Final Project Development

##### Learning Content
- Project Work: Develop your data pipeline
- Documentation: Document your process in GitHub

##### Exercises
1. Implement your data ingestion pipeline.
2. Implement data validation and quality checks.

#### Day 15: Final Project Review & Presentation

##### Learning Content
- Final Review: Complete the project
- Presentation: Prepare a demo of your project

##### Exercises
1. Complete and deploy your project.
2. Write comprehensive documentation.

## Resources
- GitHub: [data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- YouTube: [free_data_engineering_course](https://www.youtube.com/playlist?list=PL3MmuxUbc0IjHhLlBHKTqRyeONrzIcyLc)