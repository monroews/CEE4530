# Third-party imports
- import numpy as np
- import pandas as pd
- import matplotlib.pyplot as plt
- import matplotlib

# AIDE imports
- import aide_design
- import aide_design.pipedatabase as pipe
- from aide_design.units import unit_registry as u
- from aide_design import physchem as pc
- import aide_design.expert_inputs as exp
- import aide_design.materials_database as mat
- import aide_design.utility as ut
- import aide_design.k_value_of_reductions_utility as k
- import aide_design.pipeline_utility as pipeline
- import warnings

## Steps

```python
from aide_design.play import *
import Environmental_Processes_Analysis as EPA
import importlib
importlib.reload(EPA)

#The following file is from a CMFR
data_file_path = 'Lab5Part2(CMFR_Final).xls'
print(EPA.notes(data_file_path))

#I eliminate the beginning of the data file because this is a CMFR and the first data was taken before the dye reached the sensor.
firstrow = 50
time_data = EPA.ftime(data_file_path,firstrow,-1)
concentration_data = EPA.Column_of_data(data_file_path,firstrow,-1,1,'mg/L')
V_CMFR = 1.5*u.L
Q_CMFR = 380 * u.mL/u.min

#here we set estimates that we will use as starting values for the curve fitting
theta_guess = (V_CMFR/Q_CMFR).to(u.s)

C_bar_guess = concentration_data[0]

#The Solver_CMFR_N will return the initial tracer concentration, residence time, and number of reactors in series.
#This experiment was for a single reactor and so we expect N to be 1!
CMFR = EPA.Solver_CMFR_N(time_data, concentration_data, theta_guess, C_bar_guess)
#use dot notation to get the 3 elements of the tuple that are in CMFR.
CMFR.C_bar
CMFR.N
CMFR.theta
#create a model curve given the curve fit parameters.
#
CMFR_model = EPA.E_CMFR_N(CMFR.C_bar,,time_data/CMFR.theta)
plt.plot(time_data.to(u.min), concentration_data.to(u.mg/u.L),'r',time_data.to(u.min), CMFR_model,'b')

plt.xlabel(r'$\frac{t}{\theta}$')
plt.ylabel(r'$\frac{C}{C_0}$')
plt.legend(['Measured dye','CMFR Model'])

plt.savefig('images/reactorplot.png')
plt.show()


data_file_path = 'Advection_dispersion.txt'


firstrow = 0
time_data = EPA.ftime(data_file_path,firstrow,-1)
concentration_data = EPA.Column_of_data(data_file_path,firstrow,-1,1,'mole/L')
V_CMFR = 1.5*u.L
Q_CMFR = 380 * u.mL/u.min
theta_guess = (V_CMFR/Q_CMFR).to(u.s)
theta_guess
C_bar_guess = np.max(concentration_data)
C_bar_guess

CMFR = EPA.Solver_CMFR_N(time_data, concentration_data, theta_guess, C_bar_guess)
CMFR.C_bar
CMFR.N
CMFR.theta
CMFR_model = (CMFR.C_bar*EPA.E_CMFR_N(time_data/CMFR.theta, CMFR.N)).to(u.mole/u.L)

AD = EPA.Solver_AD_Pe(time_data, concentration_data, theta_guess, C_bar_guess)
AD.C_bar
AD.Pe
AD.theta

AD_model = (AD.C_bar*EPA.E_Advective_Dispersion((time_data/AD.theta).to_base_units(), AD.Pe)).to(u.mole/u.L)


plt.plot(time_data.to(u.min), concentration_data.to(u.mole/u.L),'r')
plt.plot(time_data.to(u.min), CMFR_model,'b')
plt.plot(time_data.to(u.min), AD_model,'g')
plt.xlabel(r'$\frac{t}{\theta}$')
plt.ylabel(r'$\frac{C}{C_0}$')
plt.legend(['Measured dye','CMFR Model', 'AD Model'])

plt.savefig('images/reactorplot.png')
plt.show()



```
