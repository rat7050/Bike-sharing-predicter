# 🚲 Bike Sharing Demand Predictor

A machine learning project that predicts **bike-sharing demand** using weather, season, calendar, and working-day information. The project compares multiple regression approaches and exposes the trained models through a **FastAPI backend** with a **Streamlit frontend**.

## 📌 Project Overview

Bike-sharing systems need accurate demand estimates to improve bike availability, fleet planning, and operational efficiency. This project uses historical bike-sharing data to learn the relationship between environmental and calendar features and the number of rented bikes.

The project supports three regression models:

- **Multiple Linear Regression**
- **Polynomial Regression (Degree 2)**
- **Random Forest Regression**

The prediction API can run an individual model or compare predictions from all three models. The current API recommends **Random Forest Regression** as the best model used by the application.

## ✨ Features

- 📊 Exploratory data analysis and preprocessing
- 🤖 Multiple regression models
- 🌲 Random Forest regression for nonlinear relationships
- 🔌 FastAPI prediction backend
- 🖥️ Streamlit user interface
- 🔄 Compare predictions from all models
- 💾 Saved models using Joblib
- ❤️ Health-check API endpoint
- 🧩 Modular backend, frontend, data, and model structure

## 🧠 Machine Learning Models

### 1. Multiple Linear Regression

Used as a simple and interpretable baseline model for understanding the relationship between input features and bike demand.

### 2. Polynomial Regression

A degree-2 polynomial model is used to capture nonlinear relationships that a simple linear model may miss.

### 3. Random Forest Regression

An ensemble of decision trees that can model complex nonlinear relationships and interactions between features. It is used as the recommended model in the prediction API.

## 📥 Input Features

The prediction system uses the following features:

| Feature | Description |
|---|---|
| `season` | Season category |
| `yr` | Year indicator |
| `mnth` | Month |
| `holiday` | Whether the day is a holiday |
| `weekday` | Day of the week |
| `workingday` | Whether the day is a working day |
| `weathersit` | Weather condition category |
| `temp` | Normalized temperature |
| `hum` | Normalized humidity |
| `windspeed` | Normalized wind speed |

## 🏗️ Project Structure

```text
Bike-sharing-predicter/
│
├── backend/
│   ├── main.py
│   └── models/
│       ├── multiple_linear_regression.pkl
│       ├── polynomial_regression_degree2.pkl
│       └── random_forest_regression.pkl
│
├── fronted/
│   └── app.py
│
├── data/
│   └── Bike Sharing dataset files
│
├── bike.ipynb
├── requirements.txt
└── README.md
```

## 🔄 Workflow

```text
Historical Bike Sharing Data
          ↓
Data Cleaning & Preprocessing
          ↓
Exploratory Data Analysis
          ↓
Feature Selection
          ↓
Train Regression Models
          ↓
Evaluate Models
          ↓
Save Models with Joblib
          ↓
FastAPI Backend
          ↓
Streamlit Frontend
          ↓
Bike Demand Prediction
```

## ⚙️ Tech Stack

- **Python**
- **Pandas** – data manipulation
- **NumPy** – numerical operations
- **Scikit-learn** – machine learning
- **Joblib** – model serialization
- **FastAPI** – REST API
- **Pydantic** – request validation
- **Uvicorn** – ASGI server
- **Streamlit** – frontend interface
- **Jupyter Notebook** – experimentation and analysis

The repository's dependency file includes FastAPI, Uvicorn, Streamlit, Requests, Scikit-learn, Pandas, NumPy, Joblib, and Pydantic.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rat7050/Bike-sharing-predicter.git
cd Bike-sharing-predicter
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Backend

Start the FastAPI server from the project root:

```bash
uvicorn backend.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### Health Check

```text
GET /health
```

Expected response:

```json
{
  "status": "healthy"
}
```

## 🧪 Prediction API

The main prediction endpoint is:

```text
POST /predict
```

Example request:

```json
{
  "season": 2,
  "yr": 1,
  "mnth": 6,
  "holiday": 0,
  "weekday": 2,
  "workingday": 1,
  "weathersit": 1,
  "temp": 0.6,
  "hum": 0.5,
  "windspeed": 0.2,
  "model": "random_forest"
}
```

### Available Models

```text
linear
polynomial
random_forest
all
```

Selecting `all` returns predictions from all three models and the application's recommended prediction.

## 🖥️ Run the Streamlit Frontend

After starting the FastAPI backend, open another terminal and run:

```bash
streamlit run fronted/app.py
```

The Streamlit application provides a user-friendly interface for entering bike-sharing conditions and obtaining predictions from the trained models.

> **Note:** Make sure the frontend is configured to use the correct FastAPI backend URL before running the application.

## 📊 Model Development

The main machine learning experimentation and analysis are contained in:

```text
bike.ipynb
```

The notebook can be used to inspect the dataset, perform preprocessing and exploratory analysis, train regression models, and evaluate model performance.

## 🎯 Use Cases

This type of prediction system can support:

- Bike fleet allocation
- Demand forecasting
- Station-level planning
- Operational resource planning
- Seasonal demand analysis
- Weather-aware bike availability planning

## 🔮 Future Improvements

- Add more regression algorithms such as Gradient Boosting, XGBoost, and HistGradientBoosting
- Add model evaluation metrics such as MAE, MSE, RMSE, and R² to the application
- Add visual comparison of model performance
- Add prediction confidence/uncertainty information
- Add historical demand charts
- Improve feature engineering with date/time variables
- Containerize the application with Docker
- Deploy the FastAPI backend and Streamlit frontend
- Add automated model retraining
- Add API authentication and production monitoring

## 📸 Demo

Add screenshots of the Streamlit application here:

```markdown
![Bike Sharing Predictor Demo](path/to/your-screenshot.png)
```

For example, you can create an `images` folder:

```text
images/
└── bike-predictor-demo.png
```

Then use:

```markdown
![Bike Sharing Predictor Demo](images/bike-predictor-demo.png)
```

## 👨‍💻 Author

**Ratnesh Kumar**

B.Tech – Artificial Intelligence & Data Science

GitHub: [@rat7050](https://github.com/rat7050)

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

**Built with Python, Machine Learning, FastAPI, and Streamlit.**