import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv'
df = pd.read_csv(url)

df['Year Acquired'] = pd.to_numeric(df['Year Acquired'], errors='coerce')
df['Square Footage'] = pd.to_numeric(df['Square Footage'], errors='coerce')

df = df[(df['Year Acquired'] > 0) & (df['Square Footage'] > 0)]

import altair as alt

# Aggregate data for the bar chart
agency_buildings = df.groupby('Agency Name')['Agency Name'].count().reset_index(name='Building Count')

# Bar chart
chart1 = alt.Chart(agency_buildings).mark_bar().encode(
    x=alt.X('Building Count', title='Number of Buildings'),
    y=alt.Y('Agency Name', sort='-x', title='Agency'),
    tooltip=['Agency Name', 'Building Count']
).properties(title="Number of Buildings by Agency", width=600, height=400)


chart1.properties(width='container').save("charts1.json")

import altair as alt

alt.data_transformers.disable_max_rows()

slider = alt.binding_range(min=int(df['Year Acquired'].min()), max=int(df['Year Acquired'].max()), step=1)
select_year = alt.selection_single(
    fields=['Year Acquired'],
    bind=slider,
    name="Year"
)

chart2 = alt.Chart(df).mark_circle(size=60).encode(
    x=alt.X('Congress Dist:N', title='Congressional District'),
    y=alt.Y('Senate Dist:N', title='Senate District'),
    color='Agency Name:N',
    tooltip=['Agency Name', 'Location Name', 'Year Acquired', 'Square Footage']
).add_selection(
    select_year
).transform_filter(
    select_year
).properties(title="Buildings by Congressional and Senate Districts (Filtered by Year Acquired)", width=600, height=400)


chart2.properties(width='container').save("chart2.json")


status_dropdown = alt.binding_select(options=[None] + list(df['Bldg Status'].unique()), name='Status ')
select_status = alt.selection_single(fields=['Bldg Status'], bind=status_dropdown, name="Select")

square_footage_chart = alt.Chart(df).mark_circle(opacity=0.5, stroke='black', strokeWidth=0.5).encode(
    x=alt.X('Year Constructed:Q', title='Year Constructed', scale=alt.Scale(domain=[1700, 2025])),
    y=alt.Y('Square Footage:Q', title='Square Footage'),
    color=alt.Color('Bldg Status:N', legend=alt.Legend(title="Building Status")),
    tooltip=['Agency Name', 'Location Name', 'City', 'Square Footage', 'Year Constructed', 'Bldg Status']
).properties(
    title="Square Footage of Buildings Over Years by Status",
    width=600,
    height=400
).add_selection(
    select_status
).transform_filter(
    select_status
).transform_filter(
    alt.datum['Year Constructed'] > 0  # Filter out records without a valid 'Year Constructed'
)

square_footage_chart.properties(width='container').save("chart3.json")
print("Data refreshed successfully!") 

