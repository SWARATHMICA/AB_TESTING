# A/B Testing and Survey Optimization System
An interactive A/B testing and survey optimization system built using Streamlit. This project enables users to create surveys, deploy A/B tests, analyze responses, and leverage machine learning to optimize survey designs for improved outcomes.

# Project Overview
This project is designed to facilitate effective A/B testing and survey management through an intuitive interface. It provides user login functionality, survey creation, response analysis, and machine learning-driven recommendations to identify the best-performing variations and optimize the survey experience.

# Features
User Authentication: Supports user login for secured access.
Survey Creation and Management: Create new surveys or select from existing ones.
Survey Variations: Add and manage multiple variations of surveys for A/B testing.
A/B Testing Deployment: Simulate A/B testing distribution to large audiences.
Response Analysis: Visualize completion rates and response quality for each variation.
Machine Learning Recommendations: Uses RandomForestRegressor to identify the best-performing variation.
Optimization Engine: Automatically generates new variations based on analysis results.
Interactive Dashboard: Visualizes completion rates and response quality using Plotly.

# Usage
1. User Login
Log in using the available credentials (user1 or user2 with respective passwords).
2. Survey Creation
Create a new survey by specifying a unique survey ID and providing details such as title, description, and variations.
3. A/B Test Deployment
Choose target audiences and distribution methods to simulate A/B testing with a large number of participants.
4. Response Analysis
Analyze completion rates and response quality using interactive visualizations.
5. Optimization and Recommendations
Use the built-in machine learning model to determine the best-performing variation.
Automatically generate an optimized variation based on model results.
6. Dashboard
View all the results on an interactive dashboard that provides insights for improvement.

# Technologies Used
Python
Streamlit: For building the web interface.
Scikit-learn: For machine learning model training and predictions.
Pandas & Numpy: For data manipulation.
Plotly: For interactive visualizations.



