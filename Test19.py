import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from matplotlib.ticker import FuncFormatter

# Load data from CSV
file_path = 'C:/Users/abhishekr/OneDrive - USEReady Technology Private Limited/Desktop/PBI/Case Study/Data Files/Sales.csv'
df = pd.read_csv(file_path)

# Aggregate data by Country and sum revenue
revenue_by_country = df.groupby('Country')['Revenue'].sum().reset_index()

# Initialize Dash app
app = dash.Dash(__name__)
server =app.server

# Define app layout
app.layout = html.Div([
    html.H1('Matplotlib Visualization with Dash'),

    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in ['All'] + list(revenue_by_country['Country'].unique())],
        value='All',
        clearable=False
    ),

    html.Div([
        html.Div(id='plots-container'),
        html.Img(id='plot-image')
    ])
])

# Function to generate matplotlib plot and return image as base64
def generate_plot(country):
    # Filter data based on selected country
    if country == 'All':
        filtered_data = revenue_by_country
    else:
        filtered_data = revenue_by_country[revenue_by_country['Country'] == country]

    # Create figure and subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))

    # Plotting bar chart on ax1
    bars = ax1.bar(filtered_data['Country'], filtered_data['Revenue'], color='skyblue')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Total Revenue')
    ax1.set_title('Total Revenue by Country')
    ax1.tick_params(axis='x', rotation=45)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0f}k'.format(x / 1000)))  # Format y-axis labels in thousands

    # Annotate each bar with its value
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval, '{:.1f}k'.format(yval / 1000), ha='center', va='bottom')

    # Plotting pie chart on ax2
    ax2.pie(filtered_data['Revenue'], labels=filtered_data['Country'], autopct='%1.1f%%', startangle=140)
    ax2.set_title('Revenue Distribution by Country')
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Plotting donut chart on ax3
    wedges, texts, autotexts = ax3.pie(filtered_data['Revenue'], labels=None, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4))
    ax3.set_title('Revenue Distribution by Country')
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Adding a circle at the center to turn the pie chart into a donut chart
    centre_circle = plt.Circle((0,0),0.2,color='white',fc='white',linewidth=1.25)
    ax3.add_artist(centre_circle)

    # Displaying matrix table on ax4
    ax4.axis('off')  # Turn off axis for table
    table_data = df.pivot_table(index='Country', values='Revenue', aggfunc='sum').reset_index()
    if country != 'All':
        table_data = table_data[table_data['Country'] == country]  # Filter table data if country is selected
    table = ax4.table(cellText=table_data.values, colLabels=table_data.columns, cellLoc='center', loc='center', colColours=['skyblue']*len(table_data.columns))
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.5, 1.5)  # Adjust table size

    # Save plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode plot image to base64
    plot_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return plot_data

# Callback to update plots based on dropdown selection
@app.callback(
    Output('plot-image', 'src'),
    [Input('country-dropdown', 'value')]
)
def update_plot(selected_country):
    plot_data = generate_plot(selected_country)
    return 'data:image/png;base64,{}'.format(plot_data)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
