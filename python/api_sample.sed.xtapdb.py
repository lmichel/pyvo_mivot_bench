"""
"""

import pytest
pytestmark = pytest.mark.skipif(True)
from pyvo.utils import activate_features
from pyvo.dal import TAPService
# from pyvo.mivot.utils.dict_utils import DictUtils
from pyvo.mivot.viewer.mivot_viewer import MivotViewer


# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

@pytest.mark.skip(reason="no way of currently testing this")
def run():
    
    # run a regular TAP query against  XtapDB
    URL = "https://xcatdb.unistra.fr/xtapdb"
    FORMAT = "application/x-votable+xml;content=mivot"
    QUERY = 'SELECT TOP 5 * FROM "public".mergedentry'
    
    service = TAPService(URL)
    result = service.run_sync(
        QUERY,
        format=FORMAT)

    # Give the query result to the MIVOt viewer which
    # generates the model view of the data
    m_viewer = MivotViewer(result, resolve_ref=True)
    
    while m_viewer.next_row_view():
        # get the Python object (MangoObject)representing the current row
        mivot_instance = m_viewer.dm_instance
        sp_location = []
        sp_filter = []
        mag = []
        mag_error = []
        if mivot_instance.dmtype == "mango:MangoObject":
            for mango_property in mivot_instance.propertyDock:
                if  mango_property.dmtype == "mango:Brightness":
                    if mango_property.value.value:
                        # get the flux value, error and unit
                        unit = mango_property.value.unit
                        mag.append(mango_property.value.value)
                        mag_error.append(mango_property.error.sigma.value)
                        phot_cal = mango_property.photCal
                        # get the filter spectral location (filter name + location)
                        spectral_location = phot_cal.photometryFilter.spectralLocation
                        sp_location.append(
                            spectral_location.value.value)
                        sp_filter.append(phot_cal.identifier.value)
                        sp_unit = spectral_location.unitexpression.value
                    
            plot_sed(mivot_instance.identifier.value, unit, sp_unit, mag, mag_error,
                     sp_filter, sp_location)  
                         
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
