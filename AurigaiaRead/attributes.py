from .aurigaia_read import AurigaiaSnap
from pynbody import units
from pynbody.array import SimArray

# from pynbody.zooms.property_cache import multiple_read

kms = units.km / units.s
kms2 = kms * kms

extra_mag_index = {f"{band}magnitude": i for i, band in enumerate(["U", "B", "R", "J", "H", "K", "V", "I"])}

# PosVel
# @AurigaiaSnap.derived_quantity
# def R(sim) -> SimArray:
#     return sim["rxy"]


# @AurigaiaSnap.derived_quantity
# def angle_phi(sim) -> SimArray:
#     return sim["az"]


# @AurigaiaSnap.derived_quantity
# def vR(sim) -> SimArray:
#     return sim["vrxy"]


# @AurigaiaSnap.derived_quantity
# def vT(sim) -> SimArray:
#     return sim["vcxy"]


# @AurigaiaSnap.derived_quantity
# def E_sim(sim) -> SimArray:
#     return sim["te"]


# @AurigaiaSnap.derived_quantity
# def U_sim(sim) -> SimArray:
#     return sim["phi"]


# @AurigaiaSnap.derived_quantity
# def Lvec(sim) -> SimArray:
#     return sim["j"]


# @AurigaiaSnap.derived_quantity
# def Lx(sim) -> SimArray:
#     return sim["Lvec"][:, 0]


# @AurigaiaSnap.derived_quantity
# def Ly(sim) -> SimArray:
#     return sim["Lvec"][:, 1]


# @AurigaiaSnap.derived_quantity
# def Lz(sim) -> SimArray:
#     return sim["jz"]


# @AurigaiaSnap.derived_quantity
# def Lp(sim) -> SimArray:
#     return sim["Lperp"]


# @AurigaiaSnap.derived_quantity
# def En(sim) -> SimArray:
#     return sim["E"]


# @AurigaiaSnap.derived_quantity
# def touch_a_ind(sim) -> SimArray:
#     touch_data = match_touch_z0ids(sim)
#     return multiple_read(sim, touch_data, "touch_a_ind")


# @AurigaiaSnap.derived_quantity
# def touch_z0ids(sim) -> SimArray:
#     touch_data = match_touch_z0ids(sim)
#     return multiple_read(sim, touch_data, "touch_z0ids")


# @AurigaiaSnap.derived_quantity
# def touch_r_sat(sim) -> SimArray:
#     touch_data = match_touch_z0ids(sim)
#     return multiple_read(sim, touch_data, "touch_r_sat")


# @AurigaiaSnap.derived_quantity
# def touch_U_sim(sim) -> SimArray:
#     touch_data = match_touch_z0ids(sim)
#     return multiple_read(sim, touch_data, "touch_U_sim")


# @AurigaiaSnap.derived_quantity
# def touch_E_sim(sim) -> SimArray:
#     touch_data = match_touch_z0ids(sim)
#     return multiple_read(sim, touch_data, "touch_E_sim")


# TODO
# @AurigaiaSnap.derived_quantity
# def birth_snap(sim) -> SimArray:
#     fam_str = get_fam_str(sim)
#     if fam_str != "star":
#         raise AttributeError("Only for stars")
#     return group_id


# @AurigaiaSnap.derived_quantity
# def birth_sub(sim) -> SimArray:
#     fam_str = get_fam_str(sim)
#     if fam_str != "star":
#         raise AttributeError("Only for stars")
#     return group_id
