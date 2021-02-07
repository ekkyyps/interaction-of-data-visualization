# import libraries
import pandas as pd
import numpy as np
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Select, CheckboxGroup, RadioButtonGroup
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc


# Read the csv files
df = pd.read_csv('stock_market.csv', parse_dates=['Date'])

# Create dataframe for each index name
df_hangseng = df[df['Name'] == 'HANG SENG']
df_nasdaq = df[df['Name'] == 'NASDAQ']
df_nikkei = df[df['Name'] == 'NIKKEI']

# Create columndatasource for each index name
hangseng_cds = ColumnDataSource(df_hangseng)
nasdaq_cds = ColumnDataSource(df_nasdaq)
nikkei_cds = ColumnDataSource(df_nikkei)

# Create checkbox 
labels = ['Adj Close', 'Volume', 'Day Perc Change']
rb = RadioButtonGroup(labels=labels, active=0,width=800)

# Create and config figure
def create_figure():
  #  Dict for each index name
  dict_df = dict({0:'Adj Close', 1:'Volume', 2:'Day_Perc_Change'})
  # Create figure
  fig = figure(x_axis_type='datetime',
                 plot_height=500,
                 plot_width=800,
                 title='Stock Market of Hang Seng, Nasdaq, and Nikkei',
                 x_axis_label='Date',
                 y_axis_label=dict_df[rb.active])

  # Render stock market as lines
  fig.line('Date', dict_df[rb.active], 
                color='darkgreen', legend_label='Hang Seng',
                source=hangseng_cds) 
  fig.line('Date', dict_df[rb.active],
                color='darkblue', legend_label='Nasdaq',
                source=nasdaq_cds)
  fig.line('Date', dict_df[rb.active], 
                color='darkgoldenrod', legend_label='Nikkei',
                source=nikkei_cds)
  
  # RadioButton action
  # Tooltips and Formatter using HoverTool
  temp = []
  formatter = dict()
  if (rb.active == 0):
    temp.append(('Index Name','@Name'))
    temp.append(('Adj Close', '$@{Adj Close}{%0.2f}'))
  elif (rb.active == 1):
    temp.append(('Index Name','@Name'))
    temp.append(('Volume', '@Volume{0.00 a}'))
  elif (rb.active == 2):
    temp.append(('Index Name','@Name'))
    temp.append(('Day Perc Change', '@Day_Perc_Change'))


  hover = HoverTool(tooltips=temp, formatters=formatter)
  fig.add_tools(hover)

  # Config the legend
  fig.legend.location = 'top_right'
  fig.legend.orientation = 'horizontal'
  
  # Legend Policy
  fig.legend.click_policy = 'hide'
  
  return fig


# Callback for open file
def callback(attr, old, new):
    layout = column(rb, create_figure())

    curdoc().clear()
    curdoc().add_root(layout)
    curdoc().title = "Stock Market"


rb.on_change('active', callback)
layout = column(rb, create_figure())

# open file in py
curdoc().add_root(layout)
curdoc().title = "Stock Market"

# run file
# python -m bokeh serve --show 1301174038_tubes2_level123.py
# or
# bokeh serve --show 1301174038_tubes2_level123.py