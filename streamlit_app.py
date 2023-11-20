from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from sqlalchemy import inspect

def main():    
    conn = st.connection('10000_db', type='sql')
    # Insert some data with conn.session.
    with conn.session as s:
        # Check if the table exists
        inspector = inspect(s.bind)
        if 'hours_table' not in inspector.get_table_names():
            # Table doesn't exist, create it
            s.execute('CREATE TABLE hours_table (hours int);')
            if 'hours' not in st.session_state:
                st.session_state.hours = 0
        else:
            # query table to get stored hours 
            if 'hours' not in st.session_state:
                result = conn.query('select * from hours_table')
                st.session_state.hours = result['hours'].iloc[0]
        # update input field and output field 
        col1, col2 = st.columns([8, 1])
        with col1:
            # add statefulness to hours variable 
            increment = st.number_input('Enter number of hours', step=1)  
            if increment:
                st.session_state.hours += increment                             
        with col2:
            total_hours = 10000
            rows = int(math.sqrt(total_hours))
            cols = int(total_hours/rows)
            st.metric(label="% to target", value=st.session_state.hours*100/total_hours) 
        # save data to database 
        s.execute(
                'INSERT INTO hours_table (hours) VALUES (:cum_hours);',
                params={'cum_hours': st.session_state.hours}
            )
        s.commit()
    st.header('Road to 10,000 hours of AI', divider='gray')
    
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
            if count != st.session_state.hours:
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
    chart = alt.Chart(pd.concat([phantom.assign(dataset='df1'), real.assign(dataset='df2')]), height=1000, width=2000).mark_circle(opacity=0.5).encode(
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
 
if __name__ == "__main__":
    main() 