# Crops AI Full Stack Application 🌾🤖

AN AI-powered agricultural advisor that helps farmers select optimal crops based on soil conditions and market data.

## 🎥 Demo

![App Demo](demo.webp)

## 🚀 Features

- **AI Chat Advisor**: Conversational interface to query crop recommendations.
- **Market Insights**: Real-time visualization of market prices and demand.
- **Data-Driven**: key decisions based on Farmer Profiles and Market Research data.

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python, SQLite, Google GenAI SDK.
- **Frontend**: React, Vite, Recharts, Vanilla CSS.

## 📦 Installation

1.  **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd Crops_AI_Full_Stack
    ```

2.  **Backend Setup**:

    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

    - Create a `.env` file in `backend/` and add your `GOOGLE_API_KEY`.

3.  **Frontend Setup**:
    ```bash
    cd frontend
    npm install
    ```

## 🏃‍♂️ Usage

1.  Run the startup script:
    - **Windows**: Double-click `start_app.bat` or run `.\start_app.bat` in terminal.
2.  Open your browser to `http://localhost:5173`.

## 📂 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── genai_service.py
│   │   └── routers/
│   ├── requirements.txt
│   └── agriculture_optimization.db
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   └── package.json
└── start_app.bat
```
