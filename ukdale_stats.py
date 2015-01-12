from __future__ import print_function, division
from nilmtk import DataSet

dataset = DataSet('/data/mine/vadeec/merged/ukdale.h5')

window_per_house = {1: ("2013-04-12", None), 
                    2: ("2013-05-22", None), 
                    3: (None, None), 
                    4: (None, None), 
                    5: (None, "2014-09-06")}

descriptions = []
for building_id, building in dataset.buildings.iteritems():
    print("*********** House", building_id, "*************")
    dataset.set_window(*window_per_house[building_id])
    description = building.describe()
    descriptions.append(description)
    print(description)
    print()
