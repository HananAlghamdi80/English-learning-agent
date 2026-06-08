# English Learning Agent

AI-powered English learning assistant for Saudi tech learners.

## Features

* English conversation practice
* Grammar correction and feedback
* Job interview role-play
* English level assessment
* Daily learning tasks
* Learner profile management
* Progress tracking
* Long-term memory using SQLite
* RAG knowledge base

## Technologies

* Python
* Streamlit
* OpenAI API
* SQLite
* Docker
* Kubernetes (Minikube)

## Project Architecture

User → Streamlit UI → AI Agent → RAG Knowledge Base → OpenAI API

User data and learning history are stored in SQLite for progress tracking and personalization.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Kubernetes Deployment

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

This project was containerized using Docker and deployed on Kubernetes using Minikube.
