import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import zscore

# Function to load data with caching
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# Sidebar
st.sidebar.title('Options')
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Sidebar options
    option = st.sidebar.selectbox('Select Analysis', 
                                  ['Summary Statistics', 'Data Quality Check', 
                                   'Time Series Analysis', 'Correlation Analysis', 
                                   'Wind Analysis', 'Temperature Analysis', 
                                   'Histograms', 'Bubble Charts', 'Data Cleaning'])
    
    # Summary Statistics
    if option == 'Summary Statistics':
        st.header('Summary Statistics')
        st.write(df.describe())
    
    # Data Quality Check
    elif option == 'Data Quality Check':
        st.header('Data Quality Check')
        missing_values = df.isnull().sum()
        st.write('Missing Values:')
        st.write(missing_values)
        
        st.header('Outlier Detection')
        # Example: Using Z-score to detect outliers
        df_z = df[['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']].apply(zscore)
        st.write(df_z.describe())
    
    # Time Series Analysis
    elif option == 'Time Series Analysis':
        st.header('Time Series Analysis')
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
        fig, ax = plt.subplots()
        df[['GHI', 'DNI', 'DHI', 'Tamb']].plot(ax=ax)
        st.pyplot(fig)
        
        st.header('Impact of Cleaning on Sensor Readings')
        # Implement comparison of sensor readings before and after cleaning here
    
    # Correlation Analysis
    elif option == 'Correlation Analysis':
        st.header('Correlation Analysis')
        fig, ax = plt.subplots()
        sns.heatmap(df[['GHI', 'DNI', 'DHI', 'TModA', 'TModB']].corr(), annot=True, ax=ax)
        st.pyplot(fig)
    
    # Wind Analysis
    elif option == 'Wind Analysis':
        st.header('Wind Analysis')
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        # Plot wind data here
        st.pyplot(fig)
    
    # Temperature Analysis
    elif option == 'Temperature Analysis':
        st.header('Temperature Analysis')
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='RH', y='Tamb')
        st.pyplot(fig)
    
    # Histograms
    elif option == 'Histograms':
        st.header('Histograms')
        fig, ax = plt.subplots()
        df[['GHI', 'DNI', 'DHI', 'WS', 'Tamb']].hist(ax=ax, bins=20)
        st.pyplot(fig)
    
    # Bubble Charts
    elif option == 'Bubble Charts':
        st.header('Bubble Charts')
        if 'RH' in df.columns and 'GHI' in df.columns and 'Tamb' in df.columns and 'WS' in df.columns:
            fig, ax = plt.subplots()
            sc = ax.scatter(df['GHI'], df['Tamb'], s=df['RH'] * 10, c=df['WS'], cmap='viridis', alpha=0.6, edgecolors='w', linewidth=0.5)
            ax.set_xlabel('GHI')
            ax.set_ylabel('Tamb')
            ax.set_title('Bubble Chart: GHI vs. Tamb vs. WS (Bubble size = RH)')
            cbar = plt.colorbar(sc, ax=ax, label='WS')
            st.pyplot(fig)
        else:
            st.write("Required columns for bubble chart are missing in the dataset.")
    
    # Data Cleaning
    elif option == 'Data Cleaning':
        st.header('Data Cleaning')
        # Display cleaned data or data cleaning results
        st.write(df.head())
