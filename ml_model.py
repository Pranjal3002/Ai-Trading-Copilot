import yfinance as yf
import ta
import pandas as pd
import traceback

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def predict_signal(symbol):

    try:

        print(f"🤖 Running ML model for {symbol}")

        # Download stock data
        df = yf.download(
            symbol,
            period="6mo",
            auto_adjust=True
        )

        if df.empty:
            print("❌ Empty dataframe")
            return None

        # Fix MultiIndex issue
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Ensure Close exists
        if "Close" not in df.columns:
            print("❌ Close column missing")
            return None

        # Convert Close to 1D Series
        close_prices = df["Close"].squeeze()

        # =========================
        # Technical Indicators
        # =========================

        # RSI
        rsi_indicator = ta.momentum.RSIIndicator(
            close=close_prices,
            window=14
        )

        df["RSI"] = rsi_indicator.rsi()

        # MACD
        macd_indicator = ta.trend.MACD(
            close=close_prices
        )

        df["MACD"] = macd_indicator.macd()

        # SMA
        sma_indicator = ta.trend.SMAIndicator(
            close=close_prices,
            window=14
        )

        df["SMA"] = sma_indicator.sma_indicator()

        # Remove NaN rows
        df.dropna(inplace=True)

        if len(df) < 30:
            print("❌ Not enough rows after indicators")
            return None

        # =========================
        # Create Target
        # =========================
        df["Target"] = (
            df["Close"].shift(-1) > df["Close"]
        ).astype(int)

        df.dropna(inplace=True)

        # Features
        features = ["RSI", "MACD", "SMA"]

        X = df[features]

        y = df["Target"]

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        # Model
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        model.fit(X_train, y_train)

        # Latest row prediction
        latest = X.iloc[-1:]

        prediction = model.predict(latest)[0]

        confidence = max(
            model.predict_proba(latest)[0]
        )

        signal = (
            "BUY"
            if prediction == 1
            else "SELL"
        )

        # RSI analysis
        latest_rsi = round(
            float(df["RSI"].iloc[-1]),
            2
        )

        market = (
            "Overbought"
            if latest_rsi > 70
            else "Oversold"
            if latest_rsi < 30
            else "Neutral"
        )

        print("✅ ML prediction success")

        return {
            "symbol": symbol,
            "signal": signal,
            "confidence": round(confidence * 100, 2),
            "rsi": latest_rsi,
            "market_condition": market,
        }

    except Exception as e:

        print("❌ ML ERROR:")
        traceback.print_exc()

        return None