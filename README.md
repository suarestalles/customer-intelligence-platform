# Customer Intelligence Platform

An end-to-end **Customer Intelligence Platform** built with **Python, FastAPI, DuckDB, SQL, Streamlit, and Data Analytics**, combining Software Engineering, Data Engineering, Analytics Engineering, and Business Intelligence practices.

> **Status:** 🚀 MVP — Analytics Platform with Data Quality, automated testing, CI/CD, Docker, production-oriented configuration, health checks, and observability foundations

---

# 📖 Overview

The **Customer Intelligence Platform** is a portfolio project designed to simulate a real-world analytics platform for an e-commerce company.

The project follows the complete analytical data flow:

```text
External Dataset
      ↓
Data Ingestion
      ↓
Raw Data
      ↓
DuckDB
      ↓
Analytical Models
      ↓
Analytics API
      ↓
Streamlit Dashboard
```

The platform currently provides analytical capabilities for:

* Customer analytics
* Customer segmentation
* RFM analysis
* Customer cohort analysis
* Revenue analytics
* Product analytics
* Product category analysis
* KPI monitoring
* Interactive dashboard visualization
* Automated testing of analytical models and API endpoints

The project is being developed incrementally, with the goal of demonstrating how Data Engineering, Analytics, Backend Development, Testing, and Software Engineering can be combined into a single solution.

---

# 🏗️ Architecture

The current architecture separates data processing, analytical modeling, API access, and visualization.

```text
                        Public Dataset
                              │
                              ▼
                    Dataset Ingestion Pipeline
                              │
                              ▼
                         Raw Data Layer
                              │
                              ▼
                            DuckDB
                              │
                 ┌────────────┴─────────────┐
                 │                          │
                 ▼                          ▼
          Analytical Models          Customer Models
                 │                          │
                 ├── order_metrics           ├── customer_metrics
                 │                           └── customer_rfm
                 │                           └── customer_cohorts
                 └──────────────┬────────────┘
                                ▼
                         Analytics Repository
                                │
                                ▼
                          Analytics Service
                                │
                                ▼
                            FastAPI
                         ┌──────┴──────┐
                         │             │
                         ▼             ▼
                    Health/        Analytics
                   Readiness          API
                         │             │
                         └──────┬──────┘
                                ▼
                       Analytics API Client
                                │
                                ▼
                         Streamlit Dashboard
```

The application follows a layered architecture:

```text
Data Engineering
      ↓
DuckDB Analytical Layer
      ↓
Repository
      ↓
Service
      ↓
REST API
      ↓
Dashboard
```

This separation allows the analytical logic to remain independent from the visualization layer.

---

# 🚀 Tech Stack

## Backend

* Python 3.12
* FastAPI
* Uvicorn
* Pydantic
* Pydantic Settings

## Production Readiness & Observability

* Environment-based configuration
* Application lifecycle management
* Structured application logging
* Health checks
* Readiness checks
* Error handling
* Request logging
* CI quality gates

## Data Engineering

* DuckDB
* Polars
* SQL
* PyArrow
* Dataset ingestion pipeline

## Analytics

* Customer metrics
* Order metrics
* Revenue analytics
* Product analytics
* Product category analytics
* RFM analysis
* Customer segmentation

## Dashboard

* Streamlit
* Streamlit charts
* Reusable formatting utilities
* REST API integration

## Testing

* Pytest
* FastAPI TestClient
* Analytical model tests
* API endpoint tests
* Data quality assertions

## Development

* uv
* Ruff
* MyPy
* Pytest
* Pre-commit

## Infrastructure

* Docker
* Docker Compose

## Machine Learning — Planned

* Scikit-learn
* Feature engineering pipelines
* Predictive analytics
* Churn prediction
* Recommendation models

---

# 📂 Project Structure

```text
customer-intelligence-platform/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── health_routes.py
│   │       └── analytics_routes.py
│   │
│   ├── core/
│   │   ├── application.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── logging.py
│   │
│   ├── repositories/
│   │   └── analytics_repo.py
│   │
│   ├── schemas/
│   │   └── analytics_schema.py
│   │
│   ├── services/
│   │   └── analytics_service.py
│   │
│   └── main.py
│
├── dashboard/
│   ├── app.py
│   ├── api_client.py
│   ├── utils/
│   │   └── formatters.py
│   │
│   └── pages/
│       ├── customers.py
│       └── products.py
│       └── cohorts.py
│
├── pipelines/
│   ├── ingestion/
│   │   ├── models.py
│   │   ├── registry.py
│   │   ├── sources.py
│   │   ├── downloader.py
│   │   └── workspace.py
│   │
│   ├── analytics/
│   │   ├── order_metrics.py
│   │   ├── customer_metrics.py
│   │   └── customer_rfm.py
│   │
│   ├── quality/
│   │   ├── checks.py
│   │   └── contracts.py
│   │
│   └── warehouse/
│       └── database_config.py
│
├── data/
│   ├── external/
│   │   └── olist/
│   │       └── raw/
│   │
│   └── warehouse/
│       └── customer_intelligence.duckdb
│
├── scripts/
│   ├── download_dataset.py
│   ├── check_database.py
│   ├── check_data_quality.py
│   └── build_analytics.py
│
├── tests/
│   ├── analytics/
│   │   ├── test_customer_cohorts.py
│   │   ├── test_customer_metrics.py
│   │   ├── test_customer_rfm.py
│   │   └── test_order_metrics.py
│   │
│   ├── api/
│   │   ├── test_analytics.py
│   │   ├── test_cohorts.py
│   │   └── test_health.py
│   │
│   ├── pipelines/
│   │   └── ingestion/
│   │
│   └── warehouse/
│
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── .env.example
```

---

# ⚙️ Running the Project

## Clone the repository

```bash
git clone https://github.com/suarestalles/customer-intelligence-platform.git

cd customer-intelligence-platform
```

---

## Install dependencies

The project uses **uv** for Python version and dependency management.

```bash
uv sync
```

---

# 📥 Dataset Ingestion

The project includes an ingestion pipeline responsible for downloading and organizing external datasets.

Implemented capabilities include:

* Dataset metadata modeling
* Dataset registry
* Dataset workspace management
* Automated file download
* Idempotent downloads
* Raw data organization
* Dataset source abstraction

The current dataset is the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains information about:

* Customers
* Orders
* Products
* Sellers
* Payments
* Reviews
* Geolocation

Download the dataset:

```bash
uv run python scripts/download_dataset.py
```

The raw files are stored under:

```text
data/
└── external/
    └── olist/
        └── raw/
```

The ingestion process is designed to be **idempotent**, preventing unnecessary downloads when files already exist.

---

# 🗄️ Data Warehouse

The analytical database is implemented using **DuckDB**.

The database is stored at:

```text
data/warehouse/customer_intelligence.duckdb
```

The warehouse is organized into logical schemas.

## Raw Layer

The `raw` schema contains data loaded from the original dataset.

Examples:

```text
raw.customers
raw.orders
raw.order_items
raw.order_payments
raw.products
```

The Raw Layer preserves the source data structure and provides the foundation for analytical transformations.

---

# 📊 Analytics Layer

The `analytics` schema contains transformed and business-oriented models.

Current analytical models include:

```text
analytics.order_metrics
analytics.customer_metrics
analytics.customer_rfm
analytics.customer_cohorts
```

---

## Order Metrics

`analytics.order_metrics` provides an order-level analytical model.

The model consolidates information from multiple order-related datasets while avoiding duplication caused by one-to-many relationships.

Current metrics include:

* Order status
* Order timestamps
* Total items
* Product value
* Freight value
* Payment value

A key data-quality principle is that each `order_id` should appear exactly once in the analytical model.

---

## Customer Metrics

`analytics.customer_metrics` aggregates order-level information by customer.

Current metrics include:

* Total orders
* Total items
* Total spent
* Average order value
* First order date
* Last order date
* Customer lifetime days

---

# 🎯 RFM Analysis

The platform implements **RFM analysis** for customer segmentation.

RFM represents:

* **Recency** — how recently the customer purchased
* **Frequency** — how frequently the customer purchases
* **Monetary** — how much the customer spends

The resulting analytical model is:

```text
analytics.customer_rfm
```

It contains:

* Recency
* Frequency
* Monetary
* Recency score
* Frequency score
* Monetary score
* RFM score
* Customer segment

Current segments include:

```text
Champions
Loyal Customers
Potential Loyalists
At Risk
Lost
```

---

## Customer Cohorts

`analytics.customer_cohorts` provides a cohort-based view of customer retention.

Customers are grouped according to their first purchase month, allowing customer activity to be analyzed over subsequent months.

The model includes:

* Cohort month
* Months since first purchase
* Cohort size
* Retained customers
* Retention rate

The cohort model prevents duplicate customer activity within the same month and ignores orders without a purchase timestamp.

Example:

```text
Cohort Month   Month 0   Month 1   Month 2   Month 3
2024-01        100%      100%       0%       100%
2024-03        100%        0%     100%        0%

---

# 📡 Analytics API

The Analytics API exposes the analytical models through REST endpoints.

Base path:

```text
/api/v1/analytics
```

Interactive API documentation is available through Swagger:

```text
http://localhost:8000/docs
```

---

## KPI Analytics

```http
GET /api/v1/analytics/kpis
```

Provides:

* Total customers
* Total orders
* Total revenue
* Average order value

---

## Revenue Analytics

```http
GET /api/v1/analytics/revenue
```

Provides:

* Total revenue
* Total orders
* Average order value
* Monthly revenue
* Monthly order volume
* Monthly average order value

---

## Customer Segments

```http
GET /api/v1/analytics/segments
```

Provides aggregated information for each customer segment.

Current metrics include:

* Number of customers
* Average spending
* Average frequency
* Average recency

---

## Customer Analytics

```http
GET /api/v1/analytics/customers
```

Returns customer-level analytical information.

Supported parameters:

```text
segment
limit
offset
```

Example:

```http
GET /api/v1/analytics/customers?segment=Champions&limit=20
```

---

## Customer Details

```http
GET /api/v1/analytics/customer/{customer_id}
```

Returns detailed customer information including:

* Customer metrics
* RFM metrics
* Customer segment

---

## Customer Summary

```http
GET /api/v1/analytics/customers/summary
```

Provides aggregated customer indicators:

* Total customers
* Total revenue
* Average customer spend
* Average orders per customer

---

## Product Analytics

```http
GET /api/v1/analytics/products
```

Provides product-level analytical information.

Current metrics include:

* Product ID
* Product category
* Total items sold
* Total orders
* Product revenue
* Freight value
* Average item price

Supported parameters:

```text
category
limit
offset
```

Example:

```http
GET /api/v1/analytics/products?limit=10
```

---

## Product Categories

```http
GET /api/v1/analytics/products/categories
```

Provides aggregated analytics by product category.

Current metrics include:

* Total items
* Total orders
* Total revenue
* Total freight

---

# 🎨 Streamlit Dashboard

The project now includes an interactive dashboard built with **Streamlit**, consuming the Analytics API through a dedicated API client.

The dashboard is organized into analytical views.

## Overview

The main dashboard provides:

* Revenue
* Orders
* Customers
* Average Order Value
* Revenue over time
* Customer segment distribution

---

## Customer Analytics

The Customers page provides:

* Total customers
* Total revenue
* Average customer spend
* Average orders
* Customer segment distribution
* Customer-level analytical table
* Segment filtering

Customers can be filtered by RFM segment such as:

```text
Champions
Loyal Customers
Potential Loyalists
At Risk
Lost
```

---

## Product Analytics

The Products page provides:

* Total products
* Items sold
* Revenue
* Number of categories
* Revenue by category
* Top products
* Product-level metrics
* Category filtering

Product-level information includes:

* Product ID
* Category
* Revenue
* Items sold
* Orders
* Average price

---

# 🧩 Dashboard Formatting

The dashboard contains reusable formatting utilities to keep the presentation layer consistent across pages.

Current formatting capabilities include:

* Brazilian Real currency formatting
* Thousands separators
* Decimal precision control
* Integer formatting
* Date formatting
* Consistent presentation of analytical values

This keeps presentation concerns inside the dashboard layer rather than modifying the analytical values returned by the API.

For example:

```text
Raw API value
      ↓
Dashboard formatter
      ↓
User-friendly presentation
```

This separation allows the API to continue returning structured numerical and temporal data while the dashboard controls how those values are displayed to users.

---

# 🧱 Application Architecture

The backend follows a layered architecture:

```text
Route
  │
  ▼
Service
  │
  ▼
Repository
  │
  ▼
Database
  │
  ▼
DuckDB
```

### Routes

Responsible for:

* HTTP endpoints
* Request parameters
* Response models
* Dependency injection

### Services

Responsible for:

* Business logic
* Data transformation
* Response construction

### Repositories

Responsible for:

* SQL queries
* Data access
* DuckDB interaction

### Schemas

Responsible for:

* Response validation
* API contracts
* Data structures

### Dashboard API Client

Responsible for:

* Communication with the Analytics API
* Endpoint abstraction
* HTTP requests
* JSON response handling

### Dashboard

Responsible for:

* Data visualization
* User interaction
* Filtering
* Presentation formatting

This separation keeps the API, analytical database, and visualization layer independently maintainable.

---

# 🧪 Data Quality & Testing

Testing and data quality validation are core parts of the project architecture.

The project uses **Pytest** for automated testing and includes a dedicated **Data Quality framework** for validating the analytical warehouse.

## Automated Testing

Current testing areas include:

* Ingestion
  - Dataset models
  - Dataset registry
  - Dataset workspace
  - File downloading
  - Download idempotency
* Warehouse
  - DuckDB database operations
  - Database initialization
  - Data loading
* Analytics
  - Order-level aggregation
  - Prevention of duplicated order records
  - Customer-level aggregation
  - Customer lifetime calculations
  - RFM score generation
  - RFM segment generation
* API
  - Health endpoint
  - Analytics endpoints
  - KPI responses
  - Customer segment responses
  - Response structure validation
  - Response type validation
  - Analytical value validation
* Data Quality
  - Table existence
  - Table population
  - Column type contracts
  - Null checks
  - Uniqueness checks
  - Composite uniqueness
  - Foreign-key integrity
  - Non-negative financial values
  - Analytical model validation
  - Revenue reconciliation
  - Customer metric validation
  - RFM score and segment validation

Analytical tests use temporary DuckDB databases, allowing transformations to be tested in isolation without depending on the production warehouse.

API tests use FastAPI's `TestClient` to validate the application through the HTTP layer.

## Data Quality Framework

The Data Quality layer defines explicit contracts for the raw and analytical schemas.

The complete test suite is also executed automatically through GitHub Actions as part of the CI quality gate.

The framework validates:

```text
Raw Layer
   │
   ├── Schema existence
   ├── Table population
   ├── Column types
   ├── Null constraints
   ├── Uniqueness
   ├── Foreign keys
   └── Numeric constraints
            │
            ▼
Analytics Layer
   │
   ├── Schema existence
   ├── Table population
   ├── Column types
   ├── Uniqueness
   ├── Revenue reconciliation
   ├── Metric validity
   ├── Date consistency
   ├── Lifetime calculations
   ├── RFM scores
   └── Customer segmentation

Run the complete test suite:

```bash
uv run pytest
```

---

# 🎨 Formatting

The project uses **Ruff** for code formatting.

```bash
uv run ruff format .
```

---

# 🔎 Lint

Run:

```bash
uv run ruff check .
```

---

# ✅ Type Checking

Run:

```bash
uv run mypy app
```

---

# 🪝 Pre-commit

The project uses **pre-commit** to perform local validation before commits.

GitHub Actions provides an additional CI quality gate that validates every push and pull request.

Configured checks include:

* Ruff linting
* Ruff formatting
* Code quality checks

Run all hooks manually:

```bash
uv run pre-commit run --all-files
```

---

# 🐳 Running with Docker

Build the image:

```bash
docker compose build
```

Start the application:

```bash
docker compose up
```

Or rebuild after changes:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 📊 Running the Dashboard

With the Analytics API running, start Streamlit with:

```bash
uv run streamlit run dashboard/app.py
```

The dashboard will be available at the URL displayed by Streamlit, typically:

```text
http://localhost:8501
```

The dashboard communicates with the API through:

```text
ANALYTICS_API_URL
```

Example:

```env
ANALYTICS_API_URL=http://localhost:8000
```

---

# 🌱 Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
APP_NAME=Customer Intelligence Platform
APP_VERSION=0.1.0
ENVIRONMENT=development
LOG_LEVEL=INFO
ANALYTICS_API_URL=http://localhost:8000
```

---

# 🛣️ Roadmap

## Phase 1 — Foundation ✅

* [x] Project initialization with uv
* [x] FastAPI application
* [x] Environment configuration
* [x] Logging
* [x] Application lifespan
* [x] Health endpoint
* [x] Docker support
* [x] Docker Compose
* [x] Ruff configuration
* [x] MyPy configuration
* [x] Pytest configuration
* [x] Pre-commit integration

---

## Phase 2 — Data Engineering ✅

* [x] Dataset ingestion pipeline
* [x] Dataset metadata models
* [x] Dataset registry
* [x] Dataset workspace
* [x] Automated dataset download
* [x] Raw data organization
* [x] DuckDB integration
* [x] Raw data loading
* [x] Warehouse schemas
* [x] Data quality checks
* [x] Analytical transformations

---

## Phase 3 — Analytics API ✅

* [x] Order metrics
* [x] Customer metrics
* [x] RFM analysis
* [x] Customer segmentation
* [x] Customer cohort analysis
* [x] Analytics API
* [x] KPI endpoint
* [x] Revenue analytics
* [x] Monthly revenue analytics
* [x] Customer analytics
* [x] Customer detail endpoint
* [x] Customer summary endpoint
* [x] Customer cohort endpoint
* [x] Product analytics
* [x] Product category analytics
* [x] API client for dashboard integration
* [x] Response validation tests

---

## Phase 4 — Dashboard ✅

* [x] Streamlit dashboard foundation
* [x] API integration
* [x] KPI visualization
* [x] Revenue over time
* [x] Customer segmentation views
* [x] Customer analytics
* [x] Customer filtering
* [x] Customer cohort analysis
* [x] Customer retention visualization
* [x] Product analytics
* [x] Product category analysis
* [x] Product filtering
* [x] Reusable formatting utilities
* [x] Currency formatting
* [x] Number formatting
* [x] Date formatting

---

## Phase 5 — Quality & CI/CD ✅

* [x] Automated analytical model tests
* [x] Automated API tests
* [x] Data transformation validation
* [x] Response validation
* [x] Data quality validation
* [x] GitHub Actions
* [x] Automated linting
* [x] Automated type checking
* [x] Automated test execution
* [x] CI pipeline
* [x] Docker build validation

---

## Phase 6 — Production Readiness & Observability ✅

* [x] Application lifecycle management
* [x] Health check
* [x] Environment-based configuration
* [x] Application logging
* [x] Database abstraction
* [x] Readiness check
* [x] Structured logging
* [x] Request logging
* [x] Centralized error handling
* [x] Observability improvements
* [x] Production configuration hardening

---

## Phase 7 — Machine Learning 🚧

* [ ] Feature engineering
* [ ] Churn definition and labeling
* [ ] Training dataset generation
* [ ] Churn prediction model
* [ ] Model evaluation pipeline
* [ ] Prediction persistence
* [ ] Churn prediction API
* [ ] Dashboard integration
* [ ] Recommendation models

---

# 🔮 Future Improvements

The current MVP establishes the core analytical platform. Future iterations may include:

### Engineering

* [x] CI/CD pipeline
* [x] Automated test execution
* [x] Automated linting
* [x] Automated type checking
* [x] Docker build validation
* [ ] Automated API integration tests
* [ ] API contract testing
* [ ] Structured logging
* [ ] Request logging
* [ ] Centralized error handling
* [ ] Authentication and authorization

### Data Engineering

* [ ] Data quality monitoring
* [ ] Workflow orchestration with Airflow or Dagster
* [ ] Automated dataset refresh
* [ ] Cloud deployment
* [ ] Production-grade analytical database

### Dashboard

* [ ] Advanced business intelligence views
* [ ] Date-range filters
* [ ] Comparative KPIs
* [ ] Customer detail visualization
* [ ] More advanced interactive charts
* [ ] Export capabilities

### Machine Learning

* [ ] Feature engineering pipeline
* [ ] Churn prediction
* [ ] Customer lifetime value prediction
* [ ] Recommendation systems
* [ ] Experiment tracking
* [ ] Model registry
* [ ] Model monitoring

These features are intentionally outside the current MVP scope and will be introduced incrementally after the analytical foundation has been consolidated.

---

# 📌 Current MVP

The current MVP provides a complete analytical flow from raw data to business visualization:

```text
Public Dataset
      │
      ▼
Ingestion Pipeline
      │
      ▼
Raw Data
      │
      ▼
DuckDB
      │
      ▼
Analytics Models
      │
      ├── Order Metrics
      ├── Customer Metrics
      └── RFM
      └── Customer Cohorts
      │
      ▼
Analytics API
      │
      ├── KPIs
      ├── Revenue
      ├── Customers
      ├── Customer Segments
      ├── Customer Cohorts
      └── Products
      │
      ▼
Streamlit Dashboard
      │
      ├── Overview
      ├── Customer Analytics
      ├── Customer Cohorts
      └── Product Analytics
```

The platform currently demonstrates:

* Data ingestion
* Analytical data modeling
* DuckDB-based analytics
* Customer intelligence
* RFM segmentation
* Customer cohort analysis
* Customer retention analysis
* REST API development
* Dashboard development
* API-to-dashboard integration
* Data presentation and formatting
* Automated testing
* Data quality validation
* API response validation
* Automated development tooling
* Continuous integration with GitHub Actions
* Automated quality gates
* Environment-based application configuration
* Application lifecycle management
* Health checks
* Application logging
* Production-oriented architecture
* Containerization

The current MVP has established an automated quality gate through GitHub Actions, validating formatting, linting, type checking, automated tests, and data quality.

The project now includes a CI/CD validation pipeline through GitHub Actions, automatically validating formatting, linting, type checking, automated tests, and Docker image builds on pushes and pull requests.

With the analytical foundation, customer segmentation, cohort analysis, Data Quality framework, automated testing, containerization, CI/CD pipeline, and production-oriented architecture established, the next evolution of the project is the Machine Learning layer.

The Machine Learning phase will build predictive capabilities on top of the existing customer analytics foundation, starting with feature engineering and churn prediction.

---

# 📄 License

This project is licensed under the MIT License.
