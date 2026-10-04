import streamlit as st
import requests


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bike Sharing Prediction",
    page_icon="🚲",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}

.prediction-box {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #ddd;
    margin-top: 20px;
}

.prediction-value {
    font-size: 42px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">🚲 Bike Sharing Demand Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Predict daily bike rental demand using Machine Learning</div>',
    unsafe_allow_html=True
)


# =========================================================
# BACKEND URL
# =========================================================

API_URL = "http://127.0.0.1:8000/predict"


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Prediction Settings")

model = st.sidebar.selectbox(
    "Choose Prediction Model",
    [
        "Multiple Linear Regression",
        "Polynomial Regression",
        "Random Forest Regression",
        "Compare All Models"
    ]
)


# Convert frontend name to backend value

model_mapping = {
    "Multiple Linear Regression": "linear",
    "Polynomial Regression": "polynomial",
    "Random Forest Regression": "random_forest",
    "Compare All Models": "all"
}

selected_model = model_mapping[model]


# =========================================================
# INPUT SECTION
# =========================================================

st.subheader("📊 Enter Bike Sharing Information")

col1, col2 = st.columns(2)


# =========================================================
# COLUMN 1
# =========================================================

with col1:

    season = st.selectbox(
        "Season",
        options=[1, 2, 3, 4],
        help="1: Spring, 2: Summer, 3: Fall, 4: Winter"
    )

    yr = st.selectbox(
        "Year",
        options=[0, 1],
        format_func=lambda x: "2011" if x == 0 else "2012"
    )

    mnth = st.selectbox(
        "Month",
        options=list(range(1, 13))
    )

    holiday = st.selectbox(
        "Holiday",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )

    weekday = st.selectbox(
        "Weekday",
        options=list(range(7)),
        format_func=lambda x: [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ][x]
    )


# =========================================================
# COLUMN 2
# =========================================================

with col2:

    workingday = st.selectbox(
        "Working Day",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )

    weathersit = st.selectbox(
        "Weather Situation",
        options=[1, 2, 3, 4],
        help="1: Clear, 2: Mist, 3: Light Rain/Snow, 4: Heavy Rain/Snow"
    )

    temp = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01
    )

    hum = st.slider(
        "Humidity",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01
    )

    windspeed = st.slider(
        "Windspeed",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.01
    )


# =========================================================
# PREDICTION BUTTON
# =========================================================

st.divider()

predict_button = st.button(
    "🚀 Predict Bike Rentals",
    use_container_width=True,
    type="primary"
)


# =========================================================
# PREDICTION
# =========================================================

if predict_button:

    payload = {

        "season": season,
        "yr": yr,
        "mnth": mnth,
        "holiday": holiday,
        "weekday": weekday,
        "workingday": workingday,
        "weathersit": weathersit,
        "temp": temp,
        "hum": hum,
        "windspeed": windspeed,

        "model": selected_model
    }


    try:

        with st.spinner("Making prediction..."):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=30
            )


        # =================================================
        # SUCCESS
        # =================================================

        if response.status_code == 200:

            result = response.json()


            # =============================================
            # ALL MODELS
            # =============================================

            if selected_model == "all":

                st.subheader("📈 Model Comparison")

                predictions = result["predictions"]

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Multiple Linear",
                        f"{predictions['multiple_linear_regression']:,.0f}"
                    )

                with col2:

                    st.metric(
                        "Polynomial",
                        f"{predictions['polynomial_regression']:,.0f}"
                    )

                with col3:

                    st.metric(
                        "Random Forest 🏆",
                        f"{predictions['random_forest_regression']:,.0f}"
                    )


                st.success(
                    f"Recommended Model: "
                    f"{result['best_model']}"
                )


                st.markdown(
                    f"""
                    <div class="prediction-box">

                    <div>Recommended Prediction</div>

                    <div class="prediction-value">
                    {result['recommended_prediction']:,.0f}
                    </div>

                    <div>bike rentals</div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =============================================
            # SINGLE MODEL
            # =============================================

            else:

                st.subheader("🎯 Prediction Result")

                prediction = result["prediction"]

                st.markdown(
                    f"""
                    <div class="prediction-box">

                    <div>{result['model']}</div>

                    <div class="prediction-value">
                    {prediction:,.0f}
                    </div>

                    <div>Predicted Bike Rentals</div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # =================================================
        # API ERROR
        # =================================================

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.json(response.json())


    # =====================================================
    # CONNECTION ERROR
    # =====================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI backend."
        )

        st.info(
            "Start your backend using: "
            "`uvicorn app:app --reload`"
        )


    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The backend request timed out."
        )


    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Bike Sharing Demand Prediction • "
    "Multiple Linear Regression • "
    "Polynomial Regression • "
    "Random Forest Regression"
)