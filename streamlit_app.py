from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    hours = 0
    hours += st.number_input('Enter number of hours', step=1)                                
    total_hours = 10000
    rows = int(math.sqrt(total_hours))
    cols = int(total_hours/rows)
    st.metric(label="% to target", value=hours*100/total_hours) 

    # Create a 2D grid of points
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            point = (i, j)  # Each point is represented as a tuple (row, column)
            row.append(point)
        grid.append(row)

    # Create data points for the entered number of hours
    data = []
    count = 0
    flag = False
    for i in range(rows):
        row = []
        for j in range(cols):
            if count != hours:
                data_point = (i, j)
                count += 1
                row.append(data_point)
            else:
                flag = True
                break
        data.append(row) 
        if flag:
            break              

    # Flatten the grid for Altair
    flat_grid = [(i, j) for row in grid for (i, j) in row]
    flat_data = [(j, i) for row in data for (i, j) in row]

    # Create a DataFrame from the flattened grid
    phantom = pd.DataFrame(flat_grid, columns=['x', 'y'])
    real = pd.DataFrame(flat_data, columns=['x', 'y'])
    
    # Chart using Altair
    chart = alt.Chart(pd.concat([phantom.assign(dataset='df1'), real.assign(dataset='df2')]), height=1000, width=1000).mark_circle(opacity=0.5).encode(
    x=alt.X('x:Q', axis=alt.Axis(labels=False, ticks=False)),  # Hide x-axis labels and ticks
    y=alt.Y('y:Q', axis=alt.Axis(labels=False, ticks=False)),  # Hide y-axis labels and ticks
    color=alt.Color('dataset:N', scale=alt.Scale(range=['#0068c9', '#ff7f0e']))).configure_axis(
    grid=False  # Hide gridlines  # Specify colors for each dataset
).configure_legend(
    title=None,  # Hide legend title
    labelFontSize=0  # Hide legend labels
)

    # Display the Altair chart using Streamlit
    st.altair_chart(chart)  
 