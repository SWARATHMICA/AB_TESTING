import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Simulated database for users and surveys
users_db = {
    "user1": "password123",
    "user2": "mypassword"
}

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'selected_survey' not in st.session_state:
    st.session_state.selected_survey = None
if 'surveys_db' not in st.session_state:
    st.session_state.surveys_db = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = None
if 'new_survey_id_temp' not in st.session_state:
    st.session_state.new_survey_id_temp = None

# Function to simulate user login
def login(username, password):
    if username in users_db and users_db[username] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    return False

# Function to create or select a survey
def create_or_select_survey(user):
    st.write(f"Welcome, {user}! Choose an option:")
    choice = st.radio("Select an option:", ["Create a new survey", "Select an existing survey"], key="survey_choice")

    if choice == 'Create a new survey':
        survey_id_input = st.text_input("Enter survey ID for the new survey:", key="new_survey_id_input")
        if survey_id_input:
            if survey_id_input in st.session_state.surveys_db:
                st.write("Survey ID already exists. Choose a different ID.")
            else:
                st.session_state.new_survey_id_temp = survey_id_input
                st.session_state.current_step = "title"
        st.write(f"Current step: Create or Select Survey, New Survey ID Temp: {st.session_state.new_survey_id_temp}")
    
    elif choice == 'Select an existing survey':
        survey_ids = list(st.session_state.surveys_db.keys())
        if not survey_ids:
            st.write("No surveys available.")
        else:
            survey_id = st.selectbox("Select a survey:", survey_ids, key="existing_survey_id")
            st.session_state.selected_survey = survey_id
            st.session_state.current_step = None
        st.write(f"Current step: Select Survey, Selected Survey: {st.session_state.selected_survey}")

# Function to handle survey inputs
def handle_survey_inputs():
    if st.session_state.current_step == "title":
        st.write("Current step: Title")
        title = st.text_input("Enter survey title:", key="survey_title")
        if title and st.button("Save Title"):
            survey_id = st.session_state.new_survey_id_temp
            st.session_state.surveys_db[survey_id] = {
                "title": title,
                "description": "",
                "variations": [],
                "responses": []
            }
            st.session_state.current_step = "description"
            st.write(f"Survey Created with ID: {survey_id}, Title: {title}")
    
    elif st.session_state.current_step == "description":
        st.write("Current step: Description")
        description = st.text_area("Enter survey description:", key="survey_description")
        if description and st.button("Save Description"):
            survey_id = st.session_state.new_survey_id_temp
            st.session_state.surveys_db[survey_id]['description'] = description
            st.session_state.current_step = "variations"
            st.write(f"Description Added to Survey ID: {survey_id}")

    elif st.session_state.current_step == "variations":
        st.write("Current step: Variations")
        customize_or_generate_variations()

# Function to generate or customize survey variations
def customize_or_generate_variations():
    survey_id = st.session_state.new_survey_id_temp
    st.write("Customize or generate variations:")
    survey_data = st.session_state.surveys_db[survey_id]
    st.write(f"Survey data for ID {survey_id}:")
    st.write(f"Title: {survey_data.get('title', 'N/A')}")
    st.write(f"Description: {survey_data.get('description', 'N/A')}")
    st.write(f"Variations: {survey_data.get('variations', [])}")

    new_variations = st.text_area("Enter variations (comma-separated):", key="survey_variations").split(",")
    if st.button("Save Variations"):
        st.session_state.surveys_db[survey_id]['variations'] = [var.strip() for var in new_variations if var.strip()]
        st.write(f"Updated variations: {st.session_state.surveys_db[survey_id]['variations']}")
    
    # Proceed to deployment
    deploy_ab_test()

# Function to deploy A/B test
def deploy_ab_test():
    survey_id = st.session_state.new_survey_id_temp
    st.write(f"Deploying A/B test for survey '{st.session_state.surveys_db[survey_id]['title']}'")

    audience_choice = st.radio("Select target audience:", ["Existing customers", "New users"], key="audience_choice")
    distribution_choice = st.radio("Select distribution method:", ["Email", "Social Media", "Website"], key="distribution_choice")

    st.write(f"Target Audience: {audience_choice}")
    st.write(f"Distribution Method: {distribution_choice}")

    num_participants = 200000 # Simulated number of participants
    participants = pd.DataFrame({
        'Survey_ID': [st.session_state.surveys_db[survey_id]['title']] * num_participants,
        'Variation': np.random.choice(st.session_state.surveys_db[survey_id]['variations'], num_participants),
        'Completion_Time': np.random.randint(1, 30, num_participants),
        'Response_Quality': np.random.uniform(0, 1, num_participants)
    })
    st.session_state.surveys_db[survey_id]['responses'] = participants
    st.write(f"Survey distributed to {num_participants} participants.")

    # Handle analysis and recommendations
    st.session_state.current_step = "analysis"

# Function to analyze survey responses
def analyze_responses(participants):
    st.write("Analyzing responses...")

    completion_rates = participants.groupby('Variation').size() / len(participants) * 100
    st.write("Completion Rates (%):")
    st.write(completion_rates)

    avg_quality = participants.groupby('Variation')['Response_Quality'].mean()
    st.write("Average Response Quality:")
    st.write(avg_quality)

    return completion_rates, avg_quality

# Function to provide optimization recommendations using ML
def provide_recommendations(participants):
    st.write("Providing optimization recommendations...")

    # Prepare data for ML model
    X = pd.get_dummies(participants[['Variation', 'Completion_Time']], drop_first=True)
    y = participants['Response_Quality']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    st.write(f"Model R^2 Score: {accuracy:.2f}")

    best_variation = participants.groupby('Variation')['Response_Quality'].mean().idxmax()
    st.markdown(f"**Best-performing variation:** <span style='color:red;'>{best_variation}</span>", unsafe_allow_html=True)


    return best_variation

# Optimization engine to adjust survey designs
def optimization_engine(best_variation):
    st.write("Optimization Engine")
    survey_id = st.session_state.new_survey_id_temp
    optimized_variation = f"{best_variation} - Optimized"
    st.session_state.surveys_db[survey_id]['variations'].append(optimized_variation)
    st.write(f"New optimized variation added: {optimized_variation}")

# Function to create the dashboard
def create_dashboard(participants):
    st.write("Dashboard")
    
    # Completion Rates
    fig = px.bar(participants.groupby('Variation').size(), title="Completion Rates per Variation")
    st.plotly_chart(fig)
    
    # Average Quality
    fig = px.bar(participants.groupby('Variation')['Response_Quality'].mean(), title="Average Response Quality per Variation")
    st.plotly_chart(fig)
    
    # Combined Analysis
    fig = go.Figure()
    for var in participants['Variation'].unique():
        var_data = participants[participants['Variation'] == var]
        fig.add_trace(go.Box(y=var_data['Response_Quality'], name=var))
    fig.update_layout(title="Response Quality Distribution per Variation")
    st.plotly_chart(fig)

def main():
    st.title("A/B Testing and Survey Optimization System")
    
    if not st.session_state.logged_in:
        st.write("Please log in:")
        username = st.text_input("Enter username:", key="username")
        password = st.text_input("Enter password:", type="password", key="password")
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.write(f"Welcome, {username}!")
            else:
                st.write("Invalid credentials")
    else:
        if st.session_state.current_step is None:
            create_or_select_survey(st.session_state.current_user)
        
        if st.session_state.current_step:
            handle_survey_inputs()

        if st.session_state.current_step == "analysis":
            participants = st.session_state.surveys_db[st.session_state.new_survey_id_temp]['responses']
            analyze_responses(participants)
            best_variation = provide_recommendations(participants)
            optimization_engine(best_variation)
            create_dashboard(participants)

if __name__ == "__main__":
    main()
