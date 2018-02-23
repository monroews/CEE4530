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


data_file_path = 'Lab5Part2(CMFR_Final).xls'
print(EPA.notes(data_file_path))

firstrow = 36
time_data = EPA.ftime(data_file_path,firstrow,-1)
concentration_data = EPA.Column_of_data(data_file_path,firstrow,-1,1,'mg/L')
V_CMFR = 1.5*u.L
Q_CMFR = 380 * u.mL/u.min
time_residence = V_CMFR/Q_CMFR
C_initial = 30*u.mg/u.L
CMFR_model = EPA.CMFR(C_initial,0*u.mg/u.L,time_data/time_residence)
plt.plot(time_data.to(u.min), concentration_data.to(u.mg/u.L),'r',time_data.to(u.min), CMFR_model,'b')
plt.xlabel('Time (minutes)')
plt.ylabel('Concentration (mg/L)')
plt.legend(['Measured dye','CMFR Model'])

plt.savefig('images/reactorplot.png')
plt.show()

#Redo the analysis in dimensionless form.
#We need to force this to be dimensionless so that it simplifies the units.
time_dim = np.divide(time_data,time_residence).to(u.dimensionless)
E_CMFR_data = concentration_data/C_initial
plt.plot(time_dim, E_CMFR_data,'r',time_dim, EPA.E_CMFR_N(1,time_dim),'b')
plt.xlabel(r'$\frac{t}{\theta}$')
plt.ylabel(r'$\frac{C}{C_0}$')
plt.legend(['Measured dye','CMFR Model'])

plt.savefig('images/reactorplot.png')
plt.show()


```
The concentration data shows a rapid increase followed by the classic washout of a CMFR.

```Python
myt=t=np.linspace(0,3,50)
EPA.E_Advective_Dispersion
print(EPA.E_CMFR_N(0.5,myt))

```
