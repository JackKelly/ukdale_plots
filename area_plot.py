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

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
TZ_STRING = dataset.metadata['timezone']
TZ = pytz.timezone(TZ_STRING)
elec = dataset.buildings[1].elec
submeters = elec.meters_directly_downstream_of_mains()

# Select appliances used in top K plot
# APPLIANCES = ['kettle', 'dish washer', 'HTPC', 'washer dryer', 'fridge freezer']
APPLIANCES = ['fridge freezer', 'HTPC', 'dish washer', 'washer dryer', 'kettle']
selected_meters = [submeters[appliance] for appliance in APPLIANCES]
remainder = []
for meter in submeters.meters:
    matches = False
    for appliance in APPLIANCES:
        if meter.matches_appliances({'type': appliance}):
            matches = True
            break
    if not matches:
        remainder.append(meter)

remainder = MeterGroup(remainder)
remainder.name = 'Remainder'
selected_meters = MeterGroup(selected_meters[:2] + [remainder] + selected_meters[2:])

# Reverse the colour palette so it matched top_5_energy
colors = sns.color_palette('deep')
colors.reverse()
colors = [colors[i] for i in [4, 2, 5, 1, 3, 0]]
sns.set_palette(colors)

# Plot one day of data
DATE = "2014-12-07"
next_day = pd.Timestamp(DATE) + timedelta(days=1)
timeframe = TimeFrame(DATE, next_day, tz=TZ_STRING)
ax, df = selected_meters.plot(kind='area', timeframe=timeframe, unit='kW', 
                              width=2000, plot_kwargs={'linewidth': 0.001})

# Prettify
ax.grid(False)
ax.set_ylim([0, 2.6])
ax.set_xlabel('Time (hour of day {})'.format(DATE))
ax.xaxis.set_major_formatter(DateFormatter("%H", tz=TZ))
ax.xaxis.set_major_locator(HourLocator(interval=6, tz=TZ))
for text in ax.get_xticklabels():
    text.set_rotation(0)
    text.set_ha('center')
sns.despine(ax=ax)

plot_config.format_axes(ax)

plt.draw()

plt.savefig(join(plot_config.FIG_DIR, '03_area_plot.eps'), bbox_inches='tight')
