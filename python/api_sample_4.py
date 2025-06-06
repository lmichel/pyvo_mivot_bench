"""
"""

import os
import pytest
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


# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

@pytest.mark.skip(reason="no way of currently testing this")
def run():
    votable_path = os.path.realpath(
        os.path.join(__file__, "..", "data", "vizier_votable.xml")
    )

    votable = parse(votable_path)
    builder = InstancesFromModels(votable, dmid="URAT1")

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
    m_viewer = MivotViewer(votable, resolve_ref=True)
    

    mivot_instance = m_viewer.dm_instance
    # DictUtils.print_pretty_json(mivot_instance.to_dict())
    ras = []
    decs = []
    now_ras = []
    now_decs = []
    dates = []
    while m_viewer.next():
        sp_location = []
        sp_filter = []
        mag = []
        mag_error = []
        wl = []
        if mivot_instance.dmtype == "mango:MangoObject":
            print(f"Read source {mivot_instance.identifier.value}")
            for mango_property in mivot_instance.propertyDock:
                if  mango_property.dmtype == "mango:Brightness":
                    if mango_property.value.value:
                        mag.append(mango_property.value.value)
                        mag_error.append(mango_property.error.sigma.value)
                        sp_location.append(
                            mango_property.photCal.photometryFilter.spectralLocation.value.value)
                        sp_filter.append(mango_property.photCal.identifier.value)
                    
            plot_sed(mivot_instance.identifier.value, mag, mag_error, sp_filter, sp_location)  
                         
def plot_sed(identifier, mag, mag_error, sp_filter, sp_location):          
    import matplotlib.pyplot as plt
    _, ax = plt.subplots()
    plt.title(f"SED of source {identifier}")

    ax.ticklabel_format(useOffset=False)
    ax.scatter(sp_location, mag, color="blue")
    ax.errorbar(sp_location, mag, yerr=mag_error, fmt="o")
    for i, txt in enumerate(sp_filter):
        if sp_location[i] and mag[i]:
            ax.annotate(txt, (sp_location[i], mag[i]))
    plt.xlabel("Angstrom")
    plt.ylabel("Mag")   
    plt.show()

if __name__ == "__main__":
    run()
