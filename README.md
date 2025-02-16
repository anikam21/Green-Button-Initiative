# Green Button Initiative - Weather-Based Utility Optimization
# Overview
The Green Button Initiative is a standardized effort that allows consumers to securely access their energy and water usage data from utility providers. This initiative was launched to promote data-driven energy efficiency and help individuals and businesses make informed decisions about their electricity and water consumption.

This project was developed as part of my capstone project, where my group and I integrated machine learning models to predict electricity usage, electricity costs, and water consumption based on historical trends and real-time weather data. By analyzing past utility usage alongside temperature and precipitation forecasts, this system provides valuable insights that can help users optimize their energy consumption, reduce costs, and improve efficiency.

The goal of this project is to bridge the gap between energy data and predictive analytics, making it easier for consumers to make data-driven decisions about their utility usage. This system is designed to work with Green Button data in both XML and CSV formats, ensuring compatibility with different utility data sources.

# Project Summary
This project integrates Green Button energy usage data with real-time weather forecasting to provide actionable insights for optimizing energy consumption. By analyzing historical energy usage patterns and combining them with weather predictions, the system can:

- Identify peak energy consumption periods.
- Suggest ways to reduce electricity usage based on weather conditions.
- Improve energy efficiency by leveraging weather insights.

# Project Features
This project integrates historical energy and water consumption data with real-time weather forecasts to provide actionable insights for optimizing electricity usage, water consumption, and cost estimation. By leveraging machine learning models, users can better understand how environmental factors impact their utility usage and make informed decisions to improve efficiency.

 Key features include:

- Water Usage Prediction → Uses historical Green Button water consumption data and weather forecasts to predict daily water usage.
- Electricity Usage Forecasting → Analyzes past energy consumption trends and predicts future electricity usage based on temperature and precipitation data.
- Electricity Cost Estimation → Utilizes Lasso Regression to estimate future electricity costs based on past trends and peak-hour pricing.
- Machine Learning Models → Implements Random Forest, Decision Trees, Lasso Regression, and Linear Regression for data-driven forecasting.
- Green Button Data Compatibility → Supports both XML and CSV formats, making it adaptable for different data sources.

#  User Interfaces: Windows GUI & Flask Web Application
The Green Button Initiative project includes two interactive user interfaces:

A Windows Desktop Application with a Graphical User Interface (GUI)
A Flask-based Web Application with Cloud Integration

These interfaces allow users to upload Green Button data, view historical energy usage, and run predictive models to optimize energy consumption.

Windows Desktop GUI Application
The Windows GUI application provides an interactive, user-friendly experience for accessing Green Button data in real-time.

- Built with Python & PyQt
- Allows users to log in & upload Green Button CSV files
- Displays electricity & water usage data in an easy-to-read format
- Runs ML models to forecast energy & water consumption
- Generates graphs to visualize past trends and future predictions

Features of the GUI
- Login & Signup Pages → Secure authentication system for users.
- Data Upload & Processing Page → Users can select & upload Green Button files for processing.
- Visualization Dashboard → Displays graphs & trends for energy and water consumption.
- Prediction Results Page → Runs ML models and shows future electricity and water usage.

Flask Web Application with Cloud Instance
In addition to the Windows GUI, the project includes a Flask-based web application that provides a cloud-based solution for Green Button data processing.

- Users can access the platform via a web browser
- Data is stored & processed in the cloud
- Real-time energy consumption predictions
- Visual dashboards for analysis

Cloud Integration
- Hosted on AWS → The web app can be deployed on a cloud platform.
- Stores user data in a cloud database → Enables historical tracking & forecasting.
- Allows remote access → Users can upload their Green Button files and get insights from anywhere.

# How to run
Guide
1. Clone the project to local: clone "https..."
2. Create your own branch
3. Activate python venv: .\venv\Scripts\activate. Must install packages in this venv. Type pip install "library name" to install.
4. Install all required packages: pip install -r path/to/requirements.txt
