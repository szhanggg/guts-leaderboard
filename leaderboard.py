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
    gsheet = rsheet.iloc[0:10]
    bsheet = rsheet.iloc[15:25]
    
    # Select only 'Team Name' and 'Score' columns
    gsheet = gsheet[['Team Name', 'Score']]
    bsheet = bsheet[['Team Name', 'Score']]
    sheet1 = rsheet[['Teams 1', 'Scores 1']]
    sheet2 = rsheet[['Teams 2', 'Scores 2']]
    sheet3 = rsheet[['Teams 3', 'Scores 3']]

    # Rename columns
    gsheet.columns = ['Team Name', 'Score']
    bsheet.columns = ['Team Name', 'Score']
    sheet1.columns = ['Team Name', 'Score']
    sheet2.columns = ['Team Name', 'Score']
    sheet3.columns = ['Team Name', 'Score']

    gsheet = pd.concat([sheet1.iloc[0:10], sheet2.iloc[0:10], sheet3.iloc[0:10]], ignore_index=True)
    bsheet = pd.concat([sheet1.iloc[11:25], sheet2.iloc[11:25], sheet3.iloc[11:25]], ignore_index=True)

    gsheet = gsheet[gsheet['Team Name'].notna()]
    bsheet = bsheet[bsheet['Team Name'].notna()]

    gsheet.loc[:, 'Score'] = pd.to_numeric(gsheet['Score'], errors='coerce')
    bsheet.loc[:, 'Score'] = pd.to_numeric(bsheet['Score'], errors='coerce')

    if division == 'Godel':
        return gsheet
    else:
        return bsheet 

# Load and sort leaderboard data
leaderboard_data = load_data(division)
leaderboard_data = leaderboard_data.sort_values('Score', ascending=False).reset_index(drop=True)

# Split the data into top 10 and the rest
top_10_data = leaderboard_data.head(10)
rest_data = leaderboard_data.tail(len(leaderboard_data) - 10)

# Function to create chart for top 10 teams
def create_chart(data):
    # Append rank to team names
    data['Team Name'] = (data.index + 1).astype(str) + '. ' + data['Team Name'].astype(str)

    # Create the base chart with Altair
    base = alt.Chart(data).encode(
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
        dx=3  # Nudge text to the right for readability
    ).encode(
        text=alt.Text('Score:Q', format='.1f')  # Format score to one decimal place
    )

    # Layer charts
    return bar_chart + text_chart

custom_css = """
<style>
    .rest-teams {
        font-size: 12px;
        font-family: sans-serif;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Use Streamlit's columns to display charts side by side with spacing
col1, spacer, col2 = st.columns([5, 3, 5])  # Adjust the middle column width for spacing

with col1:
    st.write("Top 10 Teams")
    st.write(create_chart(top_10_data))

with col2:
    # Format and display each team and score using markdown
    markdown_text = "<div class='rest-teams'>"
    ind = 11
    for _, row in rest_data.iterrows():
        markdown_text += f"{ind}. {row['Team Name']}: {row['Score']}<br>"
        ind += 1
    markdown_text += "</div>"
    st.markdown(markdown_text, unsafe_allow_html=True)
