from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import pytz
from os.path import join

from pylab import rcParams
rcParams.update({'figure.figsize': plot_config._mm_to_inches(180, 100)})

print("plotting appliance power histograms...")

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
dataset.set_window("2013-04-26", None) # ignore tungsten kitchen lamps
elec = dataset.buildings[1].elec

fig, axes = plt.subplots(3, 3)
meter_keys = ['fridge freezer', 'kettle', 'toaster', 
              'vacuum cleaner', 'television', 'oven',
              'laptop computer', 'computer monitor', ('light', 1)]
kwargs_per_meter = {'range': [(  2,  275), (2200, 2460), (1480, 1650), 
                              ( 400, 2200), (  80,  140), (None,   60),
                              (   2,   65), (  30,   85), (35, 290)]}

axes = elec.plot_multiple(axes, meter_keys, 'plot_power_histogram', 
                          kwargs_per_meter, 
                          plot_kwargs={'color': plot_config.BLUE})

# Formatting
for i, ax in enumerate(axes):
    ax.grid(False)
    ax.set_yticks([])
    ax.set_ylabel('')
    plot_config.format_axes(ax, tick_size=2)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_locator(MaxNLocator(4))
    for spine in ax.spines.values():
        spine.set_visible(False)
    if i == 7:
        ax.set_xlabel('Power (watts)')
    else:
        ax.set_xlabel('')
    
    title = ax.get_title()
    if title in plot_config.new_names:
        title = plot_config.new_names[title]
    ax.set_title(title, y=0.95)

plt.tight_layout()
plt.subplots_adjust(hspace=1.0)

plt.draw()
plt.savefig(join(plot_config.FIG_DIR, '07_appliance_power_histograms.eps'), 
            bbox_inches='tight')
