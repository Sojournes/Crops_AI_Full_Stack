import React, { useState, useRef, useEffect } from "react";

export default function Chat({ setPlotData }) {
  const [messages, setMessages] = useState([
    {
      role: "model",
      parts: [
        {
          text: "Hello! I'm your Agricultural AI Advisor. How can I help you today?",
        },
      ],
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", parts: [{ text: input }] };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const history = messages.map((m) => ({
        role: m.role,
        parts: m.parts.map((p) => p.text), // Simplify for API
      }));

      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.parts[0].text,
          history: history, // This assumes backend handles simplified history or we format it correctly
        }),
      });

      const data = await response.json();

      if (data.response) {
        setMessages((prev) => [
          ...prev,
          { role: "model", parts: [{ text: data.response }] },
        ]);

        // Simple heuristic to extract potential plot data from text or add a separate field in backend
        // For now, let's assume if response mentions "market data", we might fetch visualization
        // tailored to the context. Or backend could return it.
        // Let's implement a direct fetch for viz if needed.
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "model",
            parts: [{ text: "Error: No response from server." }],
          },
        ]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "model", parts: [{ text: "Error connecting to server." }] },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card chat-container">
      <h2>AI Assistant</h2>
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.parts[0].text.split("\n").map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        ))}
        {loading && <div className="message model loading">Thinking...</div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask about crops..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
