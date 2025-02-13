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

# Define file paths for each dataset
file_paths = {
    "Contradiction": "dev_c.xlsx",  
    "Entailment": "dev_e.xlsx",       
    "Neutral": "dev_n.xlsx"             
}

def load_dataset(file_path):
    """Load the dataset from the given file path."""
    return pd.read_excel(file_path)

def update_dataset(file_path, df):
    """Save the updated DataFrame to the given file path."""
    df.to_excel(file_path, index=False)

def display_current_row(df, current_row):
    """Display the premise and hypothesis for the current row."""
    st.write(f"**Premise:** {df.loc[current_row, 'premise']}")
    st.write(f"**Hypothesis:** {df.loc[current_row, 'hypothesis']}")
    st.write(f"**Comment:** {df.loc[current_row, 'comm1']}")

def main():
    """Main function to run the Streamlit app."""
    # Dropdown to select the dataset type
    dataset_choice = st.selectbox(
        "Choose a dataset type:",
        ("Entailment", "Neutral", "Contradiction")
    )

    # Load the dataset based on the selected choice
    file_path = file_paths.get(dataset_choice)
    df = load_dataset(file_path)

    # Initialize session state to keep track of the current row and DataFrame
    if 'current_row' not in st.session_state:
        st.session_state.current_row = 0
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = df

    # Display the current row's hypothesis and premise
    display_current_row(st.session_state.dataframe, st.session_state.current_row)

    # Check if a comment already exists for the current row
    existing_comment = st.session_state.dataframe.loc[st.session_state.current_row, 'comm1']

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
                st.session_state.dataframe.loc[st.session_state.current_row, 'comm1'] = comment
                # Save the updated DataFrame to the file
                update_dataset(file_path, st.session_state.dataframe)
            # Move to the next row
            st.session_state.current_row += 1
            if st.session_state.current_row >= len(st.session_state.dataframe):
                st.session_state.current_row = 0  # Loop back to the first row
                st.info("Reached the end of the dataset. Looping back to the first row.")

    # Button to skip to the next row
    with skip_column:
        if st.button("Skip to Next Row"):
            st.session_state.current_row += 1
            if st.session_state.current_row >= len(st.session_state.dataframe):
                st.session_state.current_row = 0  # Loop back to the first row
                st.info("Reached the end of the dataset. Looping back to the first row.")

    # Add a button to show the full DataFrame
    if st.button("Show Full Dataset"):
        st.dataframe(st.session_state.dataframe)

if __name__ == "__main__":
    main()
