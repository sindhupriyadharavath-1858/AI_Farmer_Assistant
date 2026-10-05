# 🌾 AI Farmer Assistant

AI Farmer Assistant is an AI-powered agriculture application designed to help farmers with useful and simple farming information.

## 🚀 Features

- 🤖 AI Farmer Chat using Groq
- 🌦️ Real-time weather information
- 🌱 Crop recommendation
- 📚 Crop information
- 🦠 Disease information
- 📊 CSV-based agricultural datasets

## 🛠️ Technologies Used

- Python
- Streamlit
- Groq API
- OpenWeatherMap API
- CSV Datasets

## 📁 Project Structure

```text
AI Farmer Assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── data/
│   ├── crop_data.csv
│   ├── disease_data.csv
│   └── farmer_qa.csv
│
└── utils/
    ├── __init__.py
    ├── dataset.py
    ├── llm.py
    ├── weather.py
    └── recommendations.py