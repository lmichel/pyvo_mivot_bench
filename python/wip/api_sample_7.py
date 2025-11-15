"""
"""

import pytest
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy.coordinates import SkyCoord
from pyvo.dal.scs import SCSService

from pyvo.utils import activate_features
from pyvo.mivot.viewer.mivot_viewer import MivotViewer
from pyvo.mivot.features.sky_coord_builder import SkyCoordBuilder
from pyvo.mivot.utils.dict_utils import DictUtils
from pyvo.mivot.utils.xml_utils import XmlUtils

dates =[]
ras = []
decs = []
now_ras = []
now_decs = []

# Enable MIVOT-specific features in the pyvo library
activate_features("MIVOT")

scs_srv = SCSService("https://vizier.cds.unistra.fr/viz-bin/conesearch/V1.5/I/239/hip_main")

query_result = scs_srv.search(
    pos=SkyCoord(ra=52.26708 * u.degree, dec=59.94027 * u.degree, frame='icrs'),
    radius=0.5)

# The MIVOt viewer generates the model view of the data
m_viewer = MivotViewer(query_result, resolve_ref=True)
# Get the first instance mapped in the MIVOt <TEMPLATES>
XmlUtils.pretty_print(m_viewer._mapping_block)
mivot_instance = m_viewer.dm_instance
# iterate over the table rows
while m_viewer.next_row_view():

    if mivot_instance.dmtype == "mango:EpochPosition":
        scb = SkyCoordBuilder(mivot_instance)
        sky_coord = scb.build_sky_coord()
        print(sky_coord)

            
        dates.append(f" ({str(sky_coord.obstime).replace('J', '')})")
        ras.append(sky_coord.ra.deg)
        decs.append(sky_coord.dec.deg)
        sky_coord = sky_coord.apply_space_motion(new_obstime=Time('J2500'))
        now_ras.append(sky_coord.ra.deg)
        now_decs.append(sky_coord.dec.deg)

_, ax = plt.subplots()
ax.ticklabel_format(useOffset=False)
plt.title("I/239 in 2500")
plt.xlabel("RA")
plt.ylabel("DEC")
ax.scatter(ras, decs, color="blue")
ax.scatter(now_ras, now_decs, color="red")

for i, txt in enumerate(dates):
    ax.annotate(txt, (ras[i], decs[i]))

plt.show()


if __name__ == "__main__":
    run()
