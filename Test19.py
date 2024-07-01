import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Step 1: Load data from CSV
file_path = 'C:/Users/abhishekr/OneDrive - USEReady Technology Private Limited/Desktop/PBI/Case Study/Data Files/Sales.csv'
df = pd.read_csv(file_path)

# Step 2: Aggregate data by Product Category and sum revenue
revenue_by_category = df.groupby('Country')['Revenue'].sum().reset_index()
app = dash.Dash(__name__)
server=app.server

# Step 3: Create figure and subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))

# Plotting bar chart on ax1
bars = ax1.bar(revenue_by_category['Country'], revenue_by_category['Revenue'], color='skyblue')
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
ax2.pie(revenue_by_category['Revenue'], labels=revenue_by_category['Country'], autopct='%1.1f%%', startangle=140)
ax2.set_title('Revenue Distribution by Country')
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Plotting donut chart on ax3
wedges, texts, autotexts = ax3.pie(revenue_by_category['Revenue'], labels=None, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4))
ax3.set_title('Revenue Distribution by Country')
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Adding a circle at the center to turn the pie chart into a donut chart
centre_circle = plt.Circle((0,0),0.2,color='white',fc='white',linewidth=1.25)
ax3.add_artist(centre_circle)

# Displaying matrix table on ax4
ax4.axis('off')  # Turn off axis for table
table_data = df.pivot_table(index='Country', values='Revenue',aggfunc='sum').reset_index()
table = ax4.table(cellText=table_data.values, colLabels=table_data.columns, cellLoc='center', loc='center', colColours=['skyblue']*len(table_data.columns))
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.5, 1.5)  # Adjust table size

# Adjust layout
plt.tight_layout()


# Display the charts and table
plt.show()
