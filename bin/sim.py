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
rng = np.random.default_rng(7)
#Define the simulator
simulator = wfsim.SimpleSimulator(
    obs_params,
    atm_params,
    auxtel0,
    bandpass,
    shape=(4000, 4000),
    rng=rng,
)

    

for a in range(5000):
    star_temp = rng.uniform(4_000, 10_000) 
    sed = wfsim.BBSED(star_temp) 
    flux = rng.integers(1_000_000, 2_000_000)
    background = rng.uniform(0, 0.0001)*flux #random percentage of the flux
    
    # random translations (meters)
    dx = rng.uniform(-0.001, 0.001)
    dy = rng.uniform(-0.001, 0.001)
    dz = rng.uniform(-0.0001, 0.0001)
    
    #Translational data in meters
    Trans_data = np.array([dx, dy, dz - 0.0008]) #positive displacement is extrafocal, negative is intrafocal
    
    #Rotational data in radians
    Rot_data = (batoid.RotX(0) @ batoid.RotY(0))
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
    image0 = simulator.image.array
    signal = image0[image0 > 0].mean()

    simulator.add_background(background, rng)
    noise = np.sqrt(background)

    image = simulator.image.array
    cropped_image=image[1850:2150, 1850:2150]
    
    dof = np.array([dx, dy, dz])

    np.savez(
        '../data/intrafocal3_donut'+str(a)+'.npz', 
        image=cropped_image,
        dof=dof,
        temp=star_temp, 
        flux=flux, 
        background=background,
        snr=(signal/noise)
    )

    #Set blank baseline image
    simulator.image.setZero()