

### Carbonate Chemistry
Carbonic acid and bicarbonate
$${H_2}CO_3^* \overset {K_1} \longleftrightarrow {H^+} + HCO_3^- $$
Why is this purple?
$${K_1} = \frac{{\left[ {{H^ + }} \right]\left[ {HCO_3^ - } \right]}}{{\left[ {{H_2}CO_3^* } \right]}}$$
$$p{K_1} = 6.3$$

bicarbonate and carbonate
$$HCO_3^ - \overset {{K_2}} \longleftrightarrow {H^ + } + CO_3^{ - 2}$$
$${K_2} = \frac{{\left[ {{H^ + }} \right]\left[ {CO_3^{ - 2}} \right]}}{{\left[ {HCO_3^ - } \right]}}$$
$$p{K_2} = 10.3$$

Total concentration of carbonates
$${C_T} = \left[ {{H_2}CO_3^* } \right] + \left[ {HCO_3^ - } \right] + \left[ {CO_3^{ - 2}} \right]$$

Alpha notation
$$\left[ {{H_2}CO_3^* } \right] = {\alpha_0}{C_T}$$
$$\left[ {HCO_3^ - } \right] = {\alpha_1}{C_T}$$
$$\left[ {CO_3^{ - 2}} \right] = {\alpha_2}{C_T}$$

Acid Neutralizing Capacity (ANC)
$${\text{ANC}} = [HCO_3^ - {\text{] + 2[CO}}_3^{ - 2}{\text{] + [O}}{{\text{H}}^{\text{ - }}}{\text{] - [}}{{\text{H}}^{\text{ + }}}{\text{]}}$$
ANC in alpha notation
$$ANC = {C_T}({\alpha_1} + 2{\alpha_2}) + \frac{{{K_w}}}{{\left[ {{H^ + }} \right]}} - \left[ {{H^ + }} \right]$$

Alphas
Alpha0
$${\alpha_{\text{0}}} = \frac{1}{{1 + \frac{{{K_1}}}{{[{H^ + }]}} + \frac{{{K_1}{K_2}}}{{{{[{H^ + }]}^2}}}}}$$

$${\alpha_{\text{0}}} = \frac{1}{{1 + \frac{{{K_1}}}{{[{H^ + }]}}\left( {1 + \frac{{{K_2}}}{{[{H^ + }]}}} \right)}}$$

$${\alpha_{\text{1}}}  =  \frac{1}{{\frac{{[{{\rm H}^ + }]}}{{{{\rm K}_1}}} + 1 + \frac{{{{\rm K}_2}}}{{[{{\rm H}^ + }]}}}}$$
$${\alpha_{\text{2}}}  =  \frac{1}{{\frac{{{{[{{\rm H}^ + }]}^2}}}{{{{\rm K}_1}{{\rm K}_2}}} + \frac{{[{{\rm H}^ + }]}}{{{{\rm K}_2}}} + 1}}$$

$${\alpha_{\text{2}}}  =  \frac{1}{{1 + \frac{{[{{\rm H}^ + }]}}{{{{\rm K}_2}}}\left( {1 + \frac{{[{{\rm H}^ + }]}}{{{{\rm K}_1}}}} \right)}}$$

open to the atmosphere
$$ANC = \frac{{{P_{C{O_2}}}{K_H}}}{{{\alpha_0}}}({\alpha_1} + 2{\alpha_2}) + \frac{{{K_w}}}{{\left[ {{H^ + }} \right]}} - \left[ {{H^ + }} \right]$$

```python
from aide_design.play import *
K1_carbonate = 10**(-6.37)*u.mol/u.L
K2_carbonate = 10**(-10.25)*u.mol/u.L
K_Henry_CO2 = 10**(-1.5)
P_CO2 = 10**(-3.5)


def invpH(pH):
  return 10**(-pH)*u.mol/u.L

def alpha0_carbonate(pH):
   alpha0_carbonate = 1/(1+(K1_carbonate/invpH(pH))*(1+(K2_carbonate/invpH(pH))))
   return alpha0_carbonate

def alpha1_carbonate(pH):
  alpha1_carbonate = 1/((invpH(pH)/K1_carbonate) + 1 + (K2_carbonate/invpH(pH)))
  return alpha1_carbonate

def alpha2_carbonate(pH):
  alpha2_carbonate = 1/(1+(invpH(pH)/K2_carbonate)*(1+(invpH(pH)/K1_carbonate)))
  return alpha2_carbonate

def ANC_open(arg):
  pass
```
Let's plot the alphas!
```python
# Create a uniform spaced array from 3 to 12
pH_graph = np.linspace(3,12,50)
plt.plot(pH_graph, alpha0_carbonate(pH_graph),'r', pH_graph, alpha1_carbonate(pH_graph),'b',pH_graph, alpha2_carbonate(pH_graph),'g')
plt.xlabel('pH')
plt.ylabel('Fraction of total carbonates')
plt.legend(['alpha_0', 'alpha_1', 'alpha_2'], loc='best')

plt.savefig('images\alphagraph.png')
plt.show()
```

Here is the graph ![graph](images\alphagraph.png)

```Python
