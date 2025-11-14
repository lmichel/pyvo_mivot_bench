import pytest
import astropy.units as u
from astropy.coordinates import SkyCoord
from pyvo.dal.scs import SCSService

from pyvo.utils import activate_features
from pyvo.mivot.utils.xml_utils import XmlUtils
from pyvo.mivot.writer.instances_from_models import InstancesFromModels
from pyvo.mivot.viewer.mivot_viewer import MivotViewer
from pyvo.mivot.features.sky_coord_builder import SkyCoordBuilder

from pyvo.mivot.utils.dict_utils import DictUtils

pytestmark = pytest.mark.skipif(True)

# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

@pytest.mark.skip(reason="no way of currently testing this")
def run():

    scs_srv = SCSService("https://vizier.cds.unistra.fr/viz-bin/conesearch/V1.5/I/239/hip_main")

    query_result = scs_srv.search(
        pos=SkyCoord(ra=52.26708 * u.degree, dec=59.94027 * u.degree, frame='icrs'),
        radius=0.5)


    m_viewer = MivotViewer(query_result, resolve_ref=True)

    mivot_instance = m_viewer.dm_instance
    DictUtils.print_pretty_json(mivot_instance.to_dict())
    while m_viewer.next_row_view():
        print(mivot_instance.dmtype)
        if mivot_instance.dmtype == "mango:EpochPosition":
            scb = SkyCoordBuilder(mivot_instance)
            print(scb.build_sky_coord())


if __name__ == "__main__":
    run()
