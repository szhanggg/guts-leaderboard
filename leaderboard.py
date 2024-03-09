import pandas as pd
import streamlit as st
import altair as alt
from streamlit_autorefresh import st_autorefresh

division = st.selectbox('Please select a division.', ['Godel', 'Brahmagupta'])

count = st_autorefresh(interval=2000, limit=1000000, key="refresh")

def load_data(division):
    sheet = pd.read_csv("https://docs.google.com/spreadsheets/d/1m_S9K3eirLCN-LJ1IHOp7u04ESZ1Vlaq384FIsdv__Y/export?format=csv", skiprows=3)
    if division == 'Godel':
        # Take only first 10 rows from 0 to 9
        sheet = sheet.iloc[0:10]
    elif division == 'Brahmagupta':
        sheet = sheet.iloc[15:25]
    # Take only team name and score columns
    sheet = sheet[['Team Name', 'Score']]
    return sheet

leaderboard_data = load_data(division)
leaderboard_data = leaderboard_data.sort_values('Score', ascending=False).reset_index(drop=True)
print(leaderboard_data.head())
leaderboard_data['Team Name'] = (leaderboard_data.index + 1).astype(str) + '. ' + leaderboard_data['Team Name'].astype(str)

# Create the base chart
base = alt.Chart(leaderboard_data).encode(
    alt.X('Score:Q', title='Score'),
    alt.Y('Team Name:N', title='Team Name', sort=alt.EncodingSortField(field='Total', op='max', order='descending'))
)

# Create the bar chart
bar_chart = base.mark_bar().encode(
    color=alt.Color('row_number:O', scale=alt.Scale(scheme='reds'), legend=None)
).transform_window(
    row_number='row_number()'
).properties(
    title=alt.TitleParams(
        text=(division + ' Leaderboard'),
        fontSize=24,
        anchor='middle',
        align='center'
    ),
)

# Create the text layer for displaying the scores on the bars
text_chart = base.mark_text(
    align='left',
    baseline='middle',
    dx=3,  # Shift the text to the right for better readability
    color='white'
).encode(
    text=alt.Text('Total:Q', format='.1f')  # Format the score to 1 decimal place
)

# Combine the bar chart and text layer
chart = bar_chart + text_chart


st.write(chart)
