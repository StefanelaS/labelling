# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 14:02:22 2025

@author: Korisnik
"""

import pandas as pd
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

def main():
    """Main function to run the Streamlit app."""
    st.title("DataFrame Editor")

    # Dropdown to select the dataset type
    dataset_choice = st.selectbox(
        "Choose a dataset type:",
        ("Entailment", "Neutral", "Contradiction")
    )

    # Load the dataset based on the user's choice
    if 'dataframe' not in st.session_state or st.session_state.dataset_choice != dataset_choice:
        st.session_state.dataset_choice = dataset_choice
        st.session_state.dataframe = load_dataset(file_paths.get(dataset_choice))
        st.session_state.current_row = 0  # Reset to the first row

    # Initialize current_row if it doesn't exist
    if 'current_row' not in st.session_state:
        st.session_state.current_row = 0

    # Display the current row's premise, hypothesis, and comment
    st.write(f"**Premise:** {st.session_state.dataframe.loc[st.session_state.current_row, 'premise']}")
    st.write(f"**Hypothesis:** {st.session_state.dataframe.loc[st.session_state.current_row, 'hypothesis']}")
    existing_comment = st.session_state.dataframe.loc[st.session_state.current_row, 'comm1']
    st.write(f"**Current Comment:** {existing_comment if pd.notna(existing_comment) else 'No comment yet.'}")

    # Input for user to add or edit a comment
    new_comment = st.text_area(
        "Add or edit a comment (or leave blank to skip):",
        value=existing_comment if pd.notna(existing_comment) else ""
    )

    # Buttons for saving or skipping
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Comment"):
            if new_comment:
                st.session_state.dataframe.loc[st.session_state.current_row, 'comm1'] = new_comment
                update_dataset(file_paths.get(dataset_choice), st.session_state.dataframe)
                st.success("Comment saved!")
            else:
                st.warning("No comment provided. Skipping save.")

    with col2:
        if st.button("Skip to Next Row"):
            st.session_state.current_row += 1
            if st.session_state.current_row >= len(st.session_state.dataframe):
                st.session_state.current_row = 0  # Loop back to the first row
                st.info("Reached the end of the dataset. Looping back to the first row.")

    # Display the full dataset if requested
    if st.button("Show Full Dataset"):
        st.dataframe(st.session_state.dataframe)

if __name__ == "__main__":
    main()
