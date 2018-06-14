#this program will take the voltage drop across a strain gauge and known strain values and will determine the gauge factor of the strain gauge.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

pd.set_option('precision', 8)


#Load data from the .csv file.
data = pd.read_csv('GaugeFactor_worksheet.csv')
strain = data.iloc[0:5,0]
strain1 = pd.to_numeric(strain)
#Locates the most recently added voltage drop data, on the far right.
voltage = data.iloc[0:5,-1]

#Locates the Vpp used during testing.
vpp = data.iloc[-1,-1]

#Size of the large resistor in series that helps calculate the assumed constant current.
total_resistance = 25e6

#Convertes values in dataframe that can be used to perform math on each other
voltage1 = pd.to_numeric(voltage)
vpp1 = pd.to_numeric(vpp)

#Finds the constant current
current = vpp1/total_resistance

#Finds the resistance of the strain gauge
resistance = voltage1/current
minresistance = resistance.min()
delta = resistance-minresistance
delta_R = delta/resistance
plot_data = pd.DataFrame({'Delta R/R': delta_R,'Strain': strain1})
#slope, intercept, r_value, p_value, std_err = stats.linregress(strain1, delta_R)
#print(slope)
#print(r_value**2)

plt.scatter(strain1, delta_R)
slope, intercept = np.polyfit(strain1, delta_R, 1)
print(slope)
plt.plot(strain, strain*slope + intercept, 'r')
plt.show()

plt.scatter
