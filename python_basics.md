# Python Basics

## Common Import Statements
```Python
from aguaclara.core.units import unit_registry as u
import aguaclara.research.environmental_processes_analysis as epa
import aguaclara.core.utility as ut
import aguaclara.core.physchem as pc
import numpy as np
import matplotlib.pyplot as plt
import collections
import os
from pathlib import Path
import pandas as pd
import math
```

There are many functions which have already been coded out that you can find here: https://github.com/AguaClara/aguaclara/tree/master/aguaclara. Instead of copying and pasting the code into your markdown file, you can call the function directly from the AguaClara repository.

### Example 1: Calling an AguaClara Function
For example, if you want to calculate the density of water at a given temperature, you can use the function "density_water()" located in physchem under the core AguaClara folder.

**Warning** some functions specify which units its inputs must be in. For example, for the density function, if you don't append units to the input variable it will assume that the input is in Kelvins which would give you an incorrect answer if the input was intended to be in Celsius. However, if you add the unit Celsius to your input, the function will automatically convert this value to Kelvins which will give you the correct answer.

```Python
import aguaclara.core.physchem as pc
temp = 20*(u.degC)
density = pc.density_water(temp)
print('The density of water at 20 degrees Celsius is', ut.round_sf(density,3), '.') # The density of water at 20 degrees Celsius is 998 kilogram / meter ** 3.
```

## Units
The AguaClara code handles units which is extremely helpful in preventing unit errors, but it can cause some coding headaches.

To ensure that the resulting units of a function are your desired set of units, use "to_base_units()" to convert the resulting unit to the most simple unifying base unit.

### Example 2: Units
```Python
# adding units
temp = 10*(u.degC)
area = 20*(u.m**2)
density = 30*(u.kg/u.m**3)
# removing units
temp = temp.magnitude
# changing units
area =  area.to(u.cm**2)
# making units compatible
length = 40*(u.m)
width = 50*(u.cm)
# unit error example
area = length*width
area # 2000 centimeter meter (not what we want)
# correct answer
area = (length*width).to_base_units()
area # 20.0 meter^2
```

## Plotting Data
When plotting, make sure that the arrays you are planning on plotting against one another are the same length and dimension. To do the former you can use the function 'len()'.

### Example 3: Plotting
```Python
x = [1,2,3,4]
y = [1,2,3,4]
plt.plot(x, y, 'o')
plt.plot(x, y, '-')
plt.xlabel('Time (s)')
plt.ylabel('pH (dimensionless)');
plt.title('pH vs Time')
plt.show()
```

![Figure 1](https://github.com/monroews/CEE3530/raw/master/python_basics_1.png)

Figure 1: This is what the result of Example 3 should look like.

## For Loops
If you need to run the same function for a variety of inputs, you can save yourself some time with a for loop. The range of the for loop can be an array or if you just want to loop through some integers, one through five for example, then you can just set the range to be (0,5). The most common error that results from for loops is a result of unit errors. If you add the appropriate expected units to the empty array which will contain your answers, you shouldn't have any unit errors.

The only reason to use "".magnitude" is if you are using a package that isn't compatible with units. An example of this is the curve fitting algorithms in SciPy. It is necessary to remove units for those functions.

### Example 4: For Loop (Calculating Density + Plotting Results)
```Python
temp = [20, 40, 60, 80]*(u.degC)
density = np.zeros(4)*(u.kg/u.m**3) # add the expected outcome units to the new array to prevent unit errors
for i in range(temp.size):
  density[i] = pc.density_water(temp[i])

plt.plot(temp, density, 'o')
plt.xlabel('Temperature (deg C)')
plt.ylabel('Density (kg/m^3)');
plt.title('Density vs Temperature')
plt.show()
```

![Figure 2](https://github.com/monroews/CEE3530/raw/master/python_basics_2.png)

Figure 2: This is what the result of Example 4 should look like.
