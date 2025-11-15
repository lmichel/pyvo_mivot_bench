"""
"""

import os
import pytest
from pyvo.mivot.utils.dict_utils import DictUtils
pytestmark = pytest.mark.skipif(True)
from __init__ import *
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


# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

@pytest.mark.skip(reason="no way of currently testing this")
def run():
    votable_path = get_raw_data_folder("vizier_votable.xml")

    votable = parse(votable_path)
    
    builder = InstancesFromModels(votable, dmid="URAT1")
    # Extract possible mapping rules from the VOTavle metadata
    parameters = builder.extract_epoch_position_parameters()
    #
    # The mapping rules can be fixed/updated here....
    #
    # add the epoch position mapping 
    builder.add_mango_epoch_position(**parameters)

    
    # map VOTable columns on individual properties
    # Properties are mapped  one by one
    
    builder.pack_into_votable()

    ras = []
    decs = []
    future_ras = []
    future_decs = []
    dates = []
    
    XmlUtils.pretty_print(builder.mivot_block)
    
    m_viewer = MivotViewer(votable, resolve_ref=True)
    mivot_instance = m_viewer.dm_instance
    # iterate over all rows
    while m_viewer.next_row_view():
        if mivot_instance.dmtype == "mango:MangoObject":
            for mango_property in mivot_instance.propertyDock:
                if mango_property.dmtype == "mango:EpochPosition":
                    # get a SkyCoord from MIVOT annotations
                    scb = SkyCoordBuilder(mango_property)
                    sky_coord = scb.build_sky_coord()
                    # Store the parameter to plot
                    dates.append(f"{mivot_instance.identifier.value}"
                                 f" ({str(sky_coord.obstime).replace('J', '')})")
                    ras.append(sky_coord.ra.deg)
                    decs.append(sky_coord.dec.deg)
                    # Compute a position at a future date
                    sky_coord = sky_coord.apply_space_motion(new_obstime=Time('J2225.5'))
                    future_ras.append(sky_coord.ra.deg)
                    future_decs.append(sky_coord.dec.deg)
                    
    plot_urat_sky(ras, decs, dates, future_ras, future_decs )
    
def plot_urat_sky(ras, decs, dates, future_ras, future_decs ):
    import matplotlib.pyplot as plt

    _, ax = plt.subplots()
    ax.ticklabel_format(useOffset=False)
    plt.title("URAT Sky (part of)")
    plt.xlabel("RA")
    plt.ylabel("DEC")
    ax.scatter(ras, decs, color="blue", label="at observation time")
    ax.scatter(future_ras, future_decs, color="red",  label="in year 2225")
    plt.legend(loc="upper left")

    for i, txt in enumerate(dates):
        ax.annotate(txt, (ras[i], decs[i]))

    plt.show()

if __name__ == "__main__":
    run()
