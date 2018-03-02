```python
from aide_design.play import *
from scipy import stats
import Environmental_Processes_Analysis as EPA
import importlib
importlib.reload(EPA)
data_file_path = 'Lab4_Sample1_Time0.txt'
print(EPA.notes(data_file_path))
firstrow = 6
#This data file doesn't have time as the first column so we don't use the time function. Instead simply extract both relevant columns of data.
V_titrant = EPA.Column_of_data(data_file_path,firstrow,-1,0,'mL')
#The Column_of_data function automatically adds units. For this case we don't want units for the pH column. We can get this by sending an empty string for the units.
#I modified the EPA file so that it doesn't apply units if the string is empty.

pH_data = (EPA.Column_of_data(data_file_path,firstrow,-1,1,''))
# I didn't write the code to pull these numbers from the data file. It would be good to do that for next year!
V_sample = 50*u.mL
titrant_normality = 0.1*u.mole/u.L

```
## Equation for the First Gran Function
$${F_1}  =  \frac{{{V_S} + {V_T}}}{{{V_S}}}{\text{[}}{{\text{H}}^ + }{\text{]}}$$

```Python
#Define the gran function.
def F1(V_sample,V_titrant,pH):
  return (V_sample + V_titrant)/V_sample * EPA.invpH(pH)
#Create an array of the F1 values.
F1_data = F1(V_sample,V_titrant,pH_data)
#By inspection I guess that there are 4 good data points in the linear region.
N_good_points = 4
#use scipy linear regression. Note that the we can extract the last n points from an array using the notation [-N:]
slope, intercept, r_value, p_value, std_err = stats.linregress(V_titrant[-N_good_points:],F1_data[-N_good_points:])
#reattach the correct units to the slope and intercept.
intercept = intercept*u.mole/u.L
slope = slope*(u.mole/u.L)/u.mL
V_eq = -intercept/slope

V_eq
#The equivilent volume agrees well with the value calculated by ProCoDA.
#create an array of points to draw the linear regression line
x=[V_eq.magnitude,V_titrant[-1].magnitude ]
y=[0,(V_titrant[-1]*slope+intercept).magnitude]
#Now plot the data and the linear regression
plt.plot(V_titrant, F1_data,'o')
plt.plot(x, y,'r')
plt.xlabel('Titrant Volume (mL)')
plt.ylabel('Gran function (mole/L)')
plt.legend(['data'])

plt.savefig('images/Gran.png')
plt.show()

```
