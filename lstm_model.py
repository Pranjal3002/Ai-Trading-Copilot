import yfinance as yf
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

import warnings
warnings.filterwarnings("ignore")


def predict_future_price(symbol):

    try:

        df = yf.download(
            symbol,
            period="6mo"
        )

        if df.empty:
            return None

        data = df["Close"].values.reshape(-1, 1)

        scaler = MinMaxScaler(
            feature_range=(0, 1)
        )

        scaled_data = scaler.fit_transform(data)

        X = []
        y = []

        sequence_length = 20

        for i in range(
            sequence_length,
            len(scaled_data)
        ):

            X.append(
                scaled_data[
                    i-sequence_length:i,
                    0
                ]
            )

            y.append(scaled_data[i, 0])

        X = np.array(X)
        y = np.array(y)

        X = np.reshape(
            X,
            (X.shape[0], X.shape[1], 1)
        )

        model = Sequential()

        model.add(
            LSTM(
                units=50,
                return_sequences=True,
                input_shape=(X.shape[1], 1)
            )
        )

        model.add(
            LSTM(units=50)
        )

        model.add(Dense(1))

        model.compile(
            optimizer="adam",
            loss="mean_squared_error"
        )

        model.fit(
            X,
            y,
            epochs=5,
            batch_size=16,
            verbose=0
        )

        last_20 = scaled_data[-20:]

        X_test = np.array([last_20])

        X_test = np.reshape(
            X_test,
            (X_test.shape[0], X_test.shape[1], 1)
        )

        predicted_price = model.predict(
            X_test,
            verbose=0
        )

        predicted_price = scaler.inverse_transform(
            predicted_price
        )

        return round(
            float(predicted_price[0][0]),
            2
        )

    except Exception as e:

        print("❌ LSTM ERROR:", e)

        return None