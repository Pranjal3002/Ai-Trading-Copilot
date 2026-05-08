import { useState } from "react";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [charts, setCharts] = useState([]);

  const [signals, setSignals] = useState([]);

  const [futurePredictions, setFuturePredictions] = useState([]);

  const [loading, setLoading] = useState(false);


  const sendMessage = async () => {

    if (!question.trim()) return;

    const userMsg = {
      role: "user",
      text: question,
    };

    const updatedMessages = [...messages, userMsg];

    setMessages(updatedMessages);

    setQuestion("");

    setLoading(true);

    try {

      const res = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
          }),
        }
      );

      const data = await res.json();

      console.log(data);

      const aiMsg = {
        role: "assistant",
        text: data?.data?.response || "No response",
      };

      setMessages([...updatedMessages, aiMsg]);

      setCharts(data?.data?.charts || []);

      setSignals(data?.data?.signals || []);

      setFuturePredictions(
        data?.data?.future_predictions || []
      );

    } catch (err) {

      console.error(err);

      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          text: "Error connecting to backend",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>

      <h1>📈 AI Trading Copilot + ML</h1>

      {/* Signals */}
      <div style={styles.card}>

        <h2>AI Trading Signals</h2>

        {signals.map((sig, idx) => (

          <div key={idx} style={styles.signalBox}>

            <h3>{sig.symbol}</h3>

            <p>
              <b>Signal:</b> {sig.signal}
            </p>

            <p>
              <b>Confidence:</b> {sig.confidence}%
            </p>

            <p>
              <b>RSI:</b> {sig.rsi}
            </p>

            <p>
              <b>Market:</b> {sig.market_condition}
            </p>

          </div>

        ))}

      </div>

      {/* LSTM */}
      <div style={styles.card}>

        <h2>LSTM Future Predictions</h2>

        {futurePredictions.map((pred, idx) => (

          <div key={idx} style={styles.signalBox}>

            <h3>{pred.symbol}</h3>

            <p>
              <b>Predicted Next Price:</b>
              ${pred.predicted_price}
            </p>

          </div>

        ))}

      </div>

      {/* Charts */}
      {charts.map((chartItem, idx) => (

        <div key={idx} style={styles.card}>

          <h2>{chartItem.symbol} Stock Chart</h2>

          <Line
            data={{
              labels: chartItem.data.labels,
              datasets: [
                {
                  label: chartItem.symbol,
                  data: chartItem.data.prices,
                  borderColor: "#3b82f6",
                  tension: 0.3,
                },
              ],
            }}
          />

        </div>

      ))}

      {/* Chat */}
      <div style={styles.card}>

        <div style={styles.chatBox}>

          {messages.map((msg, i) => (

            <div
              key={i}
              style={{
                ...styles.message,
                alignSelf:
                  msg.role === "user"
                    ? "flex-end"
                    : "flex-start",
                background:
                  msg.role === "user"
                    ? "#2563eb"
                    : "#374151",
              }}
            >

              <b>
                {msg.role === "user"
                  ? "You"
                  : "AI"}
              </b>

              <div
                style={{
                  marginTop: "5px",
                  whiteSpace: "pre-wrap",
                }}
              >
                {msg.text}
              </div>

            </div>

          ))}

          {loading && <p>AI is thinking...</p>}

        </div>

        <div style={styles.inputArea}>

          <input
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            placeholder="Ask about stocks..."
            style={styles.input}
          />

          <button
            onClick={sendMessage}
            style={styles.button}
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

const styles = {

  container: {
    background: "#111827",
    minHeight: "100vh",
    color: "white",
    padding: "20px",
    fontFamily: "Arial",
  },

  card: {
    background: "#1f2937",
    padding: "20px",
    marginBottom: "20px",
    borderRadius: "10px",
  },

  signalBox: {
    background: "#374151",
    padding: "15px",
    borderRadius: "10px",
    marginBottom: "10px",
  },

  chatBox: {
    height: "350px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },

  message: {
    padding: "10px",
    borderRadius: "8px",
    maxWidth: "70%",
    lineHeight: "1.5",
  },

  inputArea: {
    display: "flex",
    marginTop: "10px",
    gap: "10px",
  },

  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "5px",
    border: "none",
    fontSize: "16px",
  },

  button: {
    padding: "10px 15px",
    background: "#2563eb",
    border: "none",
    color: "white",
    borderRadius: "5px",
    cursor: "pointer",
  },

};

export default App;