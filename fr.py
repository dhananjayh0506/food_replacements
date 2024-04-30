import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Sample data for two groups of food items
data_group1 = {
    'Food': ['Poha', 'Paneer', 'Rice', 'A', 'B', 'C', 'D'],
    'Weight': [100, 50, 100, 40, 50, 60, 70],
    'Group': ['Group 1'] * 7
}

data_group2 = {
    'Food': ['E', 'F', 'G', 'Z', 'H', 'I', 'J'],
    'Weight': [100, 50, 100, 40, 50, 60, 70],
    'Group': ['Group 2'] * 7
}

df_group1 = pd.DataFrame(data_group1)
df_group2 = pd.DataFrame(data_group2)

# Combine both dataframes
df_combined = pd.concat([df_group1, df_group2], ignore_index=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Food Weight Visualization"),
    html.Div([
        dcc.Dropdown(
            id='food-dropdown',
            options=[{'label': food, 'value': food} for food in df_combined['Food']],
            placeholder="Select a food item",
            style={'width': '50%'}
        ),
        dcc.Slider(
            id='amount-slider',
            min=0,
            max=200,
            step=10,
            value=100,
            marks={i: str(i) for i in range(0, 201, 20)}  # Display marks every 20 units
        ),
    ], style={'width': '80%', 'margin': 'auto', 'textAlign': 'center', 'padding': '20px'}),
    
    html.Div(id='table-container')
])

# Define callback to update table based on selected food item and slider value
@app.callback(
    Output('table-container', 'children'),
    [Input('food-dropdown', 'value'),
     Input('amount-slider', 'value')]
)
def update_table(selected_food, selected_amount):
    if selected_food is None:
        return html.Div("Please select a food item.")

    selected_food_group = df_combined.loc[df_combined['Food'] == selected_food, 'Group'].values[0]
    filtered_df = df_combined[df_combined['Group'] == selected_food_group]

    # Calculate adjusted weights proportionately based on slider value
    original_weights = filtered_df['Weight']
    original_selected_weight = df_combined.loc[df_combined['Food'] == selected_food, 'Weight'].values[0]
    
    if original_selected_weight == 0:
        adjusted_weights = original_weights  # Avoid division by zero
    else:
        proportion = selected_amount / original_selected_weight
        adjusted_weights = original_weights * proportion
    
    # Create a Plotly table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=['Food', 'Weight'],
                    fill_color='lightblue',
                    align='left'),
        cells=dict(values=[filtered_df['Food'], adjusted_weights],
                   fill_color='white',
                   align='left'))
    ])
    
    # Update table layout
    table_fig.update_layout(
        title=f"Food Weights ({selected_food_group}) excluding {selected_food}",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Convert Plotly figure to HTML and return
    table_html = dcc.Graph(figure=table_fig)
    return table_html

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
