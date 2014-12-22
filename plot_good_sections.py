from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
import matplotlib.pyplot as plt
import pytz
from os.path import join

from pylab import rcParams
rcParams.update({'figure.figsize': plot_config._mm_to_inches(180, 200)})

print("plotting good sections...")

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
# dataset.set_window("2014-12-01", "2014-12-02") 

axes = dataset.plot_good_sections()

for i, ax in enumerate(axes):
    ax.grid(False)
    plot_config.format_axes(ax, tick_size=2)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_linewidth(0.5)    
    sns.despine(ax=ax)
    if i==1:
        ax.set_ylabel('Meter')
    elif i==4:
        ax.set_xlabel('Date')

plt.subplots_adjust(hspace=0.3)
plt.tight_layout()

plt.draw()

plt.savefig(join(plot_config.FIG_DIR, '04_good_sections.eps'), 
            bbox_inches='tight')
