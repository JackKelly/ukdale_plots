from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
import matplotlib.pyplot as plt
import pytz
from os.path import join

from pylab import rcParams
rcParams.update({'figure.figsize': plot_config._mm_to_inches(180, 100)})

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
TZ_STRING = dataset.metadata['timezone']
TZ = pytz.timezone(TZ_STRING)
elec = dataset.buildings[1].elec
elec.use_alternative_mains()

dataset.set_window("2014-07-01", "2014-07-07") 
submeters = elec.meters_directly_downstream_of_mains()
grouped = submeters.groupby('type')
top_k = grouped.select_top_k(group_remainder=True)

DATE = "2014-07-03"
timeframe = TimeFrame(DATE, "2014-07-04", tz=TZ_STRING)
ax, df = top_k.plot(kind='area', timeframe=timeframe, unit='kW')

ax.grid(False)
ax.set_ylim([0, 2.45])
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
