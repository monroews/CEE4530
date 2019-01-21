```python
from aguaclara.core.units import unit_registry as u
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
```


# Python Tutorial for CEE 4530

This tutorial assumes that you have already installed atom on your computer, that you've configured it to be able to use python, and that you've installed the AguaClara code. The goal of this tutorial is to help you learn some of the essential tools for data analysis and presentation that you will need throughout the semester.

## Objectives

1. illustrate how to load data from a file
1. perform a linear regression
1. create a well formatted graph

```python
  data_file_path = "https://raw.githubusercontent.com/monroews/CEE4530/master/linear_regression.tsv"


  df = pd.read_csv(data_file_path,delimiter='\t')
  x = df['x'].values * u.
  y = df['y'].values

  x
x=pd()

```

### 11)
What did you find most difficult about learning to use Python? Create a brief example as an extension to this tutorial to help students learn the topic that you found most difficult.
