# import numpy as np
# import h5py
# import AurigaiaRead

# lv_4_halos = np.arange(1, 31)
# lv_3_halos = np.array([6, 16, 21, 23, 24, 27])

# ptypes = ["star", "dm", "gas"]
# p_ind = {"dm": 1, "gas": 0, "star": 4}
# dm_inds = [1, 2, 3]
# snap0s = {3: 63, 4: 127}
# snap_1Gyrs = {3: 13, 4: 28}
# hubble_time = 13.815

# folder = AurigaiaRead.__path__[0]  # type:ignore
# snap_times_lv4 = np.load(folder + "/data/AuLv4SnapTimes.npy")
# snap_times_lv3 = np.load(folder + "/data/AuLv3SnapTimes.npy")
# snap_times_dic = {3: snap_times_lv3, 4: snap_times_lv4}


# def get_snap_times(level=4) -> np.ndarray:
#     snap_times = np.load(folder + f"data/AuLv{level}SnapTimes.npy")
#     print(snap_times)
#     return snap_times


# def get_sim_snap_dic(sim_snap) -> dict:
#     sim_snap_dic = {"star": sim_snap.s, "dm": sim_snap.dm, "gas": sim_snap.gas}
#     return sim_snap_dic


# def snap_to_time(snaps: np.ndarray, level=4) -> np.ndarray:
#     times = np.full(snaps.shape, fill_value=np.nan)
#     snap_filt = snaps > 0
#     times[snap_filt] = snap_times_dic[level][snap0s[level] - snaps[snap_filt]]
#     return times


# def time_to_snap(times: float | np.ndarray, round: bool = True, level: int = 4) -> np.ndarray:
#     snaps = np.interp(times, snap_times_dic[level], np.arange(1, snap0s[level] + 1))
#     if round:
#         snaps = np.round(snaps).astype(int)
#     return snaps


# def create_snap_times() -> np.ndarray:
#     hubble_time = 13.815
#     folder = "/cosma5/data/Gigagalaxy/pakmorr/level3_MHD/halo6/output/"
#     n_snaps = 63
#     snaps_lv3 = np.arange(1, n_snaps + 1)[::-1]
#     snap_times_lv3 = np.zeros(n_snaps)
#     for i, snap in enumerate(snaps_lv3):
#         file = f"{folder}/snapdir_{snap:03}/snapshot_{snap:03}.0.hdf5"
#         with h5py.File(file) as hf:
#             snap_times_lv3[i] = float(dict(hf["Header"].attrs)["Time"]) * hubble_time  # type:ignore
#         print(snap, snap_times_lv3[i])
#     # np.save("AuLv3SnapTimes",snap_times_lv3)
#     return snap_times_lv3


# def snaps0_to_level(snaps0: int) -> int:
#     if snaps0 == 127:
#         level = 4
#     elif snaps0 == 63:
#         level = 3
#     else:
#         raise ValueError(f"snaps0={snaps0}, unrecognised level!")
#     return level
