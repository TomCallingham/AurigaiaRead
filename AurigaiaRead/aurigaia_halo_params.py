from .config import aurigaia_folder, folder_type


class AuGHaloParams:
    def __init__(self, halo_n: int = 6, angle=30, ext=True, gaia_dr=3):
        self.halo_n = halo_n
        self.angle = angle
        self.ext = ext
        self.gaia_dr = gaia_dr

        self.data_file = aurigaia_file_names(self.halo_n, self.angle, self.ext, self.gaia_dr)

    #     self.analysis_folder = (
    #         f"{my_aurigaia_folder}/level{self.level}_{self.sim_type}/halo_{self.halo_n}/snap_{self.snap:03d}/"
    #     )
    #     self.analysis_folder_root = f"{my_aurigaia_folder}/level{self.level}_{self.sim_type}/halo_{self.halo_n}/"
    #     self.analysis_folder_z0 = (
    #         f"{my_aurigaia_folder}/level{self.level}_{self.sim_type}/halo_{self.halo_n}/snap_{self.snap0:03d}"
    #     )

    def __str__(self):
        return f"AuParams= [halo_n:{self.halo_n}, angle:{self.angle}, ext: {self.ext}]"


def aurigaia_file_names(halo_n, angle, ext, gaia_dr=3) -> str:
    if folder_type == "cosma":
        return aurigaia_file_names_cosma(halo_n, angle, ext, gaia_dr)
    print("Only cosma files defined!")
    return aurigaia_file_names_cosma(halo_n, angle, ext, gaia_dr)

    # return aurigaia_file_names_not_cosma(halo_n, angle, ext, gaia_dr)


def aurigaia_file_names_cosma(halo_n, angle, ext, gaia_dr=3) -> str:
    """type is either 'MHD' or 'DM'"""
    angle_text = f"{angle:03d}"
    noex_text = "" if ext else "noex_"
    "halo_6/mockdir_angle030/mock_030"
    data_file = aurigaia_folder + f"halo_{halo_n}/mockdir_angle{angle_text}/mock_{noex_text}{angle_text}"
    return data_file
