# Python Tutorial for CEE 3530

This tutorial assumes that you have already installed atom on your computer, that you've configured it to be able to use python, and that you've installed the AguaClara code. The goal of this tutorial is to help you learn some of the essential tools for data analysis and presentation that you will need throughout the semester.

For a more detailed tutorial see the [python tutorial](https://aguaclara.github.io/Textbook/Introduction/Python_Tutorial.html) used for CEE 3520.

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

Functions **will not** automatically convert units so that its variables have compatible units. For example, if you try to multiply two things which have different units, your code will either work but give you incorrect units (most likely it will give you the two units multiplied together) or the code will simply give you an error. You should either make sure ahead of time that your variables have the same units, or use the function "to_base_units()" which will convert your input units to the most simple unifying base unit.

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

## For Loops
If you need to run the same function for a variety of inputs, you can save yourself some time with a for loop. The most common errors that result from for loops are a result of unit errors. If you add the appropriate expected units to the empty array which will contain your answers, you shouldn't have any unit errors. However, as a last resort, you can use ".magnitude" inside your for loop so that it will run without any errors then append the appropriate units outside of the for loop.

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

## Objectives

1. illustrate how to load data from a file
1. learn about dataframes
1. perform a linear regression
1. create a well formatted graph
1. create an equation
1. add the graph to your document as a figure.

See [Selecting Subsets of Data in Pandas](https://medium.com/dunder-data/selecting-subsets-of-data-in-pandas-6fcd0170be9c) for a good background on working with a pandas dafaframe.

```python
  from aguaclara.core.units import unit_registry as u
  import numpy as np
  import matplotlib.pyplot as plt
  import pandas as pd
  from scipy import stats
  #The data file path is the raw data url on github. Happily python can read directly from a web page.
  data_file_path = "https://raw.githubusercontent.com/monroews/CEE4530/master/linear_regression.tsv"

  #Now we create a pandas dataframe with the data in the file
  df = pd.read_csv(data_file_path,delimiter='\t')
  #if you want to see what is in the dataframe you can print it!
  print(df)
  # The column headers can be access by using the list command
  list(df)
  columns = df.columns
  print(columns)
  #Below are three equally fine methods of extracting a column of data from the pandas dataframe.

  # 1) We can select a column by using the column header. Here we use the column header by selecting one array element from the list command.
  x = df[list(df)[0]].values * u.mg/u.L
  x
  # 2) We can use the loc command to select all of the rows (: command) and the column with the label given by list(df)[0].
  x = df.loc[:, list(df)[0]].values * u.mg/u.L
  x
  # 3) We can use the iloc command and select all of the rows in column 0.
  x = df.iloc[:,0].values * u.mg/u.L
  x
  #The iloc method is simple and efficient, so I'll use that to get the y values.
  y = df.iloc[:,1].values * u.mg/u.L

  # We will use the stats package to do the linear regression.
  # It is important to note that the units are stripped from the x and y arrays when processed by the stats package.
  slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

  #We can add the units to intercept by giving it the same units as the y values.
  intercept = intercept * y.units
  # Note that slope is dimensionless for this case, but not in general!
  # For the general case we can attach the correct units to slope.
  slope = slope * y.units/x.units

  # Now create a figure and plot the data and the line from the linear regression.
  fig, ax = plt.subplots()
  # plot the data as red circles
  ax.plot(x, y, 'ro', )

  #plot the linear regression as a black line
  ax.plot(x, slope * x + intercept, 'k-', )

  # Add axis labels using the column labels from the dataframe
  ax.set(xlabel=list(df)[0])
  ax.set(ylabel=list(df)[1])
  ax.legend(['Measured', 'Linear regression'])
  ax.grid(True)
  # Here I save the file to my local harddrive. You will need to change this to work on your computer.
  # We don't need the file type (png) here.
  plt.savefig('C:/Users/mw24/github/CEE4530/images/linear')
  plt.show()

```

Now we will display our figure in Markdown. To have the figure show up for anyone who opens this markdown file we will push the figure to github and then link to it there. To find the link in github, go to the code tab and then browse to the image.
![linear](https://github.com/monroews/CEE4530/blob/master/images/linear.png)

Figure 1: Captions are very important for figures. Captions go below figures.


Equations can be copied directly from the lab manual by clicking on the equation and requesting that it be displayed in Latex. Below is equation 2 from the [Laboratory Manual](https://monroews.github.io/EnvEngLabTextbook/Laboratory_Measurements/Laboratory_Measurements.html)

$$A=\log \left(\frac{P_{o} }{P} \right)$$


# Assignment

1) Find a set of data that includes units (or make one up!) that could reasonably be fit with linear regression.
1) Save the data to a tab delimited file in your atom project workspace.
1) Load the data from the file into a Pandas dataframe.
1) Plot the data and the linear regression line.
1) Make sure to handle units carefully and to attach units to the linear regression line.
1) Add a figure in Markdown showing the graph you produced.
1) Show the linear regression equation that you obtained using latex.
