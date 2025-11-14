import pytest
import astropy.units as u
from astropy.coordinates import SkyCoord
from pyvo.dal.scs import SCSService

from pyvo.utils import activate_features
from pyvo.mivot.viewer.mivot_viewer import MivotViewer
from pyvo.mivot.features.sky_coord_builder import SkyCoordBuilder

# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

def run():
    # run a regular SCS query against SIMBAD
    scs_srv = SCSService("https://simbad.cds.unistra.fr/cone")

    query_result = scs_srv.search(
        pos=SkyCoord(ra=269.452076 * u.degree,
                     dec=4.6933649 * u.degree, frame='icrs'),
        radius=0.1,
        verbosity=3,
        responseformat="mivot",
        maxrec=10)
    # Give the query result to the MIVOt viewer which
    # generates the model view of the data
    m_viewer = MivotViewer(query_result, resolve_ref=True)

    while m_viewer.next_row_view():
        # get the Python object (MangoObject)representing the current row
        mivot_instance = m_viewer.dm_instance
        # Iterate over the properties of the MangoObject
        for mango_property in mivot_instance.propertyDock:
            # build SkyCoord for EpochPosition properties
            if mango_property.dmtype == "mango:EpochPosition":
                scb = SkyCoordBuilder(mivot_instance)
                print(scb.build_sky_coord())


if __name__ == "__main__":
    run()
