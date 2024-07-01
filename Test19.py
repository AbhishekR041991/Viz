import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Dropdown

# Step 1: Load data from CSV
file_path = 'C:/Users/abhishekr/OneDrive - USEReady Technology Private Limited/Desktop/PBI/Case Study/Data Files/Sales.csv'
df = pd.read_csv(file_path)

# Step 2: Aggregate data by Country and sum revenue
revenue_by_country = df.groupby('Country')['Revenue'].sum().reset_index()

# Function to update plots and table based on selected country
def update_data(country):
    # Filter data for selected country
    filtered_data = df[df['Country'] == country]
    
    # Update bar chart
    ax1.clear()
    bars = ax1.bar(filtered_data['Country'], filtered_data['Revenue'], color='skyblue')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Total Revenue')
    ax1.set_title(f'Total Revenue for {country}')
    ax1.tick_params(axis='x', rotation=45)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0f}k'.format(x / 1000)))  # Format y-axis labels in thousands

    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval, '{:.1f}k'.format(yval / 1000), ha='center', va='bottom')
    
    # Update pie chart
    ax2.clear()
    ax2.pie(filtered_data['Revenue'], labels=filtered_data['Country'], autopct='%1.1f%%', startangle=140)
    ax2.set_title(f'Revenue Distribution for {country}')
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Update donut chart
    ax3.clear()
    wedges, texts, autotexts = ax3.pie(filtered_data['Revenue'], labels=None, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4))
    ax3.set_title(f'Revenue Distribution for {country}')
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    centre_circle = plt.Circle((0,0),0.2,color='white',fc='white',linewidth=1.25)
    ax3.add_artist(centre_circle)
    
    # Update table
    ax4.clear()
    ax4.axis('off')  # Turn off axis for table
    table_data = filtered_data.pivot_table(index='Country', values='Revenue', aggfunc='sum').reset_index()
    table = ax4.table(cellText=table_data.values, colLabels=table_data.columns, cellLoc='center', loc='center', colColours=['skyblue']*len(table_data.columns))
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.5, 1.5)  # Adjust table size
    
    # Adjust layout
    plt.tight_layout()
    fig.canvas.draw_idle()

# Create figure and subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))

# Initial plot with all data
bars = ax1.bar(revenue_by_country['Country'], revenue_by_country['Revenue'], color='skyblue')
ax1.set_xlabel('Country')
ax1.set_ylabel('Total Revenue')
ax1.set_title('Total Revenue by Country')
ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0f}k'.format(x / 1000)))  # Format y-axis labels in thousands

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval, '{:.1f}k'.format(yval / 1000), ha='center', va='bottom')

ax2.axis('off')
ax3.axis('off')
ax4.axis('off')

# Create dropdown menu for country selection
countries = list(revenue_by_country['Country'])
ax_dropdown = plt.axes([0.1, 0.95, 0.3, 0.03], facecolor='lightgoldenrodyellow')
dropdown = Dropdown(ax_dropdown, 'Select Country', countries, 
                    label_opts={'fontsize': 12, 'fontweight': 'bold'})

# Define function to handle dropdown menu selection
def on_select_country(event):
    selected_country = dropdown.val
    update_data(selected_country)

dropdown.on_changed(on_select_country)

# Adjust layout
plt.tight_layout()

# Display the charts and table
plt.show()
