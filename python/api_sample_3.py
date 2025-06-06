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

    
    # map VOTable columns on individual properties
    # Properties are mapped  one by one
    
    builder.pack_into_votable()
    
    XmlUtils.pretty_print(builder.mivot_block)
    
    
    m_viewer = MivotViewer(votable, resolve_ref=True)
    mivot_instance = m_viewer.dm_instance
    while m_viewer.next():
        if mivot_instance.dmtype == "mango:MangoObject":
            print(f"Read source {mivot_instance.identifier.value}")
            for mango_property in mivot_instance.propertyDock:
                if  mango_property.dmtype == "mango:Brightness":
                    mag_value = mango_property.value.value
                    mag_error = mango_property.error.sigma.value
                    mag_wl = mango_property.photCal.photometryFilter.spectralLocation.value.value
                    mag_filter = mango_property.photCal.identifier.value
                    print(f"magnitude at {mag_wl} Angstrom (filter {mag_filter}) is {mag_value:.2f} +/- {mag_error:.2f}")
        break
                    


if __name__ == "__main__":
    run()
