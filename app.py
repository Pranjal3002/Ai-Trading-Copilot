from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import requests
import yfinance as yf

from ml_model import predict_signal
from lstm_model import predict_future_price

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🔥 AI Trading Copilot + ML + LSTM Started 🔥")


# =========================
# Request Model
# =========================
class QuestionRequest(BaseModel):
    question: str


# =========================
# Extract Symbols
# =========================
def extract_symbols(question):

    mapping = {
        "apple": "AAPL",
        "tesla": "TSLA",
        "microsoft": "MSFT",
        "amazon": "AMZN",
        "google": "GOOGL",
        "nvidia": "NVDA",
        "meta": "META",
    }

    question = question.lower()

    symbols = []

    for company, ticker in mapping.items():

        if company in question:
            symbols.append(ticker)

    return symbols


# =========================
# Ollama AI
# =========================
def ask_ollama(question):

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": question,
                "stream": False,
            },
        )

        data = response.json()

        return data.get(
            "response",
            "No response"
        )

    except Exception as e:

        print("OLLAMA ERROR:", e)

        return "Error talking to AI"


# =========================
# Chart Data
# =========================
def get_chart_data(symbol):

    try:

        stock = yf.Ticker(symbol)

        hist = stock.history(period="5d")

        if hist.empty:
            return None

        return {
            "labels": [
                str(date.date())
                for date in hist.index
            ],
            "prices": [
                round(price, 2)
                for price in hist["Close"].tolist()
            ]
        }

    except Exception as e:

        print("Chart Error:", e)

        return None


# =========================
# MAIN ENDPOINT
# =========================
@app.post("/ask")
def ask_question(req: QuestionRequest):

    question = req.question

    print(f"\n📩 Question: {question}")

    symbols = extract_symbols(question)

    ai_response = ask_ollama(question)

    charts = []

    signals = []

    future_predictions = []

    for symbol in symbols:

        print(f"📊 Processing {symbol}")

        chart = get_chart_data(symbol)

        signal = predict_signal(symbol)

        future_price = predict_future_price(symbol)

        if chart:

            charts.append({
                "symbol": symbol,
                "data": chart
            })

        if signal:

            signals.append(signal)

        if future_price:

            future_predictions.append({
                "symbol": symbol,
                "predicted_price": future_price
            })

    return {
        "success": True,
        "data": {
            "question": question,
            "symbols": symbols,
            "response": ai_response,
            "charts": charts,
            "signals": signals,
            "future_predictions": future_predictions,
        }
    }