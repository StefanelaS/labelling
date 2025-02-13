# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:02:22 2025

@author: Korisnik
"""

import pandas as pd
import numpy as np
import streamlit as st

# Set pandas to display full text in columns
pd.set_option('display.max_colwidth', None)

# Dropdown to select the dataset type
dataset_choice = st.selectbox(
    "Choose a dataset type:",
    ("Entailment", "Neutral", "Contradiction")
)

# Define file paths for each dataset
file_paths = {
    "Contradiction": "dev_c.xlsx",  
    "Entailment": "dev_e.xlsx",       
    "Neutral": "dev_n.xlsx"             
}

# Load the dataset based on the selected choice
if st.button("Update Dataset"):
    file_path = file_paths.get(dataset_choice)
    df = pd.read_excel(file_path)
    
    # Initialize session state to keep track of the current row
    if 'current_row' not in st.session_state:
        st.session_state.current_row = 0
    
    # Display the current row's hypothesis and premise
    st.write(f"**Premise:** {df.loc[st.session_state.current_row, 'premise']}")
    st.write(f"**Hypothesis:** {df.loc[st.session_state.current_row, 'hypothesis']}")

    # Check if a comment already exists for the current row
    existing_comment = df.loc[st.session_state.current_row, 'comm1']
    
    # Input for user to add or edit a comment
    comment = st.text_area(
        "Add or edit a comment (or leave blank to skip):",
        value=existing_comment if pd.notna(existing_comment) else ""
    )

    # Create two layout columns for the buttons
    save_column, skip_column = st.columns(2)
    
    # Button to save the comment
    with save_column:
        if st.button("Save Comment"):
            if comment:
                df.loc[st.session_state.current_row, 'comm1'] = comment
            st.session_state.current_row += 1
            if st.session_state.current_row >= len(df):
                st.session_state.current_row = 0  # Loop back to the first row
                st.info("Reached the end of the dataset. Looping back to the first row.")
    
    # Button to skip to the next row
    with skip_column:
        if st.button("Skip to Next Row"):
            st.session_state.current_row += 1
            if st.session_state.current_row >= len(df):
                st.session_state.current_row = 0  # Loop back to the first row
                st.info("Reached the end of the dataset. Looping back to the first row.")

    # Save updated df
    df.to_excel(file_path, index=False)

# Add a button to show the full DataFrame
if st.button("Show Full Dataset"):
    file_path = file_paths.get(dataset_choice)
    df = pd.read_excel(file_path)
    st.dataframe(df)
