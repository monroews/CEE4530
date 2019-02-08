```python
from aide_design.play import *
from scipy import stats
import Environmental_Processes_Analysis as EPA
import importlib
importlib.reload(EPA)
data_file_path = 'S:/Courses/4530/Spring 2018/Group 1/Lab4-Acid-round1-sample1.xls'
df = pd.read_csv(data_file_path,delimiter='\t',header=6)
V_t = pd.to_numeric(df.iloc[0,0])*u.mL
pH = pd.to_numeric(df.iloc[1,0])

V_S = 50*u.mL
N_t = 0.1*u.mole/u.L
V_titrant, pH, V_Sample, Normality_Titrant, V_equivalent, ANC = EPA.Gran(data_file_path)
V_titrant
pH

V_Sample
Normality_Titrant
V_equivalent
ANC


```
## Equation for the First Gran Function
$${F_1}  =  \frac{{{V_S} + {V_T}}}{{{V_S}}}{\text{[}}{{\text{H}}^ + }{\text{]}}$$

```Python
#Define the gran function.
def F1(V_sample,V_titrant,pH):
  return (V_sample + V_titrant)/V_sample * EPA.invpH(pH)
#Create an array of the F1 values.
F1_data = F1(V_Sample,V_titrant,pH)
#By inspection I guess that there are 4 good data points in the linear region.
N_good_points = 3
#use scipy linear regression. Note that the we can extract the last n points from an array using the notation [-N:]
slope, intercept, r_value, p_value, std_err = stats.linregress(V_titrant[-N_good_points:],F1_data[-N_good_points:])
#reattach the correct units to the slope and intercept.
intercept = intercept*u.mole/u.L
slope = slope*(u.mole/u.L)/u.mL
V_eq = -intercept/slope

V_eq
#The equivalent volume agrees well with the value calculated by ProCoDA.
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
