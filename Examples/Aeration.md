# Equations
The equilibrium concentration of oxygen in water is given by

$${C_{eq}} = {P_{{O_2}}}\mathop e\nolimits^{\left( {\frac{{1727}}{T} - 2.105} \right)} $$

$$\ln \frac{{{C_{eq}} - C}}{{{C_{eq}} - {C_0}}} =  - {\hat k_{v,l}}(t - {t_0})$$

```python
from aide_design.play import *
from scipy import stats
import Environmental_Processes_Analysis as EPA
#The following lines of code reloads the EPA code if it is updated
import importlib
importlib.reload(EPA)

# The column of data containing the dissolved oxygen concentrations
DO_column = 3
filepaths, airflows, DO_data, time_data = EPA.aeration_data(DO_column)
# Need to process each array to select target data perhaps greater than 1 mg/L and less than 6 mg/L
# Linearize the data
# Fit the first order model to the linearized data
# Plot all of the dataframe
airflows
filepaths
for i in range(airflows.size):
  plt.plot(time_data[i], DO_data[i],'o')

plt.xlabel(r'$time (s)$')
plt.ylabel(r'Oxygen concentration $\left ( \frac{mg}{L} \right )$')
plt.legend(airflows.magnitude)

plt.savefig('images/aeration.png')
plt.show()

Temperature=22*u.degC
Pressure_air = u.atm

O2_sat = EPA.O2_sat(Pressure_air,Temperature)

kvl=np.zeros(airflows.size)
r_value=np.zeros(airflows.size)

for i in range(airflows.size):
    kvl[i], intercept, r_value[i], p_value, std_err = stats.linregress(-time_data[i],np.log((O2_sat-DO_data[i])/(O2_sat-DO_data[i][0])))

kvl = kvl/u.s
r_value
plt.plot(airflows, kvl,'o')

plt.xlabel(r'Airflow $\left ( \frac{\mu mole}{s} \right )$')
plt.ylabel(r'${\hat k_{v,l}} \left ( \frac{1}{s} \right )$')


plt.savefig('images/kvl.png')
plt.show()

# Oxygen transfer efficiency
fraction_O2 = 0.21
V_reactor = 4 * u.L
MW_O2 = 32 * u.g/u.mole
C_target = C_sat - 6*u.mg/u.L
Oxygen_dissolved = (V_reactor/MW_O2*kvl*(C_sat-C_target)).to(u.micromole/u.s)
OTE = Oxygen_dissolved/(fraction_O2*airflows)

plt.semilogx(airflows, OTE,'o')

plt.xlabel(r'Airflow $\left ( \frac{\mu mole}{s} \right )$')
plt.ylabel('Oxygen Transfer Efficiency')


plt.savefig('images/OTE.png')
plt.show()


```

$$\ln \frac{{{C^*} - C}}{{{C^*} - {C_0}}} =  - {\hat k_{v,l}}(t - {t_0})$$

$${C^*} = {P_{{O_2}}}\mathop e\nolimits^{\left( {\frac{{1727}}{T} - 2.105} \right)} $$
