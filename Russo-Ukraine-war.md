## Variables and Parameters

- **$i$**:  
  - **Definition:** Index for country, where i = R represents Russia and i = U represents Ukraine.

### Stocks

- **$E_i$ (Economic Capital Stock / GDP):**  
  - **Meaning:** The total economic resources a country possesses. This stock underpins investments in technology and industrial capacity.

- **$T_{m,i}$ (Military Technology Level):**  
  - **Meaning:** The accumulated technology specifically dedicated to military applications (e.g., advanced weapons, drones).  
  - **Role:** Enhances military capability.

- **$T_{c,i}$ (Civilian/Industrial Technology Level):**  
  - **Meaning:** The technological base that boosts industrial production and overall economic efficiency (e.g., automation, process improvements).  
  - **Role:** Drives production output via the production bonus.

- **$M_i$ (Military Capability):**  
  - **Meaning:** The overall combat effectiveness of a country’s armed forces, determined by its military technology and military industrial capacity.  
  - **Role:** A key factor in determining both attrition and the outcome of military engagements.

- **$I_{c,i}$ (Civilian Industrial Capacity):**  
  - **Meaning:** The capacity of a country’s civilian production infrastructure (factories, plants) that contributes to economic output.  
  - **Role:** Directly influences economic production and thus the replenishment of economic capital.

- **$I_{m,i}$ (Military Industrial Capacity):**  
  - **Meaning:** The capacity dedicated to producing military goods and technologies.  
  - **Role:** Supports the build-up and maintenance of military capability.

### Independent Variables

- **$p_{tm,i}$ (Military Technology Investment Percentage):**  
  - **Meaning:** Indicates the percentage of available budget that is allocated to military technology development
  
- **$p_{tc,i}$ (Industrial Technology Investment Percentage):**  
  - **Meaning:** Indicates the percentage of available budget that is allocated to industrial technology development

- **$p_{Im,i}$ (Military Industrial Investment Percentage):**  
  - **Meaning:** Indicates the percentage of available budget that is allocated to Military industrial development

- **$p_{Ic,i}$ (Civilian Industrial Investment Percentage):**  
  - **Meaning:** Indicates the percentage of available budget that is allocated to civilian industrial development

- **$S_{i, \text{policy}}$ (Sancions Policy):**
  - **Meaning:** Exogenous policy that dictates the effect of sanctions placed on a country

- **$F_{i, \text{policy}}$ (Aid Policy):**
  - **Meaning:** Exogenous policy that dictates the effect of aid given to a country

### Non-Stock Functions:

- **$A_{I,i}$ (Industrial Attrition/Wear Function):**  
  - **Meaning:** The rate at which industrial capacity degrades (or “wears”) due to enemy action.
  - **Defined As:** $A_{I,i}(M_{\neg i}) = k_i \cdot M_{\neg i}^{1.1}$
  - **Role:** Reduces both civilian and military industrial capacities based on the enemy’s military strength.

- **$A_{m,i}$ (Military Attrition/Wear Function):**  
  - **Meaning:** The rate at which military capability deteriorates as a result of combat losses.  
  - **Defined As:** $A_{m,i}(M_i, M_{\neg i}) = k_m \cdot \omega(t) \cdot M_{\neg i}^{1.5}$ 
  - **Role:** Modeled as a function of the relative military strengths between the two countries.

- **$\iota_{t,i}$ (Cost Coefficient/Inflation):**  
  - **Meaning:** A parameter that adjusts costs (or resource depletion) to account for inflation, especially when military demand outstrips production.
  - **Defined As:** $\iota_{t,i} = \iota_{0,i} \cdot [1 + \eta \cdot \text{max}\{0, [\zeta \cdot M_i - r_i \cdot P_i (I_{m,i} + I_{c,i})]\}]$
  - **Role:** Enhances the effective output from civilian industrial capacity.

- **$S_i$ (Sanctions Factor):**  
  - **Meaning:** A parameter reflecting the negative impact of international sanctions on economic production.  
  - **Defined As:** $S_i(t) = S_{i, \text{policy}}(t - \tau_s)$
  - **Role:** Calculates the effect of sanctions with the implementation delay

- **$F_i$ (Foreign Aid):**  
  - **Meaning:** External financial support provided to a country.  
  - **Defined As:** $F_i(t) = F_{i, \text{policy}}(t - \tau_a)$
  - **Role:** Calculates the amount of foreign aid with the implementation delay

### Parameters / Coefficients

- **$r$ (Production Efficiency):**  
  - **Meaning:** A parameter indicating how effectively a country converts its industrial capacity and technology into economic output.

- **$\beta$ (Military Capability Weight):**  
  - **Meaning:** A scaling factor that links military technology and military industrial capacity to overall military capability.

- **$\tau_s$ (Sanctions Delay):**  
  - **Meaning:** The time lag between the imposition of sanctions and their effect on the economy.

- **$\tau_a$ (Foreign Aid Delay):**  
  - **Meaning:** The time lag between the allocation of foreign aid and its impact on the economy.
  
- **$\eta$ (Elasticity Coefficient):**  
  - **Meaning:** Measures the sensitivity of cost increases to the gap between military demand and production output.

- **$\alpha_{tm}$ (Military Technology Investment Coefficient):**  
  - **Meaning:** Indicates the efficiency with which economic capital is transformed into military technology.
  
- **$\alpha_{tc}$ (Industrial Technology Investment Coefficient):**  
  - **Meaning:** Indicates the efficiency with which economic capital is transformed into civilian/industrial technology.

- **$\alpha_{Im}$ (Military Industrial Investment Coefficient):**  
  - **Meaning:** Indicates how effectively economic capital is used to build military industrial capacity.

- **$\alpha_{Ic}$ (Civilian Industrial Investment Coefficient):**  
  - **Meaning:** Indicates how effectively economic capital is used to build civilian industrial capacity.

- **$c$ (Military Consumption/Cost Coefficient):**  
  - **Meaning:** The cost associated with maintaining and operating a military of a given size.

- **$\xi$ (Absolute attrition Coefficient)**
  - **Meaning:** Indicates how much of an impact total military size has on attrition.

- **$\zeta$ (Military Demand Coefficient):**  
  - **Meaning:** Scales the military demand in the inflation equation, affecting cost when military needs exceed production.

- **$k_I$ (Industrial Attrition Coefficient):**  
  - **Meaning:** Controls how industrial attrition increases with enemy military strength.
  
- **$k_m$ (Military Attrition Coefficient):**  
  - **Meaning:** Controls how military attrition increases as the enemy’s strength.

- **$\theta_i$ (Industrial Attrition Threshold Parameter):**  
  - **Meaning:** The level of enemy military capability at which industrial attrition begins to accelerate.

- **$\theta_m$ (Military Attrition Threshold Parameter):**  
  - **Meaning:** The relative enemy strength level at which military attrition significantly ramps up.

- **$\phi$ (Government Revanue Fraction)**
  - **Meaning:** The fraction of economic capital that the government can extract through taxes

- **$\epsilon$ (Small Non-zero Constant):**  
  - **Meaning:** A very small number used to prevent division by zero in the military attrition function.

- **$\omega$ (Attacking intensity)**
  - **Meaning:** The intensity of attacking vs defending one side is doing

- **$t$ (Time):**  
  - **Meaning:** The independent variable over which the system evolves.

## Equations

### GDP
$\Large E_i = r \cdot T_{c,i} \cdot I_{c,i} \cdot (1-S_i) + \text{min}\{(B_i - C_i), 0\}$

### Budget Equation
$\Large {B_i} = \phi \cdot E_i + F_i$

### Expendature Equation
$\Large {C_i} = \iota_{t,i} \cdot (B_i \cdot [p_{tm,i} + p_{tc,i} + p_{Im,i} + p_{Ic,i}] + c \cdot M_i)$

### Industrial Technology Growth
$\Large \frac{dT_{c,i}}{dt} = \alpha_{tc} \cdot p_{tc,i} \cdot B_i$

### Military Technology Growth
$\Large \frac{dT_{m,i}}{dt} = \alpha_{tm} \cdot p_{tm,i} \cdot B_i$

### Civilian Industrial Capacity
$\Large \frac{dI_{c,i}}{dt} = \alpha_{Ic} \cdot p_{Ic,i} \cdot B_i - A_{I,i}(M_{\neg i}) \cdot I_{c,i}$

### Military Industrial Capacity
$\Large \frac{dI_{m,i}}{dt} = \alpha_{Im} \cdot p_{Im,i} \cdot B_i - A_{I,i}(M_{\neg i}) \cdot I_{m,i}$

### Military Capability Equation
$\Large \frac{dM_i}{dt} = \beta \cdot r \cdot T_{m,i} \cdot I_{m,i} - A_{m,i}(M_{\neg i}) \cdot M_{i}$

### Price Level
$\Large \iota_{t,i} = \iota_{0,i} \cdot [1 + \eta \cdot \text{max}\{0, [\zeta \cdot M_i - r \cdot T_{c,i} \cdot (I_{m,i} + I_{c,i})]\}]$

### Industrial Attrition
$\Large A_{I,i}(M_{\neg i}) = k_i \cdot M_{\neg i}^{1.1}$

### Military Attrition
$\Large A_{m,i}(M_{\neg i}) = k_m \cdot \omega(t) \cdot M_{\neg i}^{1.5}$ 

### Sanctions
$\Large S_i(t) = S_{i, \text{policy}}(t - \tau_s)$

### Foreign Aid
$\Large F_i(t) = F_{i, \text{policy}}(t - \tau_a)$