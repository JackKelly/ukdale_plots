from __future__ import print_function, division
from nilmtk import DataSet, TimeFrame, MeterGroup
import plot_config
import seaborn as sns
from matplotlib.dates import DateFormatter, HourLocator
import matplotlib.pyplot as plt
import pytz
from os.path import join

from pylab import rcParams
rcParams.update({'figure.figsize': plot_config._mm_to_inches(180, 120)})

print("plotting good sections...")

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')
# dataset.set_window("2013-06-01", "2013-06-02") 
dataset.set_window(None, None) 

axes = dataset.plot_good_sections(color=plot_config.BLUE)

for i, ax in enumerate(axes):
    plot_config.format_axes(ax, tick_size=2)
    ax.set_title('House {:d}'.format(i+1), x=0.05, y=.4, va='top')    
    ax.set_ylabel('Meter' if i == 1 else '', 
                  rotation=0, ha='center', va='center', y=.4)


plt.savefig(join(plot_config.FIG_DIR, '03_good_sections.eps'), 
            bbox_inches='tight')
