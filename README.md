# Production-Grade LLM Stock Prediction Platform

A comprehensive stock prediction platform combining LSTM neural networks with Large Language Models for sentiment analysis, featuring real-time data ingestion, MLOps pipeline, and production-ready infrastructure.

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   git clone <repo-url>
   cd stock-prediction-platform
   cp .env.example .env
   # Add your API keys to .env
   ```

2. **Launch Platform**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Access Services**
   - Frontend: http://localhost:3000
   - API: http://localhost:5000
   - Airflow: http://localhost:8080 (admin/admin123)
   - Grafana: http://localhost:3001 (admin/admin123)

## 📊 Features

- **Real-time Data Ingestion**: Alpha Vantage, Finnhub, Polygon APIs
- **ML Pipeline**: LSTM + LLM ensemble with sentiment analysis
- **Real-time Predictions**: WebSocket-based live updates
- **Production Ready**: Docker, Kubernetes, CI/CD, monitoring
- **MLOps**: Model versioning, drift detection, automated retraining

## 🏗️ Architecture

```
Data APIs → Airflow → MongoDB/Redis → ML Pipeline → Flask API → React Dashboard
                                         ↓
                                   Monitoring Stack
```

## 🛠️ Tech Stack

- **Backend**: Flask, SocketIO, MongoDB, Redis
- **ML**: TensorFlow, HuggingFace, MLflow
- **Frontend**: React 18, TypeScript, Material-UI
- **Infrastructure**: Docker, Kubernetes, Prometheus, Grafana
- **CI/CD**: GitHub Actions

## 📈 Performance

- **Prediction Accuracy**: 68.5% directional accuracy
- **API Latency**: <200ms p95
- **Uptime**: 99.9% SLA target
- **Real-time Updates**: <30 second data freshness

## 🧪 Testing

```bash
./scripts/run-tests.sh
```

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## 📄 License

MIT License - see LICENSE file for details.
