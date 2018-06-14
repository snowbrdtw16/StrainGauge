#this program will take the voltage drop across a strain gauge and known strain values and will determine the gauge factor of the strain gauge.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

pd.set_option('precision', 8)


#Load data from the .csv file.
data = pd.read_csv('GaugeFactor_worksheet.csv')
strain = data.iloc[0:6,0]
strain1 = pd.to_numeric(strain)
#Locates the most recently added voltage drop data, on the far right.
voltage = data.iloc[0:6,-1]

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
#Finds the minimum resistance value
minresistance = resistance.min()
#Calculates the change in resistance from the 0 strain value.
delta = resistance-minresistance
#Calculate delta R/R
delta_R = delta/resistance
plot_data = pd.DataFrame({'Delta R/R': delta_R,'Strain': strain1})

def compute_limits(x, y, margin = 0.05):
    x_plot_range = strain1.max()-strain1.min()
    y_plot_range = delta_R.max()-delta_R.min()
    
    x_sx_lim = x.min()-margin*x_plot_range
    x_dx_lim = x.max()+ margin*x_plot_range
    y_sx_lim = y.min()-margin*y_plot_range
    y_dx_lim = y.max()+ margin*y_plot_range

    return x_sx_lim, x_dx_lim, y_sx_lim, y_dx_lim



#Linear Regression of plotted data
slope, intercept, r_value, p_value, std_err = stats.linregress(strain1, delta_R)

#Setting axes limits

plt.text(strain1.max()*0.05, delta_R.max()*0.95,'Gauge Factor = '+ str(round(slope,2)), ha='left', va='top')
plt.text(strain1.max()*0.05, delta_R.max()*0.88, '$R^2$ = '+ str(round(r_value**2,2)), ha='left', va='top')
axes = plt.gca()

l_x_sx, l_x_dx, l_y_sx, l_y_dx = compute_limits(strain1,delta_R, margin = 0.10)

axes.set_xlim([l_x_sx, l_x_dx])
axes.set_ylim([l_y_sx, l_y_dx])
axes.tick_params(axis='both', which='both', direction='in', bottom=True, top=True, left=True, right=True) 
plt.scatter(strain1, delta_R, s = 60, color = 'blue')
plt.plot(strain, strain*slope + intercept, 'r')
plt.xlabel('Strain', fontsize = 16)
plt.ylabel('ΔR/R', fontsize = 16)
plt.locator_params(axis='y', nbins=6)
plt.locator_params(axis='x', nbins=8)
#Scatter plot settings


plt.show()
#plt.scatter(strain1, delta_R)
#slope, intercept = np.polyfit(strain1, delta_R, 1)
#print(slope)
#plt.plot(strain, strain*slope + intercept, 'r')
#plt.show()
