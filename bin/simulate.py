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
atm_params = {
    "screen_size": 819.2,
    "screen_scale": 0.1,
    "nproc": 6,
}

def create_simulator(telescope: batoid.Optic, rng) -> wfsim.SimpleSimulator:

    simulator = wfsim.SimpleSimulator(
        obs_params,
        atm_params,
        telescope,
        bandpass,
        shape=(4000, 4000),
        rng=rng,
    )

    return simulator


rng = np.random.default_rng(0)

for a in range(2):
    star_temp = rng.uniform(4_000, 10_000) 
    sed = wfsim.BBSED(star_temp) 
    flux = rng.integers(1_000_000, 2_000_000)
    #background = rng.uniform(0, 0.002)*flux
    background = 0.0002*flux

    Trans_data = np.array([
        rng.uniform(-0.001, 0.001),  
        rng.uniform(-0.001, 0.001),
        rng.uniform(-0.0001, 0.0001)-.0008,
    ])
    
    Rot_data = (
        batoid.RotX(np.deg2rad(rng.uniform(-0.1, 0.1)/60)) @
        batoid.RotY(np.deg2rad(rng.uniform(-0.1, 0.1)/60))
    )

    intra_perturbed = (
        auxtel0
        .withGloballyShiftedOptic("M2", Trans_data)
        .withLocallyRotatedOptic("M2", Rot_data)
    )

    intra_perturbed_simulator = create_simulator(intra_perturbed, rng)
    intra_perturbed_simulator._construct_wcs()
    xfield, yfield= intra_perturbed_simulator.wcs.xyToradec(0, 0, galsim.radians)
    intra_perturbed_simulator.add_star(xfield, yfield, sed, flux, rng)
    intra_perturbed_simulator.add_background(background, rng)

    image = intra_perturbed_simulator.image.array
    cropped_image=image[1850:2150, 1850:2150]

    np.savez('../data/Test4_data'+str(a), image=cropped_image, Translation=Trans_data, Rotation=Rot_data, Temp=star_temp, flux=flux, background=background )


