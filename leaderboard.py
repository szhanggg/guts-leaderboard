import pandas as pd
import streamlit as st
import altair as alt
from streamlit_autorefresh import st_autorefresh

# Dropdown for selecting division
division = st.selectbox('Please select a division.', ['Godel', 'Brahmagupta'])

# Setup auto-refresh
count = st_autorefresh(interval=2000, limit=1000000, key="refresh")

# Function to load and process data
def load_data(division):
    # Load data from the spreadsheet
    rsheet = pd.read_csv("https://docs.google.com/spreadsheets/d/1m_S9K3eirLCN-LJ1IHOp7u04ESZ1Vlaq384FIsdv__Y/export?format=csv", skiprows=3)
    
    # Filter rows based on the selected division
    if division == 'Godel':
        sheet = rsheet.iloc[0:10]
    else:
        sheet = rsheet.iloc[15:25]
    
    # Select only 'Team Name' and 'Score' columns
    sheet = sheet[['Team Name', 'Score']]
    sheet1 = rsheet[['Teams 1', 'Scores 1']]
    sheet2 = rsheet[['Teams 2', 'Scores 2']]
    sheet3 = rsheet[['Teams 3', 'Scores 3']]

    # Rename columns
    sheet.columns = ['Team Name', 'Score']
    sheet1.columns = ['Team Name', 'Score']
    sheet2.columns = ['Team Name', 'Score']
    sheet3.columns = ['Team Name', 'Score']

    if division == 'Godel':
        sheet1 = sheet1.iloc[0:10]
        sheet2 = sheet2.iloc[0:10]
        sheet3 = sheet3.iloc[0:10]
    else:
        sheet1 = sheet1.iloc[11:25]
        sheet2 = sheet2.iloc[11:25]
        sheet3 = sheet3.iloc[11:25]

    combined_sheet = pd.concat([sheet1, sheet2, sheet3], ignore_index=True)
    sheet = combined_sheet

    sheet = sheet[sheet['Team Name'].notna()]

    if division == 'Godel':
        # Add columns
        pass

    sheet.loc[:, 'Score'] = pd.to_numeric(sheet['Score'], errors='coerce')
    
    return sheet

# Load and sort leaderboard data
leaderboard_data = load_data(division)
leaderboard_data = leaderboard_data.sort_values('Score', ascending=False).reset_index(drop=True)

# Append rank to team names
leaderboard_data['Team Name'] = (leaderboard_data.index + 1).astype(str) + '. ' + leaderboard_data['Team Name'].astype(str)

# Create the base chart with Altair
base = alt.Chart(leaderboard_data).encode(
    alt.X('Score:Q', title='Score'),
    alt.Y('Team Name:N', title='Team Name', sort=alt.EncodingSortField(field='Score', op='max', order='descending'))
)

# Bar chart to represent scores
bar_chart = base.mark_bar().encode(
    color=alt.Color('Score:Q', scale=alt.Scale(scheme='reds'), legend=None)
)

# Text layer to display scores on bars
text_chart = base.mark_text(
    align='left',
    baseline='middle',
    dx=3,  # Nudge text to the right for readability
    color='white'
).encode(
    text=alt.Text('Score:Q', format='.1f')  # Format score to one decimal place
)

# Layer charts
chart = bar_chart + text_chart

# Display chart
st.write(chart)

