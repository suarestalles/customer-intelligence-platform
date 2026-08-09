# Customer Intelligence Platform

An end-to-end Customer Intelligence Platform built with **Python**, **FastAPI**, **DuckDB**, and **Data Analytics**, following modern Software Engineering and Data Engineering practices.

> **Status:** 🚧 In Development

---

# 📖 Overview

The goal of this project is to simulate a real-world customer analytics platform used by an e-commerce company.

The platform is being developed incrementally to cover the complete data lifecycle:

* Data ingestion
* Raw data organization
* Data warehousing
* Data transformation
* Customer analytics
* Customer segmentation
* REST API
* Machine Learning
* Interactive Dashboard

The project combines **Software Engineering**, **Data Engineering**, and **Data Analytics** practices, following modern development standards such as:

* Automated testing
* Containerization
* Type checking
* Code formatting and linting
* Pre-commit hooks
* Reproducible data pipelines
* Layered architecture
* Documentation

---

# 🏗️ Architecture

The current data architecture is:

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
                ┌─────────────┴─────────────┐
                ▼                           ▼
         order_metrics              customer_metrics
                │                           │
                └─────────────┬─────────────┘
                              ▼
                       customer_rfm
                              │
                              ▼
                         Analytics API
                              │
                              ▼
                          Dashboard
```

The project is being developed incrementally, starting from the software foundation and evolving toward a complete customer analytics platform.

---

# 🚀 Tech Stack

## Backend

* Python 3.12
* FastAPI
* Uvicorn
* Pydantic Settings

## Data Engineering

* DuckDB
* Polars
* HTTPX
* SQL

## Analytics

* Customer metrics
* Order metrics
* RFM analysis
* Customer segmentation

## Machine Learning — Planned

* Scikit-learn
* Feature Engineering pipelines
* Predictive analytics
* Churn prediction
* Recommendation models

## Development

* uv
* Ruff
* MyPy
* Pytest
* Pre-commit

## Infrastructure

* Docker
* Docker Compose

---

# 📂 Project Structure

```text
customer-intelligence-platform/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── pipelines/
│   │
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
│   └── warehouse/
│       └── database.py
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
│   └── build_analytics.py
│
├── tests/
│   ├── analytics/
│   ├── ingestion/
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

## Run locally

```bash
uv run uvicorn app.main:app --reload
```

The application will be available at:

| URL                          | Description      |
| ---------------------------- | ---------------- |
| http://localhost:8000        | Root application |
| http://localhost:8000/docs   | Swagger UI       |
| http://localhost:8000/redoc  | ReDoc            |
| http://localhost:8000/health | Health Check     |

---

# 📥 Dataset Ingestion

The project includes an ingestion pipeline responsible for downloading and organizing external datasets.

Implemented features:

* Dataset metadata modeling
* Dataset registry
* Dataset workspace management
* Automated file download
* Idempotent downloads
* Raw data organization
* Dataset source abstraction

Current dataset:

**Brazilian E-Commerce Public Dataset by Olist**

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

The raw files are stored at:

```text
data/
└── external/
    └── olist/
        └── raw/
            ├── olist_customers_dataset.csv
            ├── olist_orders_dataset.csv
            ├── olist_products_dataset.csv
            └── ...
```

The ingestion process is designed to be **idempotent**. Existing files are not downloaded again unless explicitly requested.

---

# 🗄️ Data Warehouse

The project uses **DuckDB** as the analytical database.

The database is stored locally at:

```text
data/warehouse/customer_intelligence.duckdb
```

The current warehouse is organized into logical layers.

## Raw Layer

The `raw` schema contains data loaded from the original CSV files.

Examples:

```text
raw.customers
raw.orders
raw.order_items
raw.order_payments
```

The Raw Layer preserves the original dataset structure and acts as the foundation for analytical transformations.

---

# 📊 Analytics Layer

The `analytics` schema contains transformed and business-oriented datasets.

Current models:

```text
analytics.order_metrics
analytics.customer_metrics
analytics.customer_rfm
```

## Order Metrics

`analytics.order_metrics` provides an order-level analytical model.

The model consolidates information from:

```text
raw.orders
raw.order_items
raw.order_payments
```

while avoiding duplication caused by one-to-many relationships.

Current metrics include:

* Total items
* Product value
* Freight value
* Payment value
* Order status
* Order timestamps

A key data-quality rule is that each `order_id` must appear exactly once.

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

## RFM Analysis

The project currently implements **RFM analysis** for customer segmentation.

RFM represents:

* **Recency** — how recently the customer purchased
* **Frequency** — how frequently the customer purchases
* **Monetary** — how much the customer spends

The resulting model:

```text
analytics.customer_rfm
```

contains:

* Recency
* Frequency
* Monetary
* Recency score
* Frequency score
* Monetary score
* RFM score
* Customer segment

Current customer segments include:

```text
Champions
Loyal Customers
Potential Loyalists
At Risk
Lost
```

These segments will later be used by the API and dashboard layers.

---

# 🧪 Data Quality & Testing

The project uses **Pytest** to validate the ingestion, warehouse, and analytical layers.

Current tests cover:

* Dataset models
* Dataset ingestion
* File downloading
* DuckDB database operations
* Order-level transformations
* Customer-level transformations
* RFM calculations
* Data duplication prevention
* Analytical model integrity

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

The project uses **pre-commit** to automatically validate the code before commits.

Configured checks include:

* Ruff linting
* Ruff formatting
* Code quality checks

Run all hooks manually:

```bash
uv run pre-commit run --all-files
```

This helps prevent improperly formatted or invalid code from being committed to the repository.

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

---

# 🌱 Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
APP_NAME=Customer Intelligence Platform
VERSION=0.1.0
ENVIRONMENT=development
LOG_LEVEL=INFO
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

## Phase 3 — Analytics 🚧

* [x] Order metrics
* [x] Customer metrics
* [x] RFM analysis
* [x] Customer segmentation
* [ ] Analytics API endpoints
* [ ] KPI endpoints
* [ ] Revenue analytics
* [ ] Product analytics
* [ ] Customer analytics

---

## Phase 4 — Machine Learning

* [ ] Feature engineering
* [ ] Customer segmentation models
* [ ] Churn prediction
* [ ] Recommendation models
* [ ] Model evaluation pipeline

---

## Phase 5 — Dashboard

* [ ] Interactive dashboard
* [ ] KPI visualization
* [ ] Customer analytics
* [ ] Customer segmentation views
* [ ] Business intelligence views

---

# 🔮 Future Improvements

Possible future extensions:

* CI/CD pipelines
* Cloud deployment
* Data quality monitoring
* Workflow orchestration with Airflow or Dagster
* Model tracking and experiment management
* Real-time data ingestion
* Automated dataset refresh
* Production database
* Authentication and authorization

These features are intentionally kept outside the current scope until the core analytics platform is complete.

---

# 📄 License

This project is licensed under the MIT License.
