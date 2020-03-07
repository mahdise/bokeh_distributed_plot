# -*- coding: utf-8 -*-
"""


@author: Mahdi Islam
"""

import pandas as pd
import numpy as np
from pandas._libs.tslibs import timestamps
from bokeh.models import BasicTicker, ColumnDataSource, Grid, LinearAxis, DataRange1d, PanTool, Plot, \
    WheelZoomTool, BoxZoomTool, SaveTool, ResetTool
from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.models.glyphs import Circle
from bokeh.embed import components


final_dataframe = pd.DataFrame()


for key in data_plot:
    signal_name = legend_name[key]
    data = data_plot[key]['values']
    dataframe_signal = pd.DataFrame(data, columns=[signal_name])
    replace_inf = dataframe_signal.replace([np.inf, -np.inf], np.nan)
    drop_nan_value = replace_inf.dropna(how='all')
    final_dataframe = pd.concat([final_dataframe, drop_nan_value], axis=1)

xattrs = list()
plots = []
signal_data = dict()
for x in final_dataframe.columns:
    xattrs.append(str(x))
    signal_data[x] = final_dataframe[x]
final_dataframe['color'] = '#FF7F00'

signal_data['color'] = final_dataframe['color']
yattrs = list(reversed(xattrs))

source = ColumnDataSource(signal_data)
xdr = DataRange1d(bounds=None)
ydr = DataRange1d(bounds=None)
for y in yattrs:
    row = []
    for x in xattrs:
        xax = (y == yattrs[-1])
        yax = (x == xattrs[0])
        plot = metrix_plot(x, y, xax, yax, xdr, ydr, source)
        row.append(plot)
    plots.append(row)

# gp = gridplot(plots)
gp = gridplot(
    children=plots,
    toolbar_location='right',
    toolbar_options=dict(logo=None),
    merge_tools=True,
)
show(gp)
script1, div1 = components(gp)
final_plot = {
    "container": div1,
    "script": script1
}
response_data = dict(
    results=dict(
        plot=final_plot
    )
)
    
def metrix_plot(xname, yname, xax=False, yax=False, xdr=None, ydr=None, source=None):
    mbl = 40 if yax else 0
    mbb = 40 if xax else 0
    plot = Plot(
        x_range=xdr, y_range=ydr,
        plot_width=200 + mbl, plot_height=200 + mbb,
        min_border_left=1 + mbl, min_border_right=1, min_border_top=1, min_border_bottom=1 + mbb)

    circle = Circle(x=xname, y=yname, fill_color="color", size=4, line_color="color")
    r = plot.add_glyph(source, circle)

    xdr.renderers.append(r)
    ydr.renderers.append(r)

    xticker = BasicTicker()
    if xax:
        xaxis = LinearAxis()
        xaxis.axis_label = xname
        plot.add_layout(xaxis, 'below')
        xticker = xaxis.ticker
    plot.add_layout(Grid(dimension=0, ticker=xticker))

    yticker = BasicTicker()
    if yax:
        yaxis = LinearAxis()
        yaxis.axis_label = yname
        yaxis.major_label_orientation = 'vertical'
        plot.add_layout(yaxis, 'left')
        yticker = yaxis.ticker
    plot.add_layout(Grid(dimension=1, ticker=yticker))

    plot.add_tools(PanTool(), WheelZoomTool(), BoxZoomTool(), SaveTool(), ResetTool())

    return plot
