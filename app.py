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
file_paths_train = {
    "Contradiction": "contradiction_train_100_samples.tsv",  
    "Entailment": "entailment_train_100_samples.tsv",       
    "Neutral": "neutral_train_100_samples.tsv"             
}

# Define file paths for each dataset
file_paths_val = {
    "Contradiction": "contradiction_val_50_samples.tsv",  
    "Entailment": "entailment_val_50_samples.tsv",       
    "Neutral": "neutral_val_50_samples.tsv"             
}

file_paths = file_paths_val

def load_dataset(file_path):
    """Load the dataset from the given file path."""
    df = pd.read_csv(file_path, sep='\t')
    if 'comm1' not in df.columns:
        df['comm1'] = None
    if 'comm2' not in df.columns:
        df['comm2'] = None
    return df

def update_dataset(file_path, df):
    """Save the updated DataFrame to the given file path."""
    df.to_csv(file_path, sep='\t', index=False)

def find_first_empty_comm1(df):
    """Find the index of the first row where 'comm1' is empty or NaN."""
    empty_comm1_indices = df[df['comm1'].isna()].index
    if len(empty_comm1_indices) > 0:
        return empty_comm1_indices[0]  # Return the first empty row
    else:
        return 0  # If no empty rows, start from the beginning

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
        # Find the first row with an empty 'comm1' field
        st.session_state.current_row = find_first_empty_comm1(st.session_state.dataframe)

    # Initialize current_row if it doesn't exist
    if 'current_row' not in st.session_state:
        st.session_state.current_row = find_first_empty_comm1(st.session_state.dataframe)


    # Display the current row's premise, hypothesis, and comment
    st.write(f"**Premise:** {st.session_state.dataframe.loc[st.session_state.current_row, 'premise_slo']}")
    st.write(f"**Hypothesis:** {st.session_state.dataframe.loc[st.session_state.current_row, 'hypothesis_slo']}")
    st.write(f"**Premise EN:** {st.session_state.dataframe.loc[st.session_state.current_row, 'premise_eng']}")
    st.write(f"**Hypothesis EN:** {st.session_state.dataframe.loc[st.session_state.current_row, 'hypothesis_eng']}")
    existing_comment = st.session_state.dataframe.loc[st.session_state.current_row, 'comm1']
    #st.write(f"**Current Comment:** {existing_comment if pd.notna(existing_comment) else 'No comment yet.'}")

    # Input for user to add or edit a comment
    new_comment = st.text_area(
        "Insert a label for the sentence pair in Slovene:",
        value="",
        key=f"slovene_comment_{st.session_state.current_row}"
    )

    new_comment2 = st.text_area(
        "Insert a label for the sentence pair in English:",
        value="",
        key=f"english_comment_{st.session_state.current_row}"
    )

    
    # Buttons for saving or skipping
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Comment"):
            if new_comment:
                st.session_state.dataframe.loc[st.session_state.current_row, 'comm1'] = new_comment
                st.session_state.dataframe.loc[st.session_state.current_row, 'comm2'] = new_comment2
                update_dataset(file_paths.get(dataset_choice), st.session_state.dataframe)
                st.success("Comment saved!")
            else:
                st.warning("No comment provided. Skipping save.")

            # Move to the next row with an empty 'comm1' field
            remaining_empty_rows = st.session_state.dataframe[st.session_state.dataframe['comm1'].isna()].index
            if len(remaining_empty_rows) > 0:
                st.session_state.current_row = remaining_empty_rows[0]
            else:
                st.session_state.current_row = 0  # If no empty rows, loop back to the first row
                st.info("All comments have been filled. Looping back to the first row.")

    with col2:
        if st.button("Skip to Next Empty Row"):
            remaining_empty_rows = st.session_state.dataframe[st.session_state.dataframe['comm1'].isna()].index
            if len(remaining_empty_rows) > 0:
                st.session_state.current_row = remaining_empty_rows[0]
            else:
                st.session_state.current_row = 0  # If no empty rows, loop back to the first row
                st.info("All comments have been filled. Looping back to the first row.")

    # Display the full dataset if requested
    if st.button("Show Full Dataset"):
        st.dataframe(st.session_state.dataframe)

if __name__ == "__main__":
    main()
