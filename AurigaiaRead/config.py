# from pathlib import Path
# import os
# import toml

# # Define hardcoded default values
# DEFAULTS = {
#     "auriga_folder": "/cosma5/data/Gigagalaxy/pakmorr/level",
#     "my_auriga_folder": "/cosma5/data/dp004/dc-call1/AurigaPynbody/",
#     "use_cache_default": False,
#     "tree_file_type":"cosma",
#     "halo_file_type":"cosma"
# }

# config = DEFAULTS.copy()

# config_dir = (
#     Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) if os.name != "nt" else Path(os.getenv("APPDATA"))
# )

# config_file = config_dir / "AurigaRead.toml"

# if config_file.is_file():
#     with open(config_file) as f:
#         toml_config = toml.load(f)
#     config.update(toml_config)
# else:
#     print("No config file found, using defaults...")

# auriga_folder = config["auriga_folder"]
# my_auriga_folder = config["my_auriga_folder"]
# use_cache_default = config["use_cache_default"]
# tree_file_type = config["tree_file_type"]
# halo_file_type = config["halo_file_type"]

# def cosma_aurigaia(halo_n, datasets, filters=None, angle=30, ext=True, fsample=None, verbose=False, units=True):
#     return galactic_aurigaia(data_dir,halo_n, datasets, filters, angle, ext, fsample, verbose, units)

# def kapteyn_aurigaia(halo_n, datasets, filters=None, angle=30, ext=True, fsample=None, verbose=False, units=True):
#     return galactic_aurigaia(data_dir,halo_n, datasets, filters, angle, ext, fsample, verbose, units)
#
# data_dir =
# aurigaia_folder = "/net/gaia2/data/users/callingham/data/aurigaia/data/ICC/v3/chabrierIMF/level3_MHD"
aurigaia_folder = "/cosma5/data/Gigagalaxy/pakmorr/mockdataMW/new/"
folder_type = "cosma"
use_cache_default = False
