from __future__ import print_function, division
from nilmtk import DataSet
import plot_config
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import join
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

############
# Plot
rcParams.update({'figure.figsize': plot_config._mm_to_inches(70, 90)})
ax = top_k.plot(kind='energy bar', mains=elec.mains())
sns.despine(ax=ax, bottom=True, left=True)

plt.tight_layout()

plt.draw()

plt.savefig(join(plot_config.FIG_DIR, '06_top_5_energy.eps'), 
            bbox_inches='tight')
