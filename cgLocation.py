##Import Necessary Modules
import numpy as np
from tools import interpolate

##Conversion factors
lbs = 0.45359 #kg
inc = 0.0254 #m
g = 9.81 #m/s^2

w_fuel = 4100*lbs*g

##Generate input data

fuel_cg = np.genfromtxt("cg_data/fuel_cg.dat", delimiter = ",")
fuel_cg = np.column_stack((fuel_cg[:,0]*g*lbs, fuel_cg[:,1]*lbs*g*inc*100)) #convert to metric system

m_fuel = interpolate(fuel_cg[:,0],fuel_cg[:,1],w_fuel)

w_pass = np.genfromtxt("cg_data/pass_cg.dat")*g
l_pass = np.array([131,131,214,214,251,251,288,288,170])*inc
m_pass = l_pass*w_pass

w_oew = 9165.0*lbs*g
l_oew = 291.65*inc
m_oew = 2672953.5*inc*lbs*g

x_cg = (sum(m_pass)+m_oew+m_fuel)/(w_fuel+sum(w_pass)+w_oew)

def deltaCg(w_f1,w_f0, a = False):
    '''
    Inputs:
     - w_f1 = fuel used at the second point
     - w_f0 = fuel used at beginning of cg shift
     - a    = if True, returns absolute value of shift in cg, otherwise it return positive or negative value accordingly

     Outputs:
      - The shift in cg, given in m
    '''
    m_f0 = interpolate(fuel_cg[:,0],fuel_cg[:,1],w_fuel-w_f0)
    m_f1 = interpolate(fuel_cg[:,0],fuel_cg[:,1],w_fuel-w_f1)
    l_p0 = np.array([131,131,214,214,251,251,288,288,170])*inc
    l_p1 = np.array([131,131,214,214,251,251,288,134,170])*inc
    m_p0 = l_p0*w_pass
    m_p1 = l_p1*w_pass

    x_cg0 = (sum(m_p0)+m_oew+m_f0)/(sum(w_pass)+w_oew+(w_fuel-w_f0))
    x_cg1 = (sum(m_p1)+m_oew+m_f1)/(sum(w_pass)+w_oew+(w_fuel-w_f1))

    return abs(x_cg1-x_cg0) if a else x_cg1-x_cg0

if __name__ == 'main':
    dCg = deltaCg(1650*lbs*g,1650*g*lbs, True)