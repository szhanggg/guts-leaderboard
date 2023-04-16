import pandas as pd
import streamlit as st
import altair as alt
from streamlit_autorefresh import st_autorefresh

division = st.selectbox('Please select a division.', ['Bernoulli', 'Germain', ''])

count = st_autorefresh(interval=2000, limit=1000000, key="refresh")

def load_data(division):
    if division == 'Bernoulli':
        return pd.read_csv("https://docs.google.com/spreadsheets/d/1dZlXlSqBmgKh771fyiMSRir70wNc6_ccpfMjEwm7tok/export?format=csv&gid=946925391", skiprows=1)
    elif division == 'Germain':
        return pd.read_csv("https://docs.google.com/spreadsheets/d/1YDCOC-5evKzticNx6C_SZcDCGERPjnQzfkgGPwz-evg/export?format=csv&gid=946925391", skiprows=1)
    else:
        return pd.read_csv("https://docs.google.com/spreadsheets/d/12ZsQRH-s-nFwu-evY3gquxxO2Zym7gCjLZDbko7Kvns/export?format=csv&gid=946925391", skiprows=1)

leaderboard_data = load_data(division)
leaderboard_data = leaderboard_data.sort_values('Total', ascending=False).reset_index(drop=True)
print(leaderboard_data.head())
leaderboard_data['Team Name'] = (leaderboard_data.index + 1).astype(str) + '. ' + leaderboard_data['Team Name'].astype(str)

# Create the base chart
base = alt.Chart(leaderboard_data).encode(
    alt.X('Total:Q', title='Points'),
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