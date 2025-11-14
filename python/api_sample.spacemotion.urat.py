"""
"""

import os
import pytest
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
    votable_path = get_raw_data_folder("vizier_votable.xml")
    

    votable = parse(votable_path)
    builder = InstancesFromModels(votable, dmid="URAT1")
    parameters = builder.extract_epoch_position_parameters()
    builder.add_mango_epoch_position(**parameters)

    builder.add_mango_brightness( photcal_id="2MASS/2MASS.J/AB",
            mapping={"value": "Jmag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_Jmag"}
                     },
            semantics={"description": "magnitude J",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})
    builder.add_mango_brightness( photcal_id="2MASS/2MASS.H/AB",
            mapping={"value": "Hmag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_Hmag"}
                     },
            semantics={"description": "magnitude H",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})
    builder.add_mango_brightness( photcal_id="2MASS/2MASS.Ks/AB",
            mapping={"value": "Kmag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_Kmag"}
                     },
            semantics={"description": "magnitude K",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})
    
    builder.add_mango_brightness( photcal_id="Misc/APASS.B/AB",
            mapping={"value": "Bmag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_Bmag"}
                     },
            semantics={"description": "magnitude B",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})    
    builder.add_mango_brightness( photcal_id="Misc/APASS.V/AB",
            mapping={"value": "Vmag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_Vmag"}
                     },
            semantics={"description": "magnitude V",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})
    builder.add_mango_brightness( photcal_id="Misc/APASS.sdss_g/AB",
            mapping={"value": "gmag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_gmag"}
                     },
            semantics={"description": "magnitude g",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})
    builder.add_mango_brightness( photcal_id="Misc/APASS.sdss_r/AB",
            mapping={"value": "rmag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_rmag"}
                     },
            semantics={"description": "magnitude r",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})
    builder.add_mango_brightness( photcal_id="Misc/APASS.sdss_i/AB",
            mapping={"value": "imag",
                     "error": { "class": "PErrorSym1D", "sigma": "e_imag"}
                     },
            semantics={"description": "magnitude i",
                       "uri": "https://www.ivoa.net/rdf/uat/2024-06-25/uat.html#magnitude",
                       "label": "magnitude"})
    
    # map VOTable columns on individual properties
    # Properties are mapped  one by one
    
    builder.pack_into_votable()
    
    XmlUtils.pretty_print(builder.mivot_block)
    import matplotlib.pyplot as plt

    
    m_viewer = MivotViewer(votable, resolve_ref=True)
    # Get the first instance mapped in the MIVOt <TEMPLATES>
    mivot_instance = m_viewer.dm_instance
    # iterate over the table rows
    dates = []
    while m_viewer.next_row_view():
        if mivot_instance.dmtype == "mango:MangoObject":
            print(f"Read source {mivot_instance.identifier.value}")
            for mango_property in mivot_instance.propertyDock:
                #
                # Process the current property
                # the mango_property matches the model components 
                # to which data are mapped
                #
                
                
                
                
                if mango_property.dmtype == "mango:EpochPosition":
                    print(mango_property)
                    scb = SkyCoordBuilder(mango_property)
                    sky_coord = scb.build_sky_coord()
                    print(sky_coord)

                        
                    dates.append(f"{mivot_instance.identifier.value} ({str(sky_coord.obstime).replace('J', '')})")
                    ras.append(sky_coord.ra.deg)
                    decs.append(sky_coord.dec.deg)
                    sky_coord = sky_coord.apply_space_motion(new_obstime=Time('J2225.5'))
                    now_ras.append(sky_coord.ra.deg)
                    now_decs.append(sky_coord.dec.deg)
                #elif  mango_property.dmtype == "mango:Brightness":
                #    if mango_property.value.value:
                ##        mag.append(mango_property.value.value)
                 #      mag_error.append(mango_property.error.sigma.value)
                ##        sp_filter.append(mango_property.photCal.identifier.value)
        """           
        _, ax = plt.subplots()
        plt.title(f"SED of source {mivot_instance.identifier.value}")

        ax.ticklabel_format(useOffset=False)
        ax.scatter(sp_location, mag, color="blue")
        ax.errorbar(sp_location, mag, yerr=mag_error, fmt="o")
        for i, txt in enumerate(sp_filter):
            if sp_location[i] and mag[i]:
                ax.annotate(txt, (sp_location[i], mag[i]))
        plt.xlabel("Angstrom")
        plt.ylabel("Mag")

        plt.show()
         """  
    _, ax = plt.subplots()
    ax.ticklabel_format(useOffset=False)
    plt.title("URAT sky in 2225")
    plt.xlabel("RA")
    plt.ylabel("DEC")
    ax.scatter(ras, decs, color="blue")
    ax.scatter(now_ras, now_decs, color="red")

    for i, txt in enumerate(dates):
        ax.annotate(txt, (ras[i], decs[i]))

    plt.show()


if __name__ == "__main__":
    run()
