
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib as mpl

from PyNEC import *
import numpy as np
from pprint import pprint
from antenna_util import *
from context_clean import *
import math

# creation of a nec context
context=nec_context()

# get the associated geometry
geo = context.get_geometry()

# nec = context_clean(nec_context())
# nec.set_extended_thin_wire_kernel(True)

# geo = geometry_clean(nec.get_geometry())

#add wires to the geometry
freq = 146.520
length_ft = 468.0 / freq
drv_len = length_ft * 12 * 25.4 / 1000  #  driven element length in meters
print(drv_len)
num_segs = 35
tag_num = 1
wire_rad = 0.001

# throw in a polarization variable
dipole_tag = 1
center      = np.array([0, 0, 0])
half_height = np.array([0  , 0, drv_len/2.0])
top         = center + half_height
bottom      = center - half_height
nr_segments = 35
geo.wire(dipole_tag, nr_segments, bottom[0],bottom[1],bottom[2], top[0], top[1], top[2], wire_rad, 1.0, 1.0)
# examples 
# geo.wire(tag, num_segs, x1, y1, z1, x2, y2, z2, radius, rtap, rrad)
# geo.wire(tag_num, num_segs, drv_len / 2 , 0, 0, -(drv_len / 2), 0, 0, 0.001, 1.0, 1.0)


#reflector
ref_len = drv_len * 1.04
pos = -1 * ref_len * 0.5
dipole_tag = 2
center      = np.array([pos, 0, 0])
half_height = np.array([0  , 0, ref_len/2.0])
top         = center + half_height
bottom      = center - half_height
nr_segments = 35
geo.wire(dipole_tag, nr_segments, bottom[0],bottom[1],bottom[2], top[0], top[1], top[2], wire_rad, 1.0, 1.0)

#director
dir_len = drv_len * 0.96
pos = dir_len * 0.5
dipole_tag = 3
center      = np.array([pos, 0, 0])
half_height = np.array([0  , 0, dir_len/2.0])
top         = center + half_height
bottom      = center - half_height
nr_segments = 35
geo.wire(dipole_tag, nr_segments, bottom[0],bottom[1],bottom[2], top[0], top[1], top[2], wire_rad, 1.0, 1.0)

# compare these to the app.

#add wires to the geometry
# geo.wire(0, 36, 0, 0, 0, -0.042, 0.008, 0.017, 0.001, 1.0, 1.0)

brass_conductivity = 15600000 # mhos
# nec.set_wire_conductivity(brass_conductivity)

context.geometry_complete(0)

context.gn_card(-1, 0, 0, 0, 0, 0, 0, 0)

#add a "ex" card to specify an excitation
#
center_seg = int((num_segs + 1) / 2) + 1
print(f'Center Segment = {center_seg} of {num_segs}')
context.ex_card(0, tag_num, center_seg, 0, 0, 0, 0, 0, 0, 0, 0)

#add a "fr" card to specify the frequency 
context.fr_card(0, 0, freq, 1)

#add a "rp" card to specify radiation pattern sampling parameters and to cause program execution
'''
calc_mode	This integer selects the mode of calculation for the radiated field. Some values of (calc_mode) will affect the meaning of the remaining parameters on the card. Options available for calc_mode are:
    O - normal mode. Space-wave fields are computed. An infinite ground plane is included if it has been specified previously on a GN card; otherwise, the antenna is in free space.
    1 - surface wave propagating along ground is added to the normal space wave. This option changes the meaning of some of the other parameters on the RP card as explained below, and the results appear in a special output format. Ground parameters must have been input on a GN card. The following options cause calculation of only the space wave but with special ground conditions. Ground conditions include a two-medium ground (cliff where the media join in a circle or a line), and a radial wire ground screen. Ground parameters and dimensions must be input on a GN or GD card before the RP card is read. The RP card only selects the option for inclusion in the field calculation. (Refer to the GN and GD cards for further explanation.)
    2 - linear cliff with antenna above upper level. Lower medium parameters are as specified for the second medium on the GN card or on the GD card.
    3 - circular cliff centered at origin of coordinate system: with antenna above upper level. Lower medium parameters are as specified for the second medium on the GN card or on the GD card.
    4 - radial wire ground screen centered at origin.
    5 - both radial wire ground screen and linear cliff.
    6 - both radial wire ground screen ant circular cliff.
n_theta	The number of theta angles.
n_phi	The number of phi angles.
output_format	The output format:
0 major axis, minor axis and total gain printed.
1 vertical, horizontal ant total gain printed.
normalization	Controls the type of normalization of the radiation pattern
0 no normalized gain.
1 major axis gain normalized.
2 minor axis gain normalized.
3 vertical axis gain normalized.
4 horizontal axis gain normalized.
5 total gain normalized.
D	Selects either power gain or directive gain for both standard printing and normalization. If the structure excitation is an incident plane wave, the quantities printed under the heading "gain" will actually be the scattering cross section (a/lambda 2 ) and will not be affected by the value of d. The column heading for the output will still read "power" or "directive gain," however.
0 power gain.
1 directive gain.
A	- Requests calculation of average power gain over the region covered by field points.
0 no averaging.
1 average gain computed.
2 average gain computed, printing of gain at the field points used for averaging is suppressed. If n_theta or NPH is equal to one, average gain will not be computed for any value of A since the area of the region covered by field points vanishes.
theta0	- Initial theta angle in degrees (initial z coordinate in meters if calc_mode = 1).
phi0	- Initial phi angle in degrees.
delta_theta	- Increment for theta in degrees (increment for z in meters if calc_mode = 1).
delta_phi	- Increment for phi in degrees.
radial_distance	- Radial distance (R) of field point from the origin in meters. radial_distance is optional. If it is zero, the radiated electric field will have the factor exp(-jkR)/R omitted. If a value of R is specified, it should represent a point in the far-field region since near components of the field cannot be obtained with an RP card. (If calc_mode = 1, then radial_distance represents the cylindrical coordinate phi in meters and is not optional. It must be greater than about one wavelength.)
gain_norm	- Determines the gain normalization factor if normalization has been requested in the normalization parameter. If gain_norm is zero, the gain will be normalized to its maximum value. If gain_norm is not zero, the gain wi11 be normalized to the value of gain_norm.
'''

num_thetas = 91
num_phis = 91

NO_GAIN = 0
MAJOR_GAIN = 1
MINOR_GAIN = 2
VERT_GAIN = 3
HORIZ_GAIN = 4
TOTAL_GAIN = 5
norm = TOTAL_GAIN

POWER_GAIN = 0
DIREC_GAIN = 1
pd = POWER_GAIN

NO_AVG = 0
AVG_GAIN = 1
AVG_GAIN_FP = 2
avg = NO_AVG

# (0, 0) is looking down from the top
# (90, 0) is the side view
theta_0 = 90.0  # from the vertical (z) axis
phi_0 = 0.0  # from the horizontal (x) axis

theta_d = 4.0
phi_d = 4.0



context.rp_card(0, num_thetas, num_phis, 0, norm, pd, avg, theta_0, phi_0, theta_d, phi_d, 1.0, 0.0)

#get the radiation_pattern
rp = context.get_radiation_pattern(0)

# Gains are in decibels
gains_db = rp.get_gain()
gains = 10.0**(gains_db / 10.0)
thetas = rp.get_theta_angles() * 3.1415 / 180.0
phis = rp.get_phi_angles() * 3.1415 / 180.0


# Plot stuff
import matplotlib.pyplot as plt

ax = plt.subplot(111, polar=True)
ax.plot(thetas, gains[:,0], color='r', linewidth=3)
ax.grid(True)

ax.set_title("6 element NBS yagi - side view", va='bottom')
plt.savefig('RadiationPattern.png')
plt.show()

