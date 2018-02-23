from aide_design.play import *
import scipy
from scipy import special

def ftime(data_file_path,start,end):
    """ This function extracts the column of times from a ProCoDA data file.

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
    Example 'mg/L'

    Returns
    -------
    numpy array of experimental data with the units applied.

    """
    df = pd.read_csv(data_file_path,delimiter='\t')
    data = np.array(pd.to_numeric(df.iloc[start:end,column]))*u(units)
    return data;

def notes(data_file_path):
    """This function extracts any experimental notes from a ProCoDA data file.

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
def CMFR(C_initial,C_influent,t):
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

def E_CMFR_N(N,t):
    """ This function calculates a dimensionless measure of the output tracer concentration from a spike input to a series of completely mixed flow reactors.

    Parameters
    ----------
    N : The number of completely mixed flow reactors (CMFR) in series. This would logically be constrained to real numbers greater than 1.

    t: time made dimensionless by dividing by the residence time of one of the CMFR. t can be a single value or a numpy array.

    Returns
    -------
    (Concentration * volume of 1 CMFR) / (mass of tracer)

    """
    return (N**N)/special.gamma(N) * (t**(N-1))*np.exp(-N*t)

def E_Advective_Dispersion(Pe,t):
    """ This function calculates a dimensionless measure of the output tracer concentration from a spike input to reactor with advection and dispersion.
    Parameters
    ----------
    Pe : The ratio of advection to dispersion ((mean fluid velocity)/(Dispersion*flow path length))

    t: time made dimensionless by dividing by the reactor residence time. t can be a single value or a numpy array.

    Returns
    -------
    (Concentration * volume of reactor) / (mass of tracer)

    """
    return (Pe/(4*np.pi*t))**(0.5)*np.exp((-Pe*((1-t)**2))/(4*t))
