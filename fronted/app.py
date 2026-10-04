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

.stApp {
    background-color: #f5f7fb;
}

/* Main title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #172033;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #687386;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Section title */
.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #172033;
}

/* Prediction metrics */
[data-testid="stMetric"] {
    background-color: #eef8f2;
    padding: 18px;
    border-radius: 12px;
}

/* Button */
div.stButton > button {
    width: 100%;
    height: 48px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ffffff;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🚲 Bike Sharing Demand Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict daily bike rental demand using Machine Learning'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# BACKEND URL
# =========================================================

API_URL = (
    "https://bike-sharing-predicter-backend-dhuhvepp8-"
    "rat7050s-projects.vercel.app/predict"
)


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


# =========================================================
# MODEL MAPPING
# =========================================================

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

st.markdown(
    '<div class="section-title">'
    '📊 Enter Bike Sharing Information'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# =========================================================
# INPUT COLUMNS
# =========================================================

col1, col2 = st.columns(2, gap="large")


# =========================================================
# COLUMN 1 - DATE INFORMATION
# =========================================================

with col1:

    with st.container(border=True):

        st.subheader("📅 Date Information")

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
# COLUMN 2 - WEATHER INFORMATION
# =========================================================

with col2:

    with st.container(border=True):

        st.subheader("🌦️ Weather Information")

        workingday = st.selectbox(
            "Working Day",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes"
        )

        weathersit = st.selectbox(
            "Weather Situation",
            options=[1, 2, 3, 4],
            help=(
                "1: Clear, 2: Mist, "
                "3: Light Rain/Snow, "
                "4: Heavy Rain/Snow"
            )
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

st.write("")

predict_button = st.button(
    "🚀 Predict Bike Rentals",
    use_container_width=True,
    type="primary"
)


# =========================================================
# PREDICTION
# =========================================================

if predict_button:

    # -----------------------------------------------------
    # API PAYLOAD
    # -----------------------------------------------------

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

        # -------------------------------------------------
        # SEND REQUEST
        # -------------------------------------------------

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


            # =================================================
            # COMPARE ALL MODELS
            # =================================================

            if selected_model == "all":

                st.write("")
                st.subheader("📈 Model Comparison")

                predictions = result["predictions"]

                col1, col2, col3 = st.columns(3)


                # Multiple Linear Regression
                with col1:

                    with st.container(border=True):

                        st.metric(
                            "📊 Multiple Linear",
                            f"{predictions['multiple_linear_regression']:,.0f}"
                        )


                # Polynomial Regression
                with col2:

                    with st.container(border=True):

                        st.metric(
                            "📈 Polynomial",
                            f"{predictions['polynomial_regression']:,.0f}"
                        )


                # Random Forest Regression
                with col3:

                    with st.container(border=True):

                        st.metric(
                            "🌳 Random Forest",
                            f"{predictions['random_forest_regression']:,.0f}"
                        )


                st.write("")

                # Best model
                st.success(
                    f"🏆 Recommended Model: "
                    f"{result['best_model']}"
                )


                # Recommended prediction
                with st.container(border=True):

                    st.subheader("🎯 Recommended Prediction")

                    st.metric(
                        "🚲 Predicted Bike Rentals",
                        f"{result['recommended_prediction']:,.0f}"
                    )


            # =================================================
            # SINGLE MODEL
            # =================================================

            else:

                st.write("")
                st.subheader("🎯 Prediction Result")

                prediction = result["prediction"]

                with st.container(border=True):

                    st.success(
                        "Prediction completed successfully!"
                    )

                    st.metric(
                        f"🚲 {result['model']}",
                        f"{prediction:,.0f} bike rentals"
                    )


        # =================================================
        # API ERROR
        # =================================================

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            try:

                st.json(response.json())

            except Exception:

                st.write(response.text)


    # =====================================================
    # CONNECTION ERROR
    # =====================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI backend."
        )

        st.info(
            "The backend may be unavailable or protected "
            "by Vercel Authentication."
        )


    # =====================================================
    # TIMEOUT ERROR
    # =====================================================

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The backend request timed out."
        )


    # =====================================================
    # OTHER ERROR
    # =====================================================

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )


# =========================================================
# ABOUT THE MODELS
# =========================================================

st.write("")
st.divider()

st.subheader("🧠 About the Models")

st.write("")


col1, col2, col3 = st.columns(3, gap="medium")


# =========================================================
# MULTIPLE LINEAR REGRESSION
# =========================================================

with col1:

    with st.container(border=True):

        st.markdown("### 📊 Multiple Linear")

        st.write(
            "Uses multiple input features "
            "to predict bike rental demand."
        )


# =========================================================
# POLYNOMIAL REGRESSION
# =========================================================

with col2:

    with st.container(border=True):

        st.markdown("### 📈 Polynomial")

        st.write(
            "Captures nonlinear relationships "
            "between features and demand."
        )


# =========================================================
# RANDOM FOREST
# =========================================================

with col3:

    with st.container(border=True):

        st.markdown("### 🌳 Random Forest")

        st.write(
            "Uses multiple decision trees "
            "to improve prediction performance."
        )


# =========================================================
# FOOTER
# =========================================================

st.write("")
st.divider()

st.caption(
    "🚲 Bike Sharing Demand Prediction • "
    "Machine Learning • FastAPI • Streamlit"
)

st.markdown(
    "<center>Built by <b>Ratnesh Kumar</b> ❤️</center>",
    unsafe_allow_html=True
)
