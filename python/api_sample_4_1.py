"""
"""

import os
import pytest
pytestmark = pytest.mark.skipif(True)
from pyvo.utils import activate_features
from pyvo.dal import TAPService
from pyvo.mivot.utils.xml_utils import XmlUtils
# from pyvo.mivot.utils.dict_utils import DictUtils
from pyvo.mivot.writer.instances_from_models import InstancesFromModels
from pyvo.mivot.viewer.mivot_viewer import MivotViewer
from pyvo.mivot.features.sky_coord_builder import SkyCoordBuilder


# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

@pytest.mark.skip(reason="no way of currently testing this")
def run():
    
    service = TAPService('https://xcatdb.unistra.fr/xtapdb')
    result = service.run_sync(
        """
        SELECT TOP 5 * FROM "public".mergedentry 
        """,
        format="application/x-votable+xml;content=mivot")

    m_viewer = MivotViewer(result, resolve_ref=True)
    
    XmlUtils.pretty_print(m_viewer._mapping_block)
    mivot_instance = m_viewer.dm_instance
    # DictUtils.print_pretty_json(mivot_instance.to_dict())
    while m_viewer.next():
        sp_location = []
        sp_filter = []
        mag = []
        mag_error = []
        if mivot_instance.dmtype == "mango:MangoObject":
            print(f"Read source {mivot_instance.identifier.value} {mivot_instance.dmtype}")
            for mango_property in mivot_instance.propertyDock:
                if  mango_property.dmtype == "mango:Brightness":
                    if mango_property.value.value:
                        mag.append(mango_property.value.value)
                        print(mango_property)
                        unit = mango_property.value.unit
                        print(unit)
                        mag_error.append(mango_property.error.sigma.value)
                        phot_cal = mango_property.photCal
                        spectral_location = phot_cal.photometryFilter.spectralLocation
                        sp_location.append(
                            spectral_location.value.value)
                        sp_filter.append(phot_cal.identifier.value)
                        sunit = spectral_location.unitexpression.value
                    
            plot_sed(mivot_instance.identifier.value, unit, sunit, mag, mag_error, sp_filter, sp_location)  
                         
def plot_sed(identifier, unit, sunit, mag, mag_error, sp_filter, sp_location):          
    import matplotlib.pyplot as plt
    _, ax = plt.subplots()
    plt.title(f"SED of source {identifier}")

    ax.ticklabel_format(useOffset=False)
    ax.scatter(sp_location, mag, color="blue")
    ax.errorbar(sp_location, mag, yerr=mag_error, fmt="o")
    for i, txt in enumerate(sp_filter):
        if sp_location[i] and mag[i]:
            ax.annotate(txt, (sp_location[i], mag[i]))
    plt.xlabel(sunit)
    plt.ylabel('erg/cm**2/sec')   
    plt.show()

if __name__ == "__main__":
    run()
