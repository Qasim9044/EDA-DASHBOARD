# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 03:09:11 2024

@author: LENOVO
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Set Page Configurations
st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="📊",
    layout="wide"
)

# Sidebar Configuration
st.sidebar.title("📂 Upload & Options")
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV)", type="csv")

if uploaded_file:
    # Read Dataset
    df = pd.read_csv(uploaded_file)

    # Main Dashboard
    st.title("📈 Interactive EDA Dashboard")
    st.write("### Dataset Overview")
    
    # Display Dataset Preview and Info
    st.write("#### First Five Rows:")
    st.dataframe(df.head())
    st.write("#### Dataset Summary:")
    st.write(df.describe())

    # Sidebar Filters
    st.sidebar.write("### 🔍 Filter Options")
    numeric_columns = df.select_dtypes(include=["number"]).columns
    categorical_columns = df.select_dtypes(include=["object"]).columns

    # Add visualization options
    st.sidebar.write("### 📊 Select Visualization")
    viz_option = st.sidebar.selectbox(
        "Choose a chart type:", 
        ["Distribution Plot", "Correlation Heatmap", "Scatter Plot", "Pie Chart", "Box Plot"]
    )

    # Visualizations
    if viz_option == "Distribution Plot":
        col = st.selectbox("Select a column:", numeric_columns)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(f"Distribution Plot for {col}")
        st.pyplot(fig)

    elif viz_option == "Correlation Heatmap":
        st.write("#### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    elif viz_option == "Scatter Plot":
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("Select X-axis:", numeric_columns)
        with col2:
            y_col = st.selectbox("Select Y-axis:", numeric_columns)
        fig = px.scatter(df, x=x_col, y=y_col, color=categorical_columns[0] if len(categorical_columns) > 0 else None)
        st.plotly_chart(fig)

    elif viz_option == "Pie Chart":
        col = st.selectbox("Select a categorical column:", categorical_columns)
        pie_data = df[col].value_counts().reset_index()
        pie_data.columns = [col, 'Count']
        fig = px.pie(pie_data, names=col, values='Count', title=f"Pie Chart for {col}")
        st.plotly_chart(fig)

    elif viz_option == "Box Plot":
        col1, col2 = st.columns(2)
        with col1:
            num_col = st.selectbox("Select a numeric column:", numeric_columns)
        with col2:
            cat_col = st.selectbox("Select a categorical column:", categorical_columns)
        fig = px.box(df, x=cat_col, y=num_col, color=cat_col, title=f"Box Plot of {num_col} by {cat_col}")
        st.plotly_chart(fig)

    # Additional Features Section
    st.write("### 📜 Dataset Insights")
    st.write(f"Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")
    st.write("#### Missing Values:")
    st.write(df.isnull().sum())

    # Footer
    st.markdown("---")
    st.markdown("**Built with ❤️ using Streamlit**")

else:
    # Message when no file is uploaded
    st.title("📂 EDA Dashboard")
    st.write("Please upload a CSV file to start exploring!")

