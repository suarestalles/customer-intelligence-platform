# Customer Intelligence Platform

An end-to-end Customer Intelligence Platform built with **Python**, **FastAPI**, **DuckDB**, and **Machine Learning**, following modern Data Engineering and MLOps best practices.

> **Status:** 🚧 In Development

---

## 📖 Overview

The goal of this project is to simulate a real-world analytics platform used by an e-commerce company.

The platform will cover the complete data lifecycle:

* Data ingestion
* Data validation
* Data transformation
* Analytical Data Warehouse
* Machine Learning
* REST API
* Interactive Dashboard

The project is being developed incrementally, following software engineering best practices such as testing, containerization, type checking, linting and documentation.

---

# 🏗️ Current Architecture

```text
                        FastAPI
                           │
                           ▼
                    Health Endpoint
                           │
                           ▼
                 Configuration Layer
                           │
                           ▼
                 Logging & Lifespan
```

---

# 🚀 Tech Stack

## Backend

* Python 3.12
* FastAPI
* Uvicorn
* Pydantic Settings

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
├── data/
├── docker/
├── docs/
├── scripts/
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

## Running with Docker

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

## Phase 1 — Foundation

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

---

## Phase 2 — Data Engineering

* [ ] Dataset ingestion
* [ ] Data validation
* [ ] DuckDB integration
* [ ] Data Warehouse
* [ ] ETL pipeline

---

## Phase 3 — Analytics

* [ ] KPI API
* [ ] Customer metrics
* [ ] Sales metrics
* [ ] Product metrics

---

## Phase 4 — Machine Learning

* [ ] Feature engineering
* [ ] Customer segmentation
* [ ] Churn prediction
* [ ] Recommendation models

---

## Phase 5 — Dashboard

* [ ] Interactive dashboard
* [ ] KPI visualization
* [ ] Customer analytics

---

# 📄 License

This project is licensed under the MIT License.
