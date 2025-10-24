
# ⚙️ Quasar — Setup & Development Guide

This guide explains how to install and start **Quasar** from scratch, including linting, type-checking, and CI configuration.

---

## 🧩 Prerequisites

Make sure you have installed:

- **Python 3.11+**
- **pip** (comes with Python)
- **[uv](https://github.com/astral-sh/uv)** (`pip install uv`)
- **Git**
- **Docker Desktop** *(optional, if you use MongoDB/Redis containers)*

---

## 📦 Clone the Project

```bash
git clone https://github.com/andreadeluca/Quasar.git
cd Quasar
```

To work on a specific branch:

```bash
git checkout dev
```

---

## 🧰 Install Dependencies

```bash
pip install uv
uv sync --all-extras --dev
```

This will:
- create a virtual environment automatically
- install all dependencies from `pyproject.toml`
- include development dependencies (`--dev`)

---

## 🚀 Run the Application

```bash
uv run python -m quasar
```

or if you have a `main.py` entrypoint:

```bash
uv run python quasar/main.py
```

---

## 🧹 Lint & Type Checking

### Ruff (lint + auto-fix)
```bash
uv run ruff check --fix .
```

### Mypy (type checking)
```bash
uv run mypy quasar
```

---

## 🧪 Testing (if tests are present)

```bash
uv run pytest
```

---

## 🧱 Docker (optional)

If a `docker-compose.yml` exists:

```bash
docker compose up --build
```

To follow logs in real-time:
```bash
docker compose logs -f
```

---

## 🔁 Continuous Integration (GitHub Actions)

The workflow file is located at `.github/workflows/ci.yml`.  
It runs lint and mypy **only on merge or pull request to `main`**.

### CI File Snippet

```yaml
on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]
```

---

## 🪄 Pre-commit Hooks (optional but recommended)

To automatically run lint before committing:

```bash
pip install pre-commit
pre-commit install
```

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.1
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
```

---

## 🧭 Quick Recap

```bash
# 1. Install
pip install uv
uv sync --all-extras --dev

# 2. Lint & Type Check
uv run ruff check --fix .
uv run mypy quasar

# 3. Run Backend
uv run python -m quasar

# 4. (Optional) Docker
docker compose up --build
```

