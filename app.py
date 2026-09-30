import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Tournament Optimization", layout="wide")

st.title("Tournament Simulation Workbench")

# Optimized token suffix extraction function
def extract_token_suffixes(df, column_name):
    if column_name in df.columns:
        return df[column_name].astype(str).str.split('_').str[-1]
    return pd.Series(dtype=str)

# Tournament configuration sidebar
st.sidebar.header("Tournament Configuration")
num_rounds = st.sidebar.slider("Number of Rounds", min_value=1, max_value=10, value=3)
batch_size = st.sidebar.number_input("Batch Size for Processing", min_value=10, max_value=1000, value=100)

# Main simulation execution pipeline
if st.button("Run Full Optimized Tournament"):
    with st.spinner("Processing token suffixes and running tournament simulation..."):
        # Initializing sample dataset representing tournament entries
        raw_data = {
            'player_id': range(1, batch_size + 1),
            'token_match': [f"participant_token_v{i % 5 + 1}" for i in range(batch_size)]
        }
        df = pd.DataFrame(raw_data)
        
        # Applying the pre-extracted token suffix optimization
        df['token_suffix'] = extract_token_suffixes(df, 'token_match')
        
        # Simulating tournament rounds without timeouts
        results = []
        for round_num in range(1, num_rounds + 1):
            df[f'score_round_{round_num}'] = np.random.randint(50, 100, size=len(df))
            
        df['total_score'] = df[[col for col in df.columns if 'score_round_' in col]].sum(axis=1)
        df_sorted = df.sort_values(by='total_score', ascending=False).reset_index(drop=True)
        
        st.success("Tournament simulation completed successfully without timeouts!")
        
        # Display performance metrics and results table
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Players", len(df_sorted))
        col2.metric("Rounds Played", num_rounds)
        col3.metric("Top Score", int(df_sorted['total_score'].iloc[0]))
        
        st.subheader("Leaderboard Results")
        st.dataframe(df_sorted, use_container_width=True)
