# Design Challenge 1, learning Python, Jupyter, and some AguaClara Design Functions

### 1)
Calculate the minimum inner diameter of a PVC pipe that can carry a flow of at least 10 L/s for the town of Ojojona. The population is 4000 people. The water source is a dam with a surface elevation of 1500 m. The pipeline connects the reservoir to the discharge into a distribution tank at an elevation of 1440 m. The pipeline length is 2.5 km. The pipeline is made with PVC pipe with an SDR (standard diameter ratio) of 26.

The pipeline inlet at the dam is a square edge with a minor loss coefficient (${K_e}$) of 0.5. The discharge at the top of the distribution tank results in a loss of all of the kinetic energy and thus the exit minor loss coefficient is 1. See the minor loss equation below.

${h_e} = {K_e}\frac{{{V^2}}}{{2g}}$

The water temperature ranges from 10 to 30 Celsius. The roughness of a PVC pipe is approximately 0.1 mm. Use the fluids functions to calculate the minimum inner pipe diameter to carry this flow from the dam to the distribution tank.

Report the following
* critical design temperature
* kinematic viscosity (maximum viscosity will occur at the lowest temperature)
* the minimum inner pipe diameter (in mm).


```Python
x = 5
print(x)
```
