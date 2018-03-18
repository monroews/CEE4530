from aide_design.play import *
import scipy
from scipy import special
from scipy.optimize import curve_fit
import collections
import os
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

def aeration_data(DO_column):
    """ This function extracts the data from folder containing tab delimited files of aeration data.
    The file must be the original tab delimited file.
    All text strings below the header must be removed from these files.
    The file names must be the air flow rates with units of micromoles/s.
    An example file name would be "300.xls" where 300 is the flowr ate in micromoles/s
    The function opens a file dialog for the user to select the directory containing the data.

    Parameters
    ----------
    DO_column: index of the column that contains the dissolved oxygen concentration data.

    Returns
    -------
    filepaths: list of all file paths in the directory sorted by flow rate
    airflows: sorted numpy array of air flow rates with units of micromole/s attached
    DO_data: sorted list of numpy arrays. Thus each of the numpy data arrays can have different lengths to accommodate short and long experiments
    time_data: sorted list of numpy arrays containing the times with units of seconds. Each
    """

    dirpath = filedialog.askdirectory()
    #return the list of files in the directory
    filenames = os.listdir(dirpath)
    #extract the flowrates from the filenames and apply units
    airflows=((np.array([i.split('.', 1)[0] for i in filenames])).astype(np.float32))
    #sort airflows and filenames so that they are in ascending order of flow rates
    idx   = np.argsort(airflows)
    airflows = (np.array(airflows)[idx])*u.umole/u.s
    filenames = np.array(filenames)[idx]

    filepaths = [os.path.join(dirpath, i) for i in filenames]
    #DO_data is a list of numpy arrays. Thus each of the numpy data arrays can have different lengths to accommodate short and long experiments
    # cycle through all of the files and extract the column of data with oxygen concentrations and the times
    DO_data=[Column_of_data(i,0,-1,DO_column,'mg/L') for i in filepaths]
    time_data=[(ftime(i,0,-1)).to(u.s) for i in filepaths]
    aeration_collection = collections.namedtuple('aeration_results','filepaths airflows DO_data time_data')
    aeration_results = aeration_collection(filepaths, airflows, DO_data, time_data)
    return aeration_results

def O2_sat(Pressure_air,Temperature):
    """
    This equation is valid for 278 K < T < 318 K

    Parameters
    ----------
    Pressure_air: air pressure with appropriate units.
    Temperature: water temperature with appropriate units

    Returns
    -------
    Saturated oxygen concentration in mg/L
    """
    fraction_O2 = 0.21
    Pressure_O2 = Pressure_air *fraction_O2
    return (Pressure_O2.to(u.atm).magnitude)*u.mg/u.L*np.exp(1727/Temperature.to(u.K).magnitude - 2.105)

def Gran(data_file_path):
    """ This function extracts the data from a ProCoDA Gran plot file.
    The file must be the original tab delimited file.

    Parameters
    ----------
    data_file_path : string of the file name or file path.
    If the file is in the working directory, then the file name is sufficient.
    Example data_file_path = 'Reactor_data.txt'

    Returns
    -------
    V_titrant (mL) as numpy array
    ph_data as numpy array (no units)
    V_sample (mL) volume of the original sample that was titrated
    Normality_titrant (mole/L) normality of the acid used to titrate the sample
    V_equivalent (mL) volume of acid required to consume all of the ANC
    ANC (mole/L) Acid Neutralizing Capacity of the sample

    """
    df = pd.read_csv(data_file_path,delimiter='\t',header=5)
    V_t = np.array(pd.to_numeric(df.iloc[0:,0]))*u.mL
    pH = np.array(pd.to_numeric(df.iloc[0:,1]))
    df = pd.read_csv(data_file_path,delimiter='\t',header=-1,nrows=5)
    V_S = pd.to_numeric(df.iloc[0,1])*u.mL
    N_t = pd.to_numeric(df.iloc[1,1])*u.mole/u.L
    V_eq = pd.to_numeric(df.iloc[2,1])*u.mL
    ANC_sample = pd.to_numeric(df.iloc[3,1])*u.mole/u.L
    Gran_collection = collections.namedtuple('Gran_results','V_titrant ph_data V_sample Normality_titrant V_equivalent ANC')
    Gran = Gran_collection(V_titrant=V_t, ph_data=pH,V_sample=V_S, Normality_titrant=N_t, V_equivalent=V_eq, ANC=ANC_sample )
    return Gran;


def ftime(data_file_path,start,end):
    """ This function extracts the column of times from a ProCoDA data file.
    The file must be the original tab delimited file.

    Parameters
    ----------
    data_file_path : string of the file name or file path.
    If the file is in the working directory, then the file name is sufficient.
    Example data_file_path = 'Reactor_data.txt'

    start: index of first row of data to extract from the data file

    end: index of last row of data to extract from the data
    If the goal is to extract the data up to the end of the file use -1

    Returns
    -------
    numpy array of experimental times starting at 0 day with units of days.

    """
    df = pd.read_csv(data_file_path,delimiter='\t')
    start_time = pd.to_numeric(df.iloc[start,0])*u.day
    day_times = pd.to_numeric(df.iloc[start:end,0])
    time_data = np.subtract((np.array(day_times)*u.day),start_time)
    return time_data;

def Column_of_data(data_file_path,start,end,column,units):
    """ This function extracts a column of data from a ProCoDA data file.
    The file must be the original tab delimited file.

    Parameters
    ----------
    data_file_path : string of the file name or file path.
    If the file is in the working directory, then the file name is sufficient.
    Example data_file_path = 'Reactor_data.txt'

    start: index of first row of data to extract from the data file

    end: index of last row of data to extract from the data
    If the goal is to extract the data up to the end of the file use -1

    column: index of the column that you want to extract. Column 0 is time.
    The first data column is column 1.

    units: string of the units you want to apply to the data.
    Example 'mg/L'S
    If an empty string, '', is passed then no units are applied.

    Returns
    -------
    numpy array of experimental data with the units applied.

    """
    df = pd.read_csv(data_file_path,delimiter='\t')
    if units == '':
        data = np.array(pd.to_numeric(df.iloc[start:end,column]))
    else:
        data = np.array(pd.to_numeric(df.iloc[start:end,column]))*u(units)
    return data;

def notes(data_file_path):
    """This function extracts any experimental notes from a ProCoDA data file.
    The file must be the original tab delimited file.
    Parameters
    ----------
    data_file_path : string of the file name or file path.
    If the file is in the working directory, then the file name is sufficient.
    Example data_file_path = 'Reactor_data.txt'

    Returns
    -------
    dataframe showing the rows of the data file that contain text notes
    inserted during the experiment.
    Use this to identify the section of the data file that you want to extract.

    """
    df = pd.read_csv(data_file_path,delimiter='\t')
    text_row = df.iloc[0:-1,0].str.contains('[a-z]','[A-Z]')
    text_row_index = text_row.index[text_row == True].tolist()
    notes = df.loc[text_row_index]
    return notes


#carbonates
#The following code defines the carbonate system and provides functions for calculating Acid Neutralizing Capacity.
Kw = 10**(-14) * (u.mole/u.L)**2
K1_carbonate = 10**(-6.37)*u.mol/u.L
K2_carbonate = 10**(-10.25)*u.mol/u.L
K_Henry_CO2 = 10**(-1.5) * u.mole/(u.L*u.atm)
P_CO2 = 10**(-3.5) * u.atm

def invpH(pH):
    return 10**(-pH)*u.mol/u.L

def alpha0_carbonate(pH):
    alpha0_carbonate = 1/(1+(K1_carbonate/invpH(pH))*(1+(K2_carbonate/invpH(pH))))
    return alpha0_carbonate

def alpha1_carbonate(pH):
    alpha1_carbonate = 1/((invpH(pH)/K1_carbonate) + 1 + (K2_carbonate/invpH(pH)))
    return alpha1_carbonate

def alpha2_carbonate(pH):
    alpha2_carbonate = 1/(1+(invpH(pH)/K2_carbonate)*(1+(invpH(pH)/K1_carbonate)))
    return alpha2_carbonate

def ANC_closed(pH,Total_Carbonates):
    return Total_Carbonates*(alpha1_carbonate(pH)+2*alpha2_carbonate(pH)) + Kw/invpH(pH) - invpH(pH)

def ANC_open(pH):
    return ANC_closed(pH,P_CO2*K_Henry_CO2/alpha0_carbonate(pH))

# Reactors
# The following code is for reactor responses to tracer inputs.
def CMFR(t,C_initial,C_influent):
    """ This function calculates the output concentration of a completely mixed flow reactor given an influent and initial concentration.

    Parameters
    ----------
    C_initial : The concentration in the CMFR at time zero.

    C_influent : The concentration entering the CMFR.

    t: time made dimensionless by dividing by the residence time of the CMFR. t can be a single value or a numpy array.

    Returns
    -------
    Effluent concentration

    """
    return C_influent * (1-np.exp(-t)) + C_initial*np.exp(-t)

def E_CMFR_N(t, N):
    """ This function calculates a dimensionless measure of the output tracer concentration from a spike input to a series of completely mixed flow reactors.

    Parameters
    ----------
    t: time made dimensionless by dividing by the residence time of the reactor. t can be a single value or a numpy array.

    N : The number of completely mixed flow reactors (CMFR) in series. This would logically be constrained to real numbers greater than 1.

    Returns
    -------
    (Concentration * volume of 1 CMFR) / (mass oftracer)

    """
    #make sure that time is dimensionless and not a mixed time unit
    if hasattr(t, 'magnitude'):
      t.ito(u.dimensionless)
    return (N**N)/special.gamma(N) * (t**(N-1))*np.exp(-N*t)

def E_Advective_Dispersion(t, Pe):
    """ This function calculates a dimensionless measure of the output tracer concentration from a spike input to reactor with advection and dispersion.
    Parameters
    ----------
    t: time made dimensionless by dividing by the reactor residence time. t can be a single value or a numpy array.

    Pe : The ratio of advection to dispersion ((mean fluid velocity)/(Dispersion*flow path length))

    Returns
    -------
    (Concentration * volume of reactor) / (mass of tracer)

    """
    #make sure that time is dimensionless and not a mixed time unit
    if hasattr(t, 'magnitude'):
      t.ito(u.dimensionless)
    #replace any times at zero with a number VERY close to zero to avoid divide by zero errors

    t[t==0]=10**(-50)
    return (Pe/(4*np.pi*t))**(0.5)*np.exp((-Pe*((1-t)**2))/(4*t))

def Tracer_CMFR_N(t_seconds, t_bar, C_bar, N):
    """ Used by Solver_CMFR_N. All inputs and outputs are unitless.
    This is The model function, f(x, ...). It takes the independent variable as the first argument and the parameters to fit as separate remaining arguments.

    Parameters
    ----------
    t_seconds : Array of times (units of seconds, but unitless)

    t_bar : Average time spent in the total reactor (units of seconds, but unitless).

    C_bar : (Mass of tracer)/(volume of the total reactor) unitless.

    N : The number of completely mixed flow reactors (CMFR) in series. This would logically be constrained to real numbers greater than 1.

    Returns
    -------
    (C_bar*E_CMFR_N(t_seconds/t_bar, N))
    The model concentration as a function of time
    """

    return C_bar*E_CMFR_N(t_seconds/t_bar, N)

def Solver_CMFR_N(t_data, C_data, theta_guess, C_bar_guess):
    """ Use non-linear least squares to fit the function, Tracer_CMFR_N(t_seconds, t_bar, C_bar, N), to reactor data.

    Parameters
    ----------
    t_data : Array of times with units

    C_data : Array of tracer concentration data with units

    theta_guess : Estimate of time spent in the total reactor with units.

    C_bar_guess : Estimate of (Mass of tracer)/(volume of the total reactor) with units.


    Returns
    -------
    a tuple with theta (units of s), C_bar (same units as C_bar_guess), and N as the best fit to the data.

    """

    C_unitless = C_data.magnitude
    C_units = str(C_bar_guess.units)
    t_seconds = (t_data.to(u.s)).magnitude
    # assume that a guess of 1 reactor in series is close enough to get a solution
    p0 = [theta_guess.to(u.s).magnitude, C_bar_guess.magnitude,1]
    popt, pcov = curve_fit(Tracer_CMFR_N, t_seconds, C_unitless, p0)
    Solver_theta = popt[0]*u.s
    Solver_C_bar = popt[1]*u(C_units)
    Solver_N = popt[2]
    Reactor_results = collections.namedtuple('Reactor_results','theta C_bar N')
    CMFR = Reactor_results(theta=Solver_theta, C_bar = Solver_C_bar, N = Solver_N)
    return CMFR


def Tracer_AD_Pe(t_seconds, t_bar, C_bar, Pe):
    """ Used by Solver_AD_Pe. All inputs and outputs are unitless.
    This is The model function, f(x, ...). It takes the independent variable as the first argument and the parameters to fit as separate remaining arguments.

    Parameters
    ----------
    t_seconds : Array of times (units of seconds, but unitless)

    t_bar : Average time spent in the reactor (units of seconds, but unitless).

    C_bar : (Mass of tracer)/(volume of the reactor) unitless.

    Pe : The Peclet number for the reactor.

    Returns
    -------
    C_bar*E_Advective_Dispersion(t_seconds/t_bar, Pe)
    The model concentration as a function of time
    """

    return C_bar*E_Advective_Dispersion(t_seconds/t_bar, Pe)

def Solver_AD_Pe(t_data, C_data, theta_guess, C_bar_guess):
    """ Use non-linear least squares to fit the function, Tracer_AD_Pe(t_seconds, t_bar, C_bar, Pe), to reactor data.

    Parameters
    ----------
    t_data : Array of times with units

    C_data : Array of tracer concentration data with units

    theta_guess : Estimate of time spent in one CMFR with units.

    C_bar_guess : Estimate of (Mass of tracer)/(volume of one CMFR) with units.

    Returns
    -------
    a tuple with theta (units of s), C_bar (same units as C_bar_guess), and Pe as the best fit to the data.

    """

    C_unitless = C_data.magnitude
    C_units = str(C_bar_guess.units)
    t_seconds = (t_data.to(u.s)).magnitude
    # assume that a guess of 1 reactor in series is close enough to get a solution
    p0 = [theta_guess.to(u.s).magnitude, C_bar_guess.magnitude,5]
    popt, pcov = curve_fit(Tracer_AD_Pe, t_seconds, C_unitless, p0, bounds=(0,np.inf))
    Solver_theta = popt[0]*u.s
    Solver_C_bar = popt[1]*u(C_units)
    Solver_Pe = popt[2]
    Reactor_results = collections.namedtuple('Reactor_results','theta C_bar Pe')
    AD = Reactor_results(theta=Solver_theta, C_bar = Solver_C_bar, Pe = Solver_Pe)
    return AD
