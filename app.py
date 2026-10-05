import streamlit as st

from utils.llm import ask_farmer_ai
from utils.weather import get_weather
from utils.dataset import load_dataset, search_dataset
from utils.recommendations import recommend_crops
from utils.disease_detection import analyze_plant_image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Farmer Assistant",
    page_icon="🌾",
    layout="wide"
)


# -----------------------------
# Load Datasets
# -----------------------------
CROP_DATA_PATH = "data/crop_data.csv"
DISEASE_DATA_PATH = "data/disease_data.csv"
FARMER_QA_PATH = "data/farmer_qa.csv"

crop_data = load_dataset(CROP_DATA_PATH)
disease_data = load_dataset(DISEASE_DATA_PATH)
farmer_qa = load_dataset(FARMER_QA_PATH)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🌾 AI Farmer Assistant")

menu = st.sidebar.radio(
    "Choose a feature:",
    [
        "🏠 Dashboard",
        "🤖 AI Farmer Chat",
        "🌦️ Weather",
        "🌱 Crop Recommendation",
        "📚 Crop & Disease Information"
    ]
)


# -----------------------------
# Dashboard
# -----------------------------
if menu == "🏠 Dashboard":

    st.title("🌾 AI Farmer Assistant")

    st.write(
        "A simple AI-powered assistant to help farmers "
        "with agriculture-related information."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🌱 Crop Records",
            len(crop_data)
        )

    with col2:
        st.metric(
            "🦠 Disease Records",
            len(disease_data)
        )

    with col3:
        st.metric(
            "❓ Farmer Q&A",
            len(farmer_qa)
        )

    st.divider()

    st.subheader("✨ Available Features")

    st.write("🤖 **AI Farmer Chat**")
    st.write(
        "Ask farming questions and get simple AI-generated answers."
    )

    st.write("🌦️ **Weather Information**")
    st.write(
        "Check current weather information for your city."
    )

    st.write("🌱 **Crop Recommendation**")
    st.write(
        "Get crop suggestions based on soil, season and state."
    )

    st.write("📚 **Crop & Disease Information**")
    st.write(
        "Search agricultural information from the local datasets."
    )


# -----------------------------
# AI Farmer Chat
# -----------------------------
elif menu == "🤖 AI Farmer Chat":

    st.title("🤖 AI Farmer Chat")

    st.write(
        "Ask your farming-related question below."
    )

    question = st.text_area(
        "Enter your question:",
        placeholder=(
            "Example: Which crop is suitable for black soil?"
        )
    )

    if st.button("Ask AI", type="primary"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("AI is thinking..."):

                answer = ask_farmer_ai(question)

            st.subheader("🌾 AI Answer")

            st.write(answer)


# -----------------------------
# Weather
# -----------------------------
elif menu == "🌦️ Weather":

    st.title("🌦️ Weather Information")

    city = st.text_input(
        "Enter your city:",
        placeholder="Example: Hyderabad"
    )

    if st.button("Get Weather", type="primary"):

        if not city.strip():

            st.warning("Please enter a city.")

        else:

            with st.spinner("Getting weather information..."):

                weather = get_weather(city)

            if weather["success"]:

                st.success(
                    f"Weather information for "
                    f"{weather['city']}, {weather['country']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "🌡️ Temperature",
                        f"{weather['temperature']} °C"
                    )

                with col2:
                    st.metric(
                        "💧 Humidity",
                        f"{weather['humidity']}%"
                    )

                with col3:
                    st.metric(
                        "🌬️ Wind Speed",
                        f"{weather['wind_speed']} m/s"
                    )

                st.write(
                    f"**Feels like:** "
                    f"{weather['feels_like']} °C"
                )

                st.write(
                    f"**Weather:** "
                    f"{weather['description'].title()}"
                )

                st.write(
                    f"**Pressure:** "
                    f"{weather['pressure']} hPa"
                )

            else:

                st.error(weather["message"])


# -----------------------------
# Crop Recommendation
# -----------------------------
elif menu == "🌱 Crop Recommendation":

    st.title("🌱 Crop Recommendation")

    st.write(
        "Select the available information to get crop suggestions."
    )

    col1, col2 = st.columns(2)

    with col1:

        soil_type = st.selectbox(
            "Soil Type",
            [
                "",
                "clay",
                "loamy",
                "black",
                "sandy"
            ]
        )

        season = st.selectbox(
            "Season",
            [
                "",
                "monsoon",
                "kharif",
                "winter"
            ]
        )

    with col2:

        state = st.selectbox(
            "State",
            [
                "",
                "Telangana",
                "Andhra Pradesh",
                "Karnataka",
                "Maharashtra",
                "Punjab",
                "Haryana"
            ]
        )

    if st.button(
        "Recommend Crops",
        type="primary"
    ):

        results = recommend_crops(
            crop_data,
            soil_type,
            season,
            state
        )

        if results:

            st.subheader("🌾 Recommended Crops")

            for row in results:

                st.success(
                    f"**{row.get('crop', 'Unknown')}**"
                )

                st.write(
                    f"Soil: {row.get('soil_type', '-')}"
                )

                st.write(
                    f"Temperature: "
                    f"{row.get('temperature', '-')} °C"
                )

                st.write(
                    f"Humidity: "
                    f"{row.get('humidity', '-')}%"
                )

                st.write(
                    f"Rainfall: "
                    f"{row.get('rainfall', '-')} mm"
                )

                st.write(
                    f"Season: "
                    f"{row.get('season', '-')}"
                )

                st.write(
                    f"State: "
                    f"{row.get('state', '-')}"
                )

                st.divider()

        else:

            st.warning(
                "No matching crop found in the dataset."
            )


# -----------------------------
# Crop & Disease Information
# -----------------------------
elif menu == "📚 Crop & Disease Information":

    st.title("📚 Crop & Disease Information")

    # ---------------------------------
    # Existing Search Feature
    # ---------------------------------

    search_term = st.text_input(
        "Search for crop, disease or farming information:",
        placeholder="Example: rice, tomato, blight"
    )

    if search_term.strip():

        st.subheader("🌱 Crop Information")

        crop_results = search_dataset(
            crop_data,
            search_term
        )

        if crop_results:

            for row in crop_results:

                st.write(
                    f"**Crop:** {row.get('crop', '-')}"
                )

                st.write(
                    f"**Soil:** {row.get('soil_type', '-')}"
                )

                st.write(
                    f"**Season:** {row.get('season', '-')}"
                )

                st.write(
                    f"**State:** {row.get('state', '-')}"
                )

                st.divider()

        else:

            st.info(
                "No crop information found."
            )

        st.subheader("🦠 Disease Information")

        disease_results = search_dataset(
            disease_data,
            search_term
        )

        if disease_results:

            for row in disease_results:

                st.write(
                    f"**Crop:** {row.get('crop', '-')}"
                )

                st.write(
                    f"**Disease:** {row.get('disease', '-')}"
                )

                st.write(
                    f"**Symptoms:** {row.get('symptoms', '-')}"
                )

                st.write(
                    f"**Cause:** {row.get('cause', '-')}"
                )

                st.write(
                    f"**Prevention:** {row.get('prevention', '-')}"
                )

                st.divider()

        else:

            st.info(
                "No disease information found."
            )

    else:

        st.info(
            "Enter a crop or disease name to search."
        )
        # ---------------------------------
        # NEW: Disease Image Detection
        # ---------------------------------
        
        st.divider()
        
        st.subheader("🦠 AI Disease Image Analysis")
        
        st.write(
            "Upload a plant image or capture an image using your camera."
        )
        
        # Upload image
        uploaded_image = st.file_uploader(
            "📤 Drag & Drop or Browse an Image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the affected plant or leaf."
        )
        
        st.write("### OR")
        
        # Capture image
        camera_image = st.camera_input(
            "📷 Capture Plant Image"
        )
        
        # Select whichever image the user provided
        image = (
            uploaded_image
            if uploaded_image is not None
            else camera_image
        )
        
        if image is not None:
        
            st.success("✅ Image selected successfully!")
        
            st.image(
                image,
                caption="Selected Plant Image",
                use_container_width=True
            )
        
            st.divider()
        
            if st.button(
                "🤖 Analyze Image with AI",
                type="primary"
            ):
        
                with st.spinner(
                    "🔍 AI is analyzing the plant image..."
                ):
        
                    result = analyze_plant_image(image)
        
                st.subheader("🌾 AI Analysis Result")
        
                st.write(result)