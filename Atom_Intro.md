# How to use markdown
Get help at
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)
## Headers
Headers like the one above are made by using the # symbol. Each additional # moves down one level in the outline of your document. 
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
###### Heading 5 (do you really have this many levels in your outline?)

Then to add text just type in the markdown file.
## Emphasis
In order to make something italics you can use the * or _ before and after _the_ *statement*

In order to make something **bold** you can use __two__ asterisks ** or __two__ underscores __ .

If you want to ~~strikethrough~~ something you can use two tildas ~~ before and after the statement.
## Lists
### Bullets
* In order to make a bullet you can use the asterisk *
- The dashed line also works (-)
+ as does the plus sign (+)
### Numbered Lists
1. First point
2. Second point

## Tables
| Tables     | are   | cool    |
| ---------- | ----- | ------- |
| fun things | go in | them    |
| like your  | lab   | reports |


Make sure that you have the Markdown Table Editor package. To start a table you use the vertical line. Type your column headers in between and hit enter. Then in preview a table should appear and use can use the table editor to make the rest of your table and make it look nice.




Add a link to the course syllabus below.


#Latex
Create an equation at [codecogs](https://www.codecogs.com/latex/eqneditor.php)
Copy the Latex and paste it between $$ $$

$$Headloss=K\frac{V^{2}}{2g}$$
Type *Control Shift x* to toggle between displaying the Latex and the beautiful equation
$$Headloss=K\frac{V^{2}}{2g}$$

# Python
```Python
from aide_design.play import *
#Below are the items that were imported by the code above so that you know what abbreviations to use in your code.

# Third-party imports
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import matplotlib

# AIDE imports
#import aide_design
#import aide_design.pipedatabase as pipe
#from aide_design.units import unit_registry as u
#from aide_design import physchem as pc
#import aide_design.expert_inputs as exp
#import aide_design.materials_database as mat
#import aide_design.utility as ut
#import aide_design.k_value_of_reductions_utility as k
#import aide_design.pipeline_utility as pipeline
#import warnings
```

You can find available functions by typing in the shortcut for the available libraries in a python code section. Type *pipe.* below the python introduction below and then select a function from the list. type *help(pipe.)* and select a function. Then press *shift enter* to execute that line of code and get help!

```Python
pipe
```

Multiple two variables with units.

```Python
V=1.85*u.mm/u.s
Runtime=60*u.hour
Height=(V*Runtime).to(u.m)
print(Height)
