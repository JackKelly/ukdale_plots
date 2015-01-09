from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
import matplotlib.pyplot as plt
import pytz
from os.path import join
import pandas as pd

from pylab import rcParams

print("plotting energy bar...")

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
dataset.set_window("2013-04-01", None)
elec = dataset.buildings[1].elec

submeters = elec.meters_directly_downstream_of_mains()
grouped = submeters.groupby('type')
top_k = grouped.select_top_k(group_remainder=False)
try:
    top_k['HTPC'].name = "Home theatre PC"
except KeyError:
    pass
energy = top_k.energy_per_meter(mains=elec.mains(), per_period='D',
                                use_meter_labels=True)

energy.sort(ascending=False)

# Plot
rcParams.update({'figure.figsize': plot_config._mm_to_inches(70, 90)})
ax = pd.DataFrame(energy).T.plot(kind='bar', stacked=True, grid=True,
                                 edgecolor="none", legend=False, width=2)
ax.set_xticks([])
ax.set_ylabel('kWh\nper\nday', rotation=0, ha='center', va='center', labelpad=15)

text_ys = energy.cumsum() - energy.cumsum().diff().fillna(energy['Remainder']) / 2
for kwh, (label, y) in zip(energy.values, text_ys.iteritems()):
    label += " ({:.2f})".format(kwh)
    ax.annotate(label, (0, y), 
                horizontalalignment='center', verticalalignment='center', 
                color='white', size=8)
    
sns.despine(ax=ax, bottom=True, left=True)

# ax.grid(False)
# plot_config.format_axes(ax, tick_size=1)

plt.tight_layout()

plt.draw()

plt.savefig(join(plot_config.FIG_DIR, '06_top_5_energy.eps'), 
            bbox_inches='tight')
