from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
from datetime import timedelta
import matplotlib.pyplot as plt
import pytz
import pandas as pd
from os.path import join

from pylab import rcParams
rcParams.update({'figure.figsize': plot_config._mm_to_inches(180, 100)})

UNIT = 'kW'

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
TZ_STRING = dataset.metadata['timezone']
TZ = pytz.timezone(TZ_STRING)
elec = dataset.buildings[1].elec
submeters = elec.meters_directly_downstream_of_mains()

# Select appliances used in top K plot
APPLIANCES = ['fridge freezer', 'HTPC', 'dish washer', 'washer dryer', 'kettle']
selected_meters = [submeters[appliance] for appliance in APPLIANCES]
remainder = []
for meter in submeters.meters:
    for appliance in APPLIANCES:
        if meter.matches_appliances({'type': appliance}):
            break
    else:
        remainder.append(meter)

remainder = MeterGroup(remainder)
remainder.name = 'Other submeters'
selected_meters = MeterGroup(selected_meters[:2] + [remainder] + selected_meters[2:])
selected_meters['HTPC'].name = 'Home theatre PC'

# Reverse the colour palette so it matches top_5_energy
colors = sns.color_palette('deep')
colors.reverse()
colors = [colors[i] for i in [4, 2, 5, 1, 3, 0]]
sns.set_palette(colors)

# Set window
DATE = "2014-12-07"
next_day = pd.Timestamp(DATE) + timedelta(days=1)
dataset.set_window(DATE, next_day)

# Plot area
# Need to use a linewidth of 0 to prevent nasty things appearing
# in output.  Looks bad in plt.show() though!
ax, df = selected_meters.plot(kind='area', unit=UNIT, width=4000, threshold=5,
                              plot_kwargs={'linewidth': 0})

# Plot mains
ax = elec.mains().plot(ax=ax, unit=UNIT, width=10000,
                       plot_kwargs={'linewidth': 0.3, 'color': 'grey',
                                    'label': 'Mains (active power)'})

# Prettify
ax.grid(False)
ax.set_ylim([0, 4])
ax.set_xlabel('Time (hour of day)')
ax.xaxis.set_major_formatter(DateFormatter("%H", tz=TZ))
ax.xaxis.set_major_locator(HourLocator(interval=6, tz=TZ))
for text in ax.get_xticklabels():
    text.set_rotation(0)
    text.set_ha('center')
sns.despine(ax=ax)
legend = ax.legend(loc='upper left')
for line in legend.get_lines():
    line.set_linewidth(4)

plot_config.format_axes(ax)
plt.tight_layout()

plt.draw()

plt.savefig(join(plot_config.FIG_DIR, '02_area_plot.eps'),
            bbox_inches='tight', dpi=plt.gcf().dpi)
