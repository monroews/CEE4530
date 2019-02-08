
```python
from aguaclara.core.units import unit_registry as u
u.define('equivalent = mole = eq')
import aguaclara.research.environmental_processes_analysis as epa
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


```
Let's plot the alphas for the carbonate system to show the relative importance of the three species!
```python
# Create a uniform spaced array from 3 to 12
pH_graph = np.linspace(3,12,50)
fig, ax = plt.subplots()
ax.plot(pH_graph, epa.alpha0_carbonate(pH_graph),'r', pH_graph, epa.alpha1_carbonate(pH_graph),'b',pH_graph, epa.alpha2_carbonate(pH_graph),'g')
plt.xlabel('pH')
plt.ylabel('Fraction of total carbonates')
plt.legend(['Carbonic acid', 'Bicarbonate', 'carbonate'])

plt.savefig('images/alphagraph.png')
plt.show()
```

The alpha terms representing the carbonate species are shown in Figure 1.
 ![graph](https://github.com/monroews/CEE4530/raw/master/images/alphagraph.png)

Figure 1. Carbonate species relative importance as a function of pH.

```Python
pH_graph = np.linspace(5,7,50)
fig, ax = plt.subplots()
ax.plot(pH_graph, epa.ANC_open(pH_graph),'r')
plt.xlabel('pH')
plt.ylabel('ANC (mole/L)')
#plt.yscale('log')
plt.savefig('images/ANCgraph.png')
plt.show()
```
Figure 2 shows the ANC as a function of pH for a system that is in equilibrium with the atmosphere.
 ![graph](https://github.com/monroews/CEE4530/raw/master/images/ANCgraph.png)

 Figure 2. ANC as a function of pH in a system in equilibrium with the atmosphere.

```Python

def ANC_zeroed(pHguess, ANC):
  return ((epa.ANC_open(pHguess) - ANC).to(u.mol/u.L)).magnitude

# Now we use root finding to find the pH that results in the known ANC.
# Our function will call the ANC_zeroed function. The pHguess is the first
# input of the ANC_zeroed function and the range on that is set by the next
# two inputs in the optimize.brentq function. The ANC is passed as an
# additional argument.

def pH_open(ANC):
  return optimize.brentq(ANC_zeroed, 0, 14,args=(ANC))

# We can test this function to find the pH of pure water in equilibrium
# with the atmosphere
print('The pH of pure water equilibrium with the atmosphere is',pH_open(0))
```
