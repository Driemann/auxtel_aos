import numpy as np 

import batoid
import galsim
import wfsim

auxtel0 = batoid.Optic.fromYaml("AuxTel.yaml")
bandpass = galsim.Bandpass("LSST_r.dat", wave_type='nm')

obs_params = {
    "zenith": 30 * galsim.degrees,
    "raw_seeing": 0.7 * galsim.arcsec,
    "temperature": 293, 
    "pressure": 69, 
    "H2O_pressure": 1, 
    "wavelength": bandpass.effective_wavelength,
    "exptime": 30, 
}
#Atmosphere parameters
atm_params = {
    "screen_size": 819.2,
    "screen_scale": 0.1,
    "nproc": 6,
}
#Random integer generator
rng = np.random.default_rng(0)
#Define the simulator
simulator = wfsim.SimpleSimulator(
    obs_params,
    atm_params,
    auxtel0,
    bandpass,
    shape=(4000, 4000),
    rng=rng,
)

    

star_temp = rng.uniform(4_000, 10_000) 
sed = wfsim.BBSED(star_temp) 
flux = rng.integers(1_000_000, 2_000_000)
background = rng.uniform(0, 0.0001)*flux #random percentage of the flux

# random translations (meters)
dx = 3.3131847e-04 / 100
dy = 3.0265935e-04 / 100
dz = -2.5968002e-03 / 10
    
#Translational data in meters
Trans_data = np.array([dx, dy, dz + 0.0008]) #positive displacement is extrafocal, negative is intrafocal
    
# random rotations (radians)
rotx =  -6.4447522e-07
roty =  -1.8348359e-04
    
#Rotational data in radians
Rot_data = (batoid.RotX(rotx) @ batoid.RotY(roty))
#Telescope
intra_perturbed = (
    auxtel0
    .withGloballyShiftedOptic("M2", Trans_data)
    .withLocallyRotatedOptic("M2", Rot_data)
    )
simulator.telescope=intra_perturbed
simulator._construct_wcs()
xfield, yfield= simulator.wcs.xyToradec(0, 0, galsim.radians)
simulator.add_star(xfield, yfield, sed, flux, rng)
simulator.add_background(background, rng)

image = simulator.image.array
cropped_image=image[1850:2150, 1850:2150]
    
dof = np.array([dx, dy, dz, rotx, roty])

np.savez(
    '../test_data/p_donut1000.npz', 
    image=cropped_image,
    dof=dof,
    temp=star_temp, 
    flux=flux, 
    background=background,
)

#Set blank baseline image
simulator.image.setZero()