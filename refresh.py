import pandas as pd
import altair as alt
df = pd.read_excel("stocksdata.xlsx")

df.columns = df.columns.str.replace(r"\n", " ", regex=True)

df['YEAR'] = df['YEAR'].astype(int)

for month in ['Quantity January', 'Quantity February', 'Quantity March', 'Quantity April', 'Quantity May', 'Quantity June', 
              'Quantity July', 'Quantity August', 'Quantity September', 'Quantity October', 'Quantity November', 'Quantity December']:
    df[month] = pd.to_numeric(df[month], errors='coerce').fillna(0)

df['Total Quantity'] = df[
    ['Quantity January', 'Quantity February', 'Quantity March', 'Quantity April', 'Quantity May', 'Quantity June', 
     'Quantity July', 'Quantity August', 'Quantity September', 'Quantity October', 'Quantity November', 'Quantity December']
].sum(axis=1)

grouped_df = df.groupby(['Plant State']).sum()[['Total Quantity']].reset_index()

alt.data_transformers.disable_max_rows()

brush = alt.selection_interval(encodings=['x'])

chart1 = alt.Chart(grouped_df, title="Total Quantity by State").mark_bar().encode(
    x='Plant State:N',
    y='Total Quantity:Q',
    tooltip=['Plant State', 'Total Quantity']
).add_selection(brush)

df_melted = df.melt(
    id_vars=['Plant State'],
    value_vars=[
        'Quantity January', 'Quantity February', 'Quantity March', 'Quantity April', 'Quantity May', 'Quantity June',
        'Quantity July', 'Quantity August', 'Quantity September', 'Quantity October', 'Quantity November', 'Quantity December'
    ],
    var_name='Month',
    value_name='Quantity'
)

chart2 = alt.Chart(df_melted, title="Monthly Trend").mark_line().encode(
    x=alt.X('Month:N', title='Month', sort=[
        'Quantity January', 'Quantity February', 'Quantity March', 'Quantity April', 'Quantity May', 'Quantity June',
        'Quantity July', 'Quantity August', 'Quantity September', 'Quantity October', 'Quantity November', 'Quantity December'
    ]),
    y='sum(Quantity):Q',
    color=alt.value('orange'),
    tooltip=['Month', 'sum(Quantity)']
).transform_filter(brush)

chart3 = alt.Chart(df, title="Fuel Type Distribution").mark_arc().encode(
    theta='sum(Total Quantity):Q',
    color='AER Fuel Type Code:N',
    tooltip=['AER Fuel Type Code', 'sum(Total Quantity)']
).transform_filter(brush)

dashboard = chart1 | chart2 | chart3

dashboard.to_json('chart1.json')
