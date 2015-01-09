from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
import matplotlib.pyplot as plt
import pytz
from os.path import join

from pylab import rcParams
rcParams.update({'figure.figsize': plot_config._mm_to_inches(88, 60)})

print("plotting histograms...")

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
#dataset.set_window("2013-04-01", "2013-05-01")
dataset.set_window(None, None)

axes = dataset.plot_mains_power_histograms(bins=500, range=(5, 500), 
                                           plot_kwargs={'color': plot_config.BLUE})

for i, ax in enumerate(axes):
    ax.grid(False)
    ax.set_yticks([])
    ax.set_ylabel("")
    plot_config.format_axes(ax, tick_size=2)
    sns.despine(ax=ax, left=True)
    ax.spines['bottom'].set_linewidth(0.2)    
    ax.set_title('House {}'.format(i+1), y=.5, va='top', x=0.08)
    if i != 4:
        ax.set_xlabel('')

plt.tight_layout()
plt.subplots_adjust(hspace=0.1)

plt.draw()

plt.savefig(join(plot_config.FIG_DIR, '05_mains_power_histograms.eps'), 
            bbox_inches='tight')
