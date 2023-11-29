from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go

def load_energy_consumption_data():
    """Loads energy consumption data by location."""
    data = pd.read_csv("static/data/GHG_emissions_energy_by_location.csv")
    return data

def prepare_energy_consumption_chart_data(data_df):
    """Prepares data for the energy consumption pie chart."""
    # Skipping the 'Total' row and unnecessary columns
    energy_data = data_df[:-1][['Substation', 'kWh']]
    labels = energy_data['Substation'].tolist()
    values = [float(value.replace(',', '').strip()) for value in energy_data['kWh']]
    return labels, values

def create_energy_consumption_pie_chart(labels, values):
    """Creates a pie chart for energy consumption data."""
        # Add a title at the bottom
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(
        title={
            'text': "GHG Emissions From The Energy Sector by Location.",
            'y': 0.08,  # Adjust the vertical position
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'bottom'
        })

    return fig

def setup_energy_consumption_layout(app, fig_pie_chart):
    """Sets up the layout of the Dash app for energy consumption visualization."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='energy-consumption-pie-chart', figure=fig_pie_chart)
        ])
    ], id='energy-consumption-pie-chart-layout')

def create_app():
    """Creates and configures the Dash app."""
    app = Dash(__name__)

    # Load and prepare data
    data_df = load_energy_consumption_data()
    labels, values = prepare_energy_consumption_chart_data(data_df)

    # Create pie chart
    fig_pie_chart = create_energy_consumption_pie_chart(labels, values)

    # Setup layout
    setup_energy_consumption_layout(app, fig_pie_chart)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)
