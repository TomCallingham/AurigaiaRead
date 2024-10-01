from pynbody.snapshot.gadgethdf import _GadgetHdfMultiFileManager
from pynbody.family import get_family


class _AurigaiaHdfMultiFileManager(_GadgetHdfMultiFileManager):
    _size_from_hdf5_key = "ParticleID"


# from pynbody.snapshot.gadgethdf import _GadgetHdfMultiFileManager,SimSnap, namemapper,configparser, config_parser,units,_default_type_map, _all_hdf_particle_groups,functools
from pynbody.snapshot.gadgethdf import (
    _GadgetHdfMultiFileManager,
    SimSnap,
    configparser,
    config_parser,
    units,
    _default_type_map,
    _all_hdf_particle_groups,
    functools,
)

aurigaia_units_dic = {
    "Age": units.Gyr,
    "Mass": units.Msol,
    "EffectiveTemperature": units.K,
}


class AurigaiaSnap(SimSnap):
    """
    Class that reads HDF Gadget snapshots.
    """

    # _multifile_manager_class = _GadgetHdfMultiFileManager
    _multifile_manager_class = _AurigaiaHdfMultiFileManager
    _readable_hdf5_test_key = "Stardata"
    # _size_from_hdf5_key = "ParticleIDs"
    _size_from_hdf5_key = "ParticleID"
    # _namemapper_config_section = "gadgethdf-name-mapping"

    def __init__(self, filename):
        """Initialise a Gadget HDF snapshot.

        Spanned files are supported. To load a range of files ``snap.0.hdf5``, ``snap.1.hdf5``, ... ``snap.n.hdf5``,
        pass the filename ``snap``. If you pass e.g. ``snap.2.hdf5``, only file 2 will be loaded.
        """

        super().__init__()

        self._filename = filename

        self._init_hdf_filemanager(filename)

        # self._translate_array_name = namemapper.AdaptiveNameMapper(self._namemapper_config_section,
        #                                                            return_all_format_names=True) # required for swift
        self._init_unit_information()
        self.__init_family_map()
        self.__init_file_map()
        self.__init_loadable_keys()
        # self._mass_dtype =  np.float64
        # self._init_properties()
        self._decorate()
        # self = self.star

    def _get_hdf_header_attrs(self):
        return self._hdf_files.get_header_attrs()

    def _get_hdf_parameter_attrs(self):
        return self._hdf_files.get_parameter_attrs()

    def _get_hdf_unit_attrs(self):
        return self._hdf_files.get_unit_attrs()

    def _init_hdf_filemanager(self, filename):
        self._hdf_files = self._multifile_manager_class(filename)

    def __init_loadable_keys(self):
        self._loadable_family_keys = {}
        all_fams = self.families()
        if len(all_fams) == 0:
            return

        for fam in all_fams:
            # self._loadable_family_keys[fam] = {"mass"}
            self._loadable_family_keys[fam] = {"Mass"}
            for hdf_group in self._all_hdf_groups_in_family(fam):
                for this_key in self._get_hdf_allarray_keys(hdf_group):
                    # ar_name = self._translate_array_name(this_key, reverse=True)
                    ar_name = this_key
                    self._loadable_family_keys[fam].add(ar_name)
            self._loadable_family_keys[fam] = list(self._loadable_family_keys[fam])

        self._loadable_keys = set(self._loadable_family_keys[all_fams[0]])
        for fam_keys in self._loadable_family_keys.values():
            self._loadable_keys.intersection_update(fam_keys)

        self._loadable_keys = list(self._loadable_keys)

    def _all_hdf_groups(self):
        for hdf_family_name in _all_hdf_particle_groups:
            yield from self._hdf_files.iter_particle_groups_with_name(hdf_family_name)

    def _all_hdf_groups_in_family(self, fam):
        for hdf_family_name in self._family_to_group_map[fam]:
            yield from self._hdf_files.iter_particle_groups_with_name(hdf_family_name)

    def __init_file_map(self):
        family_slice_start = 0

        all_families_sorted = self._families_ordered()

        self._gadget_ptype_slice = {}  # will map from gadget particle type to location in pynbody logical file map

        for fam in all_families_sorted:
            family_length = 0
            # A simpler and more readable version of the code below would be:
            #
            # for hdf_group in self._all_hdf_groups_in_family(fam):
            #     family_length += hdf_group[self._size_from_hdf5_key].size
            #
            # However, occasionally we need to know where in the pynbody file map the gadget particle types lie.
            # (Specifically this is used when loading subfind data.) So we need to expand that out a bit and also
            # keep track of the slice for each gadget particle type.

            ptype_slice_start = family_slice_start

            for particle_type in self._family_to_group_map[fam]:
                ptype_slice_len = 0
                for hdf_group in self._hdf_files.iter_particle_groups_with_name(particle_type):
                    ptype_slice_len += hdf_group[self._size_from_hdf5_key].size
                self._gadget_ptype_slice[particle_type] = slice(ptype_slice_start, ptype_slice_start + ptype_slice_len)
                family_length += ptype_slice_len
                ptype_slice_start += ptype_slice_len

            self._family_slice[fam] = slice(family_slice_start, family_slice_start + family_length)
            family_slice_start += family_length

        self._num_particles = family_slice_start

    def _families_ordered(self):
        # order by the PartTypeN
        all_families = list(self._family_to_group_map.keys())
        all_families_sorted = sorted(all_families, key=lambda v: self._family_to_group_map[v][0])
        return all_families_sorted

    def __init_family_map(self):
        self._family_to_group_map = {get_family("star"): ["Stardata"]}

    def _family_has_loadable_array(self, fam, name):
        """Returns True if the array can be loaded for the specified family.
        If fam is None, returns True if the array can be loaded for all families."""
        return name in self.loadable_keys(fam)

    def _get_all_particle_arrays(self, gtype):
        """Return all array names for a given gadget particle type"""

        # this is a hack to flatten a list of lists
        l = [item for sublist in [self._get_hdf_allarray_keys(x[gtype]) for x in self._hdf_files] for item in sublist]

        # now just return the unique items by converting to a set
        return list(set(l))

    def loadable_keys(self, fam=None):
        if fam is None:
            return self._loadable_keys
        else:
            return self._loadable_family_keys[fam]

    @staticmethod
    def _get_hdf_allarray_keys(group):
        """Return all HDF array keys underneath group (includes nested groups)"""
        keys = []

        def _append_if_array(to_list, name, obj):
            if not hasattr(obj, "keys"):
                to_list.append(name)

        group.visititems(functools.partial(_append_if_array, keys))
        return keys

    def _get_hdf_dataset(self, particle_group, hdf_name):
        """Return the HDF dataset resolving /'s into nested groups, and returning
        an apparent Mass array even if the mass is actually stored in the header"""

        ret = particle_group
        for tpart in hdf_name.split("/"):
            ret = ret[tpart]
        return ret

    @staticmethod
    def _get_cosmo_factors(hdf, arr_name):
        """Return the cosmological factors for a given array"""
        match = [
            s for s in GadgetHDFSnap._get_hdf_allarray_keys(hdf) if ((s.endswith("/" + arr_name)) & ("PartType" in s))
        ]
        if (arr_name == "mass" or arr_name == "masses") and len(match) == 0:
            # mass stored in header. We're out in the cold on our own.
            # warnings.warn("Masses are either stored in the header or have another dataset name; assuming the cosmological factor %s" % units.h**-1)
            return units.Unit("1.0"), units.h**-1
        if len(match) > 0:
            try:
                aexp = hdf[match[0]].attrs["aexp-scale-exponent"]
            except KeyError:
                # gadget4 <sigh>
                aexp = hdf[match[0]].attrs["a_scaling"]
            try:
                hexp = hdf[match[0]].attrs["h-scale-exponent"]
            except KeyError:
                # gadget4 <sigh>
                hexp = hdf[match[0]].attrs["h_scaling"]
            return units.a ** util.fractions.Fraction.from_float(
                float(aexp)
            ).limit_denominator(), units.h ** util.fractions.Fraction.from_float(float(hexp)).limit_denominator()
        else:
            return units.Unit("1.0"), units.Unit("1.0")

    def _load_array(self, array_name, fam=None):
        if not self._family_has_loadable_array(fam, array_name):
            raise OSError("No such array on disk")
        else:
            # translated_names = self._translate_array_name(array_name)
            translated_names = [array_name]
            dtype, dy, units = self.__get_dtype_dims_and_units(fam, translated_names)
            # print("Got to the end of derive!")
            # print(dtype, dy, units)

            if fam is None:
                target = self
                all_fams_to_load = self.families()
            else:
                target = self[fam]
                all_fams_to_load = [fam]

            target._create_array(array_name, dy, dtype=dtype)

            if units is not None:
                target[array_name].units = units
            else:
                target[array_name].set_default_units()

            # print("first units go?")
            # print(target[array_name].units)

            for loading_fam in all_fams_to_load:
                i0 = 0
                for hdf in self._all_hdf_groups_in_family(loading_fam):
                    npart = hdf[self._size_from_hdf5_key].size
                    if npart == 0:
                        continue
                    i1 = i0 + npart

                    for translated_name in translated_names:
                        try:
                            dataset = self._get_hdf_dataset(hdf, translated_name)
                        except KeyError:
                            continue
                    target_array = self[loading_fam][array_name][i0:i1]
                    assert target_array.size == dataset.size

                    dataset.read_direct(target_array.reshape(dataset.shape))

                    i0 = i1

    def __get_dtype_dims_and_units(self, fam, translated_names):
        if fam is None:
            fam = self.families()[0]

        inferred_units = units.NoUnit()
        representative_dset = None
        representative_hdf = None
        # not all arrays are present in all hdfs so need to loop
        # until we find one
        print(translated_names)
        for hdf0 in self._hdf_files:
            for translated_name in translated_names:
                try:
                    representative_dset = self._get_hdf_dataset(
                        hdf0[self._family_to_group_map[fam][0]], translated_name
                    )
                    break
                except KeyError:
                    continue

            if representative_dset is None:
                continue

            representative_hdf = hdf0
            inferred_units = aurigaia_units_dic.get(translated_name, units.NoUnit())
            if len(representative_dset) != 0:
                # suitable for figuring out everything we need to know about this array
                break

        if representative_dset is None:
            raise KeyError("Array is not present in HDF file")

        assert len(representative_dset.shape) <= 2

        if len(representative_dset.shape) > 1:
            dy = representative_dset.shape[1]
        else:
            dy = 1

        # Some versions of gadget fold the 3D arrays into 1D.
        # So check if the dimensions make sense -- if not, assume we're looking at an array that
        # is 3D and cross your fingers
        npart = len(representative_hdf[self._family_to_group_map[fam][0]][self._size_from_hdf5_key])

        if len(representative_dset) != npart:
            dy = len(representative_dset) // npart

        dtype = representative_dset.dtype
        return dtype, dy, inferred_units

    # _velocity_unit_key = 'UnitVelocity_in_cm_per_s'
    # _length_unit_key = 'UnitLength_in_cm'
    # _mass_unit_key = 'UnitMass_in_g'
    # _time_unit_key = 'UnitTime_in_s'

    def _init_unit_information(self):
        vel_unit = "km s^-1"  # Not used
        dist_unit = "Mpc"  # Not used
        mass_unit = "Msol"  # Used
        self._file_units_system = [units.Unit(x) for x in [vel_unit, dist_unit, mass_unit, "K"]]

    @classmethod
    def _test_for_hdf5_key(cls, f):
        with h5py.File(f, "r") as h5test:
            test_key = cls._readable_hdf5_test_key
            if test_key[-1] == "?":
                # try all particle numbers in turn
                for p in range(6):
                    test_key = test_key[:-1] + str(p)
                    if test_key in h5test:
                        return True
                return False
            else:
                return test_key in h5test

    @classmethod
    def _can_load(cls, f):
        if hasattr(h5py, "is_hdf5"):
            if h5py.is_hdf5(f):
                return cls._test_for_hdf5_key(f)
            elif h5py.is_hdf5(f.with_suffix(".0.hdf5")):
                return cls._test_for_hdf5_key(f.with_suffix(".0.hdf5"))
            else:
                return False
        else:
            if "hdf5" in f:
                warnings.warn(
                    "It looks like you're trying to load HDF5 files, but python's HDF support (h5py module) is missing.",
                    RuntimeWarning,
                )
            return False

    def _init_properties(self):
        atr = self._get_hdf_header_attrs()

        # expansion factor could be saved as redshift
        if "ExpansionFactor" in atr:
            self.properties["a"] = atr["ExpansionFactor"]
        elif "Redshift" in atr:
            self.properties["a"] = 1.0 / (1 + atr["Redshift"])

        # Gadget 4 stores parameters in a separate dictionary <sigh>. For older formats, this will point back to the same
        # as the header attributes.
        atr = self._get_hdf_parameter_attrs()

        # not all omegas need to be specified in the attributes
        if "OmegaBaryon" in atr:
            self.properties["omegaB0"] = atr["OmegaBaryon"]
        if "Omega0" in atr:
            self.properties["omegaM0"] = atr["Omega0"]
        if "OmegaLambda" in atr:
            self.properties["omegaL0"] = atr["OmegaLambda"]
        if "BoxSize" in atr:
            self.properties["boxsize"] = atr["BoxSize"] * self.infer_original_units("cm")
        if "HubbleParam" in atr:
            self.properties["h"] = atr["HubbleParam"]

        if "a" in self.properties:
            self.properties["z"] = (1.0 / self.properties["a"]) - 1

        # time unit might not be set in the attributes
        if "Time_GYR" in atr:
            self.properties["time"] = units.Gyr * atr["Time_GYR"]
        else:
            # from .. import analysis
            from pynbody import analysis

            self.properties["time"] = analysis.cosmology.age(self) * units.Gyr

        for s, value in self._get_hdf_header_attrs().items():
            if s not in [
                "ExpansionFactor",
                "Time_GYR",
                "Time",
                "Omega0",
                "OmegaBaryon",
                "OmegaLambda",
                "BoxSize",
                "HubbleParam",
            ]:
                self.properties[s] = value

    def derivable_keys(self) -> list:
        keys = SimSnap.derivable_keys(self)
        keys = [key for key in keys if key not in bad_keys]
        return keys


bad_keys = [
    "U_mag",
    "U_lum_den",
    "B_mag",
    "B_lum_den",
    "V_mag",
    "V_lum_den",
    "R_mag",
    "R_lum_den",
    "I_mag",
    "I_lum_den",
    "J_mag",
    "J_lum_den",
    "H_mag",
    "H_lum_den",
    "K_mag",
    "K_lum_den",
    "u_mag",
    "u_lum_den",
    "g_mag",
    "g_lum_den",
    "r_mag",
    "r_lum_den",
    "i_mag",
    "i_lum_den",
    "z_mag",
    "z_lum_den",
    "y_mag",
    "y_lum_den",
    "r",
    "rxy",
    "vr",
    "v2",
    "vt",
    "ke",
    "te",
    "j",
    "j2",
    "jz",
    "vrxy",
    "vcxy",
    "vphi",
    "vtheta",
    "v_mean",
    "v_disp",
    "v_curl",
    "vorticity",
    "v_div",
    "age",
    "theta",
    "alt",
    "az",
    "cs",
    "mu",
    "p",
    "u",
    "temp",
    "zeldovich_offset",
    "aform",
    "tform",
    "iord_argsort",
    "smooth",
    "rho",
]
