import numpy as np 
import matplotlib.pyplot as plt 

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

def create_simulator(telescope: batoid.Optic) -> wfsim.SimpleSimulator:
   
    rng = np.random.default_rng(42)

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
thx = np.deg2rad(0)
thy = np.deg2rad(0)
star_temp = rng.uniform(4_000, 10_000) 
sed = wfsim.BBSED(star_temp) 
flux = rng.integers(1_000_000, 2_000_000)


M2_trans = np.array([
    rng.uniform(-0.001, 0.001),  # meters
    rng.uniform(-0.001, 0.001),
    rng.uniform(-0.0001, 0.0001),
])
M2_rot = (
    batoid.RotX(np.deg2rad(rng.uniform(-0.1, 0.1)/60)) @
    batoid.RotY(np.deg2rad(rng.uniform(-0.1, 0.1)/60))
)
intra_perturbed = (
    auxtel0
    .withGloballyShiftedOptic("M2", M2_trans)
    .withLocallyRotatedOptic("M2", M2_rot)
)