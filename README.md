# Customer Intelligence Platform

An end-to-end Customer Intelligence Platform built with **Python**, **FastAPI**, **DuckDB**, and **Machine Learning**, following modern Data Engineering and MLOps best practices.

> **Status:** 🚧 In Development

---

# 📖 Overview

The goal of this project is to simulate a real-world customer analytics platform used by an e-commerce company.

The platform is being developed to cover the complete data lifecycle:

* Data ingestion
* Data validation
* Data transformation
* Analytical Data Warehouse
* Machine Learning pipelines
* REST API
* Interactive Dashboard

The project combines **Software Engineering**, **Data Engineering**, and **Data Science** practices, following modern development standards such as:

* Automated testing
* Containerization
* Type checking
* Code formatting and linting
* Reproducible data pipelines
* Documentation

---

# 🏗️ Architecture

Current architecture:

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
                    Analytical Data Warehouse
                         (DuckDB)
                              │
                              ▼
                     Data Transformations
                              │
                              ▼
                           FastAPI
                              │
                              ▼
                         Dashboard Layer
```

The architecture is being developed incrementally, starting from the foundation layer and evolving toward a complete analytics platform.

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

## Machine Learning (Planned)

* Scikit-learn
* Feature Engineering pipelines
* Customer segmentation models
* Predictive analytics

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
│   └── warehouse/
│
├── data/
│   └── external/
│       └── olist/
│           └── raw/
│
├── scripts/
│
├── tests/
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

The project currently includes an ingestion pipeline responsible for downloading and organizing external datasets.

Implemented features:

* Dataset metadata modeling
* Dataset registry
* Dataset workspace management
* Automated file download
* Idempotent downloads
* Raw data organization

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

Download dataset:

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

# 🧪 Running Tests

```bash
uv run pytest
```

---

# 🎨 Formatting

```bash
uv run ruff format .
```

---

# 🔎 Lint

```bash
uv run ruff check .
```

---

# ✅ Type Checking

```bash
uv run mypy app
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

## Phase 2 — Data Engineering 🚧

* [x] Dataset ingestion pipeline
* [x] Dataset metadata models
* [x] Dataset registry
* [x] Raw data organization
* [x] Automated dataset download

Upcoming:

* [ ] DuckDB integration
* [ ] Raw data loading
* [ ] Data Warehouse modeling
* [ ] Data validation
* [ ] ETL pipeline

---

## Phase 3 — Analytics

* [ ] Analytical data models
* [ ] KPI generation
* [ ] Customer metrics
* [ ] Sales metrics
* [ ] Product metrics
* [ ] Analytics API endpoints

---

## Phase 4 — Machine Learning

* [ ] Feature engineering
* [ ] Customer segmentation
* [ ] Churn prediction
* [ ] Recommendation models
* [ ] Model evaluation pipeline

---

## Phase 5 — Dashboard

* [ ] Interactive dashboard
* [ ] KPI visualization
* [ ] Customer analytics
* [ ] Business intelligence views

---

# 🔮 Future Improvements

Possible future extensions:

* Data orchestration with Airflow or Dagster
* CI/CD pipelines
* Cloud deployment
* Data quality monitoring
* Model tracking and experiment management
* Real-time data ingestion

---

# 📄 License

This project is licensed under the MIT License.
