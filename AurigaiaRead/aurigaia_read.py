# from pynbody.zooms.auriga import AurigaiaLikeHDFSnap  # pyright:ignore
from .AurigaiaSnap_class import AurigaiaSnap
from .aurigaia_halo_params import AuGHaloParams  # , find_halo_p_from_path
# from .file_names import find_halo_p_from_path
# from .config import use_cache_default


class AuGPynbody(AurigaiaSnap):
    def __init__(
        self,
        p_folder: str | None = None,
        AuG_params: AuGHaloParams | None = None,
        **kwargs,
    ):
        # if p_folder is not None and AuG_params is None:
        # self.halo_p = find_halo_p_from_path(p_folder)

        self.halo_p = AuG_params if AuG_params is not None else AuGHaloParams(**kwargs)

        # self.halo_file, self.p_file, self.analysis_folder = (
        #     self.halo_p.halo_file[:-8],
        #     self.halo_p.particle_file[:-8],
        #     self.halo_p.analysis_folder,
        # )

        # if self.halo_p.snap < 20:
        #     print("too early snap to orientate")
        #     orientate = False

        AurigaiaSnap.__init__(self, self.halo_p.data_file)
        # self.physical_units()

        # self._host = None

    # def __new__(cls):
    #     return cls.star

    # @property
    # def host(self) -> HostData:
    #     if self._host is None:
    #         h0 = self.halos()[0]
    #         h0.physical_units()
    #         print("Currently host on 0")
    #         self._host = HostData(h0)
    #     return self._host

    # TODO Add group selection in similar way?
    # def groups(self):
    #
    #     return


# needed to run attributes!
from . import attributes

# class HostData:
#     """Make Host Data more accessable"""

#     def __init__(self, h0):
#         self._translate_init()
#         self.h0 = h0

#     def __getitem__(self, item):
#         return self.h0.properties[self.translate[item]]

#     def _translate_init(self):
#         translate = {
#             "M200": "Group_M_Crit200",
#             "R200": "Group_R_Crit200",
#         }
#         self.translate = translate
