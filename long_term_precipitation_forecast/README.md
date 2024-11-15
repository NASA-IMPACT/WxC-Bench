# Long-term precipitation forecast

The long-term precipitation forecast downstream task consists of forecasting the
global distribution of daily accumulated precipitation from satellite
observations up to 4 weeks into the future. The input data for this task is
derived from gridded satellite observations from geostationary and
polar-orbiting platforms and aggregated into daily files. The output data are
corresponding daily precipitation accumulations derived from gauge-calibrated
satellite-based precipitation data records.

Refer to the [OVERVIEW.md](OVERVIEW.md) for results from the baseline model.

## Creating training and test datasets

### Installing dependencies

Most depencies for the data extraction can be installed using ``conda``. 


``` shellsession
conda create --name precip --file conda-requirements.txt --channel conda-forge
conda activate precip

```

Three packages, however, are still under active development and must be installed from github using ``pip``. The commit hashed unique identify the development snapshots with which the data can be extracted.

``` shellsession
pip install git+ssh://git@github.com/see-geo/pansat@55c7b991ab4f19223664ad896caa9cb575221aee
pip install  git+ssh://git@github.com/simonpf/chimp@e1701da4d7d1a1db5b3701852cd92c48aea3b872
```

### Setting-up the environment

Downloading IMERG data requires a [NASA](https://disc.gsfc.nasa.gov). After creating the account, the username and password must be added to the pansat environment:

> NOTE: ``pansat`` stores the password in an encrypted file on the machine. Despite the file being encrypted, it is recommended to use a throwaway password 

``` shellsession
pansat account add ges_disc <user_name>
```

### Downloading the data

The following scripts downloaded the data from the four sources:


| Name                        | Data                                               |
|-----------------------------|----------------------------------------------------|
|                             |                                                    |
| ``extract_precip_data.sh``  | Daily precipitation                                |
| ``extract_gridsat_data.sh`` | Geostationary observations                         |
| ``extract_ssmi_data.sh``    | PMW observations from polar orbiting satellites    |
| ``extract_patmosx.sh``      | VIS/IR observations from polar orbiting satellites |


## Evaluation and forecast baselines

The aim of the long-term precipitation forecast task is to improve subseasonal-to-seasonal (S2S)
precipitation forecasts. The principal baselines for the long-term precipitation forecast task are
derived two state-of-the-art, conventional numerical weather prediction models (NWP). In addition
to this, a machine-learning-based baseline model is provided with this repository to prove that
the feasibility of the proposed task.

The conventional NWP forecasts are derived from the ECMWF S2S database (Vitart, 2017) and 
are part of the task's test data. The code implementing the machine-learning baseline model
is located in the ``baseline`` folder.

# References

Vitart, F., and Coauthors, 2017: The Subseasonal to Seasonal (S2S) Prediction Project Database. Bull. Amer. Meteor. Soc., 98, 163–173, https://doi.org/10.1175/BAMS-D-16-0017.1. 
