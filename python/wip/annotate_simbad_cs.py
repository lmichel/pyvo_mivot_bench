"""
"""

import os
import pytest
from pyvo.mivot.utils.dict_utils import DictUtils
print(os.environ["PYTHONPATH"])
from __init__ import *
pytestmark = pytest.mark.skipif(True)
import astropy.units as u
import numpy as np
from astropy.time import Time
from astropy.io.votable import parse
from pyvo.utils import activate_features
from pyvo.mivot.utils.xml_utils import XmlUtils
# from pyvo.mivot.utils.dict_utils import DictUtils
from pyvo.mivot.writer.instances_from_models import InstancesFromModels
from pyvo.mivot.viewer.mivot_viewer import MivotViewer
from pyvo.mivot.features.sky_coord_builder import SkyCoordBuilder
dates =[]
ras = []
decs = []
now_ras = []
now_decs = []


# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

@pytest.mark.skip(reason="no way of currently testing this")
def run():
    votable_path = get_raw_data_folder("simbad_cone_verb3.xml")
    

    votable = parse(votable_path)
    builder = InstancesFromModels(votable, dmid="main_id")
    parameters = builder.extract_epoch_position_parameters()
    
    parameters["mapping"]["obsDate"]= {
        "representation": "year",
        "dateTime": 2000
        }

    parameters["mapping"]["errors"]= { 
        "position": { "class": "PErrorEllipse", "semiMajorAxis": "coo_err_maja",
                                   "semiMinorAxis": "coo_err_mina",
                                   "angle": "coo_err_angle"},
                     
        "properMotion": { "class": "PErrorEllipse", "semiMajorAxis": "pm_err_maja",
                                       "semiMinorAxis": "pm_err_mina",
                                   "angle": "pm_err_angle"}
         }
    parameters["mapping"].pop("correlations")
    DictUtils.print_pretty_json(parameters)
    builder.add_mango_epoch_position(**parameters)
    
    builder.pack_into_votable()
    
    XmlUtils.pretty_print(builder.mivot_block)

    m_viewer = MivotViewer(votable, resolve_ref=True)

    mivot_instance = m_viewer.dm_instance
    DictUtils.print_pretty_json(mivot_instance.to_dict())
    while m_viewer.next_row_view():
        if mivot_instance.dmtype == "mango:MangoObject":
            print(f"Read source {mivot_instance.identifier.value}")
            for mango_property in mivot_instance.propertyDock:

                if mango_property.dmtype == "mango:EpochPosition":
                    print(" vitesse radiale " , mango_property.radialVelocity.value, " " , mango_property.radialVelocity.unit)
                    #scb = SkyCoordBuilder(mango_property.to_dict())
                    #print(scb.build_sky_coord().radial_velocity)

if __name__ == "__main__":
    run()
