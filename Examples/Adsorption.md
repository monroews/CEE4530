Make sure you are using aguaclara version 0.0.22 or greater!
pip install aguaclara --upgrade

# Adsorption analysis



```python
from aguaclara.core.units import unit_registry as u
import aguaclara.research.environmental_processes_analysis as epa
import aguaclara.core.physchem as pc
import aguaclara.core.utility as ut
import numpy as np
import matplotlib.pyplot as plt
import collections
import os
from pathlib import Path



def adsorption_data(C_column, dirpath):
    """This function extracts the data from folder containing tab delimited
    files of adsorption data. The file must be the original tab delimited file.
    All text strings below the header must be removed from these files.
    The file names must be the air flow rates with units of micromoles/s.
    An example file name would be "300.xls" where 300 is the flowr ate in
    micromoles/s. The function opens a file dialog for the user to select
    the directory containing the data.
    Parameters
    ----------
    C_column : int
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
    #sort airflows and filenames so that they are in ascending order of flow rates


    filepaths = [os.path.join(dirpath, i) for i in filenames]
    #DO_data is a list of numpy arrays. Thus each of the numpy data arrays can have different lengths to accommodate short and long experiments
    # cycle through all of the files and extract the column of data with oxygen concentrations and the times
    DO_data=[epa.column_of_data(i,epa.notes(i).last_valid_index() + 1,DO_column,-1,'mg/L') for i in filepaths]
    time_data=[(epa.column_of_time(i,epa.notes(i).last_valid_index() + 1,-1)).to(u.s) for i in filepaths]

    adsorption_collection = collections.namedtuple('adsorption_results','filepaths filenames C_data time_data')
    adsorption_results = aeration_collection(filepaths, filenames, C_data, time_data)
    return adsorption_results

C_column = 2
dirpath = "Examples/data/Adsorption"
filepaths, filenames, C_data, time_data = adsorption_data(DO_column,dirpath)



#Experiment characteristics
Column_D = 1 * u.inch
Column_A = pc.area_circle(Column_D)
Column_L = 15.2 * u.cm
V_column = Column_A * Column_L
Column_Q = 0.5 * u.mL/u.s
v_a = (Column_Q/Column_A).to(u.mm/u.s)

Carbon_density = 2.1 * u.g/u.cm**3
Sand_porosity = 0.4
Sand_density = 2650 * u.kg/u.m**3
Carbon_M = 5 * u.g

HRT = (Column_L/v_a).to(u.s)
HRT
Carbon_bulk_density = (29.342 * u.g/(Column_L*Column_A)).to(u.kg/u.m**3)
Carbon_bulk_density
Carbon_porosity = 1-Carbon_bulk_density/Carbon_density
Carbon_porosity
C_0 = 50 * u.mg/u.L
q_0 = 0.08


t_water = (Column_L*Sand_porosity/v_a).to(u.s)
t_mtz = 25*u.hr
# set the breakthrough time to 30 minutes = 1800 s
R_adsorption = t_mtz/t_water
Density_bulk = (R_adsorption * porosity * C_0/q_0).to(u.kg/u.m**3)
Density_bulk


M_carbon = (V_column * Density_bulk).to(u.g)
M_carbon
V_carbon = (M_carbon/carbon_apparent_bulk_density).to(u.mL)
V_carbon
V_reddye = (v_a*A_column*t_mtz).to(u.L)
V_reddye
Q_reddye = (v_a*A_column).to(u.mL/u.min)
Q_reddye

M_sand = ((V_column-V_carbon)*density_sand*(1-porosity)).to(u.g)
M_sand


#

target_C = C_0/2
idx = (np.abs(F_column5g_dye-target_C)).argmin()
breakthrough = column5g_time[idx]
breakthrough

def Breakthrough(filepath,C_column,C_0):
  firstrow = epa.notes(filepath).last_valid_index() + 1
  C = epa.column_of_data(filepath,firstrow,C_column,-1,'mg/L')
  t = (epa.column_of_time(filepath,firstrow,-1)).to(u.s)
  idx = (np.abs(C-C_0/2)).argmin()
  t_breakthrough = t[idx]
  plt.plot(t, C,'-');
  return t_breakthrough

filepath0 = 'Lab_solutions/Adsorption/500microLpers0gAC.xls'
filepath5 = 'Lab_solutions/Adsorption/500microLpers5gAC.xls'
Breakthrough(filepath0,1,50 * u.mg/u.L)
Retardation = Breakthrough(filepath5,1,50 * u.mg/u.L)/Breakthrough(filepath0,1,50 * u.mg/u.L)
Retardation
plt.xlabel(r'$time (s)$');
plt.ylabel(r'Concentration $\left ( \frac{mg}{L} \right )$');
plt.show()
M_carbon = 5 * u.g
q_0 = ((Retardation - 1)*C_0*V_column*sand_porosity/M_carbon).to(u.dimensionless).magnitude
q_0


plt.plot(column5g_time, F_column5g_dye,'-');
plt.xlabel(r'$time (s)$');
plt.ylabel(r'Concentration $\left ( \frac{mg}{L} \right )$');
plt.legend(['Measured dye', 'F_curve','E_curve']);
plt.savefig('column5g_dye.png', bbox_inches = 'tight');
plt.show()
column5g_AD = epa.Solver_AD_Pe(column5g_time, E_column5g_dye*u.mg/u.L,100*u.s,0.5 * u.mg/u.L)
column5g_AD.theta
column5g_AD.Pe
column5g_AD.C_bar

column5g_AD_model = (column5g_AD.C_bar*epa.E_Advective_Dispersion((column5g_time/column5g_AD.theta).to_base_units(), column5g_AD.Pe)).to(u.mg/u.L)

plt.plot(column5g_time, E_column5g_dye,'b')
plt.plot(column5g_time, column5g_AD_model,'r')
plt.xlabel(r'$time (s)$')
plt.ylabel(r'Concentration $\left ( \frac{mg}{L} \right )$')
plt.legend(['Measured dye','Model'])
plt.savefig('column5g_dye.png', bbox_inches = 'tight')
plt.show()
