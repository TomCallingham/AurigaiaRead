# from .auriga_read import AuHaloParams
# from .config import auriga_folder,tree_file_type
# import os

# def get_tree_file(halo_params: AuHaloParams) -> str:  # noqa: PLR0913
#     if tree_file_type=="cosma":
#         return get_tree_file_cosma(halo_params)
#     return get_tree_file_not_cosma(halo_params)


# def get_tree_file_cosma(halo_params: AuHaloParams) -> str:  # noqa: PLR0913
#     treebase = f"{auriga_folder}{halo_params.level}_{halo_params.sim_type}/mergertrees"
#     if halo_params.sim_type == "MHD":
#         treebase += "_new"
#     snap0 = halo_params.snap0
#     treebase += f"/Au-{halo_params.halo_n}/trees_sf1_{snap0:03d}.%d.hdf5"
#     return treebase

# def get_tree_file_not_cosma(halo_params: AuHaloParams) -> str:  # noqa: PLR0913
#     sim_type_folder="Original" if halo_params.sim_type=="MHD" else "Original_DMO"
#     treebase = f"{auriga_folder}level{halo_params.level}/{sim_type_folder}/mergertrees/"
#     snap0 = halo_params.snap0
#     treebase += f"/halo_{halo_params.halo_n}/trees_sf1_{snap0:03d}.%d.hdf5"
#     return treebase


# def find_halo_p_from_path(test_path) -> AuHaloParams:
#     if tree_file_type=="cosma":
#         return find_halo_p_from_path_cosma(test_path)
#     return find_halo_p_from_path_not_cosma(test_path)

# def find_halo_p_from_path_cosma(test_path) -> AuHaloParams:
#     path = os.path.realpath(test_path)
#     # Split the path into parts
#     parts = path.split("/")
#     # Extract the level, simulation type, and halo number
#     level = int(parts[5].split("_")[0][-1])  # Extracting 'MHD' from 'level4_MHD'
#     sim_type = parts[5].split("_")[1]  # Extracting 'MHD' from 'level4_MHD'
#     halo_n = int(parts[6].split("_")[1])  # Extracting '5' from 'halo_5'
#     snap = int(parts[-1][-3:])

#     return AuHaloParams(halo_n, level, sim_type, snap)

# def find_halo_p_from_path_not_cosma(test_path) -> AuHaloParams:
#     path = os.path.realpath(test_path)
#     # Split the path into parts
#     parts = path.split("/")
#     print(parts)
#     # Extract the level, simulation type, and halo number
#     # level = int(parts[5][5])  # Extracting '4' from 'level4_MHD'
#     level = int(parts[5].split("_")[0][-1])  # Extracting 'MHD' from 'level4_MHD'
#     sim_type = parts[5].split("_")[1]  # Extracting 'MHD' from 'level4_MHD'
#     halo_n = int(parts[6].split("_")[1])  # Extracting '5' from 'halo_5'
#     snap = int(parts[-1][-3:])

#     return AuHaloParams(halo_n, level, sim_type, snap)
