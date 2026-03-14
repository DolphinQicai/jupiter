import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import Time
from astropy.coordinates import (
    solar_system_ephemeris,
    get_body_barycentric,
    HeliocentricTrueEcliptic,
    GeocentricTrueEcliptic,
    SkyCoord
)
import astropy.units as u

solar_system_ephemeris.set("G:/迅雷下载/de430.bsp")

start_t = Time("2025-02-01")
end_t = Time("2026-12-30")
t = Time(np.arange(start_t.jd, end_t.jd + 1, 1), format='jd')
n_days = len(t)

jupiter = get_body_barycentric('jupiter', t)
sun = get_body_barycentric('sun', t)
jup_helio_icrs = jupiter - sun
sc_helio = SkyCoord(jup_helio_icrs, frame='icrs')
jup_helio_ecl = sc_helio.transform_to(HeliocentricTrueEcliptic)
x_h = jup_helio_ecl.cartesian.x.to(u.AU).value
y_h = jup_helio_ecl.cartesian.y.to(u.AU).value

earth = get_body_barycentric('earth', t)
jup_geo_icrs = jupiter - earth
sc_geo = SkyCoord(jup_geo_icrs, frame='icrs')
jup_geo_ecl = sc_geo.transform_to(GeocentricTrueEcliptic)
x_g = jup_geo_ecl.cartesian.x.to(u.AU).value
y_g = jup_geo_ecl.cartesian.y.to(u.AU).value


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plt.subplots_adjust(top=0.85)

x_h_lim = (-6, 2)
y_h_lim = (-2, 6)

x_g_lim = (-6, 2)
y_g_lim = (-2, 6)

ax1.set_title("Heliocentric (Top-down view)", fontsize=12)
ax1.set_xlabel("X (AU)")
ax1.set_ylabel("Y (AU)")
ax1.set_xlim(x_h_lim)
ax1.set_ylim(y_h_lim)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.plot(0, 0, 'o', color='gold', markersize=12, markeredgecolor='k', label='Sun')
line_helio, = ax1.plot([], [], '-', color='tab:orange', linewidth=2, label='Jupiter Trail')
point_helio, = ax1.plot([], [], 'o', color='red', markersize=8, label='Jupiter Now')
ax1.legend(loc='upper right')

ax2.set_title("Geocentric (Apparent motion from Earth)", fontsize=12)
ax2.set_xlabel("X (AU)")
ax2.set_ylabel("Y (AU)")
ax2.set_xlim(x_g_lim)
ax2.set_ylim(y_g_lim)
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)
ax2.plot(0, 0, 'o', color='tab:blue', markersize=12, markeredgecolor='k', label='Earth')
line_geo, = ax2.plot([], [], '-', color='tab:orange', linewidth=2, label='Jupiter Trail')
point_geo, = ax2.plot([], [], 'o', color='red', markersize=8, label='Jupiter Now')
ax2.legend(loc='upper right')


def init():
    line_helio.set_data([], [])
    point_helio.set_data([], [])
    line_geo.set_data([], [])
    point_geo.set_data([], [])
    fig.suptitle(f"Date: Loading...", fontsize=16)
    return line_helio, point_helio, line_geo, point_geo

def update(frame):
    line_helio.set_data(x_h[:frame+1], y_h[:frame+1])
    point_helio.set_data([x_h[frame]], [y_h[frame]])
    
    line_geo.set_data(x_g[:frame+1], y_g[:frame+1])
    point_geo.set_data([x_g[frame]], [y_g[frame]])
    
    current_date_str = t[frame].isot[:10]
    fig.suptitle(f"Date: {current_date_str}", fontsize=16, weight='bold')
    
    return line_helio, point_helio, line_geo, point_geo

ani = animation.FuncAnimation(
    fig,
    update,
    frames=n_days,
    init_func=init,
    interval=50,
    blit=False
)

# plt.tight_layout()
# plt.show()

ani.save('jupiter_motion_2025_2026.mp4', writer='ffmpeg', fps=20, dpi=200, bitrate=2000)