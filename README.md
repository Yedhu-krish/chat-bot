# AIBOT

A full-stack AI chatbot application built with **FastAPI**, **PostgreSQL**, **Celery**, **Redis**, and **Ollama**.

The application supports user authentication, conversations, document processing, and AI-powered question answering using locally hosted LLMs.

## Features

* User registration and JWT-based authentication
* Conversation and message management
* PDF document upload and processing
* AI-powered document Q&A
* Background document processing with Celery
* Redis as Celery broker
* Local LLM inference using Ollama
* PostgreSQL database with pgvector support
* Streaming AI responses
* Dockerized backend services
* Automated CI/CD with GitHub Actions
* AWS ECR for container images
* AWS Systems Manager (SSM) for EC2 deployment
* Frontend deployment through Cloudflare Pages

## Tech Stack

**Backend**

* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* pgvector
* Celery
* Redis
* JWT
* Ollama

**Frontend**

* React
* Vite

**DevOps / Cloud**

* Docker & Docker Compose
* GitHub Actions
* AWS ECR
* AWS EC2
* AWS Systems Manager (SSM)
* AWS IAM / GitHub OIDC
* Cloudflare Pages

## Architecture

```text
                    GitHub
                       │
                       ▼
              GitHub Actions
                       │
              ┌────────┴────────┐
              │                 │
             CI                CD
              │                 │
       Docker Build        AWS SSM
              │                 │
              ▼                 ▼
             ECR               EC2
                                │
                    ┌───────────┼───────────┐
                    │           │           │
                 Backend      Celery      Redis
                    │           │
                    └──────┬────┘
                           │
                       PostgreSQL
                           │
                         pgvector

Frontend ───────────────► Cloudflare Pages
```

## CI/CD

Every push to `main` triggers the deployment pipeline.

### CI

1. GitHub Actions authenticates with AWS using OIDC.
2. Docker image is built.
3. Image is tagged using the Git commit SHA.
4. Image is pushed to Amazon ECR.

### CD

1. GitHub Actions sends a deployment command through AWS Systems Manager.
2. EC2 authenticates with ECR using its IAM role.
3. The new image is pulled from ECR.
4. Backend and Celery containers are recreated.
5. Old unused AIBOT Docker images are cleaned up.

The frontend is deployed separately through Cloudflare Pages. Changes pushed to the `frontend` directory trigger a new frontend build and deployment.

## Running Locally

### Backend

```bash
git clone https://github.com/Yedhu-krish/chat-bot.git
cd chat-bot

uv sync
```

Configure the required environment variables in `.env`, then start the services:

```bash
docker compose up -d
```

The API will be available at:

```text
http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```text
app/
├── routes/
├── services/
├── schemas/
├── database/
├── security/
└── celery_app/

frontend/
├── src/
└── public/

alembic/
Dockerfile
compose.yaml
```

## Status

**Active project / portfolio application**

Built to explore production-style backend development, local LLM integration, asynchronous processing, containerization, and cloud deployment.
