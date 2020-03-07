from bokeh.plotting import figure
import bisect
from math import pi
from numpy import arange
from itertools import chain
from collections import OrderedDict
from bokeh.palettes import RdBu as colors  # just make sure to import a palette that centers on white (-ish)
from bokeh.models import ColorBar, LinearColorMapper
from bokeh import show

test_irish_data = pd.read_csv('iris.csv')

data1 = pd.read_csv('iris.csv')
data = data1.drop(['species'], axis=1)
def histogram_intersection(a, b):
    v = np.minimum(a, b).sum().round(decimals=1)
    return v

df = pd.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],
                  columns=['dogs', 'cats'])
test_irish_data = pd.read_csv(r'iris.csv')

data1 = pd.read_csv(r'iris.csv')
data = data1.drop(['species'], axis=1)
df = data1
corr_data = df.corr(method='kendall')
colors = list(reversed(colors[9]))
df=data
labels = df.columns
nlabels = len(labels)

def get_bounds(n):
    bottom = list(chain.from_iterable([[ii] * nlabels for ii in range(nlabels)]))
    top = list(chain.from_iterable([[ii + 1] * nlabels for ii in range(nlabels)]))
    left = list(chain.from_iterable([list(range(nlabels)) for ii in range(nlabels)]))
    right = list(chain.from_iterable([list(range(1, nlabels + 1)) for ii in range(nlabels)]))
    return top, bottom, left, right

def get_colors(corr_array, colors):
    ccorr = arange(-1, 1, 1 / (len(colors) / 2))
    color = []
    for value in corr_array:
        ind = bisect.bisect_left(ccorr, value)
        color.append(colors[ind - 1])
    return color

p = figure(plot_width=600, plot_height=600,
           x_range=(0, nlabels), y_range=(0, nlabels),
           title="Correlation Coefficient Heatmap ",
           toolbar_location=None, tools='')

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.xaxis.major_label_orientation = pi / 4
p.yaxis.major_label_orientation = pi / 4

top, bottom, left, right = get_bounds(nlabels)  # creates sqaures for plot
color_list = get_colors(corr_data.values.flatten(), colors)

p.quad(top=top, bottom=bottom, left=left,
       right=right, line_color='white',
       color=color_list)

# Set ticks with labels
ticks = [tick + 0.5 for tick in list(range(nlabels))]
tick_dict = OrderedDict([[tick, labels[ii]] for ii, tick in enumerate(ticks)])
# Create the correct number of ticks for each axis
p.xaxis.ticker = ticks
p.yaxis.ticker = ticks
# Override the labels
p.xaxis.major_label_overrides = tick_dict
p.yaxis.major_label_overrides = tick_dict

# Setup color bar
mapper = LinearColorMapper(palette=colors, low=-1, high=1)
color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
p.add_layout(color_bar, 'right')

show(p)