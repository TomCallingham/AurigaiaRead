# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: py10
#     language: python
#     name: py10
# ---

# %% [markdown]
# # Auriga Read Example
# Notebook showing some AurigaRead and Pynbody things. See Pynbody docs for more! 

# %%
import matplotlib.pyplot as plt
import numpy as np
from AurigaRead import AuPynbody

# %% [markdown]
# ## Load Snapshot
# Contains stars, darkmatter, gas and wind.
# We select only members of the main halo

# %%
Au6=AuPynbody(halo_n=6,snap=127)

# %%
main_halo = Au6.halos()[0] #FoF =0
main_subhalo = Au6.halos()[0].sub[0] #FoF =0 Subhalo=0

# %% [markdown]
# ## Selecting Stars and Properties
# Note this package handles the sharp edge of Auriga wind particles being saved as stellar type with a negative formation time. 
#
# The full particle family can be found with:  
# stars_and_wind = main_halo.s

# %%
stars = main_halo.stars
print(stars)
print(stars.all_keys())

# %% [markdown]
# Properties are loaded into a SimArray. These are fancier than numpy arrays, holding things  like units, but are also slower to repeatedly access for subselections (note in auriga stars are already a subselection). You can return them to numpy arrays with a "x.v" (note this is on Tom's Pynbody, on the usual its .view(np.array)"

# %%
x_sim_array = stars["x"]
print(type(x_sim_array))
print(x_sim_array)
print(x_sim_array.units)

# %%
x_numpy = stars["x"].v
print(type(x_numpy))

# %% [markdown]
# ## Orientation
# This package automatically lazily orientates to main halo and disc, unless the orientate=False flag is passed:
#
# Au6 = AuPynbody(halo_n=6,snap=127,orientate=False)

# %%
pos_bins = np.linspace(-50,50,200)
plt.figure()
for xkey in ["x","y","z"]:
    plt.hist(stars[xkey],bins=pos_bins,alpha=0.5,label=xkey)
plt.legend()
plt.yscale("log")
plt.show()

# %%
R = stars["R"].v
plt.figure()
plt.hist(R[R<500],bins=100)
plt.show()

# %%
for xkey in ["Fe_H","En","E_sim","Lz","JR","Jz","peri","apo"]:
    x = stars[xkey].v
    min_x,max_x = np.nanpercentile(x,[0,95])
    bins = np.linspace(min_x,max_x,200)
    plt.figure()
    plt.hist(x,bins=bins,alpha=0.5,label=xkey)
    plt.legend()
    plt.yscale("log")
    plt.xlabel(xkey)
    plt.show()

# %% [markdown]
# ## Galactic Potential
# This package automatically calculates and saves an axisymmetric AGAMA potential, assuming the default orientation. This is used for dynamical quantities, such as actions. The "En" key is calculatted with this, "E_sim" is using the original gadget potential

# %%
pot = Au6.potential

rspace = np.geomspace(0.1,100,100)
pos_space=np.column_stack([rspace,0*rspace,0*rspace])
vc_space = np.sqrt(-rspace*pot.force(pos_space)[:,0])

plt.figure()
plt.plot(rspace,vc_space)
plt.show()

# %% [markdown]
# ## Merger Tree
# Using old scripts. Could update to Tangos/Pynbody?

# %% [markdown]
# ## Particle Origin
# Two options, both based on current merger trees and accretion defs. 
#
# First based on "touch", the contents of a subhalo when first touches the main halo.
#
# Second based on "Birth" location of star (TBD)
#

# %%
a_ind = stars["touch_a_ind"]

# %%
Lz = stars["Lz"].v
En = stars["En"].v

# %%
a_groups, a_pops = np.unique(a_ind,return_counts=True)

# %%
large_a_groups = a_groups[a_pops>500]

# %%
print(large_a_groups)

# %%
percent=5
nbin=100
binsx = np.linspace(*np.nanpercentile(Lz,[percent,100-percent]),nbin)
binsy = np.linspace(*np.nanpercentile(En,[percent,100-percent]),nbin)
plt.figure()
for a_G_ind in large_a_groups:
    a_filt= a_ind ==a_G_ind
    print(a_G_ind,a_filt.sum())
    if a_G_ind<0:
        hist = np.histogram2d(Lz[a_filt],En[a_filt],bins=(binsx,binsy))[0]
        m_hist = np.ma.masked_where(hist==0,hist)
        cent_x = 0.5*(binsx[1:]+ binsx[:-1])
        cent_y = 0.5*(binsy[1:]+ binsy[:-1])
        plt.contour(cent_x,cent_y,m_hist.T,label="Insitu",zorder=10)
    else:
        plt.scatter(Lz[a_filt],En[a_filt],label=f"Accretion Group {a_G_ind}",
                   edgecolors="none",s=50)
plt.xlabel("Lz")
plt.ylabel("En")
plt.legend()
plt.show()


# %% [markdown]
# ### Birth Subhalo  
# TODO
#
# Got the scripts, just need to package them

# %%
