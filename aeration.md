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
filepaths, airflows, DO_data, time_data = EPA.aeration_data(3)
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
O2_sat

```
