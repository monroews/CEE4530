# Equations
The equilibrium concentration of oxygen in water is given by

$${C_{eq}} = {P_{{O_2}}}\mathop e\nolimits^{\left( {\frac{{1727}}{T} - 2.105} \right)} $$

$$\ln \frac{{C_{eq} - C}}{{C_{eq} - C_0}} =  - {\hat k_{v,l}}(t)$$

$$C_{eq} - C= \left(C_{eq} - C_0 \right)e^{ - {\hat k_{v,l}}(t)}$$
$$C= C_{eq} - \left(C_{eq}-C_0  \right)e^{ - {\hat k_{v,l}}(t)}$$

```python
from aguaclara.core.units import unit_registry as u
import aguaclara.research.environmental_processes_analysis as epa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import collections
import os
from pathlib import Path


def aeration_data(DO_column, dirpath):
    """This function extracts the data from folder containing tab delimited
    files of aeration data. The file must be the original tab delimited file.
    All text strings below the header must be removed from these files.
    The file names must be the air flow rates with units of micromoles/s.
    An example file name would be "300.xls" where 300 is the flowr ate in
    micromoles/s. The function opens a file dialog for the user to select
    the directory containing the data.

    Parameters
    ----------
    DO_column : int
        index of the column that contains the dissolved oxygen concentration
        data.

    dirpath : string
        path to the directory containing aeration data you want to analyze

    Returns
    -------
    filepaths : string list
        all file paths in the directory sorted by flow rate

    airflows : numpy array
        sorted array of air flow rates with units of micromole/s attached

    DO_data : numpy array list
        sorted list of numpy arrays. Thus each of the numpy data arrays can
        have different lengths to accommodate short and long experiments

    time_data : numpy array list
        sorted list of numpy arrays containing the times with units of seconds

    Examples
    --------

    """
    #return the list of files in the directory
    filenames = os.listdir(dirpath)
    #extract the flowrates from the filenames and apply units
    airflows = ((np.array([i.split('.', 1)[0] for i in filenames])).astype(np.float32))
    #sort airflows and filenames so that they are in ascending order of flow rates
    idx = np.argsort(airflows)
    airflows = (np.array(airflows)[idx])*u.umole/u.s
    filenames = np.array(filenames)[idx]

    filepaths = [os.path.join(dirpath, i) for i in filenames]
    #DO_data is a list of numpy arrays. Thus each of the numpy data arrays can have different lengths to accommodate short and long experiments
    # cycle through all of the files and extract the column of data with oxygen concentrations and the times
    DO_data=[epa.column_of_data(i,0,DO_column,-1,'mg/L') for i in filepaths]
    time_data=[(epa.column_of_time(i,0,-1)).to(u.s) for i in filepaths]
    aeration_collection = collections.namedtuple('aeration_results','filepaths airflows DO_data time_data')
    aeration_results = aeration_collection(filepaths, airflows, DO_data, time_data)
    return aeration_results

# The column of data containing the dissolved oxygen concentrations
DO_column = 2
dirpath = "Examples/data/Aeration"
filepaths, airflows, DO_data, time_data = aeration_data(DO_column,dirpath)

Accumulator = 1
Accumulator_P=[epa.column_of_data(i,0,Accumulator,-1,'Pa') for i in filepaths]
# Plot the raw data

for i in range(airflows.size):
  plt.plot(time_data[i], DO_data[i],'-')
plt.xlabel(r'$time (s)$')
plt.ylabel(r'Oxygen concentration $\left ( \frac{mg}{L} \right )$')
plt.legend(airflows.magnitude)
plt.savefig('Examples/images/raw_aeration.png')
plt.show()

#delete data that is less than 2 or greater than 6 mg/L
DO_min = 2 * u.mg/u.L
DO_max = 6 * u.mg/u.L
for i in range(airflows.size):
  idx_start = (np.abs(DO_data[i]-DO_min)).argmin()
  idx_end = (np.abs(DO_data[i]-DO_max)).argmin()
  time_data[i] = time_data[i][idx_start:idx_end] - time_data[i][idx_start]
  DO_data[i] = DO_data[i][idx_start:idx_end]
  Accumulator_P[i] = Accumulator_P[i][idx_start:idx_end]

# plot accumulator data
for i in range(1,airflows.size):
  plt.plot(time_data[i], Accumulator_P[i],'-')
plt.xlabel(r'$time (s)$')
plt.ylabel('Accumulator pressure (Pa)')
plt.legend(airflows.magnitude)
plt.savefig('Examples/images/clean_aeration.png')
plt.show()


#plot the cleaned up data
for i in range(1,airflows.size):
  plt.plot(time_data[i], DO_data[i],'-')
plt.xlabel(r'$time (s)$')
plt.ylabel(r'Oxygen concentration $\left ( \frac{mg}{L} \right )$')
plt.legend(airflows.magnitude)
plt.savefig('Examples/images/clean_aeration.png')
plt.show()

#. Plot a representative subset of the data showing dissolved oxygen vs. time. Perhaps show 5 plots on one graph.
skip = 3
for i in range(1,int(airflows.size/skip)):
  plt.plot(time_data[skip*i], DO_data[skip*i],'-')
plt.xlabel(r'$time (s)$')
plt.ylabel(r'Oxygen concentration $\left ( \frac{mg}{L} \right )$')
plt.legend(airflows.magnitude[0::skip])
plt.savefig('Examples/images/subset_aeration.png')
plt.show()

airflows[6]
DO_data[6]

#. Calculate :math:`C^{\star}` based on the average water temperature, barometric pressure, and the equation from `environmental processes <https://github.com/AguaClara/aguaclara/blob/master/aguaclara/research/environmental_processes_analysis.py>`_ analysis called O2_sat. :math:`C^{\star} =P_{O_{2}} {\mathop{e}\nolimits^{\left(\frac{1727}{T} -2.105\right)}}` where T is in Kelvin, :math:`P_{O_{2} }` is the partial pressure of oxygen in atmospheres, and :math:`C^{\star}` is in mg/L.

Temperature=22*u.degC
Pressure_air = u.atm
O2_sat = epa.O2_sat(Pressure_air,Temperature)
#.  Estimate :math:`\hat{k}_{v,l}` using linear regression and equation :eq:`eq_Gas_linearized` for each data set.
# initialize arrays
kvl=np.zeros(airflows.size)
r_value=np.zeros(airflows.size)

for i in range(airflows.size):
    kvl[i], intercept, r_value[i], p_value, std_err = stats.linregress(-time_data[i],np.log((O2_sat-DO_data[i])/(O2_sat-DO_data[i][0])))

kvl = kvl/u.s
#. Create a graph with a representative plot showing the model curve (as a smooth curve) and the data from one experiment. You will need to derive the equation for the concentration of oxygen as a function of time based on equation :eq:`eq_Gas_linearized`.

def DO_model(O2_sat,C0,kvl,t):
  DO_model = O2_sat - (O2_sat - C0)*np.exp(-kvl*t)
  return DO_model


plotidx = 6
plt.plot(time_data[plotidx], DO_data[plotidx],'o')
plt.plot(time_data[plotidx], DO_model(O2_sat,DO_data[plotidx][0],kvl[plotidx],time_data[plotidx]),'-')
plt.xlabel(r'$time (s)$')
plt.ylabel(r'Oxygen concentration $\left ( \frac{mg}{L} \right )$')
plt.legend(['data', 'model'])
plt.savefig('Examples/images/subset_aeration.png')
plt.show()


#. Plot :math:`\hat{k}_{v,l}` as a function of airflow rate (:math:`\mu mole/s`).
plt.plot(airflows, kvl,'o')
plt.xlabel(r'Airflow $\left ( \frac{\mu mole}{s} \right )$')
plt.ylabel(r'${\hat k_{v,l}} \left ( \frac{1}{s} \right )$')
plt.savefig('Examples/images/kvl.png')
plt.show()

#. Plot OTE as a function of airflow rate (?mole/s) with the oxygen deficit (:math:`C^{\star} -C`) set at 6 mg/L.
fraction_O2 = 0.21
V_reactor = 0.75 * u.L
MW_O2 = 32 * u.g/u.mole
C_target = O2_sat - 6*u.mg/u.L
Oxygen_dissolved = (V_reactor/MW_O2*kvl*(O2_sat-C_target)).to(u.micromole/u.s)
OTE = (Oxygen_dissolved/(fraction_O2*airflows)).to(u.dimensionless)
plt.semilogx(airflows, OTE,'o')
plt.xlabel(r'Airflow $\left ( \frac{\mu mole}{s} \right )$')
plt.ylabel('Oxygen Transfer Efficiency')
plt.savefig('Examples/images/OTE.png')
plt.show()



```

$$\ln \frac{{{C^*} - C}}{{{C^*} - {C_0}}} =  - {\hat k_{v,l}}(t - {t_0})$$

$${C^*} = {P_{{O_2}}}\mathop e\nolimits^{\left( {\frac{{1727}}{T} - 2.105} \right)} $$
