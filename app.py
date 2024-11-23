import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Fleet Efficiency Insights with Gemini-Pro",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Load the Google API Key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Function to call Gemini-Pro AI for fleet insights
def get_fleet_insights(fleet_data):
    # Send fleet data to Gemini-Pro to get insights
    user_prompt = f"Provide insights on the fleet based on the following data: {fleet_data}"
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    return gemini_response.text

# Sidebar - Project Information and Features
with st.sidebar:
    st.title("🚗 Fleet Efficiency Insights")
    st.header("About the Project")
    st.write("""
        This app analyzes fleet efficiency data for transportation organizations in India. 
        By leveraging **Gemini-Pro AI**, it generates insights related to fleet management, 
        staff productivity, accident risks, and fleet age. This app helps optimize the overall 
        efficiency of road transport undertakings by identifying key areas for improvement.
    """)
    
    st.header("Key Features")
    st.write("""
    - **Fleet Data Analysis**: Enter fleet data like fleet efficiency, fleet age, staff productivity, and accidents to get insights.
    - **AI-powered Insights**: Powered by **Gemini-Pro AI** to provide actionable insights based on the entered fleet data.
    - **Chatbot Functionality**: Ask questions and get real-time responses from the chatbot regarding fleet management and recommendations.
    - **Data Visualization**: Display the fleet data entered by the user in an easy-to-read format.
    """)
    
# Display the chatbot's title on the page
st.title("FleetFusion AI: Efficiency Through Intelligence")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input fields to collect fleet data from the user
st.subheader("Enter Fleet Data for Analysis:")

fleet_efficiency = st.number_input("Average Fleet Efficiency (%)", min_value=0, max_value=100, value=89)
fleet_age = st.number_input("Age of Fleet (Years)", min_value=0, max_value=50, value=15)
staff_productivity = st.number_input("Staff Productivity (Total Staff)", min_value=0, value=709232)
accidents = st.number_input("Total Number of Accidents", min_value=0, value=1250)

fleet_data = {
    "fleet_efficiency": fleet_efficiency,
    "fleet_age": fleet_age,
    "staff_productivity": staff_productivity,
    "accidents": accidents
}

# Display a summary of the entered data
st.write(f"### Fleet Data Summary:")
st.json(fleet_data)

# If the user has entered data, fetch insights from Gemini-Pro
if st.button("Get Fleet Insights"):
    fleet_insights = get_fleet_insights(fleet_data)
    
    # Display the insights from Gemini-Pro AI
    st.subheader("Fleet Insights from Gemini-Pro AI:")
    st.markdown(fleet_insights)

# Input field for user's general message to interact with Gemini-Pro
user_prompt = st.chat_input("Ask Gemini-Pro about Fleet Data...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
