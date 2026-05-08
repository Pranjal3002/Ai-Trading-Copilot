# 📈 AI Trading Copilot

An AI-powered stock market analysis platform that combines Large Language Models (LLMs), Machine Learning, and Deep Learning to provide intelligent stock analysis, trading signals, visualizations, and future price forecasting.

---

# 🚀 Features

## 🤖 AI-Powered Stock Analysis
Uses Ollama + Llama3 to generate detailed financial insights and stock analysis in natural language.

### Example Queries
- Analyze Tesla stock
- Compare Apple and Microsoft stocks
- Predict NVIDIA future trend

---

## 📊 Real-Time Stock Charts
Fetches live market data using Yahoo Finance and visualizes stock performance through interactive charts.

---

## 📉 ML-Based Trading Signals
Machine Learning model predicts:
- BUY
- SELL

with:
- confidence score
- RSI analysis
- market condition insights

---

## 🧠 LSTM Future Price Prediction
Deep Learning LSTM model forecasts future stock prices using historical stock trends.

---

## ⚡ Multi-Stock Comparison
Supports comparison of multiple stocks in a single prompt.

### Example
```bash
Compare Tesla, Apple, and Microsoft stocks
```

---

# 🛠️ Tech Stack

## Frontend
- React.js
- Chart.js

## Backend
- FastAPI
- Python

## AI / ML
- Ollama (Llama3)
- Scikit-learn
- TensorFlow / Keras
- Random Forest
- LSTM Neural Networks

## Data Source
- Yahoo Finance API (yFinance)

---

# 🧩 System Architecture

```text
User Prompt
     ↓
React Frontend
     ↓
FastAPI Backend
     ↓
┌────────────────────────────┐
│  Ollama LLM Analysis       │
│  ML Trading Signal Model   │
│  LSTM Forecasting Model    │
│  Yahoo Finance API         │
└────────────────────────────┘
     ↓
AI Insights + Charts + Predictions
```

---

# 📂 Project Structure

```text
AI-Trading-Copilot/
│
├── frontend/
│
├── app.py
├── ml_model.py
├── lstm_model.py
├── requirements.txt
├── README.md
└── DEMO.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Pranjal3002/Ai-Trading-Copilot.git
```

---

## 2️⃣ Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend server:

```bash
uvicorn app:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

## 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at:

```text
http://localhost:3000
```

---

# 📸 Demo

View complete working screenshots and outputs here:

## 👉 [DEMO.md](DEMO.md)

---

# 📌 Sample Output

## Input

```text
Analyze Tesla stock
```

## Output
- AI-generated stock analysis
- Real-time stock chart
- BUY/SELL signal
- Confidence score
- RSI indicator
- LSTM future prediction

---

# 🔮 Future Improvements

- News sentiment analysis
- Portfolio optimization
- Risk scoring engine
- Transformer-based forecasting
- Cloud deployment (AWS)
- Real-time streaming market data
- Docker & Kubernetes deployment
- Multi-agent AI architecture

---

# 👨‍💻 Author

## Pranjal

AI/ML Engineer | Full Stack AI Developer

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.
