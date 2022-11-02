# AuxTel AOS

AOS simulations for the Rubin AuxTel

## Installation

First, make sure you have `conda` and `git` installed.
If you have not installed `conda`, look [here](https://docs.conda.io/en/latest/miniconda.html).
If you do not already have `git`, look [here](https://git-scm.com).
You can also install git using `conda`, but this will be environment dependent.

Once you have `conda` and `git`,

1. clone this repo, e.g.

```bash
git clone https://github.com/jfcrenshaw/auxtel_aos.git
cd auxtel_aos
```

2. Create a conda environment with the required dependencies:

```bash
conda env create -f environment.yml
```

3. Activate the new environment:

```bash
conda activate auxtel_aos
```

4. Install a Jupyter kernel for the environment:

```bash
python -m ipykernel install --user --name auxtel_aos --display-name "AuxTel AOS"
```

If you want to install any other packages, you can use `pip install ...` or `conda install ...` to add them to this environment.
Make sure you have are in the correct environment *before* installing any packages!

If you mess up the environment, and want a fresh install, run

```bash
conda deactivate # this takes you out of this environment
cona env remove -n auxtel_aos # this removes the environment
```

You can then proceed with step 2 above.

## Working with this environment

When you do work on this project, you will want to work with the environment you installed above.
If you are working from the command line, you should activate the environment:

```bash
conda activate auxtel_aos
```

then continue doing whatever you want.
You only need to activate the environment once per terminal.
If you want to check what environment you are currently in, run

```bash
conda env list
```

and conda will list all available environments, with a star next to the currently activated environment.
The current environment might also be displayed on the current line of your terminal - but this is terminal specific.

## Working in Jupyter Lab

If you want to launch a Jupyter server on your local machine, first make sure you are in the `auxtel_aos` environment (see the previous section).
Once you are in the correct environment, run

```bash
jupyter lab
```

This should open a Jupyter Lab page in your web browser.

If you want to work with the Astronomy Department's online Jupyter server, you can use one of these links:

- Epyc -- <https://epyc.astro.washington.edu/beta-jupyter/>
- Baldur -- <https://baldur.astro.washington.edu/jupyter>

Epyc is the default machine most people use.
If you want to use GPUs, Baldur is a good option.

## Example

For an example notebook, see the `notebooks` directory.
