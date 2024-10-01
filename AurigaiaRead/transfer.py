
    extra_mag_index = {}
    for iband, band in enumerate(("U", "B", "R", "J", "H", "K", "V", "I")):
        extra_mag_index[band + "magnitude"] = iband

            for name in datasets:
                if name in extra_mag_index:
                    # This is a magnitude stored in the Magnitudes dataset
                    if mag_data is None:
                        mag_data = infile["Stardata"]["Magnitudes"][...]
                    data_thisfile[name] = mag_data[:, extra_mag_index[name]]
                else:
                    # This is a normal dataset
                    data_thisfile[name] = infile["Stardata"][name][...]
available_halos = [6, 16, 21, 23, 24, 27]
available_angles = [30, 120, 210, 300]
available_ext = [True, False]


random_sample

def add_posvel_data(data, datasets):
    checked_datasets = list(data.keys())
    solar_params = data["Parameters"]
    for p in ["", "Obs"]:
        if "Pos" + p in datasets and "Vel" + p in datasets:
            # print("Applying Cartesian_Conversion")
            data["gal_Pos"+p], data["gal_Vel"+p] = cc.galactic_cartesian_coordinates(data["HCoordinates" + p],data["HVelocities" +p])
            data["Pos" + p], data["Vel" + p] = cc.galactic_origin_coords(solar_params,data["gal_Pos"+p], data["gal_Vel"+p])
        elif "Pos" + p in datasets:
            # print("Applying Cartesian_Conversion")
            data["gal_Pos" + p] = cc.galactic_cartesian_coordinates(data["HCoordinates" + p])
            data["Pos" + p]= cc.galactic_origin_coords(solar_params,data["gal_Pos"+p])
        for x in ["HVelocities", "HCoordinates"]:
            if x + p not in datasets and x + p in checked_datasets:
                del data[x + p]
    return data

import numpy as np

import astropy.units as u
from astropy.coordinates import ICRS, Galactic


def cart_to_cylinder(pos, vel=None):
    ''' Cartesian to Cylindrical Coords'''
    x = pos[:, 0]
    y = pos[:, 1]
    z = pos[:, 2]
    R = np.sqrt((x * x) + (y * y))
    phi = np.arctan2(y, x)

    if vel is not None:
        vx = vel[:, 0]
        vy = vel[:, 1]
        vz = vel[:, 2]
        vR = ((np.cos(phi) * vx) + (np.sin(phi) * vy))
        vT = ((np.cos(phi) * vy) - (np.sin(phi) * vx))
        return (R, phi, z, vR, vT, vz)
    else:
        return (R, phi, z)

from numpy import arctan2, sqrt
import numexpr as ne

# def cart_to_spherical (pos, vel=None, ceval=ne.evaluate):
#     """ x = r cos(theta)cos(pi)
#         y = r cos(theta) sin(pi)
#         z = r sin(theta)

#         ceval: backend to use:
#               - eval :  pure Numpy
#               - numexpr.evaluate:  Numexpr """

    # """
    # ACTUALLY:
    #     x = r sin(theta)cos(pi)
    #     y = r sin(theta) sin(pi)
    #     z = r cos(theta)
    #     with theta 0<pi
    #     ceval: backend to use:
    #           - eval :  pure Numpy
    #           - numexpr.evaluate:  Numexpr """
#     x = pos[:,0]
#     y = pos[:,1]
#     z = pos[:,2]
#     phi = ceval('arctan2(y,x)')
#     xy2 = ceval('x**2 + y**2')
#     theta = ceval('arctan2(z, sqrt(xy2))')
#     r = eval('sqrt(xy2 + z**2)')
#     return r, phi, theta

def add_cart_to_cylinder(stars):
    props = list(stars.keys())
    for e in ["", "Obs"]:
        x="Pos" + e
        v = "Vel" + e
        if x in props and v in props:
            stars["R"+e], stars["phi"+e], stars["z"+e], stars["vR"+e], stars["vT"+e], stars["vZ"+e] = cart_to_cylinder(stars[x], stars[v])
        if x in props:
            stars["R"+e], stars["phi"+e], stars["z"+e] = cart_to_cylinder(stars[x], vel=None)
    return stars

def galactic_origin_coords(solar_params, gal_pos, gal_vel=None):
    print("Centring on gal")
    solar_pos = np.array([solar_params["solarradius"],0,solar_params["solarheight"]])*1000
    print(solar_pos)
    try:
        Pos = gal_pos + solar_pos[None,:]*u.kpc
    except Exception as e:
        print(e)
        Pos = gal_pos - solar_pos[None,:]
    if gal_vel is None:
        return Pos

    solar_vel = np.array([solar_params["usun"], solar_params["vsun"] + solar_params["vlsr"], solar_params["wsun"]])
    print(solar_vel)
    try:
        Vel = gal_vel + solar_vel[None,:]*(u.km/u.s)
    except Exception as e:
        print(e)
        Vel = gal_vel + solar_vel[None,:]
    return Pos, Vel

def galactic_cartesian_coordinates(hcoordinates, hvelocities=None):
    """
    John Helly Function
    Calculate Galactic cartesian coordinates of stars
    from a mock catalogue given equatorial (ICRS) coordinates.
    In this system the disk of the galaxy is in the x-y
    plane with the Sun at the origin and the galactic
    centre in the +x direction.

    hcoordinates - [N,3] array of ICRS equatorial coordinates of N
                   stars  Coordinates are defined as follows:

    hcoordinates[:,0] - right acension of the stars in radians
    hcoordinates[:,1] - declination of the stars in radians
    hcoordinates[:,2] - parallax of the stars in arcseconds

    Can optionally also specify velocities:

    hvelocities[:,0] - proper motion in right ascension * cos(declination)
                       (arcsec/yr)
    hvelocities[:,1] - proper motion in declination (arcsec/yr)
    hvelocities[:,2] - radial velocity (km/s)

    Returns:

    pos - [N,3] array with heliocentric cartesian coordinates in kpc.

    If hvelocities is not None, also returns

    vel - [N,3] array with heliocentric cartesian velocities in km/s
    """

    # Extract coordinate components from the HCoordinates dataset
    ra = u.Quantity(hcoordinates[:, 0], unit=u.radian)
    dec = u.Quantity(hcoordinates[:, 1], unit=u.radian)
    parallax = u.Quantity(hcoordinates[:, 2], unit=u.arcsec)

    # Extract velocities from HVelocities dataset if present
    if hvelocities is not None:
        pm_ra_cosdec = u.Quantity(hvelocities[:, 0], unit=u.arcsec / u.year)
        pm_dec = u.Quantity(hvelocities[:, 1], unit=u.arcsec / u.year)
        rv = u.Quantity(hvelocities[:, 2], unit=u.km / u.second)

    # Calculate distance to each star:
    # Distance in parsecs is just 1.0/(parallax in arcsecs),
    # but here we let astropy deal with the units.
    dist = parallax.to(u.kpc, equivalencies=u.parallax())

    # Translate to galactic coordinates using astropy
    if hvelocities is not None:
        # Have positions and velocities
        coords = ICRS(ra=ra, dec=dec, distance=dist,
                      pm_ra_cosdec=pm_ra_cosdec, pm_dec=pm_dec,
                      radial_velocity=rv).transform_to(Galactic)
        pos = coords.cartesian.get_xyz().transpose()
        vel = coords.cartesian.differentials["s"].get_d_xyz().transpose()
        return pos, vel
    else:
        # Just have positions
        coords = ICRS(ra=ra, dec=dec, distance=dist).transform_to(Galactic)
        pos = coords.cartesian.get_xyz().transpose()
        return pos
