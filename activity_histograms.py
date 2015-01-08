from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import pytz
from os.path import join

from pylab import rcParams
rcParams.update({'figure.figsize': plot_config._mm_to_inches(88, 150)})

print("plotting activity histograms...")

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
dataset.set_window("2013-03-01", None)#"2013-08-01")
elec = dataset.buildings[1].elec

N = 9
fig, axes = plt.subplots(N, 1)
meter_keys = ['boiler', 'kettle', 'toaster', 'oven',
              'vacuum cleaner', 'television', 
              'laptop computer', 'computer monitor', ('light', 1)]

axes = elec.plot_multiple(axes, meter_keys, 'plot_activity_histogram')

# Formatting
for i, ax in enumerate(axes):
    ax.grid(False)
    ax.set_yticks([])
    ax.set_ylabel('')
    plot_config.format_axes(ax, tick_size=2)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_major_locator(MultipleLocator(6))
    ax.spines['bottom'].set_linewidth(0.2)
    for spine in ['right', 'top', 'left']:
        ax.spines[spine].set_visible(False)
    if i == N-1:
        ax.set_xlabel('Hour of day')
    else:
        ax.set_xlabel('')
        ax.set_xticklabels([])
    title = ax.get_title()
    if title in plot_config.new_names:
        title = plot_config.new_names[title]
    ax.set_title(title, y=0.95)

plt.tight_layout()
plt.subplots_adjust(hspace=0.8)

plt.draw()
plt.savefig(join(plot_config.FIG_DIR, '09_appliance_activity_histograms.eps'), 
            bbox_inches='tight')
